from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.routes._orchestrator_utils import validate_dependency_task_elements, validate_dependency_type, validate_element_belongs_to_process
from app.db.session import get_db
from app.models.inter_process_dependency import InterProcessTaskDependency
from app.models.process_element import ProcessElement
from app.models.process_spec import ProcessSpec
from app.schemas.inter_process_dependency import InterProcessTaskDependencyCreate, InterProcessTaskDependencyRead, InterProcessTaskDependencyUpdate
router = APIRouter(prefix="/api/inter-process-dependencies", tags=["inter-process-dependencies"])
@router.get("", response_model=list[InterProcessTaskDependencyRead])
def list_inter_process_dependencies(source_process_spec_id: str | None = Query(default=None), target_process_spec_id: str | None = Query(default=None), service_relation_id: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(InterProcessTaskDependency).order_by(InterProcessTaskDependency.id)
    if source_process_spec_id: stmt = stmt.where(InterProcessTaskDependency.source_process_spec_id == source_process_spec_id)
    if target_process_spec_id: stmt = stmt.where(InterProcessTaskDependency.target_process_spec_id == target_process_spec_id)
    if service_relation_id: stmt = stmt.where(InterProcessTaskDependency.service_relation_id == service_relation_id)
    return db.execute(stmt).scalars().all()
@router.post("", response_model=InterProcessTaskDependencyRead, status_code=status.HTTP_201_CREATED)
def create_inter_process_dependency(payload: InterProcessTaskDependencyCreate, db: Session = Depends(get_db)):
    validate_dependency_type(payload.dependency_type)
    if not db.get(ProcessSpec, payload.source_process_spec_id) or not db.get(ProcessSpec, payload.target_process_spec_id):
        raise HTTPException(status_code=404, detail="Source or target process spec not found")
    source = db.get(ProcessElement, payload.source_element_id); target = db.get(ProcessElement, payload.target_element_id)
    if not source or not target: raise HTTPException(status_code=404, detail="Source or target element not found")
    validate_element_belongs_to_process(source, payload.source_process_spec_id)
    validate_element_belongs_to_process(target, payload.target_process_spec_id)
    validate_dependency_task_elements(source, target)
    item = InterProcessTaskDependency(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@router.put("/{item_id}", response_model=InterProcessTaskDependencyRead)
def update_inter_process_dependency(item_id: str, payload: InterProcessTaskDependencyUpdate, db: Session = Depends(get_db)):
    item = db.get(InterProcessTaskDependency, item_id)
    if not item: raise HTTPException(status_code=404, detail="Inter-process dependency not found")
    data = payload.model_dump(exclude_unset=True)
    if "dependency_type" in data and data["dependency_type"] is not None: validate_dependency_type(data["dependency_type"])
    for k, v in data.items(): setattr(item, k, v)
    db.commit(); db.refresh(item); return item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inter_process_dependency(item_id: str, db: Session = Depends(get_db)):
    item = db.get(InterProcessTaskDependency, item_id)
    if not item: raise HTTPException(status_code=404, detail="Inter-process dependency not found")
    db.delete(item); db.commit(); return None
