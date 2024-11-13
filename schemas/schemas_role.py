from pydantic import BaseModel
from typing import Optional
import uuid

class RoleSchema(BaseModel):
    id: str = None
    name: Optional[str] = None

    class Config:
        from_attributes = True  # En lugar de `orm_mode = True` en Pydantic v2
