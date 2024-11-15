from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base
import uuid

class Favorites(Base):
    __tablename__ = 'favorites'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    publication_id = Column(UUID(as_uuid=True), nullable=True)
