from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.order_aim import OrderAim, OrderSubAim
from app.schemas.order_aim import OrderAimCreate, OrderAimRead, OrderSubAimItem

router = APIRouter(prefix="/api/order-aims", tags=["order-aims"])

def serialize_order_aim(aim: OrderAim, db: Session) -> OrderAimRead:
    subs = db.execute(
        select(OrderSubAim).where(OrderSubAim.order_aim_id == aim.id).order_by(OrderSubAim.code)
    ).scalars().all()
    return OrderAimRead(
        id=aim.id,
        code=aim.code,
        name=aim.name,
        sub_aims=[OrderSubAimItem(id=s.id, code=s.code, name=s.name) for s in subs],
    )

@router.get("", response_model=list[OrderAimRead])
def list_order_aims(db: Session = Depends(get_db)):
    aims = db.execute(select(OrderAim).order_by(OrderAim.name)).scalars().all()
    return [serialize_order_aim(aim, db) for aim in aims]

@router.post("", response_model=OrderAimRead, status_code=status.HTTP_201_CREATED)
def create_order_aim(payload: OrderAimCreate, db: Session = Depends(get_db)):
    exists = db.execute(select(OrderAim).where(OrderAim.code == payload.code)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Order aim code already exists")

    aim = OrderAim(code=payload.code, name=payload.name)
    db.add(aim)
    db.flush()

    for item in payload.sub_aims:
        code = item.get("code") if isinstance(item, dict) else item.code
        name = item.get("name") if isinstance(item, dict) else item.name
        db.add(OrderSubAim(order_aim_id=aim.id, code=code, name=name))

    db.commit()
    db.refresh(aim)
    return serialize_order_aim(aim, db)
