from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.attribute import Attribute, AttributePossibleValue
from app.models.attribute_involvement import AttributeInvolvement, AttributeInvolvementAllowedValue
from app.models.attribute_propagation import AttributePropagation
from app.models.service import ServiceRelation
from app.schemas.attribute_propagation import AttributePropagationCreate, AttributePropagationRead

router = APIRouter(prefix="/api/attribute-propagation", tags=["attribute-propagation"])

def involvement_allowed_values(db, involvement_id, attribute_id):
    explicit = db.execute(select(AttributeInvolvementAllowedValue).where(AttributeInvolvementAllowedValue.attribute_involvement_id==involvement_id).order_by(AttributeInvolvementAllowedValue.sort_order)).scalars().all()
    if explicit:
        return [x.value_text for x in explicit]
    return [x.value_text for x in db.execute(select(AttributePossibleValue).where(AttributePossibleValue.attribute_id==attribute_id).order_by(AttributePossibleValue.sort_order)).scalars().all()]

def serialize_grouped(db, relation_id):
    rows = db.execute(select(AttributePropagation).where(AttributePropagation.relation_id==relation_id).order_by(AttributePropagation.sort_order)).scalars().all()
    grouped = defaultdict(list)
    for r in rows:
        key=(r.parent_attribute_involvement_id, r.child_attribute_involvement_id)
        if r.allowed_value_text:
            grouped[key].append(r.allowed_value_text)
    return [AttributePropagationRead(relation_id=relation_id, parent_attribute_involvement_id=k[0], child_attribute_involvement_id=k[1], allowed_values=v) for k,v in grouped.items()]

@router.get("", response_model=list[AttributePropagationRead])
def list_attribute_propagation(relation_id: str | None = None, db: Session = Depends(get_db)):
    if relation_id:
        return serialize_grouped(db, relation_id)
    rel_ids = [x.id for x in db.execute(select(ServiceRelation)).scalars().all()]
    out=[]
    for rid in rel_ids:
        out.extend(serialize_grouped(db, rid))
    return out

@router.post("", response_model=AttributePropagationRead, status_code=status.HTTP_201_CREATED)
def create_attribute_propagation(payload: AttributePropagationCreate, db: Session = Depends(get_db)):
    rel = db.get(ServiceRelation, payload.relation_id)
    p_ai = db.get(AttributeInvolvement, payload.parent_attribute_involvement_id)
    c_ai = db.get(AttributeInvolvement, payload.child_attribute_involvement_id)
    if not rel: raise HTTPException(status_code=404, detail="Relation not found")
    if not p_ai or not c_ai: raise HTTPException(status_code=404, detail="Attribute involvement not found")
    if p_ai.service_id != rel.parent_service_id:
        raise HTTPException(status_code=400, detail="Parent involvement does not belong to relation parent service")
    if c_ai.service_id != rel.child_service_id:
        raise HTTPException(status_code=400, detail="Child involvement does not belong to relation child service")
    parent_attr = db.get(Attribute, p_ai.attribute_id)
    child_attr = db.get(Attribute, c_ai.attribute_id)
    parent_allowed = set(involvement_allowed_values(db, p_ai.id, parent_attr.id))
    child_allowed = set(involvement_allowed_values(db, c_ai.id, child_attr.id))
    intersection = parent_allowed & child_allowed
    invalid = [v for v in payload.allowed_values if v not in intersection]
    if invalid:
        raise HTTPException(status_code=400, detail=f"Invalid propagated values: {invalid}")
    db.execute(delete(AttributePropagation).where(
        AttributePropagation.relation_id==payload.relation_id,
        AttributePropagation.parent_attribute_involvement_id==payload.parent_attribute_involvement_id,
        AttributePropagation.child_attribute_involvement_id==payload.child_attribute_involvement_id,
    ))
    for idx, val in enumerate(payload.allowed_values):
        db.add(AttributePropagation(
            relation_id=payload.relation_id,
            parent_attribute_involvement_id=payload.parent_attribute_involvement_id,
            child_attribute_involvement_id=payload.child_attribute_involvement_id,
            allowed_value_text=val,
            sort_order=idx
        ))
    db.commit()
    return AttributePropagationRead(
        relation_id=payload.relation_id,
        parent_attribute_involvement_id=payload.parent_attribute_involvement_id,
        child_attribute_involvement_id=payload.child_attribute_involvement_id,
        allowed_values=payload.allowed_values
    )
