from sqlalchemy.orm import Session
from models.directory import Directory
from schemas.schemas_directory import DirectoryCreate
from fastapi import HTTPException
# En services/directory_service.py
from schemas.schemas_directory import DirectoryUpdate


from uuid import UUID

import uuid  # Asegúrate de importar el módulo uuid

def create_directory(directory_data: DirectoryCreate, db: Session) -> Directory:
    new_directory = Directory(
        id=str(uuid.uuid4()),  # Convertir el UUID a string
        user_id=directory_data.user_id,
        name=directory_data.name,
        description=directory_data.description,
        phone=directory_data.phone,
        direction=directory_data.direction,
        email=directory_data.email,
        image=directory_data.image
    )
    db.add(new_directory)
    db.commit()
    db.refresh(new_directory)
    return new_directory


def get_directory_by_id(directory_id: str, db: Session) -> Directory:
    directory = db.query(Directory).filter(Directory.id == directory_id).first()
    if directory is None:
        raise HTTPException(status_code=404, detail="Directorio no encontrado")
    return directory

def get_directories(db: Session) -> list[Directory]:
    return db.query(Directory).all()

def update_directory(directory_id: str, updated_directory: DirectoryUpdate, db: Session) -> Directory:
    directory = db.query(Directory).filter(Directory.id == directory_id).first()
    if not directory:
        raise HTTPException(status_code=404, detail="Directory not found")

    for field, value in updated_directory.dict(exclude_unset=True).items():
        setattr(directory, field, value)

    db.commit()
    db.refresh(directory)
    return directory

def delete_directory(directory_id: str, db: Session) -> Directory:
    directory = db.query(Directory).filter(Directory.id == directory_id).first()
    if directory is None:
        raise HTTPException(status_code=404, detail="Directorio no encontrado")

    db.delete(directory)
    db.commit()
    return directory
