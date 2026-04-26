"""SanctionsHit model — OFAC / other list matches."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.models.base import Base


class SanctionsHit(Base):
    __tablename__ = "sanctions_hits"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), index=True
    )
    list_name: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # ofac_sdn | ofac_cons | un_consolidated
    matched_name: Mapped[str | None] = mapped_column(Text)
    match_score: Mapped[float | None] = mapped_column(Numeric(5, 4))  # 0.0 – 1.0
    match_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    sanctions_program: Mapped[str | None] = mapped_column(String(100))
    sdn_id: Mapped[str | None] = mapped_column(String(50), index=True)
    evidence: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    entity: Mapped["Entity"] = relationship(back_populates="sanctions_hits")
