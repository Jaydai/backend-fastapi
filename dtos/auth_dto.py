from pydantic import BaseModel
from typing import Optional


class SignInDTO(BaseModel):
    email: str
    password: str


class SignUpDTO(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
