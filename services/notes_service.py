import uuid
from typing import List
from datetime import date
from fastapi import HTTPException
from models.notes import Notes

# Lista temporal de notas (en una base de datos real se utilizaría una base de datos)
notes: List[Notes] = []

def create_note(note: Notes) -> Notes:
    note.id = str(uuid.uuid4())  # Genera un ID único
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
    # Obtener la nota existente
    note = get_note_by_id(note_id)

    # Convertir el modelo actualizado a un diccionario, excluyendo los campos no establecidos
    update_data = updated_note.dict(exclude_unset=True)

    # Actualizar los campos proporcionados
    for key, value in update_data.items():
        if value is not None and key != "id":  # No permitir modificar el ID
            setattr(note, key, value)

    # Actualizar la fecha de modificación
    note.modification_date = date.today()

    return note

def delete_note(note_id: str) -> Notes:
    note = get_note_by_id(note_id)
    notes.remove(note)
    return note
