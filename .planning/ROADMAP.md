# VAULT Core — lộ trình

Cập nhật: **2026-09-14**.

## P0 — A–Z Deal Workspace frontend MVP

**Trạng thái: đã làm và đã deploy Vercel.**

- Route: `#/investor-mvp`.
- 6 role tabs: Buyer, Seller, VAULT Admin, Legal, Tech DD, Finance.
- React state demo, dữ liệu giả lập.
- Có prep package fee trước closing.
- Có Indicative LOI trước VDR.
- Có Definitive Offer sau Tech DD.
- Có guide: `AZ_DEAL_WORKSPACE_RULES_AND_DEMO_GUIDE_20260913.md`.

## P1 — Backend persistence cho A–Z deal flow

Mục tiêu: biến frontend state demo thành dữ liệu có lưu trong PostgreSQL.

Các module cần có:

1. Buyer request.
2. Seller profile link / sample case.
3. Disclosure approvals: L1, L2, NDA, L3, file grants.
4. Indicative LOI trước VDR.
5. VDR opening record.
6. Tech DD findings + sign-off.
7. Definitive Offer.
8. Legal closing checklist.
9. Deal closed state.
10. Fee lines: prep package, success fee, Tech DD, Build-to-Buy opportunity.
11. Post-deal handoff.

## P1a — Kiến trúc backend đề xuất

Có thể giữ hướng chia aggregate tương lai:

- `disclosures`: buyer request → L1/L2/L3 grants.
- `closings`: VDR opening → Tech DD → Definitive Offer → closing → finance.

Nhưng cần cập nhật so với flow mới:

- `prep_package_fee_recorded` nằm sớm sau seller profile.
- `indicative_loi_submitted` nằm trước L3/VDR.
- `definitive_offer_submitted` thay cho LOI sau Tech DD.

Chi tiết DB hiện là thiết kế tương lai trong `DATABASE.md`, chưa phải trạng thái đã implement.

## P2 — Security và vận hành dữ liệu thật

Chỉ sau P1 mới xét real data. Điều kiện tối thiểu:

- Auth/RBAC/Rikkei SSO.
- MFA cho L2/L3.
- Audit log cho view/download/approve/revoke.
- VDR/object storage production.
- Watermark.
- Antivirus/file scan.
- Backup/restore.
- Retention/deletion policy.
- Legal review cho cross-border data và no-custody.

## P3 — Production integrations

- E-sign/NDA integration.
- VDR provider integration.
- Japanese language support.
- Finance/accounting export.
- Full Tech DD report builder.
- Real workflow notifications.
