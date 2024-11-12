from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import shutil
import uuid
from models import User, Publication, LoginRequest, LoginResponse, Notes, Directory, Favorites, Role
from services import (
    create_user, get_users, get_user_by_id, update_user, delete_user,
    create_publication, get_publications, get_publication_by_id, update_publication, delete_publication,
    authenticate_user, create_note, get_notes, get_note_by_id, update_note, delete_note,
    create_directory, get_directories, get_directory_by_id, update_directory, delete_directory,
    create_favorite, get_favorites, get_favorites_by_id, delete_favorite, create_role, get_roles, get_role_by_id, update_role, delete_role
)

router = APIRouter()

# Endpoints Users
@router.post("/user/", response_model=User)
async def create_user_endpoint(
    name: str,
    email: str,
    password: str,
    specialty: Optional[str] = None,
    phone: Optional[str] = None,
    role: Optional[str] = None,
    document: UploadFile = File(...), 
    address: Optional[str] = None,
    is_premium: Optional[bool] = False
):
    # Guardamos el archivo PDF en la carpeta uploads y generamos un nombre único
    unique_filename = f"{uuid.uuid4()}_{document.filename}"
    file_path = f"uploads/{unique_filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)

    
    user = User(
        name=name,
        email=email,
        password=password,
        specialty=specialty,
        phone=phone,
        role=role,
        document=file_path,  
        address=address,
        is_premium=is_premium
    )

    return create_user(user)

@router.get("/users/", response_model=list[User])
def get_users_endpoint():
    return get_users()

@router.get("/users/{user_id}", response_model=User)
def get_user_by_id_endpoint(user_id: str):
    return get_user_by_id(user_id)

@router.put("/users/{user_id}", response_model=User)
def update_user_endpoint(user_id: str, updated_user: User):
    return update_user(user_id, updated_user)

@router.delete("/users/{user_id}", response_model=User)
def delete_user_endpoint(user_id: str):
    return delete_user(user_id)

# Login Endpoint
@router.post("/login", response_model=LoginResponse)
def login_endpoint(login_data: LoginRequest):
    return authenticate_user(login_data.email, login_data.password)

# Endpoint Publications y para la imagen
@router.post("/publications/", response_model=Publication)
async def create_publication_endpoint(
    user_id: str = Form(...),  # Cambiado a str
    description: str = Form(None),
    image: UploadFile = None
):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    image_path = None
    if image:
        image_path = os.path.join(upload_dir, image.filename)
        with open(image_path, "wb") as file:
            content = await image.read()
            file.write(content)

    publication = Publication(
        id="0",  # Cambiado a str
        user_id=user_id,
        description=description,
        image=image_path
    )
    return create_publication(publication)

@router.get("/publications/", response_model=list[Publication])
def get_publications_endpoint():
    return get_publications()

@router.get("/publications/{publication_id}", response_model=Publication)
def get_publication_by_id_endpoint(publication_id: str):  # Cambiado a str
    return get_publication_by_id(publication_id)

@router.put("/publications/{publication_id}", response_model=Publication)
def update_publication_endpoint(publication_id: str, updated_publication: Publication):  # Cambiado a str
    return update_publication(publication_id, updated_publication)

@router.delete("/publications/{publication_id}", response_model=Publication)
def delete_publication_endpoint(publication_id: str):  # Cambiado a str
    return delete_publication(publication_id)

# Endpoints Notes
@router.post("/notes/", response_model=Notes)
def create_note_endpoint(note: Notes):
    return create_note(note)

@router.get("/notes/", response_model=list[Notes])
def get_notes_endpoint():
    return get_notes()

@router.get("/notes/{note_id}", response_model=Notes)
def get_note_by_id_endpoint(note_id: str):  # Cambiado a str
    return get_note_by_id(note_id)

@router.put("/notes/{note_id}", response_model=Notes)
def update_note_endpoint(note_id: str, updated_note: Notes):
    return update_note(note_id, updated_note)

@router.delete("/notes/{note_id}", response_model=Notes)
def delete_note_endpoint(note_id: str):  # Cambiado a str
    return delete_note(note_id)

# Directory Endpoint y la imagen
@router.post("/directory/", response_model=Directory)
async def create_directory_endpoint(
    user_id: str = Form(...),  # Cambiado a str
    name: str = Form(None),
    description: str = Form(None),
    phone: str = Form(None),
    direction: str = Form(None),
    email: str = Form(None),
    image: UploadFile = None
):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    image_path = None
    if image:
        image_path = os.path.join(upload_dir, image.filename)
        with open(image_path, "wb") as file:
            content = await image.read()
            file.write(content)

    directory = Directory(
        id="0",  # Cambiado a str
        user_id=user_id,
        name=name,
        description=description,
        phone=phone,
        direction=direction,
        email=email,
        image=image_path
    )
    return create_directory(directory)

@router.get("/directory/", response_model=list[Directory])
def get_directories_endpoint():
    return get_directories()

@router.get("/directory/{directory_id}", response_model=Directory)
def get_directory_by_id_endpoint(directory_id: str):  # Cambiado a str
    return get_directory_by_id(directory_id)

@router.put("/directory/{directory_id}", response_model=Directory)
def update_directory_endpoint(directory_id: str, updated_directory: Directory):  # Cambiado a str
    return update_directory(directory_id, updated_directory)

@router.delete("/directory/{directory_id}", response_model=Directory)
def delete_directory_endpoint(directory_id: str):  # Cambiado a str
    return delete_directory(directory_id)

# Endpoints Favorites
@router.post("/favorites/", response_model=Favorites)
def create_favorite_endpoint(favorite: Favorites):
    return create_favorite(favorite)

@router.get("/favorites/", response_model=list[Favorites])
def get_favorites_endpoint():
    return get_favorites()

@router.get("/favorites/{favorite_id}", response_model=Favorites)
def get_favorites_by_id_endpoint(favorite_id: str):  # Cambiado a str
    return get_favorites_by_id(favorite_id)

@router.delete("/favorites/{favorite_id}", response_model=Favorites)
def delete_favorite_endpoint(favorite_id: str):  # Cambiado a str
    return delete_favorite(favorite_id)

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