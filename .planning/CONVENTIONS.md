# Quy ước làm việc

Cập nhật **2026-09-13**. Áp dụng app mới (`backend/`, `frontend/`). Demo cũ giữ nguyên.

## Đặt tên

- Python: `snake_case`; schema/class: `PascalCase`.
- React file: `PascalCase.tsx`; thư mục feature: chữ thường.
- JSON API: `snake_case`. ID là chuỗi mờ. Enum **không** dịch trong UI (nhãn nút Work-flow giữ tiếng Anh/Việt như nguồn).
- Tiếng Việt/Nhật UTF-8 trong copy; định danh code tiếng Anh.

## Validate và mở lớp

Backend là chuẩn. Thiếu / null / 0 / chưa xác minh tách. Tiền VND chuỗi, ≤2 lẻ — không qua `number` JS. Người bán là text không tin cậy: chỉ `React` text, không HTML upload.

Tab ẩn nút **không** phải phân quyền. P3b: từ chối nhảy FLOW ở API (422).

## Lỗi HTTP

422 sai input / nhảy bước; 409 revision hoặc MST trùng; 404 theo chiếu lớp / chưa grant; 503 hết DB. Dùng `detail` FastAPI. Log không ghi nội dung NDA, sự kiện nhạy cảm, secret.

## Test

`vault_test` + rollback; không đụng DB deal thật. Fixture tổng hợp. E2E P3b bấm đúng chữ nút Work-flow. Ghi lệnh/kết quả vào STATE khi đã chạy.

## Git

Nhánh khi được phép: `feat/<chủ-đề>`, `fix/`, `docs/`. Planning **không** được commit/push trừ khi người dùng yêu cầu. Hai người P3b: không đụng file đã chia trong ROADMAP.
