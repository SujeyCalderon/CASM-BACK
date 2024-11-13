from typing import List
from fastapi import HTTPException
from models.role import Role
import uuid

# Lista para almacenar roles en memoria temporalmente (puedes reemplazar esto por acceso a la base de datos)
roles: List[Role] = []

# Servicios para Roles
def create_role(role: Role) -> Role:
    role.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    roles.append(role)
    return role

def get_roles() -> List[Role]:
    return roles

def get_role_by_id(role_id: str) -> Role:
    role = next((r for r in roles if r.id == role_id), None)
    if role is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role

def update_role(role_id: str, updated_role: Role) -> Role:
    role = get_role_by_id(role_id)
    update_data = updated_role.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != "id":  # No permitir cambiar el ID
            setattr(role, key, value)
    return role

def delete_role(role_id: str) -> Role:
    role = next((f for f in roles if f.id == role_id), None)
    if role is None:
        raise HTTPException(status_code=404, detail="Role no encontrado")
    roles.remove(role)
    return role
