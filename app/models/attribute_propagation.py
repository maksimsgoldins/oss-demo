import uuid
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class AttributePropagation(Base):
    __tablename__ = "attribute_propagation"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    relation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("service_relations.id", ondelete="CASCADE"), nullable=False)
    parent_attribute_involvement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("attribute_involvement.id", ondelete="CASCADE"), nullable=False)
    child_attribute_involvement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("attribute_involvement.id", ondelete="CASCADE"), nullable=False)
    allowed_value_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
