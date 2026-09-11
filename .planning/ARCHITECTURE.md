# Architecture and API boundary

Updated 2026-09-11. Both user-prioritized MVP modules are implemented: company/Trust Profiles and local synthetic data rooms. D-04 explicitly approves local files. The legacy demo remains preserved and unmounted.

## Current layout

```text
vault-core/
├── AGENTS.md / .planning/ / .agents/skills/
├── VAULT_text/                      # Original sources, unchanged
├── app/                            # Legacy demo, unchanged
├── tests/                          # Four legacy service tests, unchanged
├── requirements.txt                # Legacy dependencies, unchanged
├── .env.example                    # Safe root settings template
├── scripts/setup.ps1               # Windows local environment/dependency setup
├── backend/
│   ├── AGENTS.md
│   ├── requirements.txt            # Direct dependency ranges
│   ├── requirements.lock.txt       # Verified Windows dependency snapshot
│   ├── app/
│   │   ├── main.py                 # create_app and ASGI entry point
│   │   ├── api/                    # health, companies, rooms, dependencies, body limit
│   │   ├── schemas/                # Health, company facts/previews, rooms/versions
│   │   ├── services/               # Profile projections and local file storage
│   │   ├── core/config.py          # Typed environment configuration
│   │   └── db/                     # Lazy sessions, company/room/document/version models
│   ├── tests/                      # Health, PostgreSQL and local upload/version checks
│   ├── testing.py                  # Isolated vault_test configuration/migrations
│   ├── dev_database.py             # Local Docker bootstrap; secrets stay ignored
│   ├── export_openapi.py           # Deterministic export and drift check
│   ├── alembic.ini
│   └── migrations/                 # 0001 company drafts; 0002 rooms/documents/versions
├── frontend/
│   ├── AGENTS.md / package.json / package-lock.json
│   ├── vite.config.ts / playwright.config.ts
│   ├── src/
│   │   ├── Workspace.tsx           # Hash navigation: companies, rooms, health
│   │   ├── App.tsx                 # Preserved connectivity UI
│   │   ├── features/profiles/      # List, input/edit, detail, preview and fact controls
│   │   ├── features/rooms/         # Rooms, uploads, versions and PDF/image/text previews
│   │   ├── api/workspace.ts        # Profile/room/binary requests and generated types
│   │   ├── api/client.ts           # Fetch wrapper and response shape guard
│   │   ├── api/generated/schema.d.ts
│   │   └── App.test.tsx / test/setup.ts
│   ├── scripts/                    # Type generation/check and browser installer
│   └── tests/e2e/                  # Health/profile/room flows, DB/fixture preparation
├── compose.yaml / scripts/start-database.ps1 # Loopback PostgreSQL development service
└── contracts/openapi.json          # Generated shared wire contract
```

Do not add empty business modules just to fill the target layout. Future feature screens/components, backend services/provider adapters and database models are created only for authorized requirements.

## Responsibilities and communication

The browser calls health through `api/client.ts` and company APIs through `api/workspace.ts`, using types from the shared contract. Vite listens on `127.0.0.1:5173` and forwards `/api` to FastAPI on `127.0.0.1:8000`. Vite preview uses port 4173 and the same proxy. Both frontend servers use strict ports. Playwright uses 15173/18000 and vault_test, leaving normal development servers alone. No browser auto-open is configured.

FastAPI returns `status`, `service`, `version` and `scope: liveness`. Health does not open PostgreSQL or contact external services. The UI reports request failure, malformed data and a five-second timeout, and supports manual retry. Browser types come from the backend contract.

Backend owns validation, future identity/disclosure rules and persistence. Frontend owns rendering and interaction only. No CORS middleware is needed for the current same-origin frontend proxy. If separate public origins are introduced later, define explicit origins and the auth/session design; CORS does not supply authentication.

Company APIs provide list/search/pagination, create, get, revision-checked update and `preview/{1|2|3}`. SQLAlchemy persists a validated CompanyInput payload in JSONB, with UUID identity, random alias, indexed name, unique optional tax ID, revision and UTC timestamps. Money is decimal VND serialized as strings. Update acquires a row lock and rejects stale revisions (409) or a changed value that retains its verification label (422). Unique-tax conflicts return 409; unavailable/unconfigured database returns a generic 503. Sessions/engines are lazy; health does not require PostgreSQL.

Disclosure is projected by backend services into separate preview response schemas. Anonymous responses whitelist coarse enums/bands and omit identity, free text, provenance and exact financials. Layer 2/3 separation follows internal assumption A-04, not an approved buyer permission matrix. The app does not authenticate reviewers; source/review names are operator-entered records. Browser controls are not authorization. `INTERNAL_PREVIEW_ENABLED` defaults false; enabled routes reject external browser origins and hostile Host values but still require loopback-only, synthetic use.

Production hosting, identity and provider controls remain open. The D-04 local MVP uses `services/files.py`, `api/rooms.py`, `schemas/room.py`, SQLAlchemy Room/Document/DocumentVersion models and migration 0002. `features/rooms/` owns room/file/version screens and the lazily loaded PDF.js viewer. Layer 3 links to rooms filtered by company; selecting a layer never grants buyer access.

## Contract ownership and synchronization

- **Authoring source:** `backend/app/schemas/` and FastAPI routes under `backend/app/api/`.
- **Shared artifact:** `contracts/openapi.json`, exported from the default app configuration.
- **Consumer:** `frontend/src/api/generated/schema.d.ts`, generated with openapi-typescript.
- **Runtime description:** `/openapi.json`; Swagger at `/docs`, ReDoc at `/redoc`.

The preserved legacy API is not included in this contract. Export uses explicit defaults so local project names or environment files do not rewrite the snapshot. Company requests, per-fact enums, projection responses and expected HTTP error shapes are included.

For a contract change, edit backend schema/routes first, export, review the schema diff, regenerate frontend types, update consumers/fixtures and run checks:

```powershell
# Repository root
.\.venv\Scripts\python.exe -m backend.export_openapi
npm.cmd --prefix frontend run api:generate
.\.venv\Scripts\python.exe -m backend.export_openapi --check
npm.cmd --prefix frontend run api:check
```

Backend tests also compare the stored schema with the exported schema. Frontend build type-checks generated consumers. Checks exist locally; CI has not been configured. Generated files are not hand-edited. Keep operation IDs stable, review breaking changes together with both sides, and test future access-denial behavior separately from schema correctness.

## Environment configuration

The backend uses Pydantic Settings to read root `.env` in UTF-8 independent of working directory; explicit constructor values override process variables, which override the file, then defaults apply. Unknown legacy entries are ignored. Vite also uses the repository root as its environment directory. Restart both servers after changing settings.

| Variable | Consumer | Meaning |
| --- | --- | --- |
| `PROJECT_NAME`, `VERSION` | Backend | Service metadata; defaults VAULT Core / 0.1.0 |
| `API_V1_STR` | Backend | API prefix; default /api/v1; if changed, update the frontend base and contract intentionally |
| `ENVIRONMENT` | Backend settings | Environment label; not an authentication/security switch |
| `DATABASE_URL` | Backend only | postgresql+psycopg URL required for profile persistence; optional for health |
| `INTERNAL_PREVIEW_ENABLED` | Backend only | Defaults false; explicit local prototype opt-in, not authentication |
| `UPLOAD_DIRECTORY` | Backend only | Defaults .data/uploads; relative paths resolve from repository root; ignored by Git |
| `MAX_UPLOAD_BYTES` | Backend only | Default 10485760; API validates file size; request bodies limited to this plus 64 KiB multipart overhead |
| `VITE_API_BASE_URL` | Public browser bundle | Default /api/v1; never put secrets here |
| `BACKEND_PROXY_TARGET` | Vite dev/preview process | Default http://127.0.0.1:8000; not embedded as a browser secret |
| Legacy secret/DRM/webhook entries | Legacy compatibility only | Not used by the new health backend; examples are empty/inert |

Only `VITE_` values are exposed as browser environment configuration. Root `.env` is ignored by Git; setup copies the example only if no `.env` exists. It never overwrites a user's settings.

SQLAlchemy accepts the PostgreSQL psycopg driver. Alembic revision 0001 creates companies; migration is explicit, not performed at application startup. Models are registered in Alembic env for drift checks. Docker bootstrap generates and preserves a random password under ignored `.tmp/database.*`, binds PostgreSQL 17.9 to port 55432 and retains a named volume. It fills root `.env` DATABASE_URL only when blank. Runtime passwords never enter tracked example files.

`backend.testing` selects `TEST_DATABASE_URL` or the ignored local test URL and refuses a database not named vault_test. Backend tests bind sessions to per-test rollback transactions. Browser tests commit synthetic records in vault_test to demonstrate real persistence; they never use the application's DATABASE_URL. Production backup/retention are not configured.

## Preservation and future migration

The profile implementation uses new code rather than mounting legacy business modules. Keep `app/`, root tests and sample data as preserved reference; do not run it as a competing default backend or claim its business functions were migrated. Existing staged changes are not reverted or restaged by this task.

A later authorized migration must establish behavior/imports, resolve policy and update the contract/clients together. The two-part local MVP is ready for a synthetic user walkthrough; broader portal/workflows remain deferred.

## Local document storage and versions

Rooms belong to one company and represent named deals; folder enums implement the six source groups. Upload creates a Document and version 1; a new version locks the Document row, increments its number and creates separate metadata/blob bytes. PostgreSQL enforces unique document/version pairs, folder values, foreign keys and positive sizes. APIs verify room/document/version relationships before lookup; this is record consistency, not buyer authentication.

Files use generated UUID storage keys with exclusive create; client paths/filenames never control disk locations. Backend validates size and actual image/PDF/text or Office container format. Filename/type errors do not leave partial DB rows. Failed DB commits remove only the new blob. Each read checks saved length/SHA-256, so missing/tampered files return a generic 503 while metadata remains. A process crash between filesystem and DB operations can leave an orphan file; automatic crash reconciliation and coordinated backup are not implemented.

PDF.js renders one bounded-size canvas page at a time with previous/next controls and an extracted-text view; its worker is bundled locally. PNG/JPEG use image elements, UTF-8 TXT uses escaped text, and DOCX/XLSX are attachment-only. Byte routes use no-store/nosniff and restrictive response headers. Content inspection is not malware scanning. No public file mount, signing, watermark, MFA, view/download separation or buyer access exists.

Python file tests use temporary directories; browser tests use .tmp/e2e-uploads and synthetic fixtures from `backend.preview_fixtures`, leaving .data/uploads untouched.
