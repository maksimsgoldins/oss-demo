from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.service import Service, ServiceAimMapping
from app.models.order_aim import OrderAim, OrderSubAim
from app.schemas.service_aim_mapping import ServiceAimMappingCreate, ServiceAimMappingRead

router = APIRouter(prefix="/api/service-aim-mappings", tags=["service-aim-mappings"])

@router.get("", response_model=list[ServiceAimMappingRead])
def list_service_aim_mappings(service_id: str | None = None, db: Session = Depends(get_db)):
    stmt = select(ServiceAimMapping)
    if service_id:
        stmt = stmt.where(ServiceAimMapping.service_id == service_id)
    return db.execute(stmt).scalars().all()

@router.post("", response_model=ServiceAimMappingRead, status_code=status.HTTP_201_CREATED)
def create_service_aim_mapping(payload: ServiceAimMappingCreate, db: Session = Depends(get_db)):
    service = db.get(Service, payload.service_id)
    aim = db.get(OrderAim, payload.order_aim_id)
    sub = db.get(OrderSubAim, payload.order_sub_aim_id)
    if not service: raise HTTPException(status_code=404, detail="Service not found")
    if not aim: raise HTTPException(status_code=404, detail="Order aim not found")
    if not sub: raise HTTPException(status_code=404, detail="Order sub-aim not found")
    if sub.order_aim_id != payload.order_aim_id:
        raise HTTPException(status_code=400, detail="Sub-aim does not belong to selected aim")
    exists = db.execute(select(ServiceAimMapping).where(
        ServiceAimMapping.service_id==payload.service_id,
        ServiceAimMapping.order_aim_id==payload.order_aim_id,
        ServiceAimMapping.order_sub_aim_id==payload.order_sub_aim_id
    )).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Service aim mapping already exists")
    obj = ServiceAimMapping(service_id=payload.service_id, order_aim_id=payload.order_aim_id, order_sub_aim_id=payload.order_sub_aim_id)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/{mapping_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_aim_mapping(mapping_id: str, db: Session = Depends(get_db)):
    obj = db.get(ServiceAimMapping, mapping_id)
    if not obj: raise HTTPException(status_code=404, detail="Service aim mapping not found")
    db.delete(obj); db.commit()
    return None
