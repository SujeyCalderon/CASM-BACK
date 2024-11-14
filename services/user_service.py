from sqlalchemy.orm import Session
from models.user import User
from schemas.schemas_user import UserRequest, UserUpdate, UserResponse
from fastapi import HTTPException
from passlib.context import CryptContext
from services.login_service import create_access_token

def get_all_users(db: Session):
    users = db.query(User).all()
    # Convertimos los UUID a cadena para cada usuario
    return [
        UserResponse(
            id_user=str(user.id_user),
            name=user.name,
            last_name=user.last_name,
            email=user.email,
            speciality=user.speciality,
            phone=user.phone,
            role=user.role,
            document=user.document,
            profile_img=user.profile_img,
            id_referency=str(user.id_referency) if user.id_referency else None,
            premium=user.premium
        )
        for user in users
    ]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(user_data: UserRequest, db: Session):
    # Hasheamos la contraseña
    hashed_password = hash_password(user_data.password)
    # Excluimos 'password' del diccionario al pasarlo a User
    user_data_dict = user_data.dict(exclude={'password'})
    
    # Creamos el nuevo usuario, pasando la contraseña hasheada
    new_user = User(**user_data_dict, password=hashed_password)
    
    # Guardamos el nuevo usuario en la base de datos
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Crear el token para el nuevo usuario
    access_token = create_access_token(data={"sub": new_user.id_user})
    
    # Retornamos la respuesta con los datos del nuevo usuario y el token
    return UserResponse(
        id_user=str(new_user.id_user),
        name=new_user.name,
        last_name=new_user.last_name,
        email=new_user.email,
        speciality=new_user.speciality,
        phone=new_user.phone,
        role=new_user.role,
        document=new_user.document,
        profile_img=new_user.profile_img,
        id_referency=str(new_user.id_referency) if new_user.id_referency else None,
        premium=new_user.premium,
        access_token=access_token  # Incluye el token en la respuesta
    )

def get_user_by_id(user_id: str, db: Session):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Convertimos UUIDs a cadena
    return UserResponse(
        id_user=str(user.id_user),
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        speciality=user.speciality,
        phone=user.phone,
        role=user.role,
        document=user.document,
        profile_img=user.profile_img,
        id_referency=str(user.id_referency) if user.id_referency else None,
        premium=user.premium
    )

def update_user(user_id: str, updated_user: UserUpdate, db: Session):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    updated_data = updated_user.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    # Convertimos UUIDs a cadena
    return UserResponse(
        id_user=str(user.id_user),
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        speciality=user.speciality,
        phone=user.phone,
        role=user.role,
        document=user.document,
        profile_img=user.profile_img,
        id_referency=str(user.id_referency) if user.id_referency else None,
        premium=user.premium
    )

def delete_user(user_id: str, db: Session):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}
