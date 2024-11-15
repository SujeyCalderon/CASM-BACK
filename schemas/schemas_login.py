from pydantic import BaseModel, EmailStr
from uuid import UUID

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    user_id: UUID  # Si user_id es un UUID


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
