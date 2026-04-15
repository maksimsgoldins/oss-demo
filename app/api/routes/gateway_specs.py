from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.routes._orchestrator_utils import validate_gateway_type
from app.db.session import get_db
from app.models.gateway_spec import GatewaySpec
from app.schemas.gateway_spec import GatewaySpecCreate, GatewaySpecRead, GatewaySpecUpdate
router = APIRouter(prefix="/api/gateway-specs", tags=["gateway-specs"])
@router.get("", response_model=list[GatewaySpecRead])
def list_gateway_specs(db: Session = Depends(get_db)):
    return db.execute(select(GatewaySpec).order_by(GatewaySpec.name)).scalars().all()
@router.post("", response_model=GatewaySpecRead, status_code=status.HTTP_201_CREATED)
def create_gateway_spec(payload: GatewaySpecCreate, db: Session = Depends(get_db)):
    validate_gateway_type(payload.gateway_type)
    if db.execute(select(GatewaySpec).where(GatewaySpec.code == payload.code)).scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Gateway spec code already exists")
    item = GatewaySpec(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@router.put("/{item_id}", response_model=GatewaySpecRead)
def update_gateway_spec(item_id: str, payload: GatewaySpecUpdate, db: Session = Depends(get_db)):
    item = db.get(GatewaySpec, item_id)
    if not item: raise HTTPException(status_code=404, detail="Gateway spec not found")
    data = payload.model_dump(exclude_unset=True)
    if "gateway_type" in data and data["gateway_type"] is not None: validate_gateway_type(data["gateway_type"])
    for k, v in data.items(): setattr(item, k, v)
    db.commit(); db.refresh(item); return item
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gateway_spec(item_id: str, db: Session = Depends(get_db)):
    item = db.get(GatewaySpec, item_id)
    if not item: raise HTTPException(status_code=404, detail="Gateway spec not found")
    db.delete(item); db.commit(); return None
