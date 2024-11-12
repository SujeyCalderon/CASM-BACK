import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import date
class Role(BaseModel):
    id: str = None  
    name: Optional[str] = None  

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())