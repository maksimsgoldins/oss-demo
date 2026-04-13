from uuid import UUID
from pydantic import BaseModel
from app.schemas.common import ORMBase

class ServiceAimMappingCreate(BaseModel):
    service_id: UUID
    order_aim_id: UUID
    order_sub_aim_id: UUID

class ServiceAimMappingRead(ORMBase):
    id: UUID
    service_id: UUID
    order_aim_id: UUID
    order_sub_aim_id: UUID
