from sqlalchemy import Column, String, Boolean
from db.database import Base
import uuid
from typing import Optional
class LoginResponse(Base):
    __tablename__ = "login_response"
    message = Column(String, nullable=False)
    user_id = Column(String, nullable=True)