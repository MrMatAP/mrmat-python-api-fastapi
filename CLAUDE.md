# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run development server
fastapi dev src/mrmat_python_api_fastapi/app.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_greeting.py::test_greeting_v1

# Type checking
mypy --no-incremental src/mrmat_python_api_fastapi

# Linting
ruff check src/

# Build wheel
uv build --wheel

# Build container image
make container

# Install/upgrade Helm chart (requires configured kubeconfig)
make helm-install
```

## Architecture

This is a FastAPI boilerplate demonstrating code-first REST API patterns with versioned endpoints, SQLAlchemy persistence, and OAuth2 authentication.

### Structure

```
src/mrmat_python_api_fastapi/
├── __init__.py       # Exports ORMBase (SQLAlchemy DeclarativeBase), SchemaBase (Pydantic), and config
├── app.py            # FastAPI app: router wiring, CORS, OAuth2, Prometheus middleware
├── config.py         # Configuration: env vars (APP_CONFIG_*) override JSON file (APP_CONFIG path)
├── db.py             # SQLAlchemy session factory (LRU-cached), supports SQLite and PostgreSQL
└── apis/
    ├── __init__.py   # Common StatusSchema
    ├── healthz/      # Liveness, readiness, and general health endpoints
    ├── greeting/     # Three-version demonstration API (v1–v3)
    └── platform/v1/  # Full CRUD with Owner and Resource entities

tests/
├── conftest.py       # Session-scoped fixtures: client (TestClient), test_db_path
└── test_*.py         # Integration tests using TestClient
```

### Conventions for adding a new API

Each feature under `apis/` follows this layout:
- `api.py` — `APIRouter` with async endpoint functions; use `Depends(get_db)` for database access
- `schema.py` — Pydantic models inheriting from `SchemaBase` (has `from_attributes=True`); separate input/output schemas
- `db.py` (optional) — SQLAlchemy ORM models inheriting from `ORMBase` with `Mapped`/`mapped_column` types

Register the new router in `app.py` with `app.include_router(...)`.

### Key design points

- **Versioning**: Implemented as subdirectories (`v1/`, `v2/`, `v3/`) each with their own router, included separately in `app.py`.
- **Database**: Sessions are injected via FastAPI dependency injection. SQLite is used for local dev/test; PostgreSQL for production (set `APP_CONFIG_DB_URL`).
- **Configuration precedence**: `APP_CONFIG_*` environment variables > JSON config file at `APP_CONFIG` path > hardcoded defaults in `config.py`.
- **Testing**: Tests use session-scoped `TestClient` backed by a temporary SQLite file. Validate responses with `model_validate()` on Pydantic schemas.
- **Python requirement**: 3.13+, managed via `uv`.