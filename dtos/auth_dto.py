from pydantic import BaseModel


class SignInDTO(BaseModel):
    """Sign in request model"""
    email: str
    password: str
