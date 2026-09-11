# Working on VAULT Core

VAULT has a separate FastAPI/React app with internal company/Trust Profiles and local data rooms, plus a preserved legacy demo. The user selected project-local files for the synthetic VDR MVP (D-04). Keep work within these two modules; do not add other business features or commit/push.

## Read first

- [PROJECT](.planning/PROJECT.md): purpose, scope, sources and decisions
- [REQUIREMENTS](.planning/REQUIREMENTS.md): acceptance criteria
- [ROADMAP](.planning/ROADMAP.md) and [STATE](.planning/STATE.md): sequence, actual progress and next task
- [TECH_STACK](.planning/TECH_STACK.md): adopted tools and remaining choices
- [ARCHITECTURE](.planning/ARCHITECTURE.md): boundaries, environment and API contract
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
