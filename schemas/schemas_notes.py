from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

class NotesResponse(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    creation_date: Optional[date] = None
    modification_date: Optional[date] = None

    class Config:
        orm_mode = True  # Permite que FastAPI convierta entre SQLAlchemy y Pydantic automáticamente
