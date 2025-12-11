from database import users_col, tx_col
from datetime import datetime
from bson import ObjectId

async def create_user(user_dict):
    result = await users_col.insert_one(user_dict)
    return str(result.inserted_id)

async def get_user(username: str):
    user = await users_col.find_one({"username": username})
    if user:
        user["id"] = str(user["_id"])
        return user
    return None

async def get_user_by_id(user_id: str):
    user = await users_col.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        return user
    return None

async def update_balance(username: str, amount: float):
    result = await users_col.update_one(
        {"username": username},
        {"$inc": {"balance": amount}}
    )
    return result.modified_count > 0

async def record_transaction(username: str, tx_type: str, amount: float):
    transaction = {
        "username": username,
        "type": tx_type,
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat()
    }
    await tx_col.insert_one(transaction)
    return transaction

async def get_user_transactions(username: str, limit: int = 50):
    cursor = tx_col.find({"username": username}).sort("timestamp", -1).limit(limit)
    transactions = []
    async for t in cursor:
        t["id"] = str(t["_id"])
        transactions.append(t)
    return transactions

async def get_user_balance(username: str):
    user = await get_user(username)
    return user.get("balance", 0) if user else 0