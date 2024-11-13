from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    name: str
    email: str
    password: str
    specialty: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    document: Optional[str] = None
    address: Optional[str] = None
    is_premium: Optional[bool] = False

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    specialty: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    address: Optional[str] = None
    is_premium: Optional[bool] = None

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    specialty: Optional[str]
    phone: Optional[str]
    role: Optional[str]
    document: Optional[str]
    address: Optional[str]
    is_premium: bool

    class Config:
        orm_mode = True
