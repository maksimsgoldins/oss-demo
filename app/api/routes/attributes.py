from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.attribute import Attribute, AttributePossibleValue
from app.models.attribute_involvement import AttributeInvolvement
from app.schemas.attribute import AttributeCreate, AttributeRead

router = APIRouter(prefix="/api/attributes", tags=["attributes"])

def serialize(attr, db):
    values = db.execute(select(AttributePossibleValue).where(AttributePossibleValue.attribute_id==attr.id).order_by(AttributePossibleValue.sort_order)).scalars().all()
    return AttributeRead(
        id=attr.id, code=attr.code, name=attr.name, value_type=attr.value_type, required=attr.required,
        description=attr.description, created_at=attr.created_at, updated_at=attr.updated_at,
        possible_values=[v.value_text for v in values]
    )

@router.get("", response_model=list[AttributeRead])
def list_attributes(db: Session = Depends(get_db)):
    attrs = db.execute(select(Attribute).order_by(Attribute.name)).scalars().all()
    return [serialize(a, db) for a in attrs]

@router.post("", response_model=AttributeRead, status_code=status.HTTP_201_CREATED)
def create_attribute(payload: AttributeCreate, db: Session = Depends(get_db)):
    if payload.value_type not in {"string","number","boolean","date","list"}:
        raise HTTPException(status_code=400, detail="Invalid attribute value_type")
    exists = db.execute(select(Attribute).where(Attribute.code==payload.code)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Attribute code already exists")
    attr = Attribute(code=payload.code, name=payload.name, value_type=payload.value_type, required=payload.required, description=payload.description)
    db.add(attr); db.flush()
    for idx, value in enumerate(payload.possible_values):
        db.add(AttributePossibleValue(attribute_id=attr.id, value_text=value, sort_order=idx))
    db.commit(); db.refresh(attr)
    return serialize(attr, db)

@router.delete("/{attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attribute(attribute_id: str, db: Session = Depends(get_db)):
    attr = db.get(Attribute, attribute_id)
    if not attr:
        raise HTTPException(status_code=404, detail="Attribute not found")
    used = db.execute(select(AttributeInvolvement).where(AttributeInvolvement.attribute_id==attribute_id)).scalar_one_or_none()
    if used:
        raise HTTPException(status_code=400, detail="Attribute is linked to a service through involvement")
    db.delete(attr); db.commit()
    return None
