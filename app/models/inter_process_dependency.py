from uuid import uuid4
from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class InterProcessTaskDependency(Base):
    __tablename__ = "inter_process_task_dependencies"

    id = Base.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    source_process_spec_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("process_specs.id"), nullable=False, index=True)
    source_element_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("process_elements.id"), nullable=False, index=True)
    target_process_spec_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("process_specs.id"), nullable=False, index=True)
    target_element_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("process_elements.id"), nullable=False, index=True)
    service_relation_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("service_relations.id"), nullable=True, index=True)
    dependency_type = Base.mapped_column(String(30), nullable=False, default="finish_to_start")
    label = Base.mapped_column(String(255), nullable=True)
    condition_expression = Base.mapped_column(Text, nullable=True)
    metadata_json = Base.mapped_column(JSON, nullable=True)
    created_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    source_process_spec = relationship("ProcessSpec", foreign_keys=[source_process_spec_id])
    target_process_spec = relationship("ProcessSpec", foreign_keys=[target_process_spec_id])
    source_element = relationship("ProcessElement", foreign_keys=[source_element_id])
    target_element = relationship("ProcessElement", foreign_keys=[target_element_id])
