from sqlalchemy import Column, String, Boolean
from db.database import Base
import uuid

class User(Base):
    __tablename__ = "User"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    specialty = Column(String)
    phone = Column(String)
    role = Column(String)
    document = Column(String)
    address = Column(String)
    is_premium = Column(Boolean, default=False)
