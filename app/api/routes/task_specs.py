from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.routes._orchestrator_utils import validate_task_type
from app.db.session import get_db
from app.models.task_spec import TaskSpec
from app.schemas.task_spec import TaskSpecCreate, TaskSpecRead, TaskSpecUpdate
router = APIRouter(prefix="/api/task-specs", tags=["task-specs"])
@router.get("", response_model=list[TaskSpecRead])
def list_task_specs(task_type: str | None = Query(default=None), is_active: bool | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(TaskSpec).order_by(TaskSpec.name)
    if task_type: stmt = stmt.where(TaskSpec.task_type == task_type)
    if is_active is not None: stmt = stmt.where(TaskSpec.is_active == is_active)
    return db.execute(stmt).scalars().all()
@router.post("", response_model=TaskSpecRead, status_code=status.HTTP_201_CREATED)
def create_task_spec(payload: TaskSpecCreate, db: Session = Depends(get_db)):
    validate_task_type(payload.task_type)
    if db.execute(select(TaskSpec).where(TaskSpec.code == payload.code)).scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Task spec code already exists")
    item = TaskSpec(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@router.put("/{item_id}", response_model=TaskSpecRead)
def update_task_spec(item_id: str, payload: TaskSpecUpdate, db: Session = Depends(get_db)):
    item = db.get(TaskSpec, item_id)
    if not item: raise HTTPException(status_code=404, detail="Task spec not found")
    data = payload.model_dump(exclude_unset=True)
    if "task_type" in data and data["task_type"] is not None: validate_task_type(data["task_type"])
    for k, v in data.items(): setattr(item, k, v)
    db.commit(); db.refresh(item); return item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_spec(item_id: str, db: Session = Depends(get_db)):
    item = db.get(TaskSpec, item_id)
    if not item: raise HTTPException(status_code=404, detail="Task spec not found")
    db.delete(item); db.commit(); return None
