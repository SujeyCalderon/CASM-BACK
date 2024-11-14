# models/schemas_user.py
from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    name: str
    last_name: Optional[str] = None
    email: str
    password: str
    speciality: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    document: Optional[str] = None
    profile_img: Optional[str] = None
    id_referency: Optional[str] = None
    premium: Optional[bool] = False

class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    speciality: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    document: Optional[str] = None
    profile_img: Optional[str] = None
    id_referency: Optional[str] = None
    premium: Optional[bool] = None

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id_user: str  # Cambiamos a `str` para coincidir con FastAPI
    name: str
    last_name: Optional[str] = None
    email: str
    speciality: Optional[str]
    phone: Optional[str]
    role: Optional[str]
    document: Optional[str]
    profile_img: Optional[str]
    id_referency: Optional[str]  # Cambiamos a `str`
    premium: bool
    access_token: Optional[str] = None  # Campo adicional para el token

    class Config:
        orm_mode = True