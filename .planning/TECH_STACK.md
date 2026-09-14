# Công nghệ

Cập nhật **2026-09-13**. D-11/D-12 giữ nguyên. P3b không thêm stack mới (không thư viện route, không UI kit).

| Vùng | Lựa chọn | Bằng chứng hiện tại |
| --- | --- | --- |
| Backend | Python 3.12, FastAPI, Pydantic, Uvicorn | Health, công ty, phòng/file |
| Frontend | React 19, TS 5.9.3, Vite 8, CSS thuần, hash route | Hồ sơ + phòng |
| DB | PostgreSQL 17.9 Docker loopback `55432`, SQLAlchemy 2, Alembic 0001/0002 | `vault` / `vault_test` |
| Hợp đồng | OpenAPI → `contracts/openapi.json` → `schema.d.ts` | Script export/check |
| Test | pytest+httpx; Vitest+TL; Playwright 18000/15173 | 36 / 8 / 3 (lần ghi 2026-09-11) |
| File | `.data/uploads`; Pillow, pypdf; PDF.js khi xem | D-04 local |
| Design | Be Vietnam Pro, `#C62828`, SVG 01–13 | Tab deal chưa có SVG |

**Còn mở:** host Postgres production, identity, nhà VDR/e-sign, lưu trữ. Docker Desktop chỉ để dev. Chưa cấu hình Ruff/formatter Python — đừng bịa lệnh.

Lệnh Windows: [README](../README.md). Kết quả chạy: [STATE.md](STATE.md).
