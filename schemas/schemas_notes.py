from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from datetime import date
from uuid import UUID  # Ensure UUID is imported

class NotesResponse(BaseModel):
    id: UUID
    user_id: UUID  # Changed from str to UUID
    title: str
    description: Optional[str] = None
    creation_date: date
    modification_date: date

    class Config:
        orm_mode = True  # Required for SQLAlchemy integration
        json_encoders = {
            UUID: str  # Converts UUID to string when exporting to JSON
        }
        from_attributes = True  # Ensure this is added to use from_orm

class NoteCreate(BaseModel):
    user_id: UUID  # Hacerlo obligatorio, si es necesario
    title: str  # Hacerlo obligatorio, si es necesario
    description: Optional[str] = None
    creation_date: Optional[date] = None
    modification_date: Optional[date] = None

class NoteUpdate(BaseModel):
    user_id: Optional[UUID] = None  # Esto está bien si es opcional
    title: Optional[str] = None
    description: Optional[str] = None
    creation_date: Optional[date] = None
    modification_date: Optional[date] = None

    class Config:
        orm_mode = True
