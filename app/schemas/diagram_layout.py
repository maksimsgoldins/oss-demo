from uuid import UUID
from pydantic import BaseModel
from app.schemas.common import ORMBase

class DiagramLayoutItem(BaseModel):
    node_key: str
    x: float
    y: float
    width: float | None = None
    height: float | None = None

class DiagramLayoutRead(ORMBase):
    id: UUID
    node_key: str
    x: float
    y: float
    width: float | None = None
    height: float | None = None
