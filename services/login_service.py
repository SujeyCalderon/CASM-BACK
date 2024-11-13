from typing import List, Optional
from fastapi import HTTPException
from datetime import date
from models.user import User
from models.publications import Publication
import uuid 
users: List[User] = []
def authenticate_user(email: str, password: str):
    user = next((u for u in users if u.email == email and u.password == password), None)
    if user is None:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    return {"message": "Inicio de sesión exitoso", "user": user}