from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.routes._orchestrator_utils import validate_event_type
from app.db.session import get_db
from app.models.event_spec import EventSpec
from app.schemas.event_spec import EventSpecCreate, EventSpecRead, EventSpecUpdate
router = APIRouter(prefix="/api/event-specs", tags=["event-specs"])
@router.get("", response_model=list[EventSpecRead])
def list_event_specs(db: Session = Depends(get_db)):
    return db.execute(select(EventSpec).order_by(EventSpec.name)).scalars().all()
@router.post("", response_model=EventSpecRead, status_code=status.HTTP_201_CREATED)
def create_event_spec(payload: EventSpecCreate, db: Session = Depends(get_db)):
    validate_event_type(payload.event_type)
    if db.execute(select(EventSpec).where(EventSpec.code == payload.code)).scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Event spec code already exists")
    item = EventSpec(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@router.put("/{item_id}", response_model=EventSpecRead)
def update_event_spec(item_id: str, payload: EventSpecUpdate, db: Session = Depends(get_db)):
    item = db.get(EventSpec, item_id)
    if not item: raise HTTPException(status_code=404, detail="Event spec not found")
    data = payload.model_dump(exclude_unset=True)
    if "event_type" in data and data["event_type"] is not None: validate_event_type(data["event_type"])
    for k, v in data.items(): setattr(item, k, v)
    db.commit(); db.refresh(item); return item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event_spec(item_id: str, db: Session = Depends(get_db)):
    item = db.get(EventSpec, item_id)
    if not item: raise HTTPException(status_code=404, detail="Event spec not found")
    db.delete(item); db.commit(); return None
