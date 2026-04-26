"""Entity model — core nonprofit / PAC record."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.models.base import Base


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    ein: Mapped[str] = mapped_column(String(12), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    name_normalized: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="nonprofit"
    )  # nonprofit | pac | foundation | church
    address_street: Mapped[str | None] = mapped_column(Text)
    address_city: Mapped[str | None] = mapped_column(String(100))
    address_state: Mapped[str | None] = mapped_column(String(2), index=True)
    address_zip: Mapped[str | None] = mapped_column(String(10))
    registration_status: Mapped[str | None] = mapped_column(
        String(50)
    )  # active | revoked | delinquent
    exempt_status: Mapped[str | None] = mapped_column(String(10))  # 501c3 | 501c4 | etc.
    ruling_year: Mapped[int | None] = mapped_column()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    filings: Mapped[list["Filing"]] = relationship(back_populates="entity", lazy="select")
    officers: Mapped[list["Officer"]] = relationship(back_populates="entity", lazy="select")
    sanctions_hits: Mapped[list["SanctionsHit"]] = relationship(
        back_populates="entity", lazy="select"
    )
    risk_scores: Mapped[list["RiskScore"]] = relationship(
        back_populates="entity", lazy="select"
    )
    state_registries: Mapped[list["StateRegistry"]] = relationship(
        back_populates="entity", lazy="select"
    )
    grants_given: Mapped[list["Grant"]] = relationship(
        foreign_keys="Grant.grantor_id", back_populates="grantor", lazy="select"
    )
    grants_received: Mapped[list["Grant"]] = relationship(
        foreign_keys="Grant.recipient_id", back_populates="recipient", lazy="select"
    )
