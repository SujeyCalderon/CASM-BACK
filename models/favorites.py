from sqlalchemy import Column, String, Boolean
from db.database import Base
from typing import Optional
import uuid
from datetime import date
from fastapi import APIRouter, UploadFile, File
class Favorites(Base):
    __tablename__ = "favorites"
    id: str = None 
    user_id: Optional[str] = None  
    favorite_user_id: Optional[str] = None 
    publication_id : Optional[str] = None 

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4()) 