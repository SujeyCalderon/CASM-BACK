from sqlalchemy import Column, String, ForeignKey
from db.database import Base
import uuid

class Login(Base):
    __tablename__ = "login"
    id_login = Column(UUID, primary_key=True, default=uuid.uuid4)  # Cambié a UUID
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id_user"), nullable=False)  # Cambié a UUID

    def __init__(self, email: str, password: str, user_id: str):
        self.email = email
        self.password = password
        self.user_id = user_id
