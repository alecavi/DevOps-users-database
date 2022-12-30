from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values

from routes import router as user_router

app = FastAPI()
config = dotenv_values(".env")

@app.on_event("startup")
def startup():
    app.mongodb_client = MongoClient(config["DB_URL"])
    app.collection = app.mongodb_client[config["DB_NAME"]][config["DB_DOC"]]

@app.on_event("shutdown")
def shutdown():
    app.mongodb_client.close()

app.include_router(user_router, tags=["users"], prefix = "/user")
