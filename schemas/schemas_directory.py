from pydantic import BaseModel
from typing import Optional

class DirectoryCreate(BaseModel):
    user_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None

class DirectoryResponse(DirectoryCreate):
    id: str

    class Config:
        orm_mode = True
