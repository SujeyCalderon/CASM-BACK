from sqlalchemy.orm import Session
from models.user import User
from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(email: str, password: str, user_id: str, db: Session):
    try:
        user = db.query(User).filter(User.email == email, User.id_user == user_id).first()
        if user is None:
            raise HTTPException(status_code=400, detail="Usuario no encontrado")
        
        if not verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Contraseña incorrecta")
        
        access_token = create_access_token(data={"sub": str(user.id_user)})  # El 'sub' es el user_id
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la autenticación: {str(e)}")
