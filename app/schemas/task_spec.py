from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase
class TaskSpecBase(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    task_type: str = Field(min_length=1, max_length=50)
    executor_type: str | None = Field(default=None, max_length=50)
    executor_config_json: dict | None = None
    timeout_sec: int | None = None
    retry_policy_json: dict | None = None
    input_mapping_json: dict | None = None
    output_mapping_json: dict | None = None
    is_active: bool = True
class TaskSpecCreate(TaskSpecBase): pass
class TaskSpecUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    task_type: str | None = Field(default=None, min_length=1, max_length=50)
    executor_type: str | None = Field(default=None, max_length=50)
    executor_config_json: dict | None = None
    timeout_sec: int | None = None
    retry_policy_json: dict | None = None
    input_mapping_json: dict | None = None
    output_mapping_json: dict | None = None
    is_active: bool | None = None
class TaskSpecRead(ORMBase):
    id: UUID
    code: str
    name: str
    description: str | None = None
    task_type: str
    executor_type: str | None = None
    executor_config_json: dict | None = None
    timeout_sec: int | None = None
    retry_policy_json: dict | None = None
    input_mapping_json: dict | None = None
    output_mapping_json: dict | None = None
    is_active: bool
