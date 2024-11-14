from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import shutil
import os
import uuid

from models.directory import Directory
from services.directory_service import create_directory, get_directory_by_id, get_directories, update_directory, delete_directory
from schemas.schemas_directory import DirectoryCreate, DirectoryResponse
from db.database import get_db

router = APIRouter()
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/directory/", response_model=DirectoryResponse)
async def create_directory_endpoint(
    user_id: str = Form(...),
    name: str = Form(None),
    description: str = Form(None),
    phone: str = Form(None),
    direction: str = Form(None),
    email: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if image:
        filename = f"{uuid.uuid4()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    directory_data = DirectoryCreate(
        user_id=user_id,
        name=name,
        description=description,
        phone=phone,
        direction=direction,
        email=email,
        image=image_path
    )
    return create_directory(directory_data, db)

@router.get("/directory/{directory_id}", response_model=DirectoryResponse)
def get_directory_by_id_endpoint(directory_id: str, db: Session = Depends(get_db)):
    return get_directory_by_id(directory_id, db)

@router.get("/directory/", response_model=List[DirectoryResponse])
def get_directories_endpoint(db: Session = Depends(get_db)):
    return get_directories(db)

@router.put("/directory/{directory_id}", response_model=DirectoryResponse)
async def update_directory_endpoint(directory_id: str, updated_directory: DirectoryCreate, db: Session = Depends(get_db)):
    try:
        # Convertimos el directory_id a UUID
        directory_id = UUID(directory_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de directory_id inválido")
    
    return update_directory(directory_id, updated_directory, db)

@router.delete("/directory/{directory_id}", response_model=DirectoryResponse)
def delete_directory_endpoint(directory_id: str, db: Session = Depends(get_db)):
    return delete_directory(directory_id, db)
