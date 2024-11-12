from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User as UserModel
from schemas import schemas_user

def create_user(db: Session, user: schemas_user) -> UserModel:
    db_user = UserModel(
        id=user.id,
        name=user.name,
        email=user.email,
        password=user.password,
        specialty=user.specialty,
        phone=user.phone,
        role=user.role,
        document=user.document,
        address=user.address,
        is_premium=user.is_premium
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(UserModel).all()

def get_user_by_id(db: Session, user_id: str):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def update_user(db: Session, user_id: str, updated_user: schemas_user):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar solo los campos proporcionados
    for field, value in updated_user.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: str):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    return user
