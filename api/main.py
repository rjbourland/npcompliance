"""FastAPI application entrypoint."""

from __future__ import annotations

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import entities, filings, health, investigations

logger = structlog.get_logger(__name__)

app = FastAPI(
    title="npcompliance",
    description="NonProfit Risk & Compliance OSINT Scanner API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(entities.router, prefix="/entities", tags=["entities"])
app.include_router(filings.router, prefix="/filings", tags=["filings"])
app.include_router(investigations.router, prefix="/investigations", tags=["investigations"])
