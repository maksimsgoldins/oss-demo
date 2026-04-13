import uuid
from datetime import datetime
from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class DiagramLayout(Base):
    __tablename__ = "diagram_layout"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    node_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    x: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    y: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    width: Mapped[float | None] = mapped_column(Numeric(10,2), nullable=True)
    height: Mapped[float | None] = mapped_column(Numeric(10,2), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
