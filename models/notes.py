from sqlalchemy import Column, String, Boolean
from db.database import Base
from typing import Optional
import uuid
from datetime import date
from fastapi import APIRouter, UploadFile, File
class Notes(Base):
    __tablename__ = "notes"
    id: Optional[str] = None
    user_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    creation_date: Optional[date] = None
    modification_date: Optional[date] = None
    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4()) 