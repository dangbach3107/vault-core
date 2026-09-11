# VAULT current state

Updated 2026-09-11. **Both user-prioritized local MVP modules are implemented and technically verified: P2a/MVP-01 company/Trust Profiles and P3a/MVP-02 local data rooms.** V1 operational pilot and buyer sharing are not complete. No commits or pushes.

## Authorization and implementation

The user explicitly selected project-local files for the synthetic VDR MVP after D-04 clarification. This supersedes the source buy/reuse baseline for this local increment only. No matching, Tech DD, NDA/signing, buyer qualification, approvals or unrelated business features were added.

| Area | Actual result | Limits |
| --- | --- | --- |
| Company API/UI | Create/edit/list/search/detail; three per-fact labels with provenance; conflict/expiry flags; draft input/loading/error/retry/save success | Reviewer names are entered manually, not authenticated attestations; no company-wide audit claim |
| Trust Profile | Backend anonymous allowlist with alias/coarse enums/bands; identified/restricted projections and three UI tabs; Layer 3 links to company rooms | Internal preview only; no seller release or buyer permission enforcement |
| PostgreSQL | 17.9 Docker service at loopback 55432; SQLAlchemy/psycopg; revisions 0001/0002 for company and room/document/version tables | No production hosting, backup/retention or accounts |
| Consistency | Unique optional tax IDs, revision-checked/row-locked company updates; precise decimal VND; missing remains null | Draft intake is narrower than all operational V1 outputs |
| Data rooms | Company/deal list/create, six fixed categories, upload, file list, preview, download and retained versions | No delete/share/NDA/MFA/watermark/Q&A workflow |
| File storage | Ignored .data/uploads; generated exclusive keys; original filename/MIME/size/hash/note/time in DB; row-locked version numbering | Local file bytes and DB are not one crash-atomic transaction; crash reconciliation/backup not implemented |
| Validation | File/request size limit; image/PDF/text/Office-container checks; wrong-room/version rejection; failed-commit cleanup; content reads verify size/SHA-256 | Format checks are not antivirus or authenticity verification |
| Preview | PDF.js canvas with page navigation/text view, PNG/JPEG and UTF-8 text; DOCX/XLSX attachment fallback | No Office conversion/OCR; no external provider |
| Contract/setup | OpenAPI export/types cover both modules; safe .env.example; existing setup.ps1 plus idempotent Docker bootstrap | Internal preview defaults off, is not auth, and requires synthetic loopback use |
| Preservation | Root app/tests/sample_data/requirements and original VAULT_text unchanged relative to pre-task staging; staged work retained | Legacy behavior remains unmounted; no commits/pushes |

## Verification evidence

README owns exact Windows commands. Application database is vault; tests use **vault_test**. Python tests use rollback transactions and per-test temp files. Browser tests use vault_test and .tmp/e2e-uploads, retaining synthetic fixtures there.

| Check | Actual result |
| --- | --- |
| Baseline | 8 pre-existing Python checks passed before feature work |
| Runtime | Python 3.12.14, Node 22.17.0, npm 10.9.2; Docker engine 29.1.3 |
| Database startup | Fresh container healthy; bootstrap rerun preserved existing URL/credentials/data |
| Migrations | 0001 and 0002 applied to vault/vault_test; current 0002 (head); Alembic check reports no new upgrade operations |
| Python | 36 passed: legacy/health/profile, validation, exact money, missing vs zero, stale edits, anonymous leakage, upload/versions/room boundaries, rejected writes, commit cleanup, missing/tampered files and streamed-body limit |
| Components | 8 passed: health, profile error/review controls, upload-size rejection and input retention after rejection |
| Browser | 3 Chromium checks passed: health, full company lifecycle and room creation → bad/valid upload → image preview/download → version 2 → version 1 → reload → multi-page PDF |
| UI evidence | Desktop/mobile profile, file-version and PDF screenshots inspected; width 390 has no horizontal overflow |
| Dependency/build | pip check, TypeScript/Vite build and ESLint pass; Prettier configured; producer/consumer contract checks current |
| Isolation | Browser ports 18000/15173 leave user development servers at 8000/5173 alone; no real-deal fixtures used |

Resolved failures: numeric-literal preview routes initially rejected valid paths, fixed using bounded integers. Browser port 8000 was occupied and retained; isolated test ports were introduced. Ambiguous test status/folder selectors were narrowed. jsdom native required-file behavior needed handler-level component tests; actual native submission is covered in Chromium. The native PDF iframe stayed blank in headless Chromium, so PDF.js now renders and verifies actual PDF page text. A file-integrity test initially selected an unrelated retained test row; it now queries its own document ID.

Known warnings: 14 legacy/upstream Python deprecations and Playwright color-environment warnings. Final browser run passed all three checks in 14.8 seconds, including automatic test migration/fixture preparation, and cleaned up its servers. Added Pillow 12.3.0, pypdf 6.18.1, direct python-multipart and PDF.js 6.3.289; lockfiles updated. No warning is treated as feature acceptance.

## Roadmap and remaining decisions

P0/P0a/P1a remain complete for their original scope. P2a/MVP-01 and P3a/MVP-02 meet this local increment's technical criteria. P1/P2/P3 operational phases and full V1-01–V1-12 remain unaccepted: buyer briefs, matching, consent/release, scoped permissions, NDA and DD outputs are broader work.

D-01's three MVP labels and D-04's local file choice are recorded in PROJECT. A-03–A-05 label prototype draft/projection/file limits. D-02/D-03/D-05/D-09/D-10 still gate external disclosure, identity, access controls, ownership, provider operations and retention; D-06/D-07 govern later Tech DD conclusions.

**Next task: user walkthrough of both MVP flows with synthetic data, then record acceptance gaps.** Do not begin another business feature automatically. Before real files or buyer sharing, resolve and implement the appropriate identity/NDA/approval/access controls and coordinated backup/provider plan. Missing strategy/finance sources still limit calendar/budget commitments.
