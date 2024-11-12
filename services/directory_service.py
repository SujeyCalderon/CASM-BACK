from typing import List, Optional
from fastapi import HTTPException
from datetime import date
from models import User, Publication, Notes, Directory, Favorites, Role
import uuid  # Importamos uuid para generar IDs únicos

directories: List[Directory] = []
# Servicios para Directorio
def create_directory(directory: Directory) -> Directory:
    directory.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    directories.append(directory)
    return directory

def get_directories() -> List[Directory]:
    return directories

def get_directory_by_id(directory_id: str) -> Directory:
    directory = next((d for d in directories if d.id == directory_id), None)
    if directory is None:
        raise HTTPException(status_code=404, detail="Directorio no encontrado")
    return directory

def update_directory(directory_id: str, updated_directory: Directory) -> Directory:
    directory = get_directory_by_id(directory_id)
    update_data = updated_directory.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != "id":  # No permitir cambiar el ID
            setattr(directory, key, value)
    return directory

def delete_directory(directory_id: str) -> Directory:
    directory = get_directory_by_id(directory_id)
    directories.remove(directory)
    return directory