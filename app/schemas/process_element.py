from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase
class ProcessElementBase(BaseModel):
    process_spec_id: UUID
    element_key: str = Field(min_length=1, max_length=100)
    element_type: str = Field(min_length=1, max_length=20)
    task_spec_id: UUID | None = None
    gateway_spec_id: UUID | None = None
    event_spec_id: UUID | None = None
    name_override: str | None = Field(default=None, max_length=255)
    x: float | None = None
    y: float | None = None
    metadata_json: dict | None = None
class ProcessElementCreate(ProcessElementBase): pass
class ProcessElementUpdate(BaseModel):
    name_override: str | None = Field(default=None, max_length=255)
    x: float | None = None
    y: float | None = None
    metadata_json: dict | None = None
class ProcessElementRead(ORMBase):
    id: UUID
    process_spec_id: UUID
    element_key: str
    element_type: str
    task_spec_id: UUID | None = None
    gateway_spec_id: UUID | None = None
    event_spec_id: UUID | None = None
    name_override: str | None = None
    x: float | None = None
    y: float | None = None
    metadata_json: dict | None = None
