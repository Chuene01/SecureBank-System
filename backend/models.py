from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., min_length=1)
    email: str
    password: str = Field(..., min_length=1, max_length=72)

class Login(BaseModel):
    username: str
    password: str

class Deposit(BaseModel):
    username: str
    amount: float

class Withdraw(BaseModel):
    username: str
    amount: float
