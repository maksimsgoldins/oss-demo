"""add orchestration configurator core tables

Revision ID: 20260415_orchestrator_v1
Revises:
Create Date: 2026-04-15
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260415_orchestrator_v1"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("task_specs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("task_type", sa.String(length=50), nullable=False),
        sa.Column("executor_type", sa.String(length=50), nullable=True),
        sa.Column("executor_config_json", sa.JSON(), nullable=True),
        sa.Column("timeout_sec", sa.Integer(), nullable=True),
        sa.Column("retry_policy_json", sa.JSON(), nullable=True),
        sa.Column("input_mapping_json", sa.JSON(), nullable=True),
        sa.Column("output_mapping_json", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("code"))
    op.create_index(op.f("ix_task_specs_code"), "task_specs", ["code"], unique=False)

    op.create_table("gateway_specs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("gateway_type", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("code"))
    op.create_index(op.f("ix_gateway_specs_code"), "gateway_specs", ["code"], unique=False)

    op.create_table("event_specs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("code"))
    op.create_index(op.f("ix_event_specs_code"), "event_specs", ["code"], unique=False)

    op.create_table("process_specs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="draft"),
        sa.Column("is_executable", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("service_spec_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("order_aim_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("order_sub_aim_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["service_spec_id"], ["services.id"]),
        sa.ForeignKeyConstraint(["order_aim_id"], ["order_aims.id"]),
        sa.ForeignKeyConstraint(["order_sub_aim_id"], ["order_sub_aims.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.UniqueConstraint("service_spec_id", "order_aim_id", "order_sub_aim_id", "version", name="uq_process_specs_service_aim_subaim_version"))
    op.create_index(op.f("ix_process_specs_code"), "process_specs", ["code"], unique=False)
    op.create_index(op.f("ix_process_specs_service_spec_id"), "process_specs", ["service_spec_id"], unique=False)
    op.create_index(op.f("ix_process_specs_order_aim_id"), "process_specs", ["order_aim_id"], unique=False)
    op.create_index(op.f("ix_process_specs_order_sub_aim_id"), "process_specs", ["order_sub_aim_id"], unique=False)

    op.create_table("process_elements",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("process_spec_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("element_key", sa.String(length=100), nullable=False),
        sa.Column("element_type", sa.String(length=20), nullable=False),
        sa.Column("task_spec_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("gateway_spec_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("event_spec_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name_override", sa.String(length=255), nullable=True),
        sa.Column("x", sa.Float(), nullable=True),
        sa.Column("y", sa.Float(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["process_spec_id"], ["process_specs.id"]),
        sa.ForeignKeyConstraint(["task_spec_id"], ["task_specs.id"]),
        sa.ForeignKeyConstraint(["gateway_spec_id"], ["gateway_specs.id"]),
        sa.ForeignKeyConstraint(["event_spec_id"], ["event_specs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("process_spec_id", "element_key", name="uq_process_elements_key"))
    op.create_index(op.f("ix_process_elements_process_spec_id"), "process_elements", ["process_spec_id"], unique=False)

    op.create_table("process_flows",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("process_spec_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_element_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_element_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("flow_type", sa.String(length=30), nullable=False, server_default="sequenceFlow"),
        sa.Column("label", sa.String(length=255), nullable=True),
        sa.Column("condition_expression", sa.Text(), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["process_spec_id"], ["process_specs.id"]),
        sa.ForeignKeyConstraint(["source_element_id"], ["process_elements.id"]),
        sa.ForeignKeyConstraint(["target_element_id"], ["process_elements.id"]),
        sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_process_flows_process_spec_id"), "process_flows", ["process_spec_id"], unique=False)
    op.create_index(op.f("ix_process_flows_source_element_id"), "process_flows", ["source_element_id"], unique=False)
    op.create_index(op.f("ix_process_flows_target_element_id"), "process_flows", ["target_element_id"], unique=False)

    op.create_table("inter_process_task_dependencies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_process_spec_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_element_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_process_spec_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_element_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_relation_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("dependency_type", sa.String(length=30), nullable=False, server_default="finish_to_start"),
        sa.Column("label", sa.String(length=255), nullable=True),
        sa.Column("condition_expression", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["source_process_spec_id"], ["process_specs.id"]),
        sa.ForeignKeyConstraint(["source_element_id"], ["process_elements.id"]),
        sa.ForeignKeyConstraint(["target_process_spec_id"], ["process_specs.id"]),
        sa.ForeignKeyConstraint(["target_element_id"], ["process_elements.id"]),
        sa.ForeignKeyConstraint(["service_relation_id"], ["service_relations.id"]),
        sa.PrimaryKeyConstraint("id"))
    op.create_index(op.f("ix_inter_process_task_dependencies_source_process_spec_id"), "inter_process_task_dependencies", ["source_process_spec_id"], unique=False)
    op.create_index(op.f("ix_inter_process_task_dependencies_source_element_id"), "inter_process_task_dependencies", ["source_element_id"], unique=False)
    op.create_index(op.f("ix_inter_process_task_dependencies_target_process_spec_id"), "inter_process_task_dependencies", ["target_process_spec_id"], unique=False)
    op.create_index(op.f("ix_inter_process_task_dependencies_target_element_id"), "inter_process_task_dependencies", ["target_element_id"], unique=False)
    op.create_index(op.f("ix_inter_process_task_dependencies_service_relation_id"), "inter_process_task_dependencies", ["service_relation_id"], unique=False)

def downgrade() -> None:
    pass
