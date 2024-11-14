from sqlalchemy import Column, String, Boolean
from db.database import Base
from typing import Optional
import uuid
class LoginRequest(Base):
    __tablename__ = "login_request"
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)