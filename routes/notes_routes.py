from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.schemas_notes import NotesResponse, NoteCreate, NoteUpdate
from services.notes_service import create_note, get_note_by_id, get_notes, update_note, delete_note
from db.database import get_db
from uuid import UUID
from models.notes import Note
from fastapi import Depends

router = APIRouter()

@router.post("/notes/", response_model=NotesResponse)
def create_note_endpoint(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(  
        user_id=note.user_id,
        title=note.title,
        description=note.description,
        creation_date=note.creation_date,
        modification_date=note.modification_date
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return NotesResponse.from_orm(db_note)

@router.get("/notes/", response_model=List[NotesResponse])
def get_notes_endpoint(db: Session = Depends(get_db)):
    return get_notes(db)

@router.get("/notes/{note_id}", response_model=NotesResponse)
def get_note_by_id_endpoint(note_id: str, db: Session = Depends(get_db)):
    return get_note_by_id(note_id, db)

@router.put("/notes/{note_id}", response_model=NotesResponse)
def update_note_endpoint(note_id: UUID, updated_note: NoteUpdate, db: Session = Depends(get_db)):
    return update_note(note_id, updated_note, db)

@router.delete("/notes/{note_id}", response_model=NotesResponse)
def delete_note_endpoint(note_id: str, db: Session = Depends(get_db)):
    return delete_note(note_id, db)
