"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-04-13
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "services",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "order_aims",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
    )

    op.create_table(
        "order_sub_aims",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_aim_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("order_aims.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.UniqueConstraint("order_aim_id", "code", name="uq_order_sub_aim_per_aim"),
    )

    op.create_table(
        "attributes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("value_type", sa.String(length=20), nullable=False),
        sa.Column("required", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "attribute_possible_values",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("attribute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("attributes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("value_text", sa.String(length=255), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("attribute_id", "value_text", name="uq_attribute_possible_value"),
    )

    op.create_table(
        "service_aim_mappings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
        sa.Column("order_aim_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("order_aims.id", ondelete="CASCADE"), nullable=False),
        sa.Column("order_sub_aim_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("order_sub_aims.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("service_id", "order_aim_id", "order_sub_aim_id", name="uq_service_aim_mapping"),
    )

    op.create_table(
        "attribute_involvement",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
        sa.Column("attribute_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("attributes.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("service_id", "attribute_id", name="uq_attribute_involvement"),
    )

    op.create_table(
        "attribute_involvement_default_values",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("attribute_involvement_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("attribute_involvement.id", ondelete="CASCADE"), nullable=False),
        sa.Column("value_text", sa.String(length=255), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )

    op.create_table(
        "service_relations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("parent_service_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
        sa.Column("parent_order_aim_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("order_aims.id", ondelete="CASCADE"), nullable=False),
        sa.Column("parent_order_sub_aim_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("order_sub_aims.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_service_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_order_aim_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("order_aims.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_order_sub_aim_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("order_sub_aims.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relation_type", sa.String(length=50), nullable=False, server_default="decomposesTo"),
        sa.Column("instantiation_mode", sa.String(length=20), nullable=False),
    )

    op.create_table(
        "diagram_layout",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("node_key", sa.String(length=255), nullable=False, unique=True),
        sa.Column("x", sa.Numeric(10, 2), nullable=False),
        sa.Column("y", sa.Numeric(10, 2), nullable=False),
        sa.Column("width", sa.Numeric(10, 2), nullable=True),
        sa.Column("height", sa.Numeric(10, 2), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table("diagram_layout")
    op.drop_table("service_relations")
    op.drop_table("attribute_involvement_default_values")
    op.drop_table("attribute_involvement")
    op.drop_table("service_aim_mappings")
    op.drop_table("attribute_possible_values")
    op.drop_table("attributes")
    op.drop_table("order_sub_aims")
    op.drop_table("order_aims")
    op.drop_table("services")
