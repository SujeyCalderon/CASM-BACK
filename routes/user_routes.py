from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import shutil
import uuid
from models import User
from services import (
    create_user, get_users, get_user_by_id, update_user, delete_user
)

router = APIRouter()

# Endpoints Users
@router.post("/user/", response_model=User)
async def create_user_endpoint(
    name: str,
    email: str,
    password: str,
    specialty: Optional[str] = None,
    phone: Optional[str] = None,
    role: Optional[str] = None,
    document: UploadFile = File(...), 
    address: Optional[str] = None,
    is_premium: Optional[bool] = False
):
    # Guardamos el archivo PDF en la carpeta uploads y generamos un nombre único
    unique_filename = f"{uuid.uuid4()}_{document.filename}"
    file_path = f"uploads/{unique_filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)

    
    user = User(
        name=name,
        email=email,
        password=password,
        specialty=specialty,
        phone=phone,
        role=role,
        document=file_path,  
        address=address,
        is_premium=is_premium
    )

    return create_user(user)

@router.get("/users/", response_model=list[User])
def get_users_endpoint():
    return get_users()

@router.get("/users/{user_id}", response_model=User)
def get_user_by_id_endpoint(user_id: str):
    return get_user_by_id(user_id)

@router.put("/users/{user_id}", response_model=User)
def update_user_endpoint(user_id: str, updated_user: User):
    return update_user(user_id, updated_user)

@router.delete("/users/{user_id}", response_model=User)
def delete_user_endpoint(user_id: str):
    return delete_user(user_id)
