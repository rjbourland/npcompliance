"""Filing model — IRS Form 990 by year."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.models.base import Base


class Filing(Base):
    __tablename__ = "filings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), index=True
    )
    tax_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    form_type: Mapped[str] = mapped_column(String(20), default="990")  # 990 | 990-EZ | 990-PF
    object_id: Mapped[str | None] = mapped_column(String(50), unique=True)  # IRS S3 object id
    total_revenue: Mapped[float | None] = mapped_column(Numeric(18, 2))
    total_expenses: Mapped[float | None] = mapped_column(Numeric(18, 2))
    total_assets: Mapped[float | None] = mapped_column(Numeric(18, 2))
    total_liabilities: Mapped[float | None] = mapped_column(Numeric(18, 2))
    program_service_revenue: Mapped[float | None] = mapped_column(Numeric(18, 2))
    contributions: Mapped[float | None] = mapped_column(Numeric(18, 2))
    employee_count: Mapped[int | None] = mapped_column(Integer)
    anomaly_flags: Mapped[list | None] = mapped_column(JSON, default=list)
    raw_json: Mapped[dict | None] = mapped_column(JSON)  # full parsed 990
    has_anomaly: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    entity: Mapped["Entity"] = relationship(back_populates="filings")
