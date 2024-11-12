from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import shutil
import uuid
from models import  Favorites
from services import (
    create_favorite, get_favorites, get_favorites_by_id, delete_favorite
)

router = APIRouter()
# Endpoints Favorites
@router.post("/favorites/", response_model=Favorites)
def create_favorite_endpoint(favorite: Favorites):
    return create_favorite(favorite)

@router.get("/favorites/", response_model=list[Favorites])
def get_favorites_endpoint():
    return get_favorites()

@router.get("/favorites/{favorite_id}", response_model=Favorites)
def get_favorites_by_id_endpoint(favorite_id: str):  # Cambiado a str
    return get_favorites_by_id(favorite_id)

@router.delete("/favorites/{favorite_id}", response_model=Favorites)
def delete_favorite_endpoint(favorite_id: str):  # Cambiado a str
    return delete_favorite(favorite_id)