"""IRS Form 990 ingestion tasks. Implemented in Phase 2 (KIN-958)."""

from __future__ import annotations

from ingestion.celery_app import celery_app


@celery_app.task(name="ingestion.irs990.fetch_by_year", bind=True, max_retries=3)
def fetch_990_by_year(self, year: int) -> dict:
    """Bulk fetch IRS 990 filings for a given year from S3."""
    raise NotImplementedError("Implemented in Phase 2 — KIN-959")
