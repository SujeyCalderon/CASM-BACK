from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import shutil

from models.publications import Publication
from services.publications_service import (
    create_publication,
    get_publications,
    get_publication_by_id,
    update_publication,
    delete_publication
)
from schemas.schemas_publication import PublicationCreate, PublicationResponse
from db.database import get_db

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/publications/", response_model=PublicationResponse)
async def create_publication_endpoint(
    user_id: str = Form(...),
    description: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if image:
        filename = f"{uuid.uuid4()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    publication_data = PublicationCreate(
        user_id=user_id,
        description=description,
        image=image_path
    )

    created_publication = create_publication(db, publication_data)

 
    created_publication.id = str(created_publication.id)

    return created_publication


@router.get("/publications/", response_model=List[PublicationResponse])
def get_publications_endpoint(db: Session = Depends(get_db)):
    return get_publications(db)

@router.get("/publications/{publication_id}", response_model=PublicationResponse)
def get_publication_by_id_endpoint(publication_id: str, db: Session = Depends(get_db)):
    return get_publication_by_id(db, publication_id)

@router.put("/publications/{publication_id}", response_model=PublicationResponse)
def update_publication_endpoint(
    publication_id: str, updated_data: PublicationCreate, db: Session = Depends(get_db)
):
    return update_publication(db, publication_id, updated_data)
@router.put("/publications/{publication_id}", response_model=PublicationResponse)
def update_publication_endpoint(
    publication_id: str, updated_data: PublicationCreate, db: Session = Depends(get_db)
):
    updated_publication = update_publication(db, publication_id, updated_data)
    updated_publication.id = str(updated_publication.id)  
    return updated_publication

@router.delete("/publications/{publication_id}", response_model=PublicationResponse)
def delete_publication_endpoint(publication_id: str, db: Session = Depends(get_db)):
    deleted_publication = delete_publication(db, publication_id)
    deleted_publication.id = str(deleted_publication.id)  # el id es un string
    return deleted_publication

