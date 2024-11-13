from fastapi import APIRouter, HTTPException
from typing import List
from schemas.schemas_notes import NotesResponse  # Usamos el modelo de Pydantic
from services.notes_service import create_note, get_note_by_id, get_notes, update_note, delete_note

router = APIRouter()

# Endpoints Notes
@router.post("/notes/", response_model=NotesResponse)  # Cambiado a NotesResponse
def create_note_endpoint(note: NotesResponse):
    return create_note(note)

@router.get("/notes/", response_model=List[NotesResponse])  # Cambiado a NotesResponse
def get_notes_endpoint():
    return get_notes()

@router.get("/notes/{note_id}", response_model=NotesResponse)  # Cambiado a NotesResponse
def get_note_by_id_endpoint(note_id: str):
    return get_note_by_id(note_id)

@router.put("/notes/{note_id}", response_model=NotesResponse)  # Cambiado a NotesResponse
def update_note_endpoint(note_id: str, updated_note: NotesResponse):
    return update_note(note_id, updated_note)

@router.delete("/notes/{note_id}", response_model=NotesResponse)  # Cambiado a NotesResponse
def delete_note_endpoint(note_id: str):
    return delete_note(note_id)
