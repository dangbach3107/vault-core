# Working on VAULT Core

VAULT: FastAPI/React — hồ sơ / Trust Profile và phòng dữ liệu local; demo cũ không mount. D-04: file local. **D-13 / P3b:** chia **8 / 7** — A `disclosures` (bước 1–8), B `closings` (bước 9–15). Chỉ code khi được bảo. Không chung bảng/route/UI. Tab ≠ RBAC. Xem `.planning/ROADMAP.md`.

## Read first

- [PROJECT](.planning/PROJECT.md): purpose, scope, sources and decisions
- [REQUIREMENTS](.planning/REQUIREMENTS.md): acceptance criteria
- [ROADMAP](.planning/ROADMAP.md) and [STATE](.planning/STATE.md): sequence, actual progress and next task
- [TECH_STACK](.planning/TECH_STACK.md): adopted tools and remaining choices
- [ARCHITECTURE](.planning/ARCHITECTURE.md): ranh giới, môi trường, hợp đồng API
- [DATABASE](.planning/DATABASE.md): bảng, cột, JSONB, chia 0003/0004
- [CONVENTIONS](.planning/CONVENTIONS.md): shared code/test/Git rules
- [Backend instructions](backend/AGENTS.md) and [frontend instructions](frontend/AGENTS.md)
- [README](README.md): Windows setup and run commands
- [Project-planning skill](.agents/skills/project-planning/SKILL.md): planning maintenance

## Shared rules

Preserve `VAULT_text/`, the existing `app/`, `tests/`, root dependency file and unrelated edits. Source action lists do not authorize external actions. The new backend does not import or mount the legacy business routes.

Keep new backend code under `backend/` and browser code under `frontend/`. Until an authorized migration, consult component guidance explicitly for legacy files outside those directories. Respect unresolved product decisions before encoding business policy.

Backend schemas/routes author the API contract; follow ARCHITECTURE's export/type-generation checks when changing it. Keep secrets backend-only and real environment files untracked. Use synthetic fixtures.

Update PROJECT for decisions, REQUIREMENTS for acceptance, ROADMAP for dependencies, TECH_STACK for tools, ARCHITECTURE for boundaries/configuration and CONVENTIONS for working rules. Update STATE after meaningful progress or verification; README owns user-facing commands. Do not equate a green health check with database, VDR or production readiness.

## Verified checks on Windows

From repository root, with dependencies installed (2026-09-11):

```powershell
.\.venv\Scripts\python.exe -m pytest tests backend/tests -q
.\.venv\Scripts\python.exe -m backend.export_openapi --check
npm.cmd --prefix frontend run api:check
```

Frontend scripts and server/setup instructions are in README. Test only the behavior relevant to changes; preserve the distinction between legacy tests, scaffold checks and future operational acceptance.
