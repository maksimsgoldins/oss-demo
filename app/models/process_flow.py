from uuid import uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class ProcessFlow(Base):
    __tablename__ = "process_flows"

    id = Base.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    process_spec_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("process_specs.id"), nullable=False, index=True)
    source_element_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("process_elements.id"), nullable=False, index=True)
    target_element_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("process_elements.id"), nullable=False, index=True)
    flow_type = Base.mapped_column(String(30), nullable=False, default="sequenceFlow")
    label = Base.mapped_column(String(255), nullable=True)
    condition_expression = Base.mapped_column(Text, nullable=True)
    is_default = Base.mapped_column(Boolean, nullable=False, default=False)
    created_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    process_spec = relationship("ProcessSpec", back_populates="flows")
    source_element = relationship("ProcessElement", foreign_keys=[source_element_id])
    target_element = relationship("ProcessElement", foreign_keys=[target_element_id])
