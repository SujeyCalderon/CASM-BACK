from pydantic import BaseModel
from typing import Optional
import uuid

class Favorites(BaseModel):
    id: str
    user_id: Optional[str] = None
    favorite_user_id: Optional[str] = None
    publication_id: Optional[str] = None

    # Asumiendo que ya usas un UUID por defecto en la clase
    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            self.id = str(uuid.uuid4())  # Generar UUID si no se proporciona
