from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import uuid

from models.directory import Directory
from services.directory_service import create_directory
from schemas.schemas_directory import DirectoryCreate, DirectoryResponse
from db.database import get_db

router = APIRouter()
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Endpoint para crear un nuevo directorio
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
    return create_directory(db, directory_data)
