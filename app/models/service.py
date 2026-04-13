import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Service(Base):
    __tablename__ = "services"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class ServiceAimMapping(Base):
    __tablename__ = "service_aim_mappings"
    __table_args__ = (UniqueConstraint("service_id", "order_aim_id", "order_sub_aim_id", name="uq_service_aim_mapping"),)
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    order_aim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order_aims.id", ondelete="CASCADE"), nullable=False)
    order_sub_aim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order_sub_aims.id", ondelete="CASCADE"), nullable=False)

class ServiceRelation(Base):
    __tablename__ = "service_relations"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    parent_service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    parent_order_aim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order_aims.id", ondelete="CASCADE"), nullable=False)
    parent_order_sub_aim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order_sub_aims.id", ondelete="CASCADE"), nullable=False)
    child_service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    child_order_aim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order_aims.id", ondelete="CASCADE"), nullable=False)
    child_order_sub_aim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order_sub_aims.id", ondelete="CASCADE"), nullable=False)
    relation_type: Mapped[str] = mapped_column(String(50), nullable=False, default="decomposesTo")
    instantiation_mode: Mapped[str] = mapped_column(String(20), nullable=False)
