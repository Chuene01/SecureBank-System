from pydantic import BaseModel, EmailStr, Field, validator
import re

class User(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match("^[a-zA-Z0-9_]+$", v):
            raise ValueError('Username must be alphanumeric')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        if not re.search(r"[A-Z]", v):  # At least one uppercase
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", v):  # At least one lowercase
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r"\d", v):  # At least one digit
            raise ValueError('Password must contain at least one digit')
        return v

class Login(BaseModel):
    username: str
    password: str

class Deposit(BaseModel):
    amount: float = Field(gt=0, description="Amount must be greater than 0")

class Withdraw(BaseModel):
    amount: float = Field(gt=0, description="Amount must be greater than 0")

class Transaction(BaseModel):
    type: str
    amount: float
    timestamp: str = None