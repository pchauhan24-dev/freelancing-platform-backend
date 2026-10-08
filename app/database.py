import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["freelancing_platform"]

users_collection = db["users"]
projects_collection = db["projects"]
proposals_collection = db["proposals"]