from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
import shutil
import uuid
from models import  Notes
from services import (
  create_note, get_notes, get_note_by_id, update_note, delete_note
)

router = APIRouter()
# Endpoints Notes
@router.post("/notes/", response_model=Notes)
def create_note_endpoint(note: Notes):
    return create_note(note)

@router.get("/notes/", response_model=list[Notes])
def get_notes_endpoint():
    return get_notes()

@router.get("/notes/{note_id}", response_model=Notes)
def get_note_by_id_endpoint(note_id: str):  # Cambiado a str
    return get_note_by_id(note_id)

@router.put("/notes/{note_id}", response_model=Notes)
def update_note_endpoint(note_id: str, updated_note: Notes):
    return update_note(note_id, updated_note)

@router.delete("/notes/{note_id}", response_model=Notes)
def delete_note_endpoint(note_id: str):  # Cambiado a str
    return delete_note(note_id)
