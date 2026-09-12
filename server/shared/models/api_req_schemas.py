from pydantic import BaseModel
from pydantic import EmailStr


class RegisterRequest(BaseModel):

    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):

    username: str
    password: str