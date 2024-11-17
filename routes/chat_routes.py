from fastapi import APIRouter, HTTPException, Depends
from schemas.chat_schemas import MensajeBase, MensajeResponse
from db.database import chat_collection
from typing import List
from bson import ObjectId
from utils.auth_middleware import get_current_user  
from models.user import User


router = APIRouter()

@router.post("/", response_model=MensajeResponse)
async def enviar_mensaje(mensaje: MensajeBase, current_user: User = Depends(get_current_user)):  # Cambiado a 'User'
    # Aquí agregamos el ID del usuario autenticado como remitente
    mensaje_dict = mensaje.dict()
    mensaje_dict["id_remitente"] = str(current_user.id_user)  # Accedemos a 'id_user' de current_user
    
    # Insertar en la colección y obtener el ID generado
    result = await chat_collection.insert_one(mensaje_dict)
    
    # Mapear `_id` de MongoDB al campo `id` del modelo
    return MensajeResponse(
        id=str(result.inserted_id),
        **mensaje_dict  # Pasar los demás campos del mensaje
    )

@router.get("/leidos/recibidos/{id_destinatario}", response_model=List[MensajeResponse])
async def obtener_mensajes_enviados(id_destinatario: str):
    mensajes = []
    # Buscar mensajes donde el destinatario sea el especificado
    async for mensaje in chat_collection.find({"id_destinatario": id_destinatario}):
        print(f"Mensaje encontrado: {mensaje}")  # Para depurar y verificar lo que se encuentra
        # Mapear `_id` de MongoDB al campo `id` del modelo
        mensajes.append(
            MensajeResponse(
                id=str(mensaje["_id"]),
                id_remitente=mensaje["id_remitente"],
                id_destinatario=mensaje["id_destinatario"],
                mensaje=mensaje["mensaje"],
                fecha_envio=mensaje["fecha_envio"],
                estado=mensaje["estado"]
            )
        )
    
    if not mensajes:
        print(f"No se encontraron mensajes para el destinatario {id_destinatario}")
    
    return mensajes

@router.patch("/leer/{mensaje_id}", response_model=MensajeResponse)
async def marcar_como_leido(mensaje_id: str, id_destinatario: str):
    # Agregar un log para verificar los valores de los parámetros
    print(f"Buscando mensaje con ID: {mensaje_id} para el destinatario: {id_destinatario}")
    
    # Buscar el mensaje en la base de datos
    mensaje = await chat_collection.find_one({"_id": ObjectId(mensaje_id), "id_destinatario": id_destinatario})
    
    if not mensaje:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado o no autorizado para marcarlo como leído")
    
    # Agregar otro log para verificar si el mensaje fue encontrado
    print(f"Mensaje encontrado: {mensaje}")
    
    # Si el mensaje ya está leído, no hacer nada
    if mensaje["estado"] == "leído":
        raise HTTPException(status_code=400, detail="El mensaje ya ha sido marcado como leído")

    # Actualizar el estado del mensaje a "leído"
    updated_mensaje = await chat_collection.update_one(
        {"_id": mensaje["_id"]},
        {"$set": {"estado": "leído"}}
    )

    if updated_mensaje.modified_count == 0:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el estado del mensaje")
    
    # Retornar el mensaje actualizado
    return MensajeResponse(
        id=str(mensaje["_id"]),
        id_remitente=mensaje["id_remitente"],
        id_destinatario=mensaje["id_destinatario"],
        mensaje=mensaje["mensaje"],
        fecha_envio=mensaje["fecha_envio"],
        estado="leído"
    )
#casm
