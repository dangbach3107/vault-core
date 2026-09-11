# Technology stack

Updated 2026-09-11. D-11/D-12 remain selected. Company/Trust Profiles and user-approved local data rooms are implemented with PostgreSQL. Production VDR integrations remain unimplemented.

## Choices, reasons and current status

| Area | Choice and reason | Current evidence |
| --- | --- | --- |
| Backend | Python/FastAPI/Pydantic/Uvicorn; retain the existing language/API approach from the repo and S16 | Python 3.12.14; health, company CRUD/preview and local room/upload/version routes, per-fact validation and decimal VND |
| Frontend | React + TypeScript + Vite; S16's React direction with separate tooling and typed API consumption | React 19.3.0, TypeScript 5.9.3, Vite 8.3.0; profile list/form/detail/previews, local room/file/version screens and health; hash navigation uses browser history without a new routing dependency |
| Database | PostgreSQL + SQLAlchemy + Alembic; selected relational metadata and tracked migrations | Local PostgreSQL 17.9; SQLAlchemy 2.0.52, Alembic 1.19.2, psycopg 3.3.5; revisions 0001/0002 match metadata and run on separate vault/vault_test databases |
| Settings | Pydantic Settings with python-dotenv; typed root-file configuration and process overrides | Root `.env` loading tested; `DATABASE_URL` optional for health |
| Backend tests | pytest + httpx; exercise actual persistence and HTTP behavior | 36 tests pass, including local uploads, immutable versions, room boundaries, content validation, cleanup and missing/tampered files |
| Frontend tests | Vitest + React Testing Library; user-visible behavior | Eight tests pass: health/profile and upload size/error/input retention |
| Browser tests | Playwright/Chromium; actual API/DB/file round trips | Three checks pass: health, company lifecycle and room/upload/version/PDF flow; isolated ports 18000/15173, vault_test and .tmp/e2e-uploads |
| Development | Node.js/npm, ESLint/Prettier; one frontend lockfile and consistent code reviews | Node 22.17.0/npm 10.9.2 verified; Node 22.12+ required; ESLint 10 configured |
| API contract | FastAPI OpenAPI + openapi-typescript 7.13.0; shared export and generated consumer types | `contracts/openapi.json`, generated TypeScript, export/check scripts exist |
| Styling | Plain CSS; keep the small MVP without a UI framework dependency | Responsive profile forms/list/detail; desktop/mobile browser screenshots reviewed; no frontend CDN dependency |
| Commodity services | Source buy/reuse baseline with explicit D-04 local synthetic exception | Project-local blobs and PostgreSQL room/document/version metadata; no external provider, auth, signing or scanners |

Detailed exact versions are in `backend/requirements.lock.txt` and `frontend/package-lock.json`. Python's lock snapshot includes dependencies needed by preserved legacy tests; root `requirements.txt` is unchanged. It records the verified Windows/Python 3.12 environment, not a cross-platform guarantee.

TypeScript's newest registry version conflicted with openapi-typescript and typescript-eslint; 5.9.3 satisfies their peer constraints. ESLint 9 was replaced with supported ESLint 10. No dependency conflict was bypassed with force flags.

## Remaining decisions

Production PostgreSQL hosting/version policy, identity/session mechanism, VDR/e-sign providers and retention remain open. Docker Desktop (existing installation; engine 29.1.3 observed) now runs the local PostgreSQL instance, bound to loopback port 55432. This is development provisioning, not a production database decision. Ruff and a Python formatter remain unconfigured; no corresponding commands are claimed.

The user authorizes company/Trust Profiles and local VDR only. Added Pillow 12.3.0 and pypdf 6.18.1 for image/PDF checks; python-multipart 0.0.32 is now a direct dependency. PDF.js (pdfjs-dist 6.3.289) renders PDFs with a bundled worker, loaded only when needed. This avoids dependence on unavailable native PDF viewing in headless Chromium. No PDF scripts, forms or annotations are executed by the app's canvas viewer. Package versions are locked.

## References and commands

Sources S14/S16 are linked in [PROJECT](PROJECT.md). Official capability references: [React/Vite](https://react.dev/learn/build-a-react-app-from-scratch), [FastAPI OpenAPI](https://fastapi.tiangolo.com/features/), [SQLAlchemy PostgreSQL/psycopg](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html), [OpenAPI TypeScript](https://openapi-ts.dev/node), [Playwright](https://playwright.dev/docs/intro).

[README](../README.md) owns Windows setup/run/check commands. [STATE](STATE.md) records results and limits; [ARCHITECTURE](ARCHITECTURE.md) describes implementation boundaries.

File/viewer references: [FastAPI uploads](https://fastapi.tiangolo.com/tutorial/request-files/), [Pillow image verification](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.verify), [pypdf](https://pypdf.readthedocs.io/en/stable/user/installation.html), [PDF.js rendering](https://mozilla.github.io/pdf.js/examples/).
