"""Grant model — grant flows between entities."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.models.base import Base


class Grant(Base):
    __tablename__ = "grants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    grantor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("entities.id", ondelete="SET NULL"), index=True
    )
    recipient_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("entities.id", ondelete="SET NULL"), index=True
    )
    grantor_ein: Mapped[str | None] = mapped_column()  # raw EIN even if entity not yet resolved
    recipient_ein: Mapped[str | None] = mapped_column(index=True)
    recipient_name: Mapped[str | None] = mapped_column(Text)  # raw name from 990
    amount: Mapped[float | None] = mapped_column(Numeric(18, 2))
    tax_year: Mapped[int | None] = mapped_column(Integer)
    purpose: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    grantor: Mapped["Entity | None"] = relationship(
        foreign_keys=[grantor_id], back_populates="grants_given"
    )
    recipient: Mapped["Entity | None"] = relationship(
        foreign_keys=[recipient_id], back_populates="grants_received"
    )
