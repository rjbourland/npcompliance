"""Entity CRUD endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_entities() -> dict:
    """List nonprofit entities. Populated in Phase 2."""
    return {"entities": [], "total": 0}
