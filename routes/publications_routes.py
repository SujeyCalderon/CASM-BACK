from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import shutil

from models.publications import Publication
from services.publications_service import create_publication, get_publications, get_publication_by_id, delete_publication
from schemas.schemas_publication import PublicationCreate, PublicationResponse
from db.database import get_db
from utils.auth_middleware import get_current_user
from models.user import User
from uuid import UUID

router = APIRouter()
UPLOAD_DIR = "uploads"

# Aseguramos que el directorio de subida exista
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/publications/", response_model=PublicationResponse)
async def create_publication_endpoint(
    description: str = Form(...),  # Usamos Form para recibir texto
    image: UploadFile = File(None),  # Usamos File para recibir el archivo de imagen (opcional)
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Aseguramos que el usuario esté autenticado
):
    # Si se sube una imagen, la guardamos
    image_path = None
    if image:
        filename = f"{uuid.uuid4()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    # Convertir el `user_id` de UUID a string antes de pasarlo al modelo Pydantic
    user_id_str = str(current_user.id_user)

    # Usamos los datos proporcionados por el cliente (incluyendo la imagen si la hay)
    publication_data = PublicationCreate(
        user_id=user_id_str,  # Asignamos el ID del usuario como una cadena
        description=description,
        image=image_path  # Si hay una imagen, la asignamos
    )

    # Llamamos al servicio para crear la publicación
    return create_publication(db, publication_data)

@router.get("/publications/", response_model=List[PublicationResponse])
def get_publications_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_publications(db, user_id=current_user.id_user)

@router.get("/publications/{publication_id}", response_model=PublicationResponse)
def get_publication_by_id_endpoint(
    publication_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    publication = get_publication_by_id(db, publication_id)
    if publication.user_id != current_user.id_user:  # Verificamos que la publicación sea del usuario autenticado
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder a esta publicación")
    return publication

@router.put("/publications/{publication_id}", response_model=PublicationResponse)
async def update_publication_endpoint(
    publication_id: UUID,
    description: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    publication = get_publication_by_id(db, publication_id)
    
    if str(publication.user_id) != str(current_user.id_user):
        raise HTTPException(status_code=403, detail="No tienes permisos para editar esta publicación")

    image_path = publication.image
    if image:
        filename = f"{uuid.uuid4()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    publication.description = description
    publication.image = image_path
    db.commit()
    db.refresh(publication)

    # Convertimos `id` a string en la respuesta
    return PublicationResponse(
        id=str(publication.id),
        user_id=str(publication.user_id),
        description=publication.description,
        image=publication.image
    )


@router.delete("/publications/{publication_id}", response_model=PublicationResponse)
def delete_publication_endpoint(
    publication_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Obtenemos la publicación a eliminar
    publication = get_publication_by_id(db, publication_id)
    
    # Verificamos que el usuario autenticado sea el dueño de la publicación
    if str(publication.user_id) != str(current_user.id_user):
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta publicación")

    # Eliminamos la publicación de la base de datos
    db.delete(publication)
    db.commit()

    # Devolvemos los datos de la publicación eliminada con `id` convertido a string
    return PublicationResponse(
        id=str(publication.id),
        user_id=str(publication.user_id),
        description=publication.description,
        image=publication.image
    )
