from enum import Enum
from pydantic import BaseModel, Field, validator, ValidationError
import re
from typing import List, Set, Type
from uuid import UUID

# This should ideally be transferred under HTTPS, since there _is_ a password.
# However, HTTPS requires a domain name, and domain names are not free, nor can they be bought with
# gcloud's trial credit.
class RegisterBody(BaseModel):
    name: str = Field(description = "Username")
    password: str = Field(description = "Password")

    @validator("name")
    def name_characters(cls: Type["RegisterBody"], v: str):
        if not re.match("[A-Za-z0-9_-]+", v):
            raise ValidationError("username must contain only letters, numbers, underscores, and dashes")
        return v
    
    @validator("password")
    def password_length(cls: Type["RegisterBody"], v: str):
        if len(v) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        return v

class ListUpdate(str, Enum):
    add = "add"
    remove = "remove"

class ListUpdateBody(BaseModel):
    update: ListUpdate = Field(description = "Whether this operation should add or remove an element")


class Success(BaseModel):
    success: bool = Field(description = "Whether the action succeded", default = True)


class UserData(BaseModel):
    likes: List[UUID] = Field(description = "The videos this user likes")
    watch_later: List[UUID] = Field(description = "The videos this user has added to their \"watch later\" list")


class HTTPError(BaseModel):
    status_code: int = Field(description = "Error code")
    detail: str = Field(description = "Error description")

    class Config:
        schema_extra = {
            "example": {
                "status_code": 404,
                "detail": "not_found",
            }
        }
