# Backend instructions

Inherits [root AGENTS](../AGENTS.md). Read [ARCHITECTURE](../.planning/ARCHITECTURE.md), [CONVENTIONS](../.planning/CONVENTIONS.md) and [TECH_STACK](../.planning/TECH_STACK.md).

- The active entry point is `backend.app.main:app`, launched from repository root. The separate `app/` at root is preserved legacy code; do not import its business routes.
- Keep Pydantic request/response schemas under `app/schemas/` and SQLAlchemy persistence code under `app/db/`. Add business services only for authorized requirements.
- `GET /api/v1/health` is liveness only. It must work without PostgreSQL or credentials and must not claim readiness of external systems.
- Pydantic Settings reads root `.env`; process environment takes precedence. Keep provider/database credentials backend-only.
- Database factories are lazy. Revisions `0001`/`0002` create companies and local rooms/documents/versions; apply migrations explicitly. Tests use isolated `vault_test` with per-test rollback and temporary file directories.
- File versions use generated storage keys, never client filenames as paths. Check room/document ownership, content, size and stored hashes. Retain old versions; remove only newly-created blobs after failed commits. Local storage is not a secure external VDR.
- Internal preview routes are disabled by default. They are for synthetic loopback use, not authenticated buyer access. Keep Layer 1 projections as a backend allowlist; preserve money precision and per-fact provenance. Reject stale edits and changes that retain an old verification label.
- Follow the shared export/type-generation workflow for API changes. Export defaults are deterministic; local runtime settings must not rewrite the checked-in schema.
- Future access-controlled routes must derive identity from the selected auth mechanism and enforce buyer/deal/document scope; request-supplied roles are not authentication.

Verified from repository root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
.\.venv\Scripts\python.exe -m pytest backend/tests -q
.\.venv\Scripts\python.exe -m backend.export_openapi --check
.\.venv\Scripts\python.exe -m alembic -c backend/alembic.ini history
```

Live PostgreSQL checks are in [STATE](../.planning/STATE.md). README owns startup, fixtures and migration commands. D-04 explicitly approves local synthetic files; production access/provider controls remain separate.
