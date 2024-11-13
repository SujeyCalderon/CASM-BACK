from fastapi import APIRouter, HTTPException
from schemas.schemas_role import RoleSchema  # Usamos el esquema Pydantic
from services.role_service import create_role, get_role_by_id, get_roles, update_role, delete_role
from models.role import Role

router = APIRouter()

# Endpoints Roles
@router.post("/roles/", response_model=RoleSchema)
def create_role_endpoint(role: RoleSchema):
    role_db = Role(name=role.name)  # Crea un objeto SQLAlchemy desde el esquema Pydantic
    return create_role(role_db)

@router.get("/roles/", response_model=list[RoleSchema])
def get_roles_endpoint():
    return get_roles()

@router.get("/roles/{role_id}", response_model=RoleSchema)
def get_role_by_id_endpoint(role_id: str):
    return get_role_by_id(role_id)

@router.put("/roles/{role_id}", response_model=RoleSchema)
def update_role_endpoint(role_id: str, updated_role: RoleSchema):
    role_db = Role(name=updated_role.name)  # Crea un objeto SQLAlchemy desde el esquema Pydantic
    return update_role(role_id, role_db)

@router.delete("/roles/{role_id}", response_model=RoleSchema)
def delete_roles_endpoint(role_id: str):
    return delete_role(role_id)
