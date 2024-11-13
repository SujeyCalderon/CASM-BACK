from sqlalchemy import Column, String, Boolean
from db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    specialty = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=True)
    document = Column(String, nullable=True)
    address = Column(String, nullable=True)
    is_premium = Column(Boolean, default=False)
