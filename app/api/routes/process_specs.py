from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.routes._orchestrator_utils import validate_process_status, validate_sub_aim_belongs_to_aim
from app.db.session import get_db
from app.models.order_aim import OrderAim
from app.models.process_spec import ProcessSpec
from app.models.service import Service
from app.schemas.process_spec import ProcessSpecCreate, ProcessSpecRead, ProcessSpecUpdate
router = APIRouter(prefix="/api/process-specs", tags=["process-specs"])
@router.get("", response_model=list[ProcessSpecRead])
def list_process_specs(service_spec_id: str | None = Query(default=None), order_aim_id: str | None = Query(default=None), order_sub_aim_id: str | None = Query(default=None), status_value: str | None = Query(default=None, alias="status"), db: Session = Depends(get_db)):
    stmt = select(ProcessSpec).order_by(ProcessSpec.name, ProcessSpec.version)
    if service_spec_id: stmt = stmt.where(ProcessSpec.service_spec_id == service_spec_id)
    if order_aim_id: stmt = stmt.where(ProcessSpec.order_aim_id == order_aim_id)
    if order_sub_aim_id: stmt = stmt.where(ProcessSpec.order_sub_aim_id == order_sub_aim_id)
    if status_value: stmt = stmt.where(ProcessSpec.status == status_value)
    return db.execute(stmt).scalars().all()
@router.post("", response_model=ProcessSpecRead, status_code=status.HTTP_201_CREATED)
def create_process_spec(payload: ProcessSpecCreate, db: Session = Depends(get_db)):
    validate_process_status(payload.status)
    if not db.get(Service, payload.service_spec_id): raise HTTPException(status_code=404, detail="Service spec not found")
    if not db.get(OrderAim, payload.order_aim_id): raise HTTPException(status_code=404, detail="Order aim not found")
    validate_sub_aim_belongs_to_aim(db, payload.order_sub_aim_id, payload.order_aim_id)
    if db.execute(select(ProcessSpec).where(ProcessSpec.code == payload.code)).scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Process spec code already exists")
    dup = db.execute(select(ProcessSpec).where(ProcessSpec.service_spec_id == payload.service_spec_id, ProcessSpec.order_aim_id == payload.order_aim_id, ProcessSpec.order_sub_aim_id == payload.order_sub_aim_id, ProcessSpec.version == payload.version)).scalar_one_or_none()
    if dup: raise HTTPException(status_code=409, detail="Process spec for service/aim/sub-aim/version already exists")
    item = ProcessSpec(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@router.put("/{item_id}", response_model=ProcessSpecRead)
def update_process_spec(item_id: str, payload: ProcessSpecUpdate, db: Session = Depends(get_db)):
    item = db.get(ProcessSpec, item_id)
    if not item: raise HTTPException(status_code=404, detail="Process spec not found")
    data = payload.model_dump(exclude_unset=True)
    if "status" in data and data["status"] is not None: validate_process_status(data["status"])
    for k, v in data.items(): setattr(item, k, v)
    db.commit(); db.refresh(item); return item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process_spec(item_id: str, db: Session = Depends(get_db)):
    item = db.get(ProcessSpec, item_id)
    if not item: raise HTTPException(status_code=404, detail="Process spec not found")
    db.delete(item); db.commit(); return None
