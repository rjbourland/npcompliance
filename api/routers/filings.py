"""Filing endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_filings() -> dict:
    """List Form 990 filings. Populated in Phase 2."""
    return {"filings": [], "total": 0}
