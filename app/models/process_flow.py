from uuid import uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class ProcessFlow(Base):
    __tablename__ = "process_flows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    process_spec_id = Column(UUID(as_uuid=True), ForeignKey("process_specs.id"), nullable=False, index=True)
    source_element_id = Column(UUID(as_uuid=True), ForeignKey("process_elements.id"), nullable=False, index=True)
    target_element_id = Column(UUID(as_uuid=True), ForeignKey("process_elements.id"), nullable=False, index=True)
    flow_type = Column(String(30), nullable=False, default="sequenceFlow")
    label = Column(String(255), nullable=True)
    condition_expression = Column(Text, nullable=True)
    is_default = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    process_spec = relationship("ProcessSpec", back_populates="flows")
    source_element = relationship("ProcessElement", foreign_keys=[source_element_id])
    target_element = relationship("ProcessElement", foreign_keys=[target_element_id])
