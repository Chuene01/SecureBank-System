from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import User, Login, Deposit, Withdraw
from crud import (
    create_user, get_user, record_transaction, 
    get_user_transactions, update_balance, get_user_balance
)
from auth_utils import (
    hash_password, verify_password, create_access_token,
    get_current_user
)

app = FastAPI(title="Banking API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"status": "Banking API is running", "version": "1.0.0"}

@app.post("/register", status_code=201)
async def register(user: User):
    existing_user = await get_user(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pwd = hash_password(user.password)
    
    user_dict = user.dict()
    user_dict["password"] = hashed_pwd
    user_dict["balance"] = 0.0
    
    await create_user(user_dict)
    
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(data: Login):
    user = await get_user(data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token({"sub": user["username"]})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user["username"],
        "email": user["email"]
    }

@app.get("/balance")
async def balance(current_user: str = Depends(get_current_user)):
    balance_amount = await get_user_balance(current_user)
    return {"username": current_user, "balance": balance_amount}

@app.post("/deposit")
async def deposit(
    data: Deposit,
    current_user: str = Depends(get_current_user)
):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    # Update balance
    await update_balance(current_user, data.amount)
    
    # Record transaction
    await record_transaction(current_user, "deposit", data.amount)
    
    new_balance = await get_user_balance(current_user)
    
    return {
        "message": "Deposit successful",
        "amount": data.amount,
        "new_balance": new_balance
    }

@app.post("/withdraw")
async def withdraw(
    data: Withdraw,
    current_user: str = Depends(get_current_user)
):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    current_balance = await get_user_balance(current_user)
    
    if current_balance < data.amount:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient funds. Available: {current_balance}"
        )
    
    # Update balance
    await update_balance(current_user, -data.amount)
    
    # Record transaction
    await record_transaction(current_user, "withdraw", data.amount)
    
    new_balance = await get_user_balance(current_user)
    
    return {
        "message": "Withdrawal successful",
        "amount": data.amount,
        "new_balance": new_balance
    }

@app.get("/transactions")
async def my_transactions(
    current_user: str = Depends(get_current_user),
    limit: int = 50
):
    transactions = await get_user_transactions(current_user, limit)
    return {"transactions": transactions}

@app.get("/profile")
async def profile(current_user: str = Depends(get_current_user)):
    user = await get_user(current_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove sensitive data
    user.pop("password", None)
    user.pop("_id", None)
    
    return user