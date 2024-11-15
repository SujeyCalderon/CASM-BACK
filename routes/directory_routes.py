from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from uuid import UUID
import shutil
import os
import uuid
from models.user import User
from models.directory import Directory
from services.directory_service import create_directory
from schemas.schemas_directory import DirectoryCreate, DirectoryResponse
from db.database import get_db
from utils.auth_middleware import get_current_user
from typing import List  
from schemas.schemas_directory import DirectoryUpdate
# En routers/directory_router.py
from services.directory_service import update_directory
# En routes/directory_routes.py
from services.directory_service import get_directory_by_id






router = APIRouter()
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/directory/", response_model=DirectoryResponse)
async def create_directory_endpoint(
    name: str = Form(...),
    description: str = Form(None),
    phone: str = Form(None),
    direction: str = Form(None),
    email: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Procesar la imagen si existe
        image_path = None
        if image:
            file_extension = os.path.splitext(image.filename)[1]  # Obtener la extensión del archivo
            unique_filename = f"{uuid.uuid4()}{file_extension}"  # Generar un nombre único
            image_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            # Guardar la imagen en el directorio configurado
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            # Verificar si la imagen se guardó correctamente
            if not os.path.exists(image_path):
                raise HTTPException(status_code=500, detail="Error al guardar la imagen.")

        # Crear datos para el directorio con los valores recibidos
        directory_data = DirectoryCreate(
            user_id=current_user.id_user,  # El UUID del usuario autenticado
            name=name,
            description=description,
            phone=phone,
            direction=direction,
            email=email,
            image=image_path  # Ruta de la imagen guardada o None
        )

        # Crear el directorio en la base de datos
        directory = create_directory(directory_data, db)

        # Devolver la respuesta con los datos guardados
        return DirectoryResponse(
            id=str(directory.id),
            user_id=str(directory.user_id),
            name=directory.name,
            description=directory.description,
            phone=directory.phone,
            direction=directory.direction,
            email=directory.email,
            image=directory.image
        )

    except Exception as e:
        db.rollback()  # Revertir cambios en caso de error
        raise HTTPException(status_code=500, detail=f"Error al crear el directorio: {str(e)}")


@router.get("/directory/{directory_id}", response_model=DirectoryResponse)
def get_directory_by_id_endpoint(
    directory_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    directory = get_directory_by_id(directory_id, db)
    if directory.user_id != current_user.id_user:  # Verificamos que el directorio sea del usuario autenticado
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder a este directorio")
    return directory

@router.get("/directory/", response_model=List[DirectoryResponse])
def get_directories_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_directories(db, user_id=current_user.id_user)

@router.put("/directory/{directory_id}", response_model=DirectoryResponse)
async def update_directory_endpoint(
    directory_id: UUID,  # Cambiar a UUID
    name: str = Form(None),
    description: str = Form(None),
    phone: str = Form(None),
    direction: str = Form(None),
    email: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Obtener el directorio existente usando UUID
        directory = db.query(Directory).filter(Directory.id == directory_id).first()
        
        if not directory:
            raise HTTPException(status_code=404, detail="Directory not found")

        # Procesar la imagen si existe
        image_path = directory.image  # Mantener la imagen actual por defecto
        if image:
            # Eliminar la imagen anterior si existe
            if directory.image and os.path.exists(directory.image):
                os.remove(directory.image)

            # Guardar la nueva imagen
            file_extension = os.path.splitext(image.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            image_path = os.path.join(UPLOAD_DIR, unique_filename)

            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

        # Crear los datos actualizados para el directorio
        directory_data = DirectoryUpdate(
            name=name if name else directory.name,
            description=description if description else directory.description,
            phone=phone if phone else directory.phone,
            direction=direction if direction else directory.direction,
            email=email if email else directory.email,
            image=image_path if image else directory.image  # Usar la imagen existente si no hay una nueva
        )

        # Actualizar el directorio en la base de datos
        updated_directory = update_directory(directory_id, directory_data, db)  # Llamar a la función

        # Devolver la respuesta con los datos actualizados
        return DirectoryResponse(
            id=str(updated_directory.id),
            user_id=str(updated_directory.user_id),
            name=updated_directory.name,
            description=updated_directory.description,
            phone=updated_directory.phone,
            direction=updated_directory.direction,
            email=updated_directory.email,
            image=updated_directory.image  # Solo la ruta de la imagen, no el contenido binario
        )

    except Exception as e:
        db.rollback()  # Revertir cambios en caso de error
        raise HTTPException(status_code=500, detail=f"Error al actualizar el directorio: {str(e)}")
@router.delete("/directory/{directory_id}")
async def delete_directory_endpoint(directory_id: str, db: Session = Depends(get_db)):
    directory = get_directory_by_id(directory_id, db)  # Aquí obtienes el directorio por ID
    # Lógica para eliminar el directorio
    db.delete(directory)
    db.commit()
    return {"detail": "Directory deleted successfully"}

