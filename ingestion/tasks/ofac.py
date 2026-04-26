"""OFAC SDN list ingestion tasks. Implemented in Phase 3 (KIN-961)."""

from __future__ import annotations

from ingestion.celery_app import celery_app


@celery_app.task(name="ingestion.ofac.sync_sdn", bind=True, max_retries=3)
def sync_ofac_sdn(self) -> dict:
    """Download and parse the OFAC SDN XML list."""
    raise NotImplementedError("Implemented in Phase 3 — KIN-961")
