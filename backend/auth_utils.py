from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from bson import ObjectId
from database import users_col
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=True)
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

SECRET_KEY = "CHANGE_THIS_TO_A_RANDOM_LONG_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get current user from token
from fastapi.security import APIKeyHeader

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_current_user(api_key: str = Depends(api_key_scheme)):
    try:
        payload = jwt.decode(api_key, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # must match token creation

        if not user_id:
            raise HTTPException(status_code=401, detail="Not authenticated")

        user = await users_col.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



