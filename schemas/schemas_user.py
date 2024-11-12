from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
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
    document: Optional[str] = None
    address: Optional[str] = None
    is_premium: Optional[bool] = False
#api casm