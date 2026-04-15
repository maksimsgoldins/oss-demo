from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text, func, Column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class TaskSpec(Base):
    __tablename__ = "task_specs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(String(50), nullable=False)
    executor_type = Column(String(50), nullable=True)
    executor_config_json = Column(JSON, nullable=True)
    timeout_sec = Column(Integer, nullable=True)
    retry_policy_json = Column(JSON, nullable=True)
    input_mapping_json = Column(JSON, nullable=True)
    output_mapping_json = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
