from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Deposit(BaseModel):
    username: str
    amount: float

class Withdraw(BaseModel):
    username: str
    amount: float

