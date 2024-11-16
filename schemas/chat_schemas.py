from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MensajeBase(BaseModel):
    id_remitente: str  
    id_destinatario: str 
    mensaje: str
    fecha_envio: datetime = datetime.utcnow()
    estado: Optional[str] = "no_leído" 

class MensajeResponse(MensajeBase):
    id: str  

    class Config:
        orm_mode = True