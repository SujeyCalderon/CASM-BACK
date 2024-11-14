from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class PublicationBase(BaseModel):
    user_id: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

class PublicationCreate(PublicationBase):
    pass

class PublicationResponse(PublicationBase):
    id: str  

    class Config:
        orm_mode = True
        json_encoders = {
            UUID: str  
        }

