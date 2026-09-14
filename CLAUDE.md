# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

VAULT Core is an internal synthetic MVP: company/Trust Profiles and deal-scoped local data rooms. It is not buyer-facing, not authenticated, and not a production VDR. Product purpose, open decisions, and scope live in `.planning/` — read those before encoding business policy.

## Planning docs (source of truth)

Read these first; do not duplicate their content here.

| File | Owns |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Working rules for this repo |
| [backend/AGENTS.md](backend/AGENTS.md) | Backend entry, DB, files, previews |
| [frontend/AGENTS.md](frontend/AGENTS.md) | UI, generated types, previews |
| [.planning/PROJECT.md](.planning/PROJECT.md) | Purpose, sources, decision register (D-01–D-13), assumptions A-01–A-11 |
| [.planning/REQUIREMENTS.md](.planning/REQUIREMENTS.md) | Acceptance criteria |
| [.planning/ROADMAP.md](.planning/ROADMAP.md) / [STATE.md](.planning/STATE.md) | Sequence and verified progress |
| [.planning/TECH_STACK.md](.planning/TECH_STACK.md) | Tool choices and versions |
| [.planning/ARCHITECTURE.md](.planning/ARCHITECTURE.md) | Layout, API contract, env, storage |
| [.planning/DATABASE.md](.planning/DATABASE.md) | Bảng/cột đã có (0001–0002) và P3b (0003–0004) |
| [.planning/CONVENTIONS.md](.planning/CONVENTIONS.md) | Naming, validation, errors, tests, Git |

Update the matching planning file when a decision, requirement, boundary, tool, or verified result changes. README owns user-facing Windows commands.

## Tech stack

- **Backend:** Python 3.12, FastAPI, Pydantic v2 / Settings, Uvicorn. Active app: `backend.app.main:app`.
- **Frontend:** React 19 + TypeScript 5.9.3 + Vite 8. Hash routing in `Workspace.tsx` (no router library). Plain CSS.
- **DB:** PostgreSQL 17 (local Docker, loopback `55432`) + SQLAlchemy 2 + Alembic. Revisions `0001` companies, `0002` rooms/documents/versions.
- **Contract:** FastAPI OpenAPI → `contracts/openapi.json` → `frontend/src/api/generated/schema.d.ts` (openapi-typescript).
- **Tests:** pytest + httpx (backend); Vitest + Testing Library (frontend); Playwright Chromium (e2e on ports 18000/15173, `vault_test`).
- **Files:** Project-local blobs under `UPLOAD_DIRECTORY` (default `.data/uploads`). Pillow + pypdf validate images/PDFs; PDF.js renders in the browser.

Root `requirements.txt` is **legacy only**. New backend deps: `backend/requirements.txt` and `backend/requirements.lock.txt`.

## Two codebases

| Tree | Role |
| --- | --- |
| `backend/`, `frontend/`, `contracts/` | Active MVP. Work here. |
| `app/`, `tests/`, root `requirements.txt`, `sample_data/` | Legacy demo. Do not import, mount, or “migrate” unless explicitly authorized. |
| `VAULT_text/` | Source documents. Do not edit. |

The new backend must not import or mount legacy business routes.

## Run (Windows, repo root)

Verified environment: Python 3.12, Node.js ≥ 22.12 (`npm.cmd`, not `npm.ps1`).

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-database.ps1
.\.venv\Scripts\python.exe -m alembic -c backend/alembic.ini upgrade head
$env:INTERNAL_PREVIEW_ENABLED = "true"
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Second terminal:

```powershell
npm.cmd --prefix frontend run dev
```

- UI: http://127.0.0.1:5173 (default `#/companies`)
- Health: http://127.0.0.1:8000/api/v1/health — **liveness only**, not PostgreSQL/readiness
- Docs: http://127.0.0.1:8000/docs

Vite proxies `/api` to `BACKEND_PROXY_TARGET` (default `http://127.0.0.1:8000`). Restart both servers after `.env` changes.

`INTERNAL_PREVIEW_ENABLED` is a local prototype switch, not authentication. Keep loopback + synthetic data only.

## Build, lint, test

From repo root:

```powershell
.\.venv\Scripts\python.exe -m backend.testing
.\.venv\Scripts\python.exe -m pytest tests backend/tests -q
.\.venv\Scripts\python.exe -m pytest backend/tests/test_companies.py -q   # one file
.\.venv\Scripts\python.exe -m alembic -c backend/alembic.ini check
.\.venv\Scripts\python.exe -m backend.export_openapi --check
npm.cmd --prefix frontend run build
npm.cmd --prefix frontend test
npm.cmd --prefix frontend run lint
npm.cmd --prefix frontend run format:check
npm.cmd --prefix frontend run api:check
```

E2E (free ports 18000/15173; uses `vault_test` and `.tmp/e2e-uploads`, not live `vault` / `.data/uploads`):

```powershell
npm.cmd --prefix frontend run browser:install   # once
npm.cmd --prefix frontend run test:e2e
```

A green health check is not database, VDR, or production readiness.

## API contract workflow

Author in `backend/app/schemas/` and `backend/app/api/`. Never hand-edit `contracts/openapi.json` or `frontend/src/api/generated/`.

```powershell
.\.venv\Scripts\python.exe -m backend.export_openapi
npm.cmd --prefix frontend run api:generate
.\.venv\Scripts\python.exe -m backend.export_openapi --check
npm.cmd --prefix frontend run api:check
```

Export uses default settings so local `.env` names do not rewrite the checked-in schema. Keep operation IDs stable.

## Architecture (runtime)

```
Browser (Vite :5173)
  health  → src/api/client.ts
  CRUD/files → src/api/workspace.ts + generated types
       │  /api proxy
FastAPI (uvicorn :8000)  backend.app.main:app
  health     — no DB
  companies  — JSONB CompanyInput, revision lock, Layer 1/2/3 projections
  rooms      — folders, upload, versions, local blobs
       │
PostgreSQL (companies, rooms, documents, document_versions)
Local disk  (.data/uploads) — generated storage keys, never client filenames
```

Frontend owns rendering. Backend owns validation, disclosure projections, persistence, and file checks. Layer tabs are internal previews (A-04), not buyer permissions. Request-supplied roles are not auth.

Money: decimal VND strings, max two fractional digits — do not convert through JS numbers. Missing/null/zero/unverified stay distinct. Verification labels: `SELF_DECLARED` / `DOCUMENT_VERIFIED` / `THIRD_PARTY_CONFIRMED`. Editing a verified value must reset the label; conflict/expiry cannot stay verified.

## Do not modify

- `VAULT_text/`
- `app/`, `tests/` (legacy), root `requirements.txt`, `sample_data/` unless a task explicitly authorizes legacy work
- `frontend/src/api/generated/`
- Checked-in `contracts/openapi.json` except via `backend.export_openapi`
- Real `.env`, `.tmp/database.*`, upload/fixture directories — never commit secrets, passwords, or live blobs
- Unrelated staged work; do not commit/push unless the user asks

## Conventions (project-specific)

- Python: `snake_case` modules/functions; PascalCase schemas/classes. React files: `PascalCase.tsx`. Feature dirs: lowercase. JSON: `snake_case`. IDs are opaque strings; do not translate enum values in the UI.
- Routes: HTTP only. Services: business rules. `app/db/`: persistence. Frontend features call the shared API wrappers.
- UTF-8 Vietnamese/Japanese content; English identifiers.
- HTTP: 422 invalid, 409 conflict (stale revision / unique tax), 503 DB unavailable, 404 per disclosure. Prefer FastAPI `detail`. Do not invent a universal success wrapper.
- Seller text is untrusted: React text only, never render uploaded HTML.
- File versions: generated keys; check room/document ownership, size, type, hashes; retain old versions; delete only new blobs after a failed commit.
- Tests: isolated `vault_test` + per-test rollback; synthetic fixtures. Do not use the deal database.
- Branches (when authorized): `feat/<topic>`, `fix/<topic>`, `docs/<topic>`.

## Adding a feature

1. Confirm it is in scope. Shipped: profiles + local rooms. **Next planned (D-13 / P3b): 15-step deal walkthrough — implement only when the user asks.** Do not add production portal, buyer auth, e-sign, or external VDR because S17 mentions them. Demo NDA/match/Legal/Finance follow FLOW-01–15, not V1 acceptance.
2. Do not encode unresolved decisions (D-02 access, D-03 VDR controls, D-05 disclosure detail, D-06 severity, production hosting/identity).
3. Backend first: schema + route + service + migration if persistence changes. Apply migrations explicitly — never on app startup.
4. Export OpenAPI, regenerate frontend types, update `workspace.ts` / screens / tests.
5. Keep secrets backend-only. Never put credentials in `VITE_*`.
6. Create modules only when the requirement needs them. No empty “future” packages.
7. Update PROJECT / REQUIREMENTS / ARCHITECTURE / TECH_STACK / CONVENTIONS / STATE as applicable. README if user commands change.
8. Test the behavior you changed (legacy + new). Do not treat health as acceptance for data features.

Ruff / a Python formatter are not configured — do not invent those commands.
