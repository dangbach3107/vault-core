# VAULT Core — database plan

Cập nhật: **2026-09-14**.

## Trạng thái hiện tại

Database hiện mới có các bảng cho:

- company profile / Trust Profile;
- room;
- document;
- document version.

A–Z Deal Workspace hiện tại **chưa có backend persistence**. Các bước deal đang nằm trong React local state.

## Mục tiêu database tương lai

Khi chuyển A–Z Deal Workspace thành platform vận hành thật, cần lưu các nhóm dữ liệu sau:

1. Buyer request.
2. Seller profile / company link.
3. Disclosure gates: L1, L2, NDA, Legal, file grants.
4. Indicative LOI trước VDR.
5. VDR opening record.
6. Tech DD findings + sign-off.
7. Definitive Offer.
8. Legal closing checklist.
9. Deal closed status.
10. Fee lines: prep package, success fee, Tech DD, Build-to-Buy opportunity.
11. Post-deal handoff.
12. Audit events.

## Đề xuất aggregate

### 1. `disclosures`

Phụ trách phần mở thông tin:

- buyer request 4 trường;
- company/seller link;
- seller L1 approval;
- match score/reasons/risks;
- identity request;
- NDA metadata;
- seller L2 approval;
- Indicative LOI metadata;
- legal L3/cross-border/no-custody flags;
- seller file grants.

### 2. `closings`

Phụ trách phần sau khi có L3/VDR:

- opened VDR documents;
- Tech DD findings;
- Tech DD sign-off;
- Definitive Offer;
- closing checklist;
- closed state;
- fee lines;
- post-deal handoff.

### 3. Audit tables

Cần audit tối thiểu:

- actor;
- role;
- action;
- target type/id;
- timestamp;
- IP/device nếu có;
- reason/override reason nếu có.

Không ghi nội dung file mật hoặc secret vào audit log.

## Ghi chú triển khai

- File này là **thiết kế tương lai**, chưa phải schema đã apply.
- Khi tạo migration, phải cập nhật `ARCHITECTURE.md`, `REQUIREMENTS.md`, OpenAPI và frontend types.
- Không sửa tay `contracts/openapi.json`; export từ backend.
