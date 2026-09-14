# VAULT Core — yêu cầu hiện tại

Cập nhật: **2026-09-14**.

## 1. Yêu cầu đã thể hiện trong A–Z Deal Workspace frontend MVP

| ID | Yêu cầu | Trạng thái / bằng chứng |
| --- | --- | --- |
| AZ-01 | Có route demo chính `#/investor-mvp` | `frontend/src/Workspace.tsx`, `InvestorMvp.tsx` |
| AZ-02 | Cùng một deal mẫu đồng bộ qua Buyer/Seller/VAULT Admin/Legal/Tech DD/Finance | `InvestorMvp.tsx` dùng một `DealState` chung |
| AZ-03 | Buyer request gồm 4 trường MVP | Buyer tab |
| AZ-04 | Seller tạo hồ sơ mẫu và duyệt L1 teaser | Seller tab |
| AZ-05 | Ghi nhận prep package fee ngay sau seller ký chuẩn hóa hồ sơ | Finance tab: `Record prep package fee` |
| AZ-06 | Matching rule-based có điểm, lý do, risks | VAULT Admin tab |
| AZ-07 | Layer 2 cần identity request + NDA + seller approval | `layer2Ready` logic |
| AZ-08 | Indicative LOI bắt buộc trước Layer 3/VDR | `layer3Ready` logic |
| AZ-09 | Legal duyệt L3, cross-border, no-custody | Legal tab |
| AZ-10 | Seller duyệt từng file Layer 3 cho buyer | Seller tab |
| AZ-11 | VDR chỉ mở sau gate L3 | VAULT Admin tab |
| AZ-12 | Tech DD sau Indicative LOI + VDR, có findings/remediation/sign-off | Tech DD tab |
| AZ-13 | Buyer gửi Definitive Offer sau Tech DD | Buyer tab |
| AZ-14 | Legal closing checklist trước khi closed | Legal tab |
| AZ-15 | Finance ghi success fee sau closing và phân biệt prep fee | Finance tab |
| AZ-16 | Post-deal handoff to Rikkei | VAULT Admin tab |
| AZ-17 | Có rule panel trong platform để demo-er không nói sai | `Quy tắc demo` section trong `InvestorMvp.tsx` |

## 2. Yêu cầu backend đã có từ trước

| ID | Yêu cầu | Trạng thái |
| --- | --- | --- |
| MVP-01 | Company / Trust Profile CRUD, 3 verification labels, L1/L2/L3 preview nội bộ | Đã có backend + frontend |
| MVP-02 | Local data room: room, 6 groups, upload/list/preview/version | Đã có backend + frontend |

Hai module này có backend thật nhưng **chưa nối persistent với A–Z Deal Workspace**.

## 3. Yêu cầu chưa đạt / roadmap tiếp theo

| ID | Yêu cầu | Ghi chú |
| --- | --- | --- |
| BE-01 | Persist A–Z deal state vào PostgreSQL | Chưa có |
| BE-02 | API cho buyer request, approvals, grants, Tech DD, fee lines | Chưa có |
| BE-03 | Audit log view/download/approve/revoke | Chưa có |
| SEC-01 | Auth/RBAC/Rikkei SSO | Chưa có |
| SEC-02 | MFA cho L2/L3 | Chưa có |
| VDR-01 | VDR/object storage production | Chưa có |
| FILE-01 | Watermark + antivirus/file scan | Chưa có |
| LEGAL-01 | Retention/deletion policy | Chưa chốt |

## 4. Acceptance hiện tại

Frontend đã được kiểm bằng:

```bash
npm --prefix frontend run build
npm --prefix frontend test
npm --prefix frontend run lint
```

Các lệnh trên đã pass sau khi thêm prep package fee, Indicative LOI trước VDR và Definitive Offer.
