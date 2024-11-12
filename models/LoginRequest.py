from sqlalchemy import Column, String, Boolean
from db.database import Base
from typing import Optional
import uuid
class LoginRequest(Base):
    __tablename__ = "LoginRequest"
    email: str
    password: str