from typing import List, Optional
from fastapi import HTTPException
from datetime import date
from models.user import User
from models.publications import Publication
from models.notes import Notes
from models.directory import Directory
from models.favorites import Favorites
from models.role import Role
import uuid  # Importamos uuid para generar IDs únicos

# Lista para almacenar notas en memoria (esto es temporal; en producción, usarías una base de datos)
notes: List[Notes] = []

# Servicios para Notas
def create_note(note: Notes) -> Notes:
    note.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    notes.append(note)
    return note

def get_notes() -> List[Notes]:
    return notes

def get_note_by_id(note_id: str) -> Notes:
    note = next((n for n in notes if n.id == note_id), None)
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return note

def update_note(note_id: str, updated_note: Notes) -> Notes:
    # Recuperar la nota actual por ID
    note = get_note_by_id(note_id)

    # Convertir el modelo actualizado a un diccionario, excluyendo los campos no establecidos
    update_data = updated_note.dict(exclude_unset=True)

    # Actualizar solo los campos que fueron proporcionados y no son None
    for key, value in update_data.items():
        if value is not None and key != "id":  # No permitir cambiar el ID
            setattr(note, key, value)

    # Actualizar la fecha de modificación
    note.modification_date = date.today()

    return note

def delete_note(note_id: str) -> Notes:
    note = get_note_by_id(note_id)
    notes.remove(note)
    return note
