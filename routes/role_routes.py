from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import shutil
import uuid
from models import  Role
from services import (
 create_role, get_roles, get_role_by_id, update_role, delete_role
)

router = APIRouter()
# Endpoints Roles
@router.post("/roles/", response_model=Role)
def create_role_endpoint(role: Role):
    return create_role(role)

@router.get("/roles/", response_model=list[Role])
def get_roles_endpoint():
    return get_roles()

@router.get("/roles/{role_id}", response_model=Role)
def get_role_by_id_endpoint(role_id: str):  # Cambiado a str
    return get_role_by_id(role_id)

@router.put("/roles/{role_id}", response_model=Role)
def update_role_endpoint(role_id: str, updated_role: Role):
    return update_role(role_id, updated_role)


@router.delete("/roles/{role_id}", response_model=Role)
def delete_roles_endpoint(role_id: str):  # Cambiado a str
    return delete_role(role_id)