# Kiến trúc và ranh giới API

Cập nhật **2026-09-13**. MVP-01/02 đã chạy. P3b (deal + tab) **chưa tạo module** cho đến khi được phép implement.

## Cây hiện tại (rút gọn)

```text
backend/app/api/     health, companies, rooms
backend/app/db/      models 0001–0002
frontend/src/features/profiles|rooms
frontend/src/Workspace.tsx    hash: companies, rooms, health
contracts/openapi.json
VAULT-Canva-SVG/     01–13 (chrome)
VAULT_text/          nguồn — không sửa
app/                 demo cũ — không mount
```

Không tạo package rỗng “cho đủ sơ đồ”.

## Khi P3b được phép

- Người A: `0003` + `/api/v1/disclosures` + `features/disclosures/` (bước 1–8).
- Người B: `0004` + `/api/v1/closings` + `features/closings/` (bước 9–15).
- Không `deals` chung. B tự seed room/file. Chi tiết: [ROADMAP.md](ROADMAP.md).

## Trách nhiệm

Trình duyệt: `api/client.ts` (health), `api/workspace.ts` (nghiệp vụ). Vite `:5173` proxy `/api` → FastAPI `:8000`.

Backend: validate, chiếu L1/L2/L3 (A-04), lưu DB/file. Frontend: vẽ. `INTERNAL_PREVIEW_ENABLED` mặc định tắt; bật vẫn chỉ loopback + dữ liệu giả — **không phải đăng nhập**.

Tiền: chuỗi VND thập phân, tối đa 2 số lẻ. Thiếu / null / 0 / chưa xác minh tách biệt.

## Hợp đồng API

Soạn schema + route → `python -m backend.export_openapi` → `npm.cmd --prefix frontend run api:generate`. Không sửa tay `openapi.json` / `schema.d.ts`.

Lỗi: 422 sai dữ liệu, 409 revision/trùng MST, 503 hết DB, 404 theo chiếu lớp. P3b thêm 422 khi nhảy FLOW.

Cột/bảng: [DATABASE.md](DATABASE.md). Chạy/cấu hình: [README](../README.md), [TECH_STACK.md](TECH_STACK.md).
