"""Initial schema — entities, filings, officers, grants, sanctions_hits, risk_scores, state_registry

Revision ID: 0001
Revises:
Create Date: 2026-04-25
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # entities
    op.create_table(
        "entities",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ein", sa.String(12), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("name_normalized", sa.Text(), nullable=False),
        sa.Column("entity_type", sa.String(50), nullable=False, server_default="nonprofit"),
        sa.Column("address_street", sa.Text()),
        sa.Column("address_city", sa.String(100)),
        sa.Column("address_state", sa.String(2)),
        sa.Column("address_zip", sa.String(10)),
        sa.Column("registration_status", sa.String(50)),
        sa.Column("exempt_status", sa.String(10)),
        sa.Column("ruling_year", sa.Integer()),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ein"),
    )
    op.create_index("ix_entities_ein", "entities", ["ein"])
    op.create_index("ix_entities_name_normalized", "entities", ["name_normalized"])
    op.create_index("ix_entities_address_state", "entities", ["address_state"])

    # filings
    op.create_table(
        "filings",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tax_year", sa.Integer(), nullable=False),
        sa.Column("form_type", sa.String(20), server_default="990"),
        sa.Column("object_id", sa.String(50)),
        sa.Column("total_revenue", sa.Numeric(18, 2)),
        sa.Column("total_expenses", sa.Numeric(18, 2)),
        sa.Column("total_assets", sa.Numeric(18, 2)),
        sa.Column("total_liabilities", sa.Numeric(18, 2)),
        sa.Column("program_service_revenue", sa.Numeric(18, 2)),
        sa.Column("contributions", sa.Numeric(18, 2)),
        sa.Column("employee_count", sa.Integer()),
        sa.Column("anomaly_flags", postgresql.JSON()),
        sa.Column("raw_json", postgresql.JSON()),
        sa.Column("has_anomaly", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["entity_id"], ["entities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("object_id"),
    )
    op.create_index("ix_filings_entity_id", "filings", ["entity_id"])
    op.create_index("ix_filings_tax_year", "filings", ["tax_year"])

    # officers
    op.create_table(
        "officers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("name_normalized", sa.Text(), nullable=False),
        sa.Column("title", sa.String(200)),
        sa.Column("compensation", sa.Numeric(14, 2)),
        sa.Column("tax_year", sa.Integer()),
        sa.Column("related_entity_ein", sa.String(12)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["entity_id"], ["entities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_officers_entity_id", "officers", ["entity_id"])
    op.create_index("ix_officers_name_normalized", "officers", ["name_normalized"])
    op.create_index("ix_officers_related_entity_ein", "officers", ["related_entity_ein"])

    # grants
    op.create_table(
        "grants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("grantor_id", postgresql.UUID(as_uuid=True)),
        sa.Column("recipient_id", postgresql.UUID(as_uuid=True)),
        sa.Column("grantor_ein", sa.String(12)),
        sa.Column("recipient_ein", sa.String(12)),
        sa.Column("recipient_name", sa.Text()),
        sa.Column("amount", sa.Numeric(18, 2)),
        sa.Column("tax_year", sa.Integer()),
        sa.Column("purpose", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["grantor_id"], ["entities.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["recipient_id"], ["entities.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_grants_grantor_id", "grants", ["grantor_id"])
    op.create_index("ix_grants_recipient_id", "grants", ["recipient_id"])
    op.create_index("ix_grants_recipient_ein", "grants", ["recipient_ein"])

    # sanctions_hits
    op.create_table(
        "sanctions_hits",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("list_name", sa.String(50), nullable=False),
        sa.Column("matched_name", sa.Text()),
        sa.Column("match_score", sa.Numeric(5, 4)),
        sa.Column("match_date", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("sanctions_program", sa.String(100)),
        sa.Column("sdn_id", sa.String(50)),
        sa.Column("evidence", postgresql.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["entity_id"], ["entities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sanctions_hits_entity_id", "sanctions_hits", ["entity_id"])
    op.create_index("ix_sanctions_hits_sdn_id", "sanctions_hits", ["sdn_id"])

    # risk_scores
    op.create_table(
        "risk_scores",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dimension", sa.String(50), nullable=False),
        sa.Column("score", sa.Numeric(5, 4), nullable=False),
        sa.Column("evidence", postgresql.JSON()),
        sa.Column("scored_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["entity_id"], ["entities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_risk_scores_entity_id", "risk_scores", ["entity_id"])

    # state_registry
    op.create_table(
        "state_registry",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("state", sa.String(2), nullable=False),
        sa.Column("registration_number", sa.String(50)),
        sa.Column("status", sa.String(50)),
        sa.Column("last_filing_date", sa.Date()),
        sa.Column("expiry_date", sa.Date()),
        sa.Column("address_mismatch", sa.Boolean(), server_default="false"),
        sa.Column("scraped_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["entity_id"], ["entities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_state_registry_entity_id", "state_registry", ["entity_id"])
    op.create_index("ix_state_registry_state", "state_registry", ["state"])


def downgrade() -> None:
    op.drop_table("state_registry")
    op.drop_table("risk_scores")
    op.drop_table("sanctions_hits")
    op.drop_table("grants")
    op.drop_table("officers")
    op.drop_table("filings")
    op.drop_table("entities")
