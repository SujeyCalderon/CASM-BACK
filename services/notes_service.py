from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.notes import Note
from datetime import date
from schemas.schemas_notes import NotesResponse, NoteUpdate
from uuid import UUID

def create_note(note_data: NotesResponse, db: Session) -> NotesResponse:
    # Crear una nueva nota
    new_note = Note(
        user_id=note_data.user_id,
        title=note_data.title,
        description=note_data.description,
        creation_date=date.today(),
        modification_date=date.today()
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def get_notes(db: Session) -> list[NotesResponse]:
    return db.query(Note).all()

def get_note_by_id(note_id: str, db: Session) -> NotesResponse:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return note

def update_note(note_id: UUID, updated_note: NoteUpdate, db: Session) -> NotesResponse:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    # Actualizar solo los campos proporcionados
    for key, value in updated_note.dict(exclude_unset=True).items():
        if value is not None:  # Solo actualizar los campos con valores no nulos
            setattr(note, key, value)

    # Actualizar la fecha de modificación
    note.modification_date = date.today()

    db.commit()
    db.refresh(note)
    return note

def delete_note(note_id: str, db: Session) -> NotesResponse:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    db.delete(note)
    db.commit()
    return note
