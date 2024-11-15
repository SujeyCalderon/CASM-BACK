from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class PublicationBase(BaseModel):
    user_id: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

class PublicationCreate(PublicationBase):
    pass

from pydantic import BaseModel
from typing import Optional

class PublicationResponse(BaseModel):
    id: str  # Cambia UUID a str
    user_id: str
    description: str
    image: Optional[str]

    class Config:
        orm_mode = True


