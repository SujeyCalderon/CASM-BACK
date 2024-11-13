from sqlalchemy.orm import Session
from models.referency import Referency
from schemas.schemas_referency import ReferencyRequest, ReferencyUpdate
from fastapi import HTTPException

def get_all_referencies(db: Session):
    return db.query(Referency).all()

def create_referency(referency_data: ReferencyRequest, db: Session):
    new_referency = Referency(**referency_data.dict())
    db.add(new_referency)
    db.commit()
    db.refresh(new_referency)
    return new_referency

def get_referency_by_id(referency_id: str, db: Session):
    referency = db.query(Referency).filter(Referency.id_referency == referency_id).first()
    if not referency:
        raise HTTPException(status_code=404, detail="Referencia no encontrada")
    return referency

def update_referency(referency_id: str, updated_referency: ReferencyUpdate, db: Session):
    referency = db.query(Referency).filter(Referency.id_referency == referency_id).first()
    if not referency:
        raise HTTPException(status_code=404, detail="Referencia no encontrada")
    
    updated_data = updated_referency.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(referency, key, value)
    
    db.commit()
    db.refresh(referency)
    return referency

def delete_referency(referency_id: str, db: Session):
    referency = db.query(Referency).filter(Referency.id_referency == referency_id).first()
    if not referency:
        raise HTTPException(status_code=404, detail="Referencia no encontrada")
    
    db.delete(referency)
    db.commit()
    return referency
