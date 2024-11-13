from sqlalchemy import Column, String
from db.database import Base
import uuid

class Directory(Base):
    __tablename__ = "directory"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    direction = Column(String, nullable=True)
    email = Column(String, nullable=True)
    image = Column(String, nullable=True)
