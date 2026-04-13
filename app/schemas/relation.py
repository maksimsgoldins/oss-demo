from uuid import UUID
from pydantic import BaseModel
from app.schemas.common import ORMBase

class RelationCreate(BaseModel):
    parent_service_id: UUID
    parent_order_aim_id: UUID
    parent_order_sub_aim_id: UUID
    child_service_id: UUID
    child_order_aim_id: UUID
    child_order_sub_aim_id: UUID
    instantiation_mode: str

class RelationUpdate(BaseModel):
    parent_service_id: UUID | None = None
    parent_order_aim_id: UUID | None = None
    parent_order_sub_aim_id: UUID | None = None
    child_service_id: UUID | None = None
    child_order_aim_id: UUID | None = None
    child_order_sub_aim_id: UUID | None = None
    instantiation_mode: str | None = None

class RelationRead(ORMBase):
    id: UUID
    parent_service_id: UUID
    parent_order_aim_id: UUID
    parent_order_sub_aim_id: UUID
    child_service_id: UUID
    child_order_aim_id: UUID
    child_order_sub_aim_id: UUID
    relation_type: str
    instantiation_mode: str
