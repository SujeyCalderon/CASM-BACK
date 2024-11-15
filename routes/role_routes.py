# Rutas de Roles (routers/role_router.py)
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.schemas_role import RoleSchema  # Usamos el esquema Pydantic
from services.role_service import create_role, get_role_by_id, get_roles, update_role, delete_role
from models.role import Role
from db.database import get_db
from utils.auth_middleware import get_current_user  # Importamos la dependencia de autenticación
from models.user import User  # O el archivo donde esté definida la clase User
from typing import List
from uuid import UUID
router = APIRouter()

# Endpoint para crear un rol
@router.post("/roles/", response_model=RoleSchema)
def create_role_endpoint(role: RoleSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    role_db = Role(name=role.name)  
    created_role = create_role(db, role_db)
    created_role.id = str(created_role.id)  
    return created_role

# Endpoint para obtener todos los roles
@router.get("/roles/", response_model=list[RoleSchema])
def get_roles_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    roles = get_roles(db)
    for role in roles:
        role.id = str(role.id) 
    return roles

# Endpoint para obtener un rol por ID
@router.get("/roles/{role_id}", response_model=RoleSchema)
def get_role_by_id_endpoint(role_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    role = get_role_by_id(db, role_id)
    role.id = str(role.id)  
    return role

@router.put("/roles/{role_id}", response_model=RoleSchema)
def update_role_endpoint(role_id: str, updated_role: RoleSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Primero, obtenemos el rol actual de la base de datos usando el role_id
    role_db = db.query(Role).filter(Role.id == role_id).first()

    # Si no se encuentra el rol, se lanza una excepción
    if not role_db:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Actualizamos los campos del rol con los datos proporcionados (excluding 'id')
    if updated_role.name:  # Solo actualizamos si hay un nuevo nombre
        role_db.name = updated_role.name

    # Guardamos los cambios en la base de datos
    db.commit()
    db.refresh(role_db)  # Refrescamos el objeto para obtener los datos actualizados

    # Convertir 'id' a str antes de devolverlo
    role_db.id = str(role_db.id)
    return role_db

# Endpoint para eliminar un rol
@router.delete("/roles/{role_id}", response_model=RoleSchema)
def delete_roles_endpoint(role_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted_role = delete_role(db, role_id)
    deleted_role.id = str(deleted_role.id)  
    return deleted_role
