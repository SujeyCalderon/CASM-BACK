from sqlalchemy import Column, String, Boolean
from db.database import Base
import uuid
from typing import Optional
class LoginResponse(Base):
    __tablename__ = "LoginResponse"
    message: str
    user_id: Optional[str] = None 