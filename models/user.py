from sqlalchemy import Column, String, Boolean, ForeignKey
from db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    id_user = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role = Column(String, nullable=True)
    name = Column(String, index=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    profile_img = Column(String, nullable=True)
    id_referency = Column(String, ForeignKey("referency.id_referency"), nullable=True)
    speciality = Column(String, nullable=True)
    premium = Column(Boolean, default=False)
    document = Column(String, nullable=True)
