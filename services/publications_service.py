from sqlalchemy.orm import Session
from models.publications import Publication
from schemas.schemas_publication import PublicationCreate
from fastapi import HTTPException
import uuid

def create_publication(db: Session, publication_data: PublicationCreate) -> Publication:
    publication = Publication(
        id=str(uuid.uuid4()),  # Convertir el id a str en el momento de creación
        user_id=publication_data.user_id,
        description=publication_data.description,
        image=publication_data.image
    )
    db.add(publication)
    db.commit()
    db.refresh(publication)

    # Convertir 'id' a str antes de devolverlo
    publication.id = str(publication.id)
    
    return publication


def get_publications(db: Session):
    publications = db.query(Publication).all()

    # Convierte los ids a str antes de devolver la lista
    for publication in publications:
        publication.id = str(publication.id)
        
    return publications


def get_publication_by_id(db: Session, publication_id: str) -> Publication:
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    # Convierte el id a str antes de devolverlo
    publication.id = str(publication.id)
    
    return publication


def update_publication(db: Session, publication_id: str, updated_data: PublicationCreate) -> Publication:
    publication = get_publication_by_id(db, publication_id)
    
    # Actualiza los campos de la publicación
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(publication, key, value)

    db.commit()
    db.refresh(publication)

    # Convertir 'id' de UUID a str antes de devolverlo
    publication.id = str(publication.id)  # Asegúrate de que el 'id' sea un string

    return publication

def delete_publication(db: Session, publication_id: str) -> Publication:
    publication = get_publication_by_id(db, publication_id)
    db.delete(publication)
    db.commit()
    
    # Convertir 'id' de UUID a str antes de devolverlo
    publication.id = str(publication.id)  # Asegúrate de que el 'id' sea un string

    return publication

