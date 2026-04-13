from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

class AttributeCreate(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    value_type: str
    required: bool = False
    description: str | None = None
    possible_values: list[str] = []

class AttributeRead(ORMBase):
    id: UUID
    code: str
    name: str
    value_type: str
    required: bool
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    possible_values: list[str] = []
