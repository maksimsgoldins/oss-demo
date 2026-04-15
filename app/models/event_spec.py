from uuid import uuid4
from sqlalchemy import DateTime, String, func, Column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class EventSpec(Base):
    __tablename__ = "event_specs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
