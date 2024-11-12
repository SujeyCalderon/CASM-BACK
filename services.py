from typing import List, Optional
from fastapi import HTTPException
from datetime import date
from models import User, Publication, Notes, Directory, Favorites, Role
import uuid  # Importamos uuid para generar IDs únicos

# Estructuras de datos
users: List[User] = []
publications: List[Publication] = []
roles: List[Role] = []
notes: List[Notes] = []
directories: List[Directory] = []
favorites: List[Favorites] = []

# Servicios para usuarios
def create_user(user: User) -> User:
    if user.role == "voluntary" and not user.specialty:
        raise HTTPException(status_code=400, detail="La especialidad es requerida para voluntarios")
    
    user.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    users.append(user)
    return user

def get_users() -> List[User]:
    return users

def get_user_by_id(user_id: str) -> User:
    user = next((u for u in users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def update_user(user_id: str, updated_user: User) -> User:
    # Recuperar el usuario actual por ID
    user = get_user_by_id(user_id)
    
    # Verificar cada campo y actualizar solo si se proporcionó un nuevo valor
    if updated_user.name is not None:
        user.name = updated_user.name
    if updated_user.email is not None:
        user.email = updated_user.email
    if updated_user.password is not None:
        user.password = updated_user.password
    if updated_user.role is not None:
        user.role = updated_user.role
    if updated_user.specialty is not None:
        user.specialty = updated_user.specialty
    if updated_user.address is not None:
        user.address = updated_user.address
    if updated_user.document is not None:
        user.document = updated_user.document
    if updated_user.is_premium is not None:
        user.is_premium = updated_user.is_premium
    
    return user

def delete_user(user_id: str) -> User:
    user = get_user_by_id(user_id)
    users.remove(user)
    return user

# Servicio para autenticar usuario
def authenticate_user(email: str, password: str):
    user = next((u for u in users if u.email == email and u.password == password), None)
    if user is None:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    return {"message": "Inicio de sesión exitoso", "user": user}

# Servicios para publicaciones
def create_publication(publication: Publication) -> Publication:
    publication.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    publications.append(publication)
    return publication

def get_publications() -> List[Publication]:
    return publications

def get_publication_by_id(publication_id: str) -> Publication:
    publication = next((p for p in publications if p.id == publication_id), None)
    if publication is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return publication

def update_publication(publication_id: str, updated_publication: Publication) -> Publication:
    publication = get_publication_by_id(publication_id)
    update_data = updated_publication.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != "id":  # No permitir cambiar el ID
            setattr(publication, key, value)
    return publication

def delete_publication(publication_id: str) -> Publication:
    publication = get_publication_by_id(publication_id)
    publications.remove(publication)
    return publication

# Servicios para Notas
def create_note(note: Notes) -> Notes:
    note.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    notes.append(note)
    return note

def get_notes() -> List[Notes]:
    return notes

def get_note_by_id(note_id: str) -> Notes:
    note = next((n for n in notes if n.id == note_id), None)
    if note is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return note


def update_note(note_id: str, updated_note: Notes) -> Notes:
    # Recuperar la nota actual por ID
    note = get_note_by_id(note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada")

    # Convertir el modelo actualizado a un diccionario, excluyendo los campos no establecidos
    update_data = updated_note.dict(exclude_unset=True)

    # Actualizar solo los campos que fueron proporcionados y no son None
    for key, value in update_data.items():
        if value is not None and key != "id":  # No permitir cambiar el ID
            setattr(note, key, value)

    # Actualizar la fecha de modificación
    note.modification_date = date.today()

    return note


def delete_note(note_id: str) -> Notes:
    note = get_note_by_id(note_id)
    notes.remove(note)
    return note

# Servicios para Directorio
def create_directory(directory: Directory) -> Directory:
    directory.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    directories.append(directory)
    return directory

def get_directories() -> List[Directory]:
    return directories

def get_directory_by_id(directory_id: str) -> Directory:
    directory = next((d for d in directories if d.id == directory_id), None)
    if directory is None:
        raise HTTPException(status_code=404, detail="Directorio no encontrado")
    return directory

def update_directory(directory_id: str, updated_directory: Directory) -> Directory:
    directory = get_directory_by_id(directory_id)
    update_data = updated_directory.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != "id":  # No permitir cambiar el ID
            setattr(directory, key, value)
    return directory

def delete_directory(directory_id: str) -> Directory:
    directory = get_directory_by_id(directory_id)
    directories.remove(directory)
    return directory

# Servicios para Favoritos
def create_favorite(favorite: Favorites) -> Favorites:
    favorite.id = str(uuid.uuid4())  # Genera un ID único usando UUID
    if favorite not in favorites:  # Evitar duplicados
        favorites.append(favorite)
    return favorite

def get_favorites() -> List[Favorites]:
    return favorites

def get_favorites_by_id(favorite_id: str) -> Favorites:
    # Llama a get_favorites() para obtener la lista de favoritos
    favorites_list = get_favorites()

    # Busca el favorito específico por ID
    favorite = next((d for d in favorites_list if d.id == favorite_id), None)
    
    # Si no se encuentra el favorito, lanza una excepción HTTP 404
    if favorite is None:
        raise HTTPException(status_code=404, detail="Favorite no encontrado")
    
    return favorite


def delete_favorite(favorite_id: str) -> Favorites:
    favorite = next((f for f in favorites if f.id == favorite_id), None)
    if favorite is None:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    favorites.remove(favorite)
    return favorite

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