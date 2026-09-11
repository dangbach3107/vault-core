# VAULT project definition

Planning baseline: 2026-09-11. The latest user request authorizes two connected MVP parts: company/Trust Profiles, then deal data rooms. The earlier health-only restriction is superseded for these two parts. Deployment, other business features, commits and pushes remain outside scope.

## Purpose and users

VAULT (Verified Access to Unlisted Listings & Transactions) supports introductions and due diligence between Vietnamese businesses and Japanese strategic buyers/investors in the Rikkeisoft ecosystem. Its value is structured, evidence-backed company information, controlled disclosure, and expert technology due diligence (Tech DD).

Users are seller owners supplying and approving information; Consulting/VAULT deal leads qualifying buyers and preparing introductions; verified buyers and their DD specialists; Rikkei Tech DD reviewers; Legal/Compliance and Finance reviewers; and IT/security administrators configuring access. Technical administration does not automatically grant permission to read deal content.

## Sources and evidence rules

The requested `VAULT_text/context-file-1.md` and `VAULT_text/context-file-2.md` do not exist. **Assumption A-01:** the two Markdown documents actually present in that directory are the intended sources. Their original names and contents are preserved:

- **S14:** [Tech action guide](../VAULT_text/14_TECH_FOCUS_TRUST_DATAROOM_TECHDD_BUILD_BUY.md), dated 2026-09-10. Practical forms, permission matrix, manual matching, Tech DD, and build/buy boundaries.
- **S16:** [Technical implementation guide](../VAULT_text/16_HUONG_DAN_TRIEN_KHAI_TECH_VAULT.md). Data model, disclosure layers, VDR integration, approvals, and staged implementation.
- **Repository evidence:** `app/`, `tests/`, `sample_data/`, `requirements.txt`, and `.env.example` describe the existing prototype, not approved business policy.

S16 references `01_VAULT_REPORT.md` and `04_VAULT_MODEL.xlsx`; neither is present. Their gate definitions, budget authority, and financial assumptions have not been verified. No source has been designated authoritative over the other. Legal assertions, named vendor capabilities, and illustrative financial figures in the sources have not been independently validated or adopted as conclusions.

## First-version scope

**Assumption A-02:** “first version” means a controlled proof/pilot workflow using forms, human review, and purchased or reused tools, consistent with S14 section 6 and S16 section 0. It is not synonymous with the current demo being ready for real deals.

The planned first version covers buyer qualification; seller intake and fact provenance; anonymous teasers, identified profiles, gap lists and DD scope drafts; manual matching with documented reasons; NDA and seller-controlled disclosure; an external data room; and a six-axis Tech DD checklist/report with reviewed remediation estimates. These may initially be documents and operational procedures rather than new application endpoints.

Future candidates are profile/report automation, deeper VDR/e-sign integration, an internal portal, and eventually matching automation supported by historical outcomes. A public marketplace, public fundraising/Book B, custom e-sign/VDR/scanners, and autonomous AI due diligence or valuation are outside this first version. They are not implicitly approved future work.

## Technology decisions and constraints

[TECH_STACK](TECH_STACK.md) owns the tool choices, reasons and configured/approved/deferred distinction. [ARCHITECTURE](ARCHITECTURE.md) owns the current and target layouts, environment configuration and shared API contract; [CONVENTIONS](CONVENTIONS.md) owns coding, testing and Git rules.

On 2026-09-11 the user selected React + TypeScript + Vite with its testing/development tools (D-11), and PostgreSQL + SQLAlchemy + Alembic (D-12), retaining Python/FastAPI. After the health scaffold, the user explicitly brought forward company forms/list/detail/previews and VDR room/folder/upload/preview/version functionality. Company drafts are now implemented for synthetic internal use. The existing combined demo remains unchanged and unmounted. Broader portal, buyer access and pilot acceptance are not brought forward by this increment.

Build VAULT's schemas, disclosure/workflow rules and Tech DD methodology. The source baseline buys/reuses VDR, storage, e-sign and scanners; D-04 now records the user's local synthetic-file exception. Production providers and controls remain unresolved. Seller-system stacks in source examples are not automatically VAULT requirements.

Use synthetic data for the prototype until access controls and operational procedures are demonstrated. Preserve seller consent and evidence lineage; do not infer that a whole company is audited. Tech DD supplies technical evidence and estimates within a stated scope; Legal decides legal/IP issues and Finance/deal owners review commercial treatment.

The sources' month ranges, 90/150 million VND budgets, 60% coverage criterion for inspected seller systems, example costs and 10–15 deals/year are source proposals or examples, not this repository's approved schedule, budget, test threshold, or operating target.

## Conflicts and decision register

These entries retain both source positions. Proposed handling is not a settled requirement unless a user selection is explicitly recorded. Owners below are suggested review roles; no person has been assigned.

| ID | Difference or ambiguity | Proposed handling / decision needed |
| --- | --- | --- |
| D-01: fact statuses — MVP labels selected | S14 section 2.3 has seven statuses; S16 section 1.1 has three. | Latest user request explicitly selects three labels: self-declared (`SELF_DECLARED`), checked against evidence (`DOCUMENT_VERIFIED`), third-party confirmed (`THIRD_PARTY_CONFIRMED`). Source/date, entered-by, reviewed-by/date and notes are recorded per fact. Missing values remain null; conflict/expiry are separate issue flags and cannot carry a verified label. Merely providing a source never upgrades verification. These are internal operator records, not authenticated attestations or a company audit. |
| D-02: access and approvals | S14 sections 4.2–4.3 require seller approval per buyer for Layer 2 and per document for Layer 3. S16 sections 1.2 and 3.2 add seller + Compliance dual approval for Layer 3, but its role table can read as automatic Layer 3 access after NDA; its Layer 2 flow also calls itself dual approval while showing only seller approval. | Legal + seller/deal lead must approve one matrix. Proposed baseline: verified buyer + seller-approved teaser for Layer 1; NDA + named-buyer seller approval for Layer 2; formal DD + per-file scope + seller and Compliance approvals for Layer 3. Decide whether Layer 2 also needs Compliance and who may grant technical access. |
| D-03: VDR controls | S14 section 4.4 recommends watermarking and permits documented download-control limits. S16 section 2.3 requires dynamic watermarking, view-only defaults and immutable granular logs. S14 IT admins have no default content access; S16 security admins can see Layer 1. | IT + Legal must define the minimum pilot controls, admin visibility, measurable log detail and accepted tool limitations. Do not claim browser restrictions prevent every copy or capture. |
| D-04: local MVP storage — selected | S14 section 6 proposes SharePoint/OneDrive or an external VDR; S16 section 2.1 proposes Google Workspace Enterprise early and dedicated VDR later. | On 2026-09-11, the user explicitly approved project-local file storage for the synthetic MVP, PostgreSQL metadata and no buyer sharing. This is a scoped exception to buy/reuse, not a production provider decision. Local room/upload/preview/version features are implemented; external controls remain unaccepted. |
| D-05: disclosure detail | S14 section 2.2 places architecture documents in Layer 3 and tech stack in Layer 2/3. S16 section 1.2 allows block architecture in Layer 2 and stack in Layer 1. | Consulting + seller + Tech must distinguish safe summaries from sensitive detail. Teaser publication needs human re-identification review; no approved anonymity threshold or free-text rules exist yet. |
| D-06: severity | S14 section 5.3 uses Critical/Major/Minor/Observation. S16 cost examples use Critical P0/High P1/Medium P2; code adds P3 Low. | Tech DD lead must define canonical severity and mapping, including deal impact. Do not equate Major and High solely by their position in a list. |
| D-07: cost and conclusions | S14 explicitly limits Tech DD's legal and valuation role. S16 gives prescriptive license/deal-action examples and a 420 million VND total with 300 million CAPEX proposed as deduction, including an item separately described as pre-closing remediation. | Legal + Finance + Tech must distinguish evidence, remediation budget, pre-closing obligations and negotiated price effects; avoid automatic double counting. Source legal statements and rate examples require review before operational use. |
| D-08: timing and automation | S14 says no matching algorithm in MVP and awaits stable manual work. S16 lists matching among build assets but puts automation/portal at scale; its long roadmap and 30-day actions describe different planning horizons. | Treat these as staged ambitions, not necessarily a contradiction. Use dependency-based phases until business gates, dates and owners are confirmed. |
| D-09: operating policy | Sources do not settle production hosting/database/identity, retention and deletion periods, data residency, exact access lifetime by layer, or integration contracts. S16 gives a 14-day Layer 2 token example. | Database engine/tooling resolved by user selection D-12; hosting, identity and other operational policies remain open before real data or integration. Current hard-coded 14-day prototype behavior is not approval of a universal access policy. |
| D-10: process ownership | S14 asks who approves buyer briefs/teasers, the matching threshold, who signs Tech DD, and whether DD costs belong to VAULT or Rikkei. S16 does not resolve these. | Consulting, Tech DD management and Finance must name owners and review criteria before a live pilot. |
| D-11: frontend/tooling — selected | S16 section 5 mentions React for a later portal; S14 favors lean manual proof work. | User selected React + TypeScript + Vite, npm, Vitest/React Testing Library, Playwright, ESLint and Prettier, retaining Python/FastAPI. The latest two-part MVP explicitly brings forward profile/room screens; broader portal work stays deferred. |
| D-12: persistence — selected | No VAULT database is specified in either context file; legacy storage is in memory. | User selected PostgreSQL + SQLAlchemy + Alembic. Local verification now uses a PostgreSQL 17.9 Docker container, psycopg and revisions 0001/0002. Profiles use validated JSONB plus indexed identity/revision fields. Production hosting/version policy remains open. |

**Implementation assumption A-03 — internal drafts only:** a draft requires a company name; other intake values may be explicitly missing. Revenue/EBITDA use decimal VND (up to two decimal places), not floating point. Tax IDs are optional, trimmed, and unique when provided; this is duplicate prevention, not legal verification. At most three distinct financial years are entered. The frontend initially suggests the three preceding years, editable by the operator.

**Implementation assumption A-04 — conservative preview:** anonymous previews expose only a random alias, coarse sector/region, employee and revenue bands, and deal type. Sector choices are software, manufacturing, services and other; regions are north/central/south. Revenue thresholds are 20/50/100/200/500 billion VND; employee thresholds are 50/200/1,000. These prototype categories/bands are not an approved publication policy. No free text, provenance, technology, address, name or exact money is included. Layer 2 shows identified facts and financials; shareholder detail, decision-maker and permitted-use notes are reserved for Layer 3. No document access is granted by selecting a preview tab. D-02/D-05/D-09/D-10 remain open before external disclosure; seller review for re-identification is still required.

**Implementation assumption A-05 — bounded local files:** one room represents a named deal under a company, with six fixed source categories. Default limit is 10 MiB/file. PDF/PNG/JPG/JPEG/TXT preview locally; DOCX/XLSX download to open. PDF must be unencrypted and at most 500 pages; images at most 20 million pixels. Format/container checks are not antivirus or authenticity verification. Each accepted upload creates separate version bytes and metadata; delete/share/approval workflows are absent. Eventual backup must cover PostgreSQL and files together.

See [ROADMAP.md](ROADMAP.md) and [STATE.md](STATE.md). V1 operational requirements remain broader than this internal prototype.
