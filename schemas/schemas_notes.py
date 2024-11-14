from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID  # Asegúrate de importar UUID aquí

class NotesResponse(BaseModel):
    id: UUID
    user_id: str
    title: str
    description: Optional[str] = None
    creation_date: date
    modification_date: date

    class Config:
        orm_mode = True
        json_encoders = {
            UUID: str
        }

class NoteCreate(BaseModel):
    user_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    creation_date: Optional[date] = None
    modification_date: Optional[date] = None

class NoteUpdate(BaseModel):
    user_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    creation_date: Optional[date] = None
    modification_date: Optional[date] = None

    class Config:
        orm_mode = True
