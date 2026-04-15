from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class TaskSpec(Base):
    __tablename__ = "task_specs"

    id = Base.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Base.mapped_column(String(100), nullable=False, unique=True, index=True)
    name = Base.mapped_column(String(255), nullable=False)
    description = Base.mapped_column(Text, nullable=True)
    task_type = Base.mapped_column(String(50), nullable=False)
    executor_type = Base.mapped_column(String(50), nullable=True)
    executor_config_json = Base.mapped_column(JSON, nullable=True)
    timeout_sec = Base.mapped_column(Integer, nullable=True)
    retry_policy_json = Base.mapped_column(JSON, nullable=True)
    input_mapping_json = Base.mapped_column(JSON, nullable=True)
    output_mapping_json = Base.mapped_column(JSON, nullable=True)
    is_active = Base.mapped_column(Boolean, nullable=False, default=True)
    created_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
