from fastapi import APIRouter
from models.favorites import Favorites as DBFavorites  # Este es el modelo de SQLAlchemy
from schemas.schemas_favorites import Favorites  # Este es el modelo Pydantic que FastAPI usará
from services.favorites_service import create_favorite, get_favorites_by_id, get_favorites, delete_favorite

router = APIRouter()

@router.post("/favorites/", response_model=Favorites)  # Usar el modelo Pydantic aquí
def create_favorite_endpoint(favorite: Favorites):
    return create_favorite(favorite)

@router.get("/favorites/", response_model=list[Favorites])  # Usar el modelo Pydantic aquí
def get_favorites_endpoint():
    return get_favorites()

@router.get("/favorites/{favorite_id}", response_model=Favorites)  # Usar el modelo Pydantic aquí
def get_favorites_by_id_endpoint(favorite_id: str):
    return get_favorites_by_id(favorite_id)

@router.delete("/favorites/{favorite_id}", response_model=Favorites)  # Usar el modelo Pydantic aquí
def delete_favorite_endpoint(favorite_id: str):
    return delete_favorite(favorite_id)
