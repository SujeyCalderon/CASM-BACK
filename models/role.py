from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base
import uuid

class Role(Base):
    __tablename__ = "role"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String)

    def __init__(self, **data):
        super().__init__(**data)
