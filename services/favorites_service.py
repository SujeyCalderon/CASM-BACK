from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.favorites import Favorites as DBFavorites  # El modelo SQLAlchemy
from schemas.schemas_favorites import Favorites  # El modelo Pydantic
import uuid

# Crear un favorito
def create_favorite(db: Session, favorite: Favorites) -> DBFavorites:
    # Asegúrate de que el ID sea un UUID válido
    favorite.id = uuid.UUID(favorite.id)  # Si el ID es un string UUID válido
    db_favorite = DBFavorites(**favorite.dict())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite
# Obtener todos los favoritos
def get_favorites(db: Session) -> List[Favorites]:
    favorites = db.query(DBFavorites).all()
    return [Favorites.from_orm(favorite) for favorite in favorites]

# Obtener un favorito por ID
def get_favorites_by_id(db: Session, favorite_id: str) -> Favorites:
    favorite = db.query(DBFavorites).filter(DBFavorites.id == favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return Favorites.from_orm(favorite)

# Eliminar un favorito
def delete_favorite(db: Session, favorite_id: str) -> Favorites:
    favorite = db.query(DBFavorites).filter(DBFavorites.id == favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
    return Favorites.from_orm(favorite)
