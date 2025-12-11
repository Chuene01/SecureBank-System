from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import User, Login, Deposit, Withdraw
from crud import create_user, get_user, record_transaction, get_user_transactions
from auth_utils import hash_password, verify_password, create_access_token, get_current_user
from database import users_col, tx_col
from schemas import LoginRequest
from datetime import datetime
from bson import ObjectId


app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"status": "backend running with MongoDB"}


@app.post("/register")
async def register(user: User):
    # check if username exists
    existing_user = await get_user(user.username)
    if existing_user:
        return {"error": "Username already exists"}

    # hash password before saving
    hashed_pwd = hash_password(user.password)

    user_dict = user.dict()
    user_dict["password"] = hashed_pwd
    user_dict["balance"] = 0  # initial balance

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
    token = create_access_token({"user_id": str(user["_id"])})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/me")
async def get_profile(user_id: str = Depends(get_current_user)):
    user = await users_col.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user["username"],
        "email": user["email"],
        "balance": user.get("balance", 0)
    }


@app.get("/balance")
async def get_balance(user_id: str = Depends(get_current_user)):
    user = await users_col.find_one({"_id": ObjectId(user_id)})
    
    return {
        "balance": user.get("balance", 0)
    }


@app.post("/deposit")
async def deposit(amount: float, user_id: str = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    # Update balance
    result = await users_col.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"balance": amount}}
    )

    # Add transaction record
    await tx_col.insert_one({
        "user_id": user_id,
        "type": "deposit",
        "amount": amount,
        "timestamp": datetime.utcnow()
    })

    return {"message": "Deposit successful", "amount": amount}


@app.post("/withdraw")
async def withdraw(amount: float, user_id: str = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    user = await users_col.find_one({"_id": ObjectId(user_id)})

    if user.get("balance", 0) < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    await users_col.update_one(
        {"_id": ObjectId(user_id)},
        {"$inc": {"balance": -amount}}
    )

    await tx_col.insert_one({
        "user_id": user_id,
        "type": "withdraw",
        "amount": amount,
        "timestamp": datetime.utcnow()
    })

    return {"message": "Withdrawal successful", "amount": amount}


@app.get("/transactions")
async def transactions(user_id: str = Depends(get_current_user)):
    cursor = tx_col.find({"user_id": user_id}).sort("timestamp", -1)
    tx_list = await cursor.to_list(length=100)

    return tx_list
