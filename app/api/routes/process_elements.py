from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.routes._orchestrator_utils import validate_element_type, validate_process_element_binding
from app.db.session import get_db
from app.models.event_spec import EventSpec
from app.models.gateway_spec import GatewaySpec
from app.models.process_element import ProcessElement
from app.models.process_spec import ProcessSpec
from app.models.task_spec import TaskSpec
from app.schemas.process_element import ProcessElementCreate, ProcessElementRead, ProcessElementUpdate
router = APIRouter(prefix="/api/process-elements", tags=["process-elements"])
@router.get("", response_model=list[ProcessElementRead])
def list_process_elements(process_spec_id: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(ProcessElement).order_by(ProcessElement.element_key)
    if process_spec_id: stmt = stmt.where(ProcessElement.process_spec_id == process_spec_id)
    return db.execute(stmt).scalars().all()
@router.post("", response_model=ProcessElementRead, status_code=status.HTTP_201_CREATED)
def create_process_element(payload: ProcessElementCreate, db: Session = Depends(get_db)):
    validate_element_type(payload.element_type)
    validate_process_element_binding(payload.element_type, payload.task_spec_id, payload.gateway_spec_id, payload.event_spec_id)
    if not db.get(ProcessSpec, payload.process_spec_id): raise HTTPException(status_code=404, detail="Process spec not found")
    exists = db.execute(select(ProcessElement).where(ProcessElement.process_spec_id == payload.process_spec_id, ProcessElement.element_key == payload.element_key)).scalar_one_or_none()
    if exists: raise HTTPException(status_code=409, detail="Element key already exists in process")
    if payload.task_spec_id and not db.get(TaskSpec, payload.task_spec_id): raise HTTPException(status_code=404, detail="Task spec not found")
    if payload.gateway_spec_id and not db.get(GatewaySpec, payload.gateway_spec_id): raise HTTPException(status_code=404, detail="Gateway spec not found")
    if payload.event_spec_id and not db.get(EventSpec, payload.event_spec_id): raise HTTPException(status_code=404, detail="Event spec not found")
    item = ProcessElement(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@router.put("/{item_id}", response_model=ProcessElementRead)
def update_process_element(item_id: str, payload: ProcessElementUpdate, db: Session = Depends(get_db)):
    item = db.get(ProcessElement, item_id)
    if not item: raise HTTPException(status_code=404, detail="Process element not found")
    for k, v in payload.model_dump(exclude_unset=True).items(): setattr(item, k, v)
    db.commit(); db.refresh(item); return item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process_element(item_id: str, db: Session = Depends(get_db)):
    item = db.get(ProcessElement, item_id)
    if not item: raise HTTPException(status_code=404, detail="Process element not found")
    db.delete(item); db.commit(); return None
