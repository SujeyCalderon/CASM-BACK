from sqlalchemy import Column, String
from db.database import Base
import uuid

class Referency(Base):
    __tablename__ = "referency"

    id_referency = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    calle = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    codigo_postal = Column(String, nullable=False)
