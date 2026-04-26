# npcompliance

Evidence-based compliance OSINT tool — IRS 990 ingestion, OFAC sanctions screening,
state charity registry checks, fraud risk scoring, and grant-flow mapping for nonprofit
and PAC entities.

## Architecture

```
npcompliance/
├── ingestion/          # IRS 990, OFAC, state registry fetchers
├── processing/         # Normalization, dedup, entity resolution
├── scoring/            # Risk scoring engine
├── api/                # FastAPI backend
├── ui/                 # React dashboard (Phase 5)
├── storage/            # SQLAlchemy models + Alembic migrations
├── tests/
├── docker-compose.yml
└── README.md
```

## Services

| Service | Port | Description |
|---|---|---|
| api | 8000 | FastAPI REST backend |
| ingestion-worker | — | Celery worker for fetch jobs |
| postgres | 5432 | Primary data store |
| redis | 6379 | Celery broker + result backend |

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

Health check: `curl http://localhost:8000/health`

## Phase Roadmap

| Phase | Description | Issue |
|---|---|---|
| 1 | Project setup, architecture, schema | KIN-955 |
| 2 | IRS Form 990 ingestion pipeline | KIN-958 |
| 3 | OFAC sanctions screening | KIN-961 |
| 4 | State charity registry scrapers | KIN-962 |
| 5 | Risk scoring engine + UI dashboard | — |

## Schema

Seven core tables: `entities`, `filings`, `officers`, `grants`,
`sanctions_hits`, `risk_scores`, `state_registry`.

See `storage/models/` for SQLAlchemy ORM definitions and
`storage/migrations/` for Alembic migration history.
