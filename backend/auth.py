from fastapi import APIRouter, HTTPException

# import in-memory DB
from main import users, balances

# import utils
from auth_utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: dict):
    username = user["username"]

    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")

    # hash the password before saving!
    hashed_pw = hash_password(user["password"])

    users[username] = {
        "email": user["email"],
        "password": hashed_pw
    }

    balances[username] = 0

    return {"message": "registered successfully"}


@router.post("/login")
def login(data: dict):
    username = data["username"]
    password = data["password"]

    if username not in users:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    stored_pw = users[username]["password"]

    # verify bcrypt hash
    if not verify_password(password, stored_pw):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # generate JWT token
    token = create_access_token({"sub": username})

    return {
        "token": token,
        "username": username,
        "email": users[username]["email"]
    }
