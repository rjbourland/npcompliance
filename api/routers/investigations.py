"""Investigation trigger endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_investigation(body: dict) -> dict:
    """Trigger a compliance investigation. Implemented in Phase 3."""
    return {"status": "queued", "query": body.get("query")}
