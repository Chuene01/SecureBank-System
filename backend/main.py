from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TEMPORARY in-memory "fake database"
users = {}
balances = {}
transactions = []

#just to test the server is running
@app.get("/")
def home():
    return {"status": "backend is running"}

@app.post("/register")
def register(user: dict):
    username = user["username"]

    if username in users:
        return {"error": "Username already exists"}

    # Store full user record
    users[username] = {
        "email": user["email"],
        "password": user["password"]
    }

    balances[username] = 0

    return {"message": "registered"}

@app.post("/login")
def login(data: dict):
    username = data["username"]
    password = data["password"]

    if username not in users:
        return {"error": "Invalid username or password"}

    # Compare stored password vs entered password
    if users[username]["password"] != password:
        return {"error": "Invalid username or password"}

    return {
        "token": "TEMP_TOKEN",
        "username": username,
        "email": users[username]["email"]
    }

@app.get("/balance/{username}")
def balance(username: str):
    return {"balance": balances.get(username, 0)}

@app.post("/deposit")
def deposit(data: dict):
    username = data["username"]
    amount = data["amount"]
    balances[username] += amount
    transactions.append({"username": username, "type": "deposit", "amount": amount})
    return {"message": "deposit ok"}

@app.post("/withdraw")
def withdraw(data: dict):
    username = data["username"]
    amount = data["amount"]
    balances[username] -= amount
    transactions.append({"username": username, "type": "withdraw", "amount": amount})
    return {"message": "withdraw ok"}

@app.get("/transactions/{username}")
def my_transactions(username: str):
    return [t for t in transactions if t["username"] == username]

@app.get("/transactions/all")
def all_tx():
    return transactions
