from sqlalchemy import Column, String, Boolean
from db.database import Base
import uuid
from typing import Optional
class Directory(Base):
    __tablename__ = "directory"
    id: str = None  
    user_id: Optional[str] = None  
    name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None
    image: Optional[str] = None  
    email: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())