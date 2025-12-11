# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Local MongoDB
MONGO_URI_LOCAL = "mongodb://localhost:27017"

# MongoDB Atlas (cloud)
# Get this from MongoDB Atlas dashboard
MONGO_URI_ATLAS = os.getenv("MONGO_URI", "your-mongodb-atlas-connection-string")

# Choose which one to use
USE_ATLAS = False  # Set to True to use MongoDB Atlas

if USE_ATLAS:
    MONGO_URI = MONGO_URI_ATLAS
else:
    MONGO_URI = MONGO_URI_LOCAL