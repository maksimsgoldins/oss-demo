from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.service import Service, ServiceAimMapping, ServiceRelation
from app.schemas.relation import RelationCreate, RelationRead, RelationUpdate

router = APIRouter(prefix="/api/relations", tags=["relations"])

def mapping_exists(db, service_id, aim_id, sub_id):
    return db.execute(select(ServiceAimMapping).where(
        ServiceAimMapping.service_id==service_id,
        ServiceAimMapping.order_aim_id==aim_id,
        ServiceAimMapping.order_sub_aim_id==sub_id
    )).scalar_one_or_none() is not None

def validate_relation(db, parent_service_id, child_service_id, parent_aim_id, parent_sub_id, child_aim_id, child_sub_id):
    if parent_service_id == child_service_id:
        raise HTTPException(status_code=400, detail="Self-relation is not allowed")
    parent = db.get(Service, parent_service_id)
    child = db.get(Service, child_service_id)
    if not parent or not child:
        raise HTTPException(status_code=404, detail="Parent or child service not found")
    valid = (parent.type=="CFS" and child.type=="RFS") or (parent.type=="RFS" and child.type=="Resource")
    if not valid:
        raise HTTPException(status_code=400, detail="Only CFS->RFS and RFS->Resource relations are allowed")
    if not mapping_exists(db, parent_service_id, parent_aim_id, parent_sub_id):
        raise HTTPException(status_code=400, detail="Parent service aim mapping does not exist")
    if not mapping_exists(db, child_service_id, child_aim_id, child_sub_id):
        raise HTTPException(status_code=400, detail="Child service aim mapping does not exist")

@router.get("", response_model=list[RelationRead])
def list_relations(parent_service_id: str | None = None, db: Session = Depends(get_db)):
    stmt = select(ServiceRelation)
    if parent_service_id:
        stmt = stmt.where(ServiceRelation.parent_service_id == parent_service_id)
    return db.execute(stmt).scalars().all()

@router.post("", response_model=RelationRead, status_code=status.HTTP_201_CREATED)
def create_relation(payload: RelationCreate, db: Session = Depends(get_db)):
    if payload.instantiation_mode not in {"CREATE","REUSE"}:
        raise HTTPException(status_code=400, detail="Invalid instantiation mode")
    validate_relation(db, payload.parent_service_id, payload.child_service_id, payload.parent_order_aim_id, payload.parent_order_sub_aim_id, payload.child_order_aim_id, payload.child_order_sub_aim_id)
    exists = db.execute(select(ServiceRelation).where(
        ServiceRelation.parent_service_id==payload.parent_service_id,
        ServiceRelation.parent_order_aim_id==payload.parent_order_aim_id,
        ServiceRelation.parent_order_sub_aim_id==payload.parent_order_sub_aim_id,
        ServiceRelation.child_service_id==payload.child_service_id,
        ServiceRelation.child_order_aim_id==payload.child_order_aim_id,
        ServiceRelation.child_order_sub_aim_id==payload.child_order_sub_aim_id,
    )).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Relation already exists")
    obj = ServiceRelation(
        parent_service_id=payload.parent_service_id,
        parent_order_aim_id=payload.parent_order_aim_id,
        parent_order_sub_aim_id=payload.parent_order_sub_aim_id,
        child_service_id=payload.child_service_id,
        child_order_aim_id=payload.child_order_aim_id,
        child_order_sub_aim_id=payload.child_order_sub_aim_id,
        relation_type="decomposesTo",
        instantiation_mode=payload.instantiation_mode
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.put("/{relation_id}", response_model=RelationRead)
def update_relation(relation_id: str, payload: RelationUpdate, db: Session = Depends(get_db)):
    obj = db.get(ServiceRelation, relation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Relation not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    if obj.instantiation_mode not in {"CREATE","REUSE"}:
        raise HTTPException(status_code=400, detail="Invalid instantiation mode")
    validate_relation(db, obj.parent_service_id, obj.child_service_id, obj.parent_order_aim_id, obj.parent_order_sub_aim_id, obj.child_order_aim_id, obj.child_order_sub_aim_id)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{relation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relation(relation_id: str, db: Session = Depends(get_db)):
    obj = db.get(ServiceRelation, relation_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Relation not found")
    db.delete(obj); db.commit()
    return None
