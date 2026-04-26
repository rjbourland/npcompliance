"""State charity registry scraping tasks. Implemented in Phase 4 (KIN-962)."""

from __future__ import annotations

from ingestion.celery_app import celery_app


@celery_app.task(name="ingestion.state_registry.scrape", bind=True, max_retries=3)
def scrape_state_registry(self, state: str) -> dict:
    """Scrape charity registry for a given US state."""
    raise NotImplementedError("Implemented in Phase 4 — KIN-962")
