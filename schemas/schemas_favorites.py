from pydantic import BaseModel
from typing import Optional
import uuid

class Favorites(BaseModel):
    id: str
    user_id: Optional[str] = None
    favorite_user_id: Optional[str] = None
    publication_id: Optional[str] = None

    # Configuración para que Pydantic pueda trabajar con el modelo de SQLAlchemy
    class Config:
        orm_mode = True
