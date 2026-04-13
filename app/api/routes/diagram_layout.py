from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.diagram_layout import DiagramLayout
from app.schemas.diagram_layout import DiagramLayoutItem, DiagramLayoutRead

router = APIRouter(prefix="/api/diagram-layout", tags=["diagram-layout"])

@router.get("", response_model=list[DiagramLayoutRead])
def list_diagram_layout(db: Session = Depends(get_db)):
    return db.execute(select(DiagramLayout).order_by(DiagramLayout.node_key)).scalars().all()

@router.put("", response_model=list[DiagramLayoutRead])
def replace_diagram_layout(payload: list[DiagramLayoutItem], db: Session = Depends(get_db)):
    db.execute(delete(DiagramLayout))
    for item in payload:
        db.add(DiagramLayout(node_key=item.node_key, x=item.x, y=item.y, width=item.width, height=item.height))
    db.commit()
    return db.execute(select(DiagramLayout).order_by(DiagramLayout.node_key)).scalars().all()
