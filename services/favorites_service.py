from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.favorites import Favorites as DBFavorites
from schemas.schemas_favorites import Favorites
import uuid
from uuid import UUID

# Crear un favorito
def create_favorite(db: Session, favorite: Favorites) -> DBFavorites:
    if not favorite.id:
        favorite.id = uuid.uuid4()
    db_favorite = DBFavorites(
        id=favorite.id,
        user_id=favorite.user_id,
        publication_id=favorite.publication_id
    )
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def get_favorites(db: Session, user_id: UUID):
    return db.query(DBFavorites).filter(DBFavorites.user_id == user_id).all()


# Obtener un favorito por ID
def get_favorites_by_id(db: Session, favorite_id: UUID) -> Favorites:
    favorite = db.query(DBFavorites).filter(DBFavorites.id == favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return Favorites.from_orm(favorite)

# Eliminar un favorito
def delete_favorite(db: Session, favorite_id: UUID) -> Favorites:
    favorite = db.query(DBFavorites).filter(DBFavorites.id == favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
    return Favorites.from_orm(favorite)
