from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.favorites import Favorites as DBFavorites
from schemas.schemas_favorites import Favorites
from services.favorites_service import create_favorite, get_favorites_by_id, get_favorites, delete_favorite
from db.database import get_db
from utils.auth_middleware import get_current_user  # Importamos el middleware de autenticación
from models.user import User  # O el archivo donde esté definida la clase User
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/favorites/", response_model=Favorites)
def create_favorite_endpoint(
    favorite: Favorites, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    favorite.user_id = current_user.id_user  # Usamos el ID del usuario autenticado
    return create_favorite(db=db, favorite=favorite)

@router.get("/favorites/", response_model=List[Favorites])
def get_favorites_endpoint(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_favorites(db, user_id=current_user.id_user)

@router.get("/favorites/{favorite_id}", response_model=Favorites)
def get_favorites_by_id_endpoint(
    favorite_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    favorite = get_favorites_by_id(db, favorite_id)
    if favorite.user_id != current_user.id_user:  # Verificamos que el favorito sea del usuario autenticado
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder a este favorito")
    return favorite

@router.delete("/favorites/{favorite_id}", response_model=Favorites)
def delete_favorite_endpoint(
    favorite_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    favorite = get_favorites_by_id(db, favorite_id)
    if favorite.user_id != current_user.id_user:  # Verificamos que el favorito sea del usuario autenticado
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar este favorito")
    return delete_favorite(db, favorite_id)
