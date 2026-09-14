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
