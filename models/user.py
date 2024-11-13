from sqlalchemy import Column, String, Boolean, ForeignKey
from db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    # Columnas existentes en tu base de datos
    id_user = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role = Column(String, nullable=True)  # Cambié "rol" a "role" para seguir el estándar en inglés
    name = Column(String, index=True)
    last_name = Column(String, nullable=True)  # Nuevo campo para apellido
    phone = Column(String, nullable=True)
    password = Column(String, nullable=False)  # Asegúrate de que la contraseña no sea nula
    email = Column(String, unique=True, index=True)
    profile_img = Column(String, nullable=True)  # Nuevo campo para imagen de perfil
    id_referency = Column(String, ForeignKey("referencies.id"), nullable=True)  # Relación con otra tabla
    speciality = Column(String, nullable=True)
    premium = Column(Boolean, default=False)
    document = Column(String, nullable=True)
