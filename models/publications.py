from sqlalchemy import Column, String, Text
from db.database import Base  # Asegúrate de que `database.py` define `Base`
import uuid

class Publication(Base):
    __tablename__ = "publications"
    id = id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String, nullable=True)
