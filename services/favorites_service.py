from typing import List, Optional
from fastapi import HTTPException
from datetime import date
from models import User, Publication, Notes, Directory, Favorites, Role
import uuid  # Importamos uuid para generar IDs únicos


favorites: List[Favorites] = []
# Servicios para Favoritos
def create_favorite(favorite: Favorites) -> Favorites:
    favorite.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    if favorite not in favorites:  # Evitar duplicados
        favorites.append(favorite)
    return favorite

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