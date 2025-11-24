from pydantic import BaseModel


class SignInDTO(BaseModel):
    email: str
    password: str


class SignUpDTO(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class OAuthSignIn(BaseModel):
    provider: str
    token: str


class RefreshTokenDTO(BaseModel):
    refresh_token: str


class UserMeResponseDTO(BaseModel):
    user_id: str
    name: str
    data_collection: bool
    profile_picture_url: str | None
