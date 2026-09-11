# Frontend instructions

Inherits [root AGENTS](../AGENTS.md). Read [ARCHITECTURE](../.planning/ARCHITECTURE.md), [CONVENTIONS](../.planning/CONVENTIONS.md) and [TECH_STACK](../.planning/TECH_STACK.md).

- `Workspace.tsx` handles hash navigation; `features/profiles/` and `features/rooms/` own their screens. Preserve the root legacy HTML demo.
- Health calls use `src/api/client.ts`; profile/room/binary calls use `src/api/workspace.ts`. Use generated contract types; do not edit `src/api/generated/`.
- PDF.js renders one page at a time with a local worker; TXT is plain React text. Offer download for unsupported Office previews. Revoke blob URLs and cancel fetch/render work on unmount; never render uploaded HTML.
- Vite forwards `/api` to the backend. Root `.env` supplies public `VITE_` values; never put secrets in these variables.
- Show loading, success, malformed-response and connection-failure behavior honestly; a health response does not establish PostgreSQL readiness.
- Keep labels and keyboard interaction accessible; render untrusted text safely. Editing a fact resets its review label. Layer previews consume backend projections; do not construct anonymous profiles by hiding fields with CSS.
- `package-lock.json` pins dependencies; TypeScript 5.9.3 is selected for generator/linter compatibility.

Verified inside `frontend/`:

```powershell
npm.cmd run dev
npm.cmd run build
npm.cmd test
npm.cmd run lint
npm.cmd run api:check
npm.cmd run test:e2e
```

Browser tests need `npm.cmd run browser:install` once, the migrated `vault_test` database, and free ports 18000/15173; they manage their own servers and use the repository's `.venv`. They preserve normal development servers on 8000/5173. See README for setup and formatting commands.
