# VAULT Core — hiện trạng

Cập nhật: **2026-09-14**.

## Đang có

| Hạng mục | Trạng thái | Ghi chú |
| --- | --- | --- |
| A–Z Deal Workspace | Đã có frontend MVP | `#/investor-mvp`, React state, dữ liệu giả lập |
| Vercel frontend demo | Đã deploy | `https://frontend-xi-eosin-36.vercel.app/#/investor-mvp` |
| Company / Trust Profile | Đã có backend + frontend | PostgreSQL, JSONB profile, preview L1/L2/L3 nội bộ |
| Local data room | Đã có backend + frontend | Upload, preview, version, local file storage |
| Prep package fee trong flow | Đã có trong frontend demo | Finance tab |
| Indicative LOI trước VDR | Đã có trong frontend demo | Buyer tab, gate Layer 3 |
| Definitive Offer sau Tech DD | Đã có trong frontend demo | Buyer tab |
| Quy tắc demo trong platform | Đã có | Section “Quy tắc demo” trong route investor MVP |
| Guide A–Z | Đã có | `.planning/AZ_DEAL_WORKSPACE_RULES_AND_DEMO_GUIDE_20260913.md` |

## Chưa có

| Hạng mục | Trạng thái |
| --- | --- |
| Backend deal persistence cho A–Z flow | Chưa có |
| Auth/RBAC/Rikkei SSO | Chưa có |
| MFA thật | Chưa có |
| VDR production/object storage | Chưa có |
| Watermark/audit/antivirus production-grade | Chưa có |
| Real data readiness | Chưa đạt |

## Kiểm thử gần nhất

Đã chạy sau cập nhật flow mới:

```bash
npm --prefix frontend run build
npm --prefix frontend test
npm --prefix frontend run lint
```

Kết quả: pass.

## Lưu ý git

Hiện có thay đổi frontend MVP, Vercel config, planning và một diff `contracts/openapi.json` không liên quan trực tiếp tới MVP frontend. Cần review trước commit.

## Cập nhật 2026-09-16 — redeploy Vercel frontend và chuẩn bị full-stack hosted demo

Đã redeploy production frontend bằng Vercel CLI lúc 2026-09-16 09:35 Asia/Ho_Chi_Minh. Production alias vẫn là:

```text
https://frontend-xi-eosin-36.vercel.app
```

Deployment ID: `dpl_ANaxZXs7SZqqbVFMz7iy4geVY3PA`; inspect URL: `https://vercel.com/dangbachsuper-8294/frontend/ANaxZXs7SZqqbVFMz7iy4geVY3PA`.

Project Vercel hiện chưa có environment variable nào, nên chưa có `VITE_API_BASE_URL`; các màn Company/Room trên link public vẫn chưa thể thao tác giống local cho đến khi có backend public + database + upload storage.

Đã chuẩn bị code/config để sau khi có Railway có thể deploy backend thật cho các màn giống local:

- Backend thêm CORS theo allowlist `ALLOWED_ORIGINS`.
- Backend thêm allowlist host `ALLOWED_HOSTS` và tự đọc `RAILWAY_PUBLIC_DOMAIN` để không còn hard-code loopback khi chạy hosted demo.
- Backend nhận Postgres URL dạng `postgres://...` hoặc `postgresql://...` và tự đổi sang `postgresql+psycopg://...`.
- Frontend không còn tự chặn Company/Room trên Vercel nếu `VITE_API_BASE_URL` đã cấu hình.
- Frontend hỗ trợ optional `DEMO_PASSWORD` qua header `X-Demo-Password`.
- Thêm `Dockerfile.railway`, `railway.json`, `.dockerignore` cho Railway backend + Railway Volume demo.
- Vẫn giữ `render.yaml` blueprint cho Render backend + persistent disk demo nếu cần phương án thay thế.

Vẫn chưa deploy full-stack vì chưa có Railway login/token/project hoặc backend public URL. Vercel hiện chỉ trở thành full-stack sau khi đặt `VITE_API_BASE_URL` về backend public URL rồi redeploy.

Kiểm tra đã chạy trong lượt này:

```bash
npm --prefix frontend run build
npm --prefix frontend test
npm --prefix frontend run lint
python3 -m pytest -p no:rerunfailures backend/tests/test_health.py -q
python3 -m backend.export_openapi --check
npm --prefix frontend run api:check
```

Kết quả: pass. Lệnh pytest không tắt plugin `pytest-rerunfailures` bị sandbox chặn socket cục bộ trên macOS, nên đã chạy lại với `-p no:rerunfailures` cho health test.
