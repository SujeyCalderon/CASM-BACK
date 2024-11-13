from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    name: str
    last_name: Optional[str] = None  # Campo agregado para apellido
    email: str
    password: str
    speciality: Optional[str] = None  # Cambié "specialty" por "speciality" para coincidir con tu base de datos
    phone: Optional[str] = None
    role: Optional[str] = None
    document: Optional[str] = None
    profile_img: Optional[str] = None  # Campo agregado para imagen de perfil
    id_referency: Optional[str] = None  # Campo agregado para la referencia
    premium: Optional[bool] = False  # Ajusté el nombre para consistencia con la base de datos

class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None  # Campo agregado para apellido
    email: Optional[str] = None
    password: Optional[str] = None
    speciality: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    document: Optional[str] = None
    profile_img: Optional[str] = None  # Campo agregado para imagen de perfil
    id_referency: Optional[str] = None  # Campo agregado para la referencia
    premium: Optional[bool] = None

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id_user: str
    name: str
    last_name: Optional[str] = None  # Campo agregado para apellido
    email: str
    speciality: Optional[str]
    phone: Optional[str]
    role: Optional[str]
    document: Optional[str]
    profile_img: Optional[str]  # Campo agregado para imagen de perfil
    id_referency: Optional[str]  # Campo agregado para la referencia
    premium: bool

    class Config:
        orm_mode = True
