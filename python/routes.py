import bcrypt
from bson import ObjectId, Binary
from bson.errors import InvalidId 
from fastapi import APIRouter, Request, Response, HTTPException
from typing import List
from uuid import UUID

from models import UserData, HTTPError, Success, ListUpdateBody, ListUpdate,RegisterBody 

router = APIRouter()

def _object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code = 422, detail = "Invalid object ID")

@router.post(
    "/register",
    responses = {
        200: {
            "model": Success,
            "description": "Registration successful"
        },
        409: {
            "model": HTTPError,
            "description": "The specified username already exists"
        }
    }
)
def register(request: Request, body: RegisterBody):
    collection = request.app.database["users"]
    if collection.count_documents({ "name": body.name }):
        raise HTTPException(status_code = 409, detail = "The specified username already exists")

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(body.password.encode("utf-8"), salt)
    collection.insert_one({
        "name": body.name,
        "password_salt": salt,
        "password_hash": hash,
        "likes": [],
        "watch_later": [],
    })

    return { "success": True }



@router.get(
    "/{id}", 
    responses = {
        200: {
            "model": UserData,
            "description": "List all data about this user", 
        },
        404: {
            "model": HTTPError,
            "description": "The specified user does not exist",
        },
        422: {
            "model": HTTPError,
            "description": "The specified id is not valid"
        }
    }
)
def get_user_data(request: Request, id: str):
    id = _object_id(id)

    data = request.app.database["users"].find_one({"_id": id})
    if data is None:
        raise HTTPException(status_code = 404, detail = "Not found")

    return {
        "likes": list(map(Binary.as_uuid, data["likes"])),
        "watch_later": list(map(Binary.as_uuid, data["watch_later"]))
    }

_put_responses = {
    200: {
        "model": Success,
        "description": "The video was liked"
    },
    404: {
        "model": HTTPError,
        "description": "The specified user does not exist"
    },
    422: {
        "model": HTTPError,
        "description": "One of the parameters is not valid"
    }
}

@router.put("/{user_id}/like/{video_id}", responses = _put_responses)
def like(request: Request, user_id: str, video_id: UUID, update: ListUpdateBody):
    user_id = _object_id(user_id)
    video_id = Binary.from_uuid(video_id)

    if update.update == ListUpdate.add:
        verb = "$addToSet"
    elif update.update == ListUpdate.remove:
        verb = "$pull"

    result = request.app.database["users"].update_one(
        { "_id": user_id, },
        { verb: { "likes": video_id } }
    )
    if not result.matched_count:
        raise HTTPException(status_code = 404, detail = "Not found")
    return { "success": True }

@router.put("/{user_id}/watch-later/{video_id}", responses = _put_responses)
def watch_later(request: Request, user_id: str, video_id: UUID, update: ListUpdateBody):
    user_id = _object_id(user_id)
    video_id = Binary.from_uuid(video_id)

    if update.update == ListUpdate.add:
        verb = "$addToSet"
    elif update.update == ListUpdate.remove:
        verb = "$pull"

    result = request.app.database["users"].update_one(
        {"_id": user_id},
        { verb: { "watch_later": video_id } }
    )
    if not result.matched_count:
        raise HTTPException(status_code = 404, detail = "Not found")
    return { "success": True }