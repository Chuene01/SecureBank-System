from fastapi import HTTPException
from auth_utils import hash_password, verify_password, create_access_token
from crud import get_user, create_user
from models import User, Login

async def register_user(user: User):
    existing = await get_user(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = hash_password(user.password)

    user_dict = user.dict()
    user_dict["password"] = hashed
    user_dict["balance"] = 0

    await create_user(user_dict)

    return {"message": "registered successfully"}


async def login_user(data: Login):
    user = await get_user(data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user["username"]})

    return {
        "token": token,
        "username": user["username"],
        "email": user["email"]
    }
