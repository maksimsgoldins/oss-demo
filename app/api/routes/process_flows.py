from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.routes._orchestrator_utils import validate_element_belongs_to_process, validate_flow_type
from app.db.session import get_db
from app.models.process_element import ProcessElement
from app.models.process_flow import ProcessFlow
from app.models.process_spec import ProcessSpec
from app.schemas.process_flow import ProcessFlowCreate, ProcessFlowRead, ProcessFlowUpdate
router = APIRouter(prefix="/api/process-flows", tags=["process-flows"])
@router.get("", response_model=list[ProcessFlowRead])
def list_process_flows(process_spec_id: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(ProcessFlow).order_by(ProcessFlow.id)
    if process_spec_id: stmt = stmt.where(ProcessFlow.process_spec_id == process_spec_id)
    return db.execute(stmt).scalars().all()
@router.post("", response_model=ProcessFlowRead, status_code=status.HTTP_201_CREATED)
def create_process_flow(payload: ProcessFlowCreate, db: Session = Depends(get_db)):
    validate_flow_type(payload.flow_type)
    if not db.get(ProcessSpec, payload.process_spec_id): raise HTTPException(status_code=404, detail="Process spec not found")
    source = db.get(ProcessElement, payload.source_element_id); target = db.get(ProcessElement, payload.target_element_id)
    if not source or not target: raise HTTPException(status_code=404, detail="Source or target element not found")
    validate_element_belongs_to_process(source, payload.process_spec_id)
    validate_element_belongs_to_process(target, payload.process_spec_id)
    if payload.source_element_id == payload.target_element_id: raise HTTPException(status_code=400, detail="Self-loop is not allowed in v1")
    item = ProcessFlow(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@router.put("/{item_id}", response_model=ProcessFlowRead)
def update_process_flow(item_id: str, payload: ProcessFlowUpdate, db: Session = Depends(get_db)):
    item = db.get(ProcessFlow, item_id)
    if not item: raise HTTPException(status_code=404, detail="Process flow not found")
    data = payload.model_dump(exclude_unset=True)
    if "flow_type" in data and data["flow_type"] is not None: validate_flow_type(data["flow_type"])
    for k, v in data.items(): setattr(item, k, v)
    db.commit(); db.refresh(item); return item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process_flow(item_id: str, db: Session = Depends(get_db)):
    item = db.get(ProcessFlow, item_id)
    if not item: raise HTTPException(status_code=404, detail="Process flow not found")
    db.delete(item); db.commit(); return None
