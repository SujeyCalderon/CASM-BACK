from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID

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

from pydantic import BaseModel, Field, validator
from uuid import UUID

class ReferencyResponse(BaseModel):
    id_referency: str
    calle: str
    ciudad: str
    estado: str
    codigo_postal: str

    @validator("id_referency", pre=True, always=True)
    def convert_uuid_to_str(cls, v):
        return str(v) if isinstance(v, UUID) else v

