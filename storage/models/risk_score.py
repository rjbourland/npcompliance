"""RiskScore model — per-dimension risk scores for an entity."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.models.base import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), index=True
    )
    dimension: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # financial_anomaly | sanctions_exposure | registration_gap | officer_overlap | grant_concentration
    score: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)  # 0.0 – 1.0
    evidence: Mapped[dict | None] = mapped_column(JSON)
    scored_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    entity: Mapped["Entity"] = relationship(back_populates="risk_scores")
