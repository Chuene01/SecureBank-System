from pymongo import MongoClient
import sys

def test_mongodb_connection(uri="mongodb://localhost:27017"):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Will throw exception if can't connect
        print("✅ MongoDB connection successful!")
        
        # List databases
        databases = client.list_database_names()
        print(f"📁 Available databases: {databases}")
        
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test with default local MongoDB
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    else:
        uri = "mongodb://localhost:27017"
    
    test_mongodb_connection(uri)