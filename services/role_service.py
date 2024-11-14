from typing import List
from fastapi import HTTPException
from models.role import Role
import uuid
from sqlalchemy.orm import Session

# Crear un rol
def create_role(db: Session, role_data: Role) -> Role:
    role = Role(
        name=role_data.name  # El ID se genera automáticamente como UUID
    )
    db.add(role)
    db.commit()
    db.refresh(role)

    # Convertir 'id' a str antes de devolverlo
    role.id = str(role.id)
    return role

# Obtener todos los roles
def get_roles(db: Session) -> List[Role]:
    roles = db.query(Role).all()

    # Convierte los ids a str antes de devolverlos
    for role in roles:
        role.id = str(role.id)
        
    return roles

# Obtener un rol por ID
def get_role_by_id(db: Session, role_id: str) -> Role:
    role = db.query(Role).filter(Role.id == role_id).first()
    if role is None:
        raise HTTPException(status_code=404, detail="Role no encontrado")

    # Convertir 'id' a str antes de devolverlo
    role.id = str(role.id)
    return role

# Actualizar un rol
def update_role(db: Session, role_id: str, updated_role: Role) -> Role:
    # Obtenemos el rol actual de la base de datos
    role = get_role_by_id(db, role_id)

    # Actualizamos los campos del rol solo si el nuevo valor no es None
    if updated_role.name:
        role.name = updated_role.name

    # Guardamos los cambios
    db.commit()
    db.refresh(role)

    # Aseguramos que el id sea de tipo string al devolverlo
    role.id = str(role.id)
    return role

# Eliminar un rol
def delete_role(db: Session, role_id: str) -> Role:
    role = get_role_by_id(db, role_id)
    db.delete(role)
    db.commit()
    
    # Convertir 'id' a str antes de devolverlo
    role.id = str(role.id)
    return role
