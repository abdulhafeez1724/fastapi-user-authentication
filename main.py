from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

# Connect to MongoDB
try:
    client = MongoClient(MONGODB_URL)
    client.server_info()  # Can throw an error if not connected
except:
    print("Failed to connect to database")
    exit()  # Exit if there's no connection, alternatively you can raise an exception

db = client.user_database
users_collection = db.users

app = FastAPI()


class User(BaseModel):
    username: str
    password: str


@app.post("/create_user/")
async def create_user(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = user.password  # In a real-world scenario, you'd hash the password
    users_collection.insert_one({"username": user.username, "password": hashed_password})
    return {"status": "success"}


@app.get("/get_user/{username}/")
async def get_user(username: str):
    user_data = users_collection.find_one({"username": username})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user_data["username"]}
