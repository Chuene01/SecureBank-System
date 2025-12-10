from database import users_col, tx_col

# Create a new user
async def create_user(user_dict):
    await users_col.insert_one(user_dict)

# Get user by username
async def get_user(username: str):
    return await users_col.find_one({"username": username})

# Record a transaction
async def record_transaction(tx):
    await tx_col.insert_one(tx)

# Get transactions for a user
async def get_user_transactions(username: str):
    cursor = tx_col.find({"username": username})
    return [t async for t in cursor]