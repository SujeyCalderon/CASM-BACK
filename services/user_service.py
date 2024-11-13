from sqlalchemy.orm import Session
from models.user import User
from schemas.schemas_user import UserRequest, UserUpdate
from fastapi import HTTPException

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(user_data: UserRequest, db: Session):
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(user_id: str, db: Session):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def update_user(user_id: str, updated_user: UserUpdate, db: Session):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    updated_data = updated_user.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: str, db: Session):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    return user
