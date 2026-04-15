from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase
class InterProcessTaskDependencyBase(BaseModel):
    source_process_spec_id: UUID
    source_element_id: UUID
    target_process_spec_id: UUID
    target_element_id: UUID
    service_relation_id: UUID | None = None
    dependency_type: str = Field(min_length=1, max_length=30)
    label: str | None = Field(default=None, max_length=255)
    condition_expression: str | None = None
    metadata_json: dict | None = None
class InterProcessTaskDependencyCreate(InterProcessTaskDependencyBase): pass
class InterProcessTaskDependencyUpdate(BaseModel):
    service_relation_id: UUID | None = None
    dependency_type: str | None = Field(default=None, min_length=1, max_length=30)
    label: str | None = Field(default=None, max_length=255)
    condition_expression: str | None = None
    metadata_json: dict | None = None
class InterProcessTaskDependencyRead(ORMBase):
    id: UUID
    source_process_spec_id: UUID
    source_element_id: UUID
    target_process_spec_id: UUID
    target_element_id: UUID
    service_relation_id: UUID | None = None
    dependency_type: str
    label: str | None = None
    condition_expression: str | None = None
    metadata_json: dict | None = None
