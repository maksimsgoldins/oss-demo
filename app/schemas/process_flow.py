from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase
class ProcessFlowBase(BaseModel):
    process_spec_id: UUID
    source_element_id: UUID
    target_element_id: UUID
    flow_type: str = Field(min_length=1, max_length=30)
    label: str | None = Field(default=None, max_length=255)
    condition_expression: str | None = None
    is_default: bool = False
class ProcessFlowCreate(ProcessFlowBase): pass
class ProcessFlowUpdate(BaseModel):
    flow_type: str | None = Field(default=None, min_length=1, max_length=30)
    label: str | None = Field(default=None, max_length=255)
    condition_expression: str | None = None
    is_default: bool | None = None
class ProcessFlowRead(ORMBase):
    id: UUID
    process_spec_id: UUID
    source_element_id: UUID
    target_element_id: UUID
    flow_type: str
    label: str | None = None
    condition_expression: str | None = None
    is_default: bool
