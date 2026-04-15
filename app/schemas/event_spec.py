from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase
class EventSpecBase(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    event_type: str = Field(min_length=1, max_length=50)
class EventSpecCreate(EventSpecBase): pass
class EventSpecUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    event_type: str | None = Field(default=None, min_length=1, max_length=50)
class EventSpecRead(ORMBase):
    id: UUID
    code: str
    name: str
    event_type: str
