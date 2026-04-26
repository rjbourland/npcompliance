"""Celery application factory."""

from __future__ import annotations

from celery import Celery

from api.config import get_settings

_settings = get_settings()

celery_app = Celery(
    "npcompliance",
    broker=_settings.celery_broker_url,
    backend=_settings.celery_result_backend,
    include=[
        "ingestion.tasks.irs990",
        "ingestion.tasks.ofac",
        "ingestion.tasks.state_registry",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,
)
