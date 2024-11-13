from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base
import uuid
from typing import Optional

class Favorites(Base):
    __tablename__ = "favorites"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    favorite_user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    publication_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
