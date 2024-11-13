from typing import List, Optional
from fastapi import HTTPException
from datetime import date
from models.user import User
from models.publications import Publication
from models.notes import Notes
from models.directory import Directory
from models.favorites import Favorites
from models.role import Role
from models.favorites import Favorites as DBFavorites  # Este es el modelo SQLAlchemy

import uuid  # Importamos uuid para generar IDs únicos

# Lista para almacenar favoritos en memoria (esto es temporal; en producción, usarías una base de datos)
favorites: List[Favorites] = []

# Servicios para Favoritos
def create_favorite(favorite: Favorites) -> Favorites:
    favorite_id = str(uuid.uuid4())
    favorite_data = DBFavorites(id=favorite_id, **favorite.dict())  # Usar el modelo de DB aquí
    favorites.append(favorite_data)  # Guarda en la lista de favoritos
    return Favorites.from_orm(favorite_data)  # Devuelve un modelo Pydantic


def get_favorites() -> List[Favorites]:
    return favorites

def get_favorites_by_id(favorite_id: str) -> Favorites:
    # Llama a get_favorites() para obtener la lista de favoritos
    favorites_list = get_favorites()

    # Busca el favorito específico por ID
    favorite = next((d for d in favorites_list if d.id == favorite_id), None)
    
    # Si no se encuentra el favorito, lanza una excepción HTTP 404
    if favorite is None:
        raise HTTPException(status_code=404, detail="Favorite no encontrado")
    
    return favorite

def delete_favorite(favorite_id: str) -> Favorites:
    favorite = next((f for f in favorites if f.id == favorite_id), None)
    if favorite is None:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    favorites.remove(favorite)
    return favorite
