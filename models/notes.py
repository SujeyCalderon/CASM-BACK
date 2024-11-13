from sqlalchemy import Column, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base
from typing import Optional
import uuid
from datetime import date

class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    creation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    modification_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
