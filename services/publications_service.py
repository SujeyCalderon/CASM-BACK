from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.publications import Publication
from schemas.schemas_publication import PublicationCreate
import uuid

def create_publication(db: Session, publication_data: PublicationCreate) -> Publication:
    publication = Publication(
        id=str(uuid.uuid4()),
        user_id=publication_data.user_id,
        description=publication_data.description,
        image=publication_data.image
    )
    db.add(publication)
    db.commit()
    db.refresh(publication)
    return publication

def get_publications(db: Session):
    return db.query(Publication).all()

def get_publication_by_id(db: Session, publication_id: str) -> Publication:
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication

def update_publication(db: Session, publication_id: str, updated_data: PublicationCreate) -> Publication:
    publication = get_publication_by_id(db, publication_id)
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(publication, key, value)
    db.commit()
    db.refresh(publication)
    return publication

def delete_publication(db: Session, publication_id: str) -> Publication:
    publication = get_publication_by_id(db, publication_id)
    db.delete(publication)
    db.commit()
    return publication
