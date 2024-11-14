from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str  # El token que el cliente usará para futuras peticiones
    token_type: str  # Tipo de token, en este caso "bearer"
