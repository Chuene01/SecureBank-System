import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get MongoDB Atlas URI from environment
MONGO_URL = os.getenv("MONGODB_URL")

if not MONGO_URL:
    raise RuntimeError("MONGODB_URL is not set in environment variables")

# Create MongoDB client
client = AsyncIOMotorClient(MONGO_URL)

# Select database
db = client["bankdb"]

# Collections
users_col = db["users"]
tx_col = db["transactions"]

