from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.directory import Directory
from schemas.schemas_directory import DirectoryCreate
import uuid

def create_directory(db: Session, directory_data: DirectoryCreate) -> Directory:
    new_directory = Directory(
        id=str(uuid.uuid4()),
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
