from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import uuid

from db.database import get_db
from schemas.schemas_user import UserRequest, UserResponse, UserUpdate
from services.user_service import create_user, get_all_users, get_user_by_id, update_user, delete_user

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
async def create_user_endpoint(
    name: str = Form(...),
    last_name: Optional[str] = Form(None),  # Agregado para el apellido
    email: str = Form(...),
    password: str = Form(...),
    speciality: Optional[str] = Form(None),  # Cambiado a "speciality"
    phone: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    document: UploadFile = File(...),
    profile_img: Optional[UploadFile] = File(None),  # Agregado para la imagen de perfil
    id_referency: Optional[str] = Form(None),  # Agregado para la referencia
    premium: Optional[bool] = Form(False),
    db: Session = Depends(get_db)
):
    # Guardar el documento
    unique_doc_filename = f"{uuid.uuid4()}_{document.filename}"
    doc_path = f"uploads/{unique_doc_filename}"
    with open(doc_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)

    # Guardar la imagen de perfil si existe
    profile_img_path = None
    if profile_img:
        unique_img_filename = f"{uuid.uuid4()}_{profile_img.filename}"
        profile_img_path = f"uploads/{unique_img_filename}"
        with open(profile_img_path, "wb") as buffer:
            shutil.copyfileobj(profile_img.file, buffer)

    # Crear datos del usuario
    user_data = UserRequest(
        name=name,
        last_name=last_name,
        email=email,
        password=password,
        speciality=speciality,
        phone=phone,
        role=role,
        document=doc_path,
        profile_img=profile_img_path,
        id_referency=id_referency,
        premium=premium
    )

    return create_user(user_data, db)

@router.get("/users/", response_model=List[UserResponse])
def get_users_endpoint(db: Session = Depends(get_db)):
    return get_all_users(db)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(user_id: str, db: Session = Depends(get_db)):
    return get_user_by_id(user_id, db)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: str, updated_user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(user_id, updated_user, db)

@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user_endpoint(user_id: str, db: Session = Depends(get_db)):
    return delete_user(user_id, db)
