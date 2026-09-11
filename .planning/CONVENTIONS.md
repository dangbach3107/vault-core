# Development conventions

Updated 2026-09-11. These rules apply to the health/profile app; legacy code is preserved. Buyer release and VDR policy remain prospective. [ARCHITECTURE](ARCHITECTURE.md) owns boundaries/contract/configuration; [TECH_STACK](TECH_STACK.md) owns tool choices; [PROJECT](PROJECT.md) owns decisions.

## Naming and organization

- Python modules/functions/variables: `snake_case`; classes and Pydantic schemas: `PascalCase`; constants: `UPPER_SNAKE_CASE`. Keep descriptive `test_*.py` names.
- React components and their files: `PascalCase.tsx`; TypeScript functions/variables/hooks: `camelCase` / `useSomething`; feature directories: lowercase names. Component tests use `*.test.tsx`, non-UI tests `*.test.ts`, browser tests `*.spec.ts`.
- API JSON stays `snake_case` to match current Python schemas. Treat IDs as opaque strings and enum values as contract data; do not silently translate them in the frontend.
- Keep route handlers focused on HTTP concerns, services on business decisions, and database/provider work behind their own modules. Frontend features use the shared API wrapper; shared components do not contain permission policy.
- Preserve UTF-8 Vietnamese/Japanese content. Use English identifiers, retain domain terminology, and explain business constraints in comments rather than narrating obvious code.

## Validation and disclosure

Backend validation is authoritative; client validation gives immediate feedback only. Validate request types/bounds in Pydantic, cross-record rules in services and persistent invariants in PostgreSQL. D-01's three MVP labels are selected; retain missing/conflict/expiry separately. D-02/D-05/D-06 still gate external release/approval/severity; internal previews follow documented A-04 without claiming buyer permissions.

Keep missing, null, zero and unverified values distinct. New company money uses decimal VND with at most two fractional digits, serialized as strings; avoid JS numeric conversion for money inputs. New timestamps use timezone-aware UTC. Do not modify legacy floating-point fields/naive timestamps as an unrelated cleanup.

Treat seller input as untrusted text. Use safe React text rendering; do not render untrusted HTML. The backend selects permitted response fields before serialization. A hidden button or absent link is not permission enforcement.

## Error handling

Target HTTP behavior: 422 for invalid request data; 401 for absent/invalid identity; 403 for denied access; 404 for unavailable resources under the chosen disclosure policy; 409 for conflicting workflow state; 500 for unexpected failures. These are conventions for future routes; do not silently change existing clients.

Prefer FastAPI's `detail` response family over a new universal success/error wrapper. Document validation error arrays separately from application errors in OpenAPI. Define stable application error codes/messages when implementing that contract; do not assume current endpoints already return them.

Map expected domain failures at the API boundary. Unexpected exceptions produce a generic client message and a server-side diagnostic reference; do not expose tracebacks, secrets or raw exception strings. Logs must omit NDA contents, sensitive facts, credentials and access tokens. Frontend handles loading, empty, validation, permission and network failures explicitly; avoid automatic retries of approval/signature mutations unless their idempotency is defined.

## Testing

- Preserve existing tests and record their baseline before moving them. Test behavior and risks relevant to each change; documentation-only edits need link/diff checks, not application test scaffolds.
- Backend: focused business-rule tests plus API denial/validation checks; isolate state between tests. Persistence tests use an isolated PostgreSQL test database once configured, never a live deal database. Verify migrations and transaction/constraint behavior when they change.
- Frontend: interaction/accessible-state tests with synthetic contract-shaped fixtures. Type checking and fixtures do not replace API or browser integration tests.
- Browser: cover representative intake/profile flows and missing NDA, wrong buyer/deal, expired/revoked access and failed approvals as those features are implemented. Use synthetic data and controlled provider substitutes.
- Contract updates follow ARCHITECTURE's producer/export/consumer checks. No coverage percentage is imposed from S16's seller-system DD example.
- Record exact commands, versions and outcomes in STATE after execution. Add CI checks only after the local commands/configuration exist. Do not invent npm scripts, migration commands or formatter settings.

## Git and review

Inspect current branch/status and preserve unrelated work. For future authorized changes, use short descriptive branches such as `docs/<topic>`, `feat/<topic>` or `fix/<topic>`; follow an established repository convention if one is later found. No branch protection or CI policy has been verified.

Keep changes small and tied to requirement/decision IDs. Reviews explain behavior, validation and remaining limits; contract changes include both sides and the schema diff. Include lockfiles when dependency tooling is configured. Exclude secrets, local environments and generated build/test output.

Do not create commits, push or rewrite history during this scaffold task. For subsequent work, act within the user's authorization; these conventions do not add permission to publish changes. Update the relevant planning documents when scope, architecture, validation or actual progress changes.
