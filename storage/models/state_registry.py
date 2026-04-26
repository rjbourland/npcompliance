"""StateRegistry model — state-level charity registration records."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.models.base import Base


class StateRegistry(Base):
    __tablename__ = "state_registry"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), index=True
    )
    state: Mapped[str] = mapped_column(String(2), nullable=False, index=True)  # CA | NY | TX
    registration_number: Mapped[str | None] = mapped_column(String(50))
    status: Mapped[str | None] = mapped_column(
        String(50)
    )  # active | delinquent | revoked | not_registered
    last_filing_date: Mapped[date | None] = mapped_column(Date)
    expiry_date: Mapped[date | None] = mapped_column(Date)
    address_mismatch: Mapped[bool | None] = mapped_column(default=False)
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    entity: Mapped["Entity"] = relationship(back_populates="state_registries")
