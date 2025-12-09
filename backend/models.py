from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

# ---------------------
# CUSTOM OBJECTID FIELD
# ---------------------
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId format")
        return ObjectId(v)

# ---------------------
# USER MODELS
# ---------------------

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: EmailStr
    password: str  # hashed password
    balance: float = 0.0

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    balance: float

# ---------------------
# TRANSACTION MODELS
# ---------------------

class TransactionBase(BaseModel):
    amount: float


class TransactionCreate(TransactionBase):
    pass  # deposit OR withdraw will use the same body


class TransactionDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    amount: float
    type: str  # "deposit" or "withdraw"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class TransactionResponse(BaseModel):
    id: str
    user_id: str
    type: str
    amount: float
    timestamp: datetime

# ---------------------
# JWT TOKEN MODELS
# ---------------------

class Token(BaseModel):
    token: str
    user: UserResponse


class TokenData(BaseModel):
    id: Optional[str] = None