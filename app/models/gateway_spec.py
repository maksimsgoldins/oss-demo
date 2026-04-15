from uuid import uuid4
from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class GatewaySpec(Base):
    __tablename__ = "gateway_specs"

    id = Base.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Base.mapped_column(String(100), nullable=False, unique=True, index=True)
    name = Base.mapped_column(String(255), nullable=False)
    gateway_type = Base.mapped_column(String(50), nullable=False)
    created_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Base.mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
