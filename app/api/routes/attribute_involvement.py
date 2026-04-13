from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.attribute import Attribute, AttributePossibleValue
from app.models.attribute_involvement import AttributeInvolvement, AttributeInvolvementAllowedValue, AttributeInvolvementDefaultValue
from app.models.service import Service
from app.schemas.attribute_involvement import AttributeInvolvementCreate, AttributeInvolvementRead, AttributeInvolvementUpdate

router = APIRouter(prefix="/api/attribute-involvement", tags=["attribute-involvement"])

def base_possible_values(db, attribute_id):
    return [x.value_text for x in db.execute(select(AttributePossibleValue).where(AttributePossibleValue.attribute_id==attribute_id).order_by(AttributePossibleValue.sort_order)).scalars().all()]

def validate_sets(attr, base_values, allowed_values, default_values):
    allowed_values = allowed_values or base_values
    invalid_allowed = [v for v in allowed_values if v not in base_values]
    if invalid_allowed:
        raise HTTPException(status_code=400, detail=f"Invalid allowed values: {invalid_allowed}")
    invalid_default = [v for v in default_values if v not in allowed_values]
    if invalid_default:
        raise HTTPException(status_code=400, detail=f"Invalid default values: {invalid_default}")
    if attr.value_type != "list" and len(default_values) > 1:
        raise HTTPException(status_code=400, detail="Atomic attribute can have only one default value")
    return allowed_values

def serialize(db, item):
    allowed = db.execute(select(AttributeInvolvementAllowedValue).where(AttributeInvolvementAllowedValue.attribute_involvement_id==item.id).order_by(AttributeInvolvementAllowedValue.sort_order)).scalars().all()
    defaults = db.execute(select(AttributeInvolvementDefaultValue).where(AttributeInvolvementDefaultValue.attribute_involvement_id==item.id).order_by(AttributeInvolvementDefaultValue.sort_order)).scalars().all()
    return AttributeInvolvementRead(
        id=item.id, service_id=item.service_id, attribute_id=item.attribute_id,
        allowed_values=[x.value_text for x in allowed],
        default_values=[x.value_text for x in defaults]
    )

@router.get("", response_model=list[AttributeInvolvementRead])
def list_attribute_involvement(service_id: str | None = None, db: Session = Depends(get_db)):
    stmt = select(AttributeInvolvement)
    if service_id:
        stmt = stmt.where(AttributeInvolvement.service_id == service_id)
    items = db.execute(stmt).scalars().all()
    return [serialize(db, x) for x in items]

@router.post("", response_model=AttributeInvolvementRead, status_code=status.HTTP_201_CREATED)
def create_attribute_involvement(payload: AttributeInvolvementCreate, db: Session = Depends(get_db)):
    service = db.get(Service, payload.service_id)
    attr = db.get(Attribute, payload.attribute_id)
    if not service: raise HTTPException(status_code=404, detail="Service not found")
    if not attr: raise HTTPException(status_code=404, detail="Attribute not found")
    exists = db.execute(select(AttributeInvolvement).where(AttributeInvolvement.service_id==payload.service_id, AttributeInvolvement.attribute_id==payload.attribute_id)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Attribute involvement already exists")
    base_values = base_possible_values(db, attr.id)
    allowed_values = validate_sets(attr, base_values, payload.allowed_values, payload.default_values)
    item = AttributeInvolvement(service_id=payload.service_id, attribute_id=payload.attribute_id)
    db.add(item); db.flush()
    for idx, value in enumerate(allowed_values):
        db.add(AttributeInvolvementAllowedValue(attribute_involvement_id=item.id, value_text=value, sort_order=idx))
    for idx, value in enumerate(payload.default_values):
        db.add(AttributeInvolvementDefaultValue(attribute_involvement_id=item.id, value_text=value, sort_order=idx))
    db.commit(); db.refresh(item)
    return serialize(db, item)

@router.put("/{item_id}", response_model=AttributeInvolvementRead)
def update_attribute_involvement(item_id: str, payload: AttributeInvolvementUpdate, db: Session = Depends(get_db)):
    item = db.get(AttributeInvolvement, item_id)
    if not item: raise HTTPException(status_code=404, detail="Attribute involvement not found")
    attr = db.get(Attribute, item.attribute_id)
    base_values = base_possible_values(db, attr.id)
    allowed_values = validate_sets(attr, base_values, payload.allowed_values, payload.default_values)
    db.execute(delete(AttributeInvolvementAllowedValue).where(AttributeInvolvementAllowedValue.attribute_involvement_id==item.id))
    db.execute(delete(AttributeInvolvementDefaultValue).where(AttributeInvolvementDefaultValue.attribute_involvement_id==item.id))
    for idx, value in enumerate(allowed_values):
        db.add(AttributeInvolvementAllowedValue(attribute_involvement_id=item.id, value_text=value, sort_order=idx))
    for idx, value in enumerate(payload.default_values):
        db.add(AttributeInvolvementDefaultValue(attribute_involvement_id=item.id, value_text=value, sort_order=idx))
    db.commit(); db.refresh(item)
    return serialize(db, item)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attribute_involvement(item_id: str, db: Session = Depends(get_db)):
    item = db.get(AttributeInvolvement, item_id)
    if not item: raise HTTPException(status_code=404, detail="Attribute involvement not found")
    db.delete(item); db.commit()
    return None
