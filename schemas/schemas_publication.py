from pydantic import BaseModel
from typing import Optional

class PublicationBase(BaseModel):
    user_id: str
    description: Optional[str] = None

class PublicationCreate(PublicationBase):
    image: Optional[str] = None

class PublicationResponse(PublicationBase):
    id: str
    image: Optional[str]

    class Config:
        orm_mode = True
