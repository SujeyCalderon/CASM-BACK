from sqlalchemy import Column, String, ForeignKey
from db.database import Base
import uuid

class Login(Base):
    __tablename__ = "login"
    id_login = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id_user"), nullable=False)
