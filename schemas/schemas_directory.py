from pydantic import BaseModel
from typing import Optional
from uuid import UUID  # Importar UUID

class DirectoryCreate(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None

class DirectoryResponse(DirectoryCreate):
    id: UUID  # Cambiar de str a UUID

    class Config:
        orm_mode = True
