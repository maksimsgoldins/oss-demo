from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.attribute import Attribute, AttributePossibleValue
from app.schemas.attribute import AttributeCreate, AttributeRead

router = APIRouter(prefix="/api/attributes", tags=["attributes"])


@router.get("", response_model=list[AttributeRead])
def list_attributes(db: Session = Depends(get_db)):
    attrs = db.execute(select(Attribute).order_by(Attribute.name)).scalars().all()
    result = []
    for attr in attrs:
        possible_values = db.execute(
            select(AttributePossibleValue)
            .where(AttributePossibleValue.attribute_id == attr.id)
            .order_by(AttributePossibleValue.sort_order, AttributePossibleValue.value_text)
        ).scalars().all()
        result.append(
            AttributeRead(
                id=attr.id,
                code=attr.code,
                name=attr.name,
                value_type=attr.value_type,
                required=attr.required,
                description=attr.description,
                created_at=attr.created_at,
                updated_at=attr.updated_at,
                possible_values=[x.value_text for x in possible_values],
            )
        )
    return result


@router.post("", response_model=AttributeRead, status_code=status.HTTP_201_CREATED)
def create_attribute(payload: AttributeCreate, db: Session = Depends(get_db)):
    if payload.value_type not in {"string", "number", "boolean", "date", "list"}:
        raise HTTPException(status_code=400, detail="Invalid attribute value_type")

    exists = db.execute(select(Attribute).where(Attribute.code == payload.code)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Attribute code already exists")

    attr = Attribute(
        code=payload.code,
        name=payload.name,
        value_type=payload.value_type,
        required=payload.required,
        description=payload.description,
    )
    db.add(attr)
    db.flush()

    for idx, value in enumerate(payload.possible_values):
        db.add(AttributePossibleValue(attribute_id=attr.id, value_text=value, sort_order=idx))

    db.commit()
    db.refresh(attr)

    return AttributeRead(
        id=attr.id,
        code=attr.code,
        name=attr.name,
        value_type=attr.value_type,
        required=attr.required,
        description=attr.description,
        created_at=attr.created_at,
        updated_at=attr.updated_at,
        possible_values=payload.possible_values,
    )
