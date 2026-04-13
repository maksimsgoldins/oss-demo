from uuid import UUID
from pydantic import BaseModel
from app.schemas.common import ORMBase

class AttributeInvolvementCreate(BaseModel):
    service_id: UUID
    attribute_id: UUID
    allowed_values: list[str] = []
    default_values: list[str] = []

class AttributeInvolvementUpdate(BaseModel):
    allowed_values: list[str] = []
    default_values: list[str] = []

class AttributeInvolvementRead(ORMBase):
    id: UUID
    service_id: UUID
    attribute_id: UUID
    allowed_values: list[str] = []
    default_values: list[str] = []
