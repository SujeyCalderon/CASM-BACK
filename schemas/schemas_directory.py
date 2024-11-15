from pydantic import BaseModel
from typing import Optional
from uuid import UUID  # Importar UUID

from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class DirectoryCreate(BaseModel):
    user_id: UUID  # Aceptará un UUID directamente
    name: str
    description: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class DirectoryResponse(BaseModel):
    id: str  # Definido como string en el esquema
    user_id: str
    name: str
    description: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional


class DirectoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    direction: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None