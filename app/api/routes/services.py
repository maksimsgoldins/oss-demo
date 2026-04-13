from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate

router = APIRouter(prefix="/api/services", tags=["services"])

@router.get("", response_model=list[ServiceRead])
def list_services(db: Session = Depends(get_db)):
    return db.execute(select(Service).order_by(Service.name)).scalars().all()

@router.get("/{service_id}", response_model=ServiceRead)
def get_service(service_id: str, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    if payload.type not in {"CFS","RFS","Resource"}:
        raise HTTPException(status_code=400, detail="Invalid service type")
    exists = db.execute(select(Service).where(Service.code == payload.code)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Service code already exists")
    obj = Service(code=payload.code, name=payload.name, type=payload.type, description=payload.description)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put("/{service_id}", response_model=ServiceRead)
def update_service(service_id: str, payload: ServiceUpdate, db: Session = Depends(get_db)):
    obj = db.get(Service, service_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Service not found")
    if payload.type and payload.type not in {"CFS","RFS","Resource"}:
        raise HTTPException(status_code=400, detail="Invalid service type")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: str, db: Session = Depends(get_db)):
    obj = db.get(Service, service_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(obj); db.commit()
    return None
