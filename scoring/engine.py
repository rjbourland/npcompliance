"""Risk scoring engine. Populated in Phase 5."""

from __future__ import annotations


class RiskScoringEngine:
    """Composite risk scorer for nonprofit entities."""

    DIMENSIONS = [
        "financial_anomaly",
        "sanctions_exposure",
        "registration_gap",
        "officer_overlap",
        "grant_concentration",
    ]

    def score(self, entity_id: str) -> dict:
        """Compute risk scores across all dimensions. Implemented in Phase 5."""
        raise NotImplementedError("Implemented in Phase 5")
