from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import User, Login, Deposit, Withdraw
from crud import create_user, get_user, record_transaction, get_user_transactions
from auth_utils import hash_password, verify_password
from database import users_col

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
async def login(data: Login):
    user = await get_user(data.username)
    if not user:
        return {"error": "Invalid username or password"}

    if not verify_password(data.password, user["password"]):
        return {"error": "Invalid username or password"}

    return {
        "message": "login successful",
        "username": user["username"],
        "email": user["email"]
    }


@app.get("/balance/{username}")
async def balance(username: str):
    user = await get_user(username)
    if not user:
        return {"error": "user not found"}
    return {"balance": user.get("balance", 0)}


@app.post("/deposit")
async def deposit(data: Deposit):
    # increase balance
    await users_col.update_one(
        {"username": data.username},
        {"$inc": {"balance": data.amount}}
    )

    # record transaction
    await record_transaction(
        {"username": data.username, "type": "deposit", "amount": data.amount}
    )

    return {"message": "deposit successful"}


@app.post("/withdraw")
async def withdraw(data: Withdraw):
    user = await get_user(data.username)
    if not user:
        return {"error": "user not found"}

    if user["balance"] < data.amount:
        return {"error": "insufficient funds"}

    await users_col.update_one(
        {"username": data.username},
        {"$inc": {"balance": -data.amount}}
    )

    await record_transaction(
        {"username": data.username, "type": "withdraw", "amount": data.amount}
    )

    return {"message": "withdraw successful"}


@app.get("/transactions/{username}")
async def my_transactions(username: str):
    return await get_user_transactions(username)