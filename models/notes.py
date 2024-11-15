from sqlalchemy import Column, String, Text, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # Changed to UUID
    title = Column(String, nullable=False)  # Set nullable to False if title is required
    description = Column(Text, nullable=True)
    creation_date = Column(Date, nullable=True)
    modification_date = Column(Date, nullable=True)
