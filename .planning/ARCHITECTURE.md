# VAULT Core — kiến trúc

Cập nhật: **2026-09-14**.

## 1. Kiến trúc hiện tại

```text
vault-core/
├── backend/app/api/companies.py      # Hồ sơ / Trust Profile backend
├── backend/app/api/rooms.py          # Local data room backend
├── backend/app/db/models.py          # Company/Room/Document/Version models
├── frontend/src/features/profiles/   # UI hồ sơ doanh nghiệp
├── frontend/src/features/rooms/      # UI phòng dữ liệu local
├── frontend/src/features/investor-mvp/InvestorMvp.tsx
├── frontend/src/Workspace.tsx        # Hash routes, gồm #/investor-mvp
├── frontend/vercel.json              # Vercel frontend deployment
└── contracts/openapi.json            # Contract backend hiện có
```

## 2. A–Z Deal Workspace hiện tại

- Route: `#/investor-mvp`.
- Dữ liệu: React local state trong `InvestorMvp.tsx`.
- Không gọi backend cho deal gates.
- Dùng một `DealState` chung cho 6 tab persona.
- Phù hợp demo flow với dữ liệu giả lập.
- Không production-ready.

Các gate chính trong `DealState`:

- buyer request;
- seller profile;
- prep package fee;
- L1/L2/L3 approvals;
- Indicative LOI trước VDR;
- VDR opened;
- Tech DD sign-off;
- Definitive Offer;
- closing checklist;
- deal closed;
- success fee;
- post-deal handoff.

## 3. Backend hiện có

Backend hiện chỉ phục vụ:

- health;
- company profile;
- Trust Profile preview;
- local room/document/version.

Backend chưa có:

- buyer request entity;
- deal workflow entity;
- approval/grant events;
- Indicative LOI / Definitive Offer persistence;
- Tech DD persistence;
- finance fee line persistence;
- audit log production.

## 4. Target backend sau MVP

Có thể triển khai theo hai aggregate để giảm coupling:

1. **Disclosure aggregate**: buyer request, seller profile link, L1/L2/L3 approval, NDA, file grants, Indicative LOI.
2. **Closing aggregate**: VDR opened, Tech DD, Definitive Offer, closing checklist, deal closed, fee lines, handoff.

Thiết kế này là roadmap, không phải trạng thái hiện tại. Xem `DATABASE.md` cho đề xuất bảng tương lai.

## 5. Vercel boundary

Vercel chỉ host frontend static build. Không dùng Vercel làm backend cho FastAPI/PostgreSQL/local file storage.

Nếu cần demo backend thật qua internet, cần deploy thêm:

- FastAPI backend ở Render/Fly/Railway/AWS/GCP/server riêng;
- Postgres managed;
- object storage/VDR provider;
- cấu hình CORS/auth/secrets.

## 6. Boundary cho hosted full-stack demo

Hosted demo vẫn là synthetic/internal preview, không phải production VDR. Khác với Vercel-only, mode này có thêm:

```text
Vercel static frontend
  → public FastAPI backend trên Railway hoặc Render
  → managed PostgreSQL
  → persistent demo upload directory
```

Railway target dùng `Dockerfile.railway`, `railway.json`, Railway PostgreSQL và Railway Volume mount `/data`.

Các route hồ sơ/phòng dữ liệu vẫn bị chặn nếu `INTERNAL_PREVIEW_ENABLED=false`. Khi bật hosted demo, phải cấu hình explicit allowlist:

- `ALLOWED_ORIGINS`: frontend origin được phép gọi CORS.
- `ALLOWED_HOSTS`: custom/backend hostname được phép phục vụ API preview; Railway-provided domain được đọc từ `RAILWAY_PUBLIC_DOMAIN`.
- `DEMO_PASSWORD`: tùy chọn shared password nhẹ cho demo; không thay thế auth/RBAC.

Health check vẫn là liveness, không chứng minh DB/storage production-ready.
