import uuid
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class AttributeInvolvement(Base):
    __tablename__ = "attribute_involvement"
    __table_args__ = (
        UniqueConstraint("service_id", "attribute_id", name="uq_attribute_involvement"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    attribute_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("attributes.id", ondelete="CASCADE"), nullable=False)


class AttributeInvolvementDefaultValue(Base):
    __tablename__ = "attribute_involvement_default_values"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    attribute_involvement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("attribute_involvement.id", ondelete="CASCADE"), nullable=False)
    value_text: Mapped[str] = mapped_column(String(255), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
