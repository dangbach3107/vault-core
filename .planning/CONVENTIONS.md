# VAULT Core — quy ước làm việc

Cập nhật: **2026-09-14**.

## 1. Quy ước chung

- Code chính nằm trong `backend/` và `frontend/`.
- Demo cũ trong `app/` giữ nguyên, không mount thành app chính.
- Không dùng dữ liệu thật trong A–Z Deal Workspace hiện tại.
- Tab persona trong `InvestorMvp` không phải auth/RBAC.
- Không claim production-ready khi chưa có auth/MFA/audit/VDR production.

## 2. Đặt tên

- Python: `snake_case`.
- Pydantic/React component: `PascalCase`.
- API JSON: `snake_case`.
- Enum code dùng tiếng Anh; UI copy có thể tiếng Việt/Anh theo đúng nút demo.
- Tiền VND nên truyền/lưu dạng chuỗi decimal khi vào backend, tránh `number` JS cho giá trị thật.

## 3. Frontend A–Z demo

- Route chính: `#/investor-mvp`.
- File chính: `frontend/src/features/investor-mvp/InvestorMvp.tsx`.
- Giữ một state deal chung nếu còn là frontend demo.
- Khi thêm bước demo, cập nhật đồng thời:
  1. `DealState`;
  2. `steps`;
  3. tab liên quan;
  4. guide `.planning/AZ_DEAL_WORKSPACE_RULES_AND_DEMO_GUIDE_20260913.md`;
  5. planning nếu thay đổi scope.

## 4. Backend / API

Backend là nguồn chuẩn khi một workflow được persistent. Khi chuyển A–Z từ frontend state sang backend:

- API phải từ chối nhảy bước không hợp lệ bằng 422.
- Không chỉ ẩn nút ở frontend.
- Sensitive logs không ghi nội dung NDA/file mật/secret.
- Audit event chỉ ghi metadata cần thiết.

## 5. Test

Trước khi báo xong frontend:

```bash
npm --prefix frontend run build
npm --prefix frontend test
npm --prefix frontend run lint
```

Trước khi báo xong backend:

```bash
python -m pytest tests backend/tests -q
python -m alembic -c backend/alembic.ini check
python -m backend.export_openapi --check
npm --prefix frontend run api:check
```

Chỉ chạy backend commands khi môi trường DB sẵn sàng.

## 6. Deploy

- Frontend demo deploy bằng Vercel từ `frontend/`.
- `frontend/vercel.json` giữ cấu hình build Vite + SPA fallback.
- Deploy Vercel không đồng nghĩa backend production đã có.

## 7. Git

- Không commit/push trừ khi người dùng yêu cầu.
- Trước commit cần kiểm tra `git status` và xác định file nào là thay đổi chủ động.
- `contracts/openapi.json` chỉ nên thay đổi khi backend contract được export có chủ đích.
