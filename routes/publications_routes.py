from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
import shutil
import uuid
from models import Publication
from services import (
    create_publication, get_publications, get_publication_by_id, update_publication, delete_publication
)

router = APIRouter()
# Endpoint Publications y para la imagen
@router.post("/publications/", response_model=Publication)
async def create_publication_endpoint(
    user_id: str = Form(...),  # Cambiado a str
    description: str = Form(None),
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

    publication = Publication(
        id="0",  # Cambiado a str
        user_id=user_id,
        description=description,
        image=image_path
    )
    return create_publication(publication)

@router.get("/publications/", response_model=list[Publication])
def get_publications_endpoint():
    return get_publications()

@router.get("/publications/{publication_id}", response_model=Publication)
def get_publication_by_id_endpoint(publication_id: str):  # Cambiado a str
    return get_publication_by_id(publication_id)

@router.put("/publications/{publication_id}", response_model=Publication)
def update_publication_endpoint(publication_id: str, updated_publication: Publication):  # Cambiado a str
    return update_publication(publication_id, updated_publication)

@router.delete("/publications/{publication_id}", response_model=Publication)
def delete_publication_endpoint(publication_id: str):  # Cambiado a str
    return delete_publication(publication_id)