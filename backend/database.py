import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get MongoDB URI from environment (Render will provide this)
MONGO_URL = os.environ.get("MONGODB_URI")

# Production fallback - on Render, this MUST be set
if not MONGO_URL:
    logger.warning("⚠️ MONGODB_URI not set in environment. Using default local MongoDB.")
    MONGO_URL = "mongodb://localhost:27017"
else:
    logger.info(f"✅ Using MongoDB URI from environment")

# Handle MongoDB Atlas connection strings
# Atlas uses mongodb+srv:// format which requires special handling
if "mongodb+srv://" in MONGO_URL:
    # For MongoDB Atlas, we need to handle the SRV connection
    logger.info("🔗 Detected MongoDB Atlas SRV connection")
    
    # Fix common issue: replace postgres:// with postgresql:// if present
    if "postgres://" in MONGO_URL:
        MONGO_URL = MONGO_URL.replace("postgres://", "postgresql://", 1)
    
    # Create Atlas-compatible client
    try:
        client = AsyncIOMotorClient(
            MONGO_URL,
            tls=True,
            tlsAllowInvalidCertificates=False,
            retryWrites=True,
            w="majority",
            maxPoolSize=50,
            minPoolSize=10,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=45000
        )
        logger.info("✅ MongoDB Atlas client configured")
    except Exception as e:
        logger.error(f"❌ Failed to create Atlas client: {e}")
        raise
else:
    # For local or standard MongoDB
    logger.info("🔗 Using standard MongoDB connection")
    try:
        client = AsyncIOMotorClient(
            MONGO_URL,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000
        )
    except Exception as e:
        logger.error(f"❌ Failed to create MongoDB client: {e}")
        raise

# Get database name from environment or connection string
def get_db_name():
    # Try to extract from connection string
    if "mongodb.net/" in MONGO_URL:
        # Extract from Atlas URL: mongodb+srv://...mongodb.net/dbname?...
        parts = MONGO_URL.split("mongodb.net/")
        if len(parts) > 1:
            db_part = parts[1].split("?")[0]
            if db_part and db_part != "":
                return db_part
    
    # Fallback to environment or default
    return os.environ.get("MONGO_DB_NAME", "bankdb")

db_name = get_db_name()
logger.info(f"📁 Using database: {db_name}")

db = client[db_name]
users_col = db["users"]
tx_col = db["transactions"]

# Create indexes for better performance
async def create_indexes():
    try:
        # Create unique index on email and username
        await users_col.create_index("email", unique=True)
        await users_col.create_index("username", unique=True)
        
        # Create index on transactions for faster queries
        await tx_col.create_index("user_id")
        await tx_col.create_index([("user_id", 1), ("timestamp", -1)])
        await tx_col.create_index("timestamp", expireAfterSeconds=60*60*24*90)  # Auto-delete after 90 days
        
        logger.info("✅ Database indexes created")
    except Exception as e:
        logger.warning(f"⚠️ Could not create indexes: {e}")
        # Non-critical, continue anyway

# Test connection function
async def test_connection():
    """Test MongoDB connection - used by health check"""
    try:
        # Try to ping the database
        await client.admin.command('ping')
        logger.info("✅ MongoDB connection test: SUCCESS")
        return True
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"❌ MongoDB connection test failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error in MongoDB test: {e}")
        return False

# Initialize on import (optional)
async def init_db():
    """Initialize database connection and indexes"""
    connected = await test_connection()
    if connected:
        await create_indexes()
    return connected

# Optional: Export connection status
is_connected = False