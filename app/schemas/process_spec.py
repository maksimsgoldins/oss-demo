from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase
class ProcessSpecBase(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    version: int = 1
    status: str = Field(min_length=1, max_length=30)
    is_executable: bool = True
    service_spec_id: UUID
    order_aim_id: UUID
    order_sub_aim_id: UUID
class ProcessSpecCreate(ProcessSpecBase): pass
class ProcessSpecUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    version: int | None = None
    status: str | None = Field(default=None, min_length=1, max_length=30)
    is_executable: bool | None = None
class ProcessSpecRead(ORMBase):
    id: UUID
    code: str
    name: str
    description: str | None = None
    version: int
    status: str
    is_executable: bool
    service_spec_id: UUID
    order_aim_id: UUID
    order_sub_aim_id: UUID
