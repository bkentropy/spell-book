import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variables
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)
db = client["dnd5eapi_crawler"]

# Collections
users = db["users"]
spells = db["resources"]
