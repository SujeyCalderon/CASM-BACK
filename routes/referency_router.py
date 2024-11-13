from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas.schemas_referency import ReferencyRequest, ReferencyResponse, ReferencyUpdate
from services.referency_service import (
    create_referency,
    get_all_referencies,
    get_referency_by_id,
    update_referency,
    delete_referency,
)

router = APIRouter()

@router.post("/referencies/", response_model=ReferencyResponse)
async def create_referency_endpoint(
    calle: str = Form(...),
    ciudad: str = Form(...),
    estado: str = Form(...),
    codigo_postal: str = Form(...),
    db: Session = Depends(get_db)
):
    referency_data = ReferencyRequest(
        calle=calle,
        ciudad=ciudad,
        estado=estado,
        codigo_postal=codigo_postal
    )
    return create_referency(referency_data, db)

@router.get("/referencies/", response_model=List[ReferencyResponse])
def get_referencies_endpoint(db: Session = Depends(get_db)):
    return get_all_referencies(db)

@router.get("/referencies/{referency_id}", response_model=ReferencyResponse)
def get_referency_by_id_endpoint(referency_id: str, db: Session = Depends(get_db)):
    return get_referency_by_id(referency_id, db)

@router.put("/referencies/{referency_id}", response_model=ReferencyResponse)
def update_referency_endpoint(referency_id: str, updated_referency: ReferencyUpdate, db: Session = Depends(get_db)):
    return update_referency(referency_id, updated_referency, db)

@router.delete("/referencies/{referency_id}", response_model=ReferencyResponse)
def delete_referency_endpoint(referency_id: str, db: Session = Depends(get_db)):
    return delete_referency(referency_id, db)
