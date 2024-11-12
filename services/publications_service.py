from typing import List, Optional
from fastapi import HTTPException
from datetime import date
from models import User, Publication, Notes, Directory, Favorites, Role
import uuid  # Importamos uuid para generar IDs únicos

publications: List[Publication] = []
def create_publication(publication: Publication) -> Publication:
    publication.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    publications.append(publication)
    return publication

def get_publications() -> List[Publication]:
    return publications

def get_publication_by_id(publication_id: str) -> Publication:
    publication = next((p for p in publications if p.id == publication_id), None)
    if publication is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return publication

def update_publication(publication_id: str, updated_publication: Publication) -> Publication:
    publication = get_publication_by_id(publication_id)
    update_data = updated_publication.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != "id":  # No permitir cambiar el ID
            setattr(publication, key, value)
    return publication

def delete_publication(publication_id: str) -> Publication:
    publication = get_publication_by_id(publication_id)
    publications.remove(publication)
    return publication
