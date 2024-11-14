import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
from models.user import User
from db.database import Session
import os

# Asegúrate de tener una clave secreta para firmar el token
SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")  # Cambia esto a una clave secreta segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # El token expirará después de 30 minutos

# Función para crear el token
def create_access_token(data: dict):
    # Convierte el UUID a cadena antes de incluirlo en el token
    data["sub"] = str(data["sub"])  # Convierte el UUID a una cadena
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para autenticar al usuario y generar el token
def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user is None or not CryptContext(schemes=["bcrypt"], deprecated="auto").verify(password, user.password):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    # Crear el token JWT
    access_token = create_access_token(data={"sub": user.id_user})
    return {"access_token": access_token, "token_type": "bearer"}
