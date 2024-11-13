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
    email: str = Form(...),
    password: str = Form(...),
    specialty: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    document: UploadFile = File(...),
    address: Optional[str] = Form(None),
    is_premium: Optional[bool] = Form(False),
    db: Session = Depends(get_db)
):
    unique_filename = f"{uuid.uuid4()}_{document.filename}"
    file_path = f"uploads/{unique_filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)

    user_data = UserRequest(
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
