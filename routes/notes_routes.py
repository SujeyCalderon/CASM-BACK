from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.notes import Note
from schemas.schemas_notes import NotesResponse, NoteCreate, NoteUpdate
from services.notes_service import create_note, get_note_by_id, get_notes, update_note, delete_note
from db.database import get_db
from utils.auth_middleware import get_current_user  # Importamos el middleware de autenticación
from models.user import User 
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/notes/", response_model=NotesResponse)
def create_note_endpoint(
    note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    db_note = Note(
        user_id=current_user.id_user,  # Usamos el ID del usuario autenticado
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
def get_notes_endpoint(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_notes(db, user_id=current_user.id_user)

@router.get("/notes/{note_id}", response_model=NotesResponse)
def get_note_by_id_endpoint(
    note_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    note = get_note_by_id(note_id, db)
    if note.user_id != current_user.id_user:  # Verificamos que la nota sea del usuario autenticado
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder a esta nota")
    return note

@router.put("/notes/{note_id}", response_model=NotesResponse)
def update_note_endpoint(
    note_id: UUID, updated_note: NoteUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    # Obtener la nota de la base de datos
    note = get_note_by_id(note_id, db)
    
    # Verificar que la nota exista
    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    # Comparar el user_id de la nota con el user_id del usuario autenticado
    if note.user_id != str(current_user.id_user):  # Asegúrate de que ambas sean del mismo tipo (UUID o str)
        raise HTTPException(status_code=403, detail="No tienes permisos para editar esta nota")
    
    # Si la verificación es exitosa, proceder con la actualización
    return update_note(note_id, updated_note, db)

@router.delete("/notes/{note_id}", response_model=NotesResponse)
def delete_note_endpoint(
    note_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    # Obtener la nota de la base de datos
    note = get_note_by_id(note_id, db)
    
    # Verificar que la nota exista
    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    # Comparar el user_id de la nota con el user_id del usuario autenticado
    if note.user_id != str(current_user.id_user):  # Asegúrate de que ambas sean del mismo tipo (UUID o str)
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar esta nota")
    
    # Si la verificación es exitosa, proceder con la eliminación
    return delete_note(note_id, db)

