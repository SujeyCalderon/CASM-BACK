from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class Favorites(BaseModel):
    id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    publication_id: Optional[UUID] = None

    class Config:
        orm_mode = True
        from_attributes = True 
