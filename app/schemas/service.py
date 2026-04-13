from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase


class ServiceCreate(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    type: str
    description: str | None = None


class ServiceUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    description: str | None = None


class ServiceRead(ORMBase):
    id: UUID
    code: str
    name: str
    type: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
