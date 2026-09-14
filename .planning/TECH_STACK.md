# VAULT Core — công nghệ

Cập nhật: **2026-09-14**.

## Stack hiện tại

| Vùng | Lựa chọn | Trạng thái |
| --- | --- | --- |
| Frontend | React 19, TypeScript 5.9, Vite 8, CSS thuần, hash route | Đang dùng cho hồ sơ, phòng dữ liệu và A–Z Deal Workspace |
| Frontend demo deploy | Vercel | Đã deploy frontend-only |
| Backend | Python 3.12, FastAPI, Pydantic, Uvicorn | Có cho health/company/rooms; chưa có deal flow API |
| DB dev | PostgreSQL 17.9 Docker loopback `55432`, SQLAlchemy 2, Alembic | Có 0001/0002 cho company/rooms |
| API contract | OpenAPI → `contracts/openapi.json` → generated TS schema | Có cho backend hiện tại |
| Tests | pytest/httpx, Vitest/Testing Library, Playwright | Frontend build/test/lint pass gần nhất |
| File local MVP | `.data/uploads`, Pillow, pypdf, PDF.js | Chỉ synthetic/local; không production VDR |

## Vercel deployment

Vercel hiện chỉ deploy frontend Vite. Không deploy FastAPI/PostgreSQL/file backend.

Production alias:

```text
https://frontend-xi-eosin-36.vercel.app/#/investor-mvp
```

Hạn chế:

- Các route cần backend thật như hồ sơ/VDR persistent không phải mục tiêu của Vercel-only demo.
- A–Z Deal Workspace hiện chạy bằng frontend state, phù hợp để test flow với đồng nghiệp.

## Stack chưa chốt cho production

- Identity / Rikkei SSO.
- MFA provider.
- Backend hosting.
- Production Postgres.
- Object storage hoặc VDR provider.
- E-sign provider.
- Watermark/DRM/file scan.

## Lệnh kiểm tra frontend

```bash
npm --prefix frontend run build
npm --prefix frontend test
npm --prefix frontend run lint
```

Backend commands xem README; backend deal persistence chưa có nên chưa có test tương ứng.
