from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import User, Login, Deposit, Withdraw
from crud import create_user, get_user, record_transaction, get_user_transactions
from auth_utils import hash_password, verify_password, create_access_token, get_current_user
from database import users_col, tx_col
from schemas import LoginRequest
from datetime import datetime
from bson import ObjectId
import os  # Added for production

app = FastAPI(
    title="Bank API",
    version="1.0.0",
    docs_url="/docs",  # Explicitly enable docs
    redoc_url="/redoc"
)

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"status": "backend running with MongoDB", "environment": os.environ.get("RENDER", "local")}

@app.get("/health")
async def health_check():
    """Health check endpoint for Render monitoring"""
    try:
        # Test MongoDB connection
        from database import test_connection
        db_ok = await test_connection()
        return {
            "status": "healthy" if db_ok else "degraded",
            "database": "connected" if db_ok else "disconnected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500

@app.post("/register")
async def register(user: User):
    # check if username exists
    existing_user = await get_user(user.username)
    if existing_user:
        return {"error": "Username already exists"}

    # hash password before saving
    hashed_pwd = hash_password(user.password)

    # Pydantic 2.x uses model_dump() instead of dict()
    user_dict = user.model_dump()
    user_dict["password"] = hashed_pwd
    user_dict["balance"] = 0  # initial balance
    user_dict["created_at"] = datetime.utcnow()

    await create_user(user_dict)

    return {"message": "registered successfully"}

@app.post("/login")
async def login_user(credentials: LoginRequest):
    # get user from DB by email
    user = await users_col.find_one({"email": credentials.email})

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # verify password
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # create JWT token
    token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(user["_id"])
    }

@app.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "balance": current_user.get("balance", 0),
        "user_id": str(current_user["_id"])
    }

@app.get("/balance")
async def get_balance(current_user=Depends(get_current_user)):
    return {
        "balance": current_user.get("balance", 0)
    }

@app.post("/deposit")
async def deposit(amount: float, current_user=Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    # Update user balance
    await users_col.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {"balance": amount}}
    )

    # Record transaction
    await tx_col.insert_one({
        "user_id": str(current_user["_id"]),
        "username": current_user["username"],
        "type": "deposit",
        "amount": amount,
        "timestamp": datetime.utcnow(),
        "new_balance": current_user.get("balance", 0) + amount
    })

    return {"message": "Deposit successful", "amount": amount}

@app.post("/withdraw")
async def withdraw(amount: float, current_user=Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    current_balance = current_user.get("balance", 0)
    if current_balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Update user balance
    await users_col.update_one(
        {"_id": current_user["_id"]},
        {"$inc": {"balance": -amount}}
    )

    # Record transaction
    await tx_col.insert_one({
        "user_id": str(current_user["_id"]),
        "username": current_user["username"],
        "type": "withdraw",
        "amount": amount,
        "timestamp": datetime.utcnow(),
        "new_balance": current_balance - amount
    })

    return {"message": "Withdrawal successful", "amount": amount}

@app.get("/transactions")
async def transactions(current_user=Depends(get_current_user)):
    cursor = tx_col.find(
        {"user_id": str(current_user["_id"])}
    ).sort("timestamp", -1).limit(100)

    tx_list = await cursor.to_list(length=100)

    # Convert ObjectId to string and format
    for tx in tx_list:
        tx["_id"] = str(tx["_id"])
        tx["timestamp"] = tx["timestamp"].isoformat() if isinstance(tx["timestamp"], datetime) else tx["timestamp"]

    return {"transactions": tx_list, "count": len(tx_list)}

# Production entry point - CRITICAL FOR RENDER
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port} with MongoDB URI: {os.environ.get('MONGODB_URI', 'Not set')}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")