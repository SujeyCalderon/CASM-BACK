from sqlalchemy import Column, String, Boolean
from db.database import Base
import uuid
from typing import Optional
class Publication(Base):
    __tablename__ = "publication"
    id: str = None  
    user_id: Optional[str] = None  
    description: Optional[str] = None
    image: Optional[str] = None  

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())