from sqlalchemy import Column, String, Boolean
from db.database import Base
from typing import Optional
import uuid
class Role(Base):
    __tablename__ = "role"
    id: str = None  
    name: Optional[str] = None  

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())