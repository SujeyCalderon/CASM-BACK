from pydantic import BaseModel
from typing import Optional

class PublicationBase(BaseModel):
    user_id: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

class PublicationCreate(PublicationBase):
    pass

class PublicationResponse(BaseModel):
    id: str  # Asegúrate de que aquí se esté usando 'id' y no '_id'
    user_id: str
    description: str
    image: Optional[str]

    class Config:
        orm_mode = True  # Pydantic usará el modo ORM para convertir los datos
        alias_generator = lambda field: field.lower()  # Cambiar nombres de campos si es necesario
        json_encoders = {
            'ObjectId': str,  # Esto maneja la conversión de ObjectId a string
        }


