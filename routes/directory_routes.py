from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import shutil
import uuid
from models import  Directory
from services import (
    create_directory, get_directories, get_directory_by_id, update_directory, delete_directory,
)

router = APIRouter()
# Directory Endpoint y la imagen
@router.post("/directory/", response_model=Directory)
async def create_directory_endpoint(
    user_id: str = Form(...),  # Cambiado a str
    name: str = Form(None),
    description: str = Form(None),
    phone: str = Form(None),
    direction: str = Form(None),
    email: str = Form(None),
    image: UploadFile = None
):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    image_path = None
    if image:
        image_path = os.path.join(upload_dir, image.filename)
        with open(image_path, "wb") as file:
            content = await image.read()
            file.write(content)

    directory = Directory(
        id="0",  # Cambiado a str
        user_id=user_id,
        name=name,
        description=description,
        phone=phone,
        direction=direction,
        email=email,
        image=image_path
    )
    return create_directory(directory)

@router.get("/directory/", response_model=list[Directory])
def get_directories_endpoint():
    return get_directories()

@router.get("/directory/{directory_id}", response_model=Directory)
def get_directory_by_id_endpoint(directory_id: str):  # Cambiado a str
    return get_directory_by_id(directory_id)

@router.put("/directory/{directory_id}", response_model=Directory)
def update_directory_endpoint(directory_id: str, updated_directory: Directory):  # Cambiado a str
    return update_directory(directory_id, updated_directory)

@router.delete("/directory/{directory_id}", response_model=Directory)
def delete_directory_endpoint(directory_id: str):  # Cambiado a str
    return delete_directory(directory_id)