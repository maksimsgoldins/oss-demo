from uuid import uuid4
from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ProcessElement(Base):
    __tablename__ = "process_elements"
    __table_args__ = (
        UniqueConstraint("process_spec_id", "element_key", name="uq_process_elements_key"),
    )

    id = Base.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    process_spec_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("process_specs.id"), nullable=False, index=True)
    element_key = Base.mapped_column(String(100), nullable=False)
    element_type = Base.mapped_column(String(20), nullable=False)
    task_spec_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("task_specs.id"), nullable=True)
    gateway_spec_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("gateway_specs.id"), nullable=True)
    event_spec_id = Base.mapped_column(UUID(as_uuid=True), ForeignKey("event_specs.id"), nullable=True)
    name_override = Base.mapped_column(String(255), nullable=True)
    x = Base.mapped_column(Float, nullable=True)
    y = Base.mapped_column(Float, nullable=True)
    metadata_json = Base.mapped_column(JSON, nullable=True)
    created_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    process_spec = relationship("ProcessSpec", back_populates="elements")
    task_spec = relationship("TaskSpec")
    gateway_spec = relationship("GatewaySpec")
    event_spec = relationship("EventSpec")
