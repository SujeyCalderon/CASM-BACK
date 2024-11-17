from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import List
import os
import uuid
import shutil
from bson import ObjectId
from fastapi.responses import JSONResponse  # Asegúrate de importarlo


from db.database import publications_collection
from services.publications_service import (
    create_publication,
    get_publications,
    get_publication_by_id,
    update_publication,
    delete_publication
)
from schemas.schemas_publication import PublicationCreate, PublicationResponse
from utils.auth_middleware import get_current_user
from models.user import User

router = APIRouter()
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/publications/", response_model=PublicationResponse)
async def create_publication_endpoint(
    description: str = Form(...),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user)
):
    image_path = None
    if image:
        filename = f"{uuid.uuid4()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    publication_data = PublicationCreate(
        user_id=str(current_user.id_user),
        description=description,
        image=image_path
    )

    # Ahora esta respuesta debe incluir el campo `id` (no `_id`)
    created_publication = await create_publication(publication_data)
    return created_publication  # Esta respuesta ahora incluye 'id' como campo 

@router.get("/publications/", response_model=List[PublicationResponse])
async def get_publications_endpoint(current_user: User = Depends(get_current_user)):
    return await get_publications(str(current_user.id_user))

@router.get("/publications/{publication_id}", response_model=PublicationResponse)
async def get_publication_by_id_endpoint(publication_id: str):
    return await get_publication_by_id(publication_id)

@router.put("/publications/{publication_id}", response_model=PublicationResponse)
async def update_publication_endpoint(
    publication_id: str,
    description: str = Form(None),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user)
):
    image_path = None
    if image:
        filename = f"{uuid.uuid4()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    updated_data = PublicationCreate(
        user_id=str(current_user.id_user),
        description=description,
        image=image_path
    )
    updated_publication = await update_publication(publication_id, updated_data)
    
    # No es necesario renombrar _id a id si ya lo manejamos en el servicio
    return updated_publication

@router.delete("/publications/{publication_id}", status_code=200)
async def delete_publication_endpoint(publication_id: str, current_user: User = Depends(get_current_user)):
    # Mostrar el publication_id recibido
    print(f"Trying to delete publication with ID: {publication_id}")

    # Convertir el publication_id a ObjectId
    try:
        publication_id_obj = ObjectId(publication_id)  # Convertir el string a ObjectId
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid publication ID format")

    # Verificar si la publicación existe
    publication = await publications_collection.find_one({"_id": publication_id_obj})

    if not publication:
        print(f"Publication with ID {publication_id} not found")  # Mensaje de depuración
        raise HTTPException(status_code=404, detail="Publication not found")
    
    # Depuración: Verificar los valores
    print(f"Current user ID: {current_user.id_user}")
    print(f"Publication owner ID: {publication['user_id']}")
    
    # Verificar si el usuario tiene permisos para eliminar la publicación
    if str(publication["user_id"]) != str(current_user.id_user):
        raise HTTPException(status_code=403, detail="Not authorized to delete this publication")

    # Realizar la eliminación
    await publications_collection.delete_one({"_id": publication_id_obj})

    # Retornar un mensaje indicando que la publicación fue eliminada con éxito
    return JSONResponse(status_code=200, content={"message": "Publication successfully deleted"})