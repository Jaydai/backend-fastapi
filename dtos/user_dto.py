from pydantic import BaseModel, EmailStr


class UserProfileResponseDTO(BaseModel):
    id: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    phone: str | None = None
    created_at: str | None = None
    email_confirmed_at: str | None = None


class UpdateUserProfileDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class UpdateDataCollectionDTO(BaseModel):
    data_collection: bool
