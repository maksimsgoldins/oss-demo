from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.common import ORMBase

class OrderSubAimItem(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)

class OrderAimCreate(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    sub_aims: list[OrderSubAimItem] = []

class OrderAimRead(ORMBase):
    id: UUID
    code: str
    name: str
    sub_aims: list[OrderSubAimItem] = []
