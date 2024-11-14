from pydantic import BaseModel
from typing import Optional

class RoleSchema(BaseModel):
    name: str  # Solo el nombre del rol, ya que el id no debe enviarse al actualizar
    class Config:
        orm_mode = True  # Esto indica que el modelo proviene de un ORM (SQLAlchemy)
