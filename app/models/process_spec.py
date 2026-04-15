from uuid import uuid4
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class ProcessSpec(Base):
    __tablename__ = "process_specs"
    __table_args__ = (
        UniqueConstraint("service_spec_id", "order_aim_id", "order_sub_aim_id", "version",
                         name="uq_process_specs_service_aim_subaim_version"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(30), nullable=False, default="draft")
    is_executable = Column(Boolean, nullable=False, default=True)
    service_spec_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False, index=True)
    order_aim_id = Column(UUID(as_uuid=True), ForeignKey("order_aims.id"), nullable=False, index=True)
    order_sub_aim_id = Column(UUID(as_uuid=True), ForeignKey("order_sub_aims.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    elements = relationship("ProcessElement", back_populates="process_spec", cascade="all, delete-orphan")
    flows = relationship("ProcessFlow", back_populates="process_spec", cascade="all, delete-orphan")
