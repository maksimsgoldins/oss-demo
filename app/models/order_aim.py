import uuid
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class OrderAim(Base):
    __tablename__ = "order_aims"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

class OrderSubAim(Base):
    __tablename__ = "order_sub_aims"
    __table_args__ = (UniqueConstraint("order_aim_id", "code", name="uq_order_sub_aim_per_aim"),)
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    order_aim_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order_aims.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
