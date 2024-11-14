from fastapi import APIRouter,Depends
from typing import List  # Asegúrate de importar List de typing
from models.favorites import Favorites as DBFavorites  # Este es el modelo SQLAlchemy
from schemas.schemas_favorites import Favorites  # Este es el modelo Pydantic
from services.favorites_service import create_favorite, get_favorites_by_id, get_favorites, delete_favorite
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter()

@router.post("/favorites/", response_model=Favorites)
def create_favorite_endpoint(favorite: Favorites, db: Session = Depends(get_db)):
    return create_favorite(db=db, favorite=favorite)

@router.get("/favorites/", response_model=List[Favorites])  # Aquí se usa List de typing
def get_favorites_endpoint():
    return get_favorites()

@router.get("/favorites/{favorite_id}", response_model=Favorites)
def get_favorites_by_id_endpoint(favorite_id: str):
    return get_favorites_by_id(favorite_id)

@router.delete("/favorites/{favorite_id}", response_model=Favorites)
def delete_favorite_endpoint(favorite_id: str):
    return delete_favorite(favorite_id)
