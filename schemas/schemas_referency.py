from pydantic import BaseModel
from typing import Optional

class ReferencyRequest(BaseModel):
    calle: str
    ciudad: str
    estado: str
    codigo_postal: str

class ReferencyUpdate(BaseModel):
    calle: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None

    class Config:
        orm_mode = True

class ReferencyResponse(BaseModel):
    id_referency: str
    calle: str
    ciudad: str
    estado: str
    codigo_postal: str

    class Config:
        orm_mode = True
