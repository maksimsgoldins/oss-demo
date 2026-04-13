from uuid import UUID
from pydantic import BaseModel
from app.schemas.common import ORMBase

class AttributePropagationCreate(BaseModel):
    relation_id: UUID
    parent_attribute_involvement_id: UUID
    child_attribute_involvement_id: UUID
    allowed_values: list[str] = []

class AttributePropagationRead(ORMBase):
    relation_id: UUID
    parent_attribute_involvement_id: UUID
    child_attribute_involvement_id: UUID
    allowed_values: list[str]
