from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Directory(Base):
    __tablename__ = "directory"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # UUID en base de datos
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    direction = Column(String, nullable=True)
    email = Column(String, nullable=True)
    image = Column(String, nullable=True)
