from db.database import publications_collection
from bson.objectid import ObjectId
from schemas.schemas_publication import PublicationCreate
from fastapi import HTTPException

async def create_publication(publication_data: PublicationCreate) -> dict:
    publication = publication_data.dict()
    result = await publications_collection.insert_one(publication)
    # Asegúrate de que el campo _id sea convertido a id
    publication["_id"] = str(result.inserted_id)  # Convierte ObjectId a string
    publication["id"] = publication.pop("_id")  # Renombra _id a id
    return publication

async def get_publications(user_id: str) -> list:
    publications = []
    async for publication in publications_collection.find({"user_id": user_id}):
        publication["_id"] = str(publication["_id"])
        publications.append(publication)
    return publications

async def get_publication_by_id(publication_id: str) -> dict:
    publication = await publications_collection.find_one({"_id": ObjectId(publication_id)})
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    publication["_id"] = str(publication["_id"])
    return publication

async def update_publication(publication_id: str, updated_data: PublicationCreate) -> dict:
    # Verificar si la publicación existe
    existing_publication = await publications_collection.find_one({"_id": ObjectId(publication_id)})
    if not existing_publication:
        raise HTTPException(status_code=404, detail="Publication not found")

    # Verificar si el usuario tiene permisos para actualizar
    if existing_publication["user_id"] != updated_data.user_id:
        raise HTTPException(status_code=403, detail="No tienes permisos para editar esta publicación")

    # Actualizar campos específicos
    update_fields = updated_data.dict(exclude_unset=True)
    result = await publications_collection.find_one_and_update(
        {"_id": ObjectId(publication_id)},
        {"$set": update_fields},
        return_document=True
    )

    # Asegurarse de que _id esté presente después de la actualización
    if result:
        result["_id"] = str(result["_id"])  # Convertir ObjectId a string
        result["id"] = result.pop("_id")  # Renombrar _id a id

    return result

async def delete_publication(publication_id: str) -> dict:
    result = await publications_collection.find_one_and_delete({"_id": ObjectId(publication_id)})
    if not result:
        raise HTTPException(status_code=404, detail="Publication not found")
    result["_id"] = str(result["_id"])
    return result
