# VAULT Core — định nghĩa dự án

Cập nhật: **2026-09-14**.

## Trạng thái dự án hiện tại

VAULT Core hiện có hai lớp sản phẩm:

1. **Nền kỹ thuật đã có backend thật**: hồ sơ doanh nghiệp / Trust Profile và phòng dữ liệu local bằng FastAPI + PostgreSQL + file storage local.
2. **A–Z Deal Workspace frontend MVP**: một luồng thương vụ mẫu từ Buyer request tới closing, dùng React state và dữ liệu giả lập, đã deploy Vercel để đồng nghiệp/nhà đầu tư test.

Đường dẫn demo chính:

```text
https://frontend-xi-eosin-36.vercel.app/#/investor-mvp
```

Route local chính:

```text
/#/investor-mvp
```

MVP này **không production-ready** và **không dùng dữ liệu thật**.

## Mục đích

VAULT hỗ trợ giới thiệu và thẩm định giữa doanh nghiệp Việt Nam và bên mua/đầu tư chiến lược Nhật trong hệ sinh thái Rikkeisoft. Giá trị cốt lõi:

- bắt đầu từ nhu cầu buyer, không phải marketplace đăng tin;
- hồ sơ doanh nghiệp có bằng chứng;
- mở thông tin theo lớp L1/L2/L3;
- seller kiểm soát disclosure;
- Legal/Compliance chặn rủi ro dữ liệu/pháp lý;
- Tech DD biến rủi ro công nghệ thành chi phí/tác động giao dịch;
- Finance theo dõi phí thực tế, không sync Excel model.

## Vai trò trong A–Z Deal Workspace

| Vai trò | Việc chính trong demo |
| --- | --- |
| Buyer | Tạo buyer request 4 trường, xem L1/L2/L3 khi đủ gate, nộp Indicative LOI trước VDR, gửi Definitive Offer sau Tech DD |
| Seller | Tạo seller profile mẫu, duyệt L1, duyệt buyer mở L2, duyệt từng file L3 |
| VAULT Admin | Điều phối task, prepare match, record NDA, open VDR, mark closed, post-deal handoff |
| Legal | Approve L3, approve cross-border data, xác nhận VAULT không giữ tiền/cổ phần, complete closing checklist |
| Tech DD | Xem findings, remediation class, sign-off |
| Finance | Record prep package fee, record success fee, theo dõi Tech DD / Build-to-Buy opportunity |

Tab persona trong demo **không phải đăng nhập/RBAC thật**.

## Source of truth hiện tại

- Luồng demo và quy tắc: [AZ_DEAL_WORKSPACE_RULES_AND_DEMO_GUIDE_20260913.md](AZ_DEAL_WORKSPACE_RULES_AND_DEMO_GUIDE_20260913.md).
- Quyết định mới nhất của người dùng ưu tiên hơn planning cũ.
- `4, OUTPUT/01_VAULT_REPORT.docx` là nguồn nghiệp vụ chiến lược tham chiếu, không chỉnh sửa trong repo này.
- `VAULT_text/14...` và `VAULT_text/16...` là nguồn kỹ thuật/ý tưởng cũ, không phải trạng thái hiện tại của app.

## Phạm vi hiện tại

### Đã có trong code

- `frontend/src/features/investor-mvp/InvestorMvp.tsx`: A–Z Deal Workspace frontend MVP.
- `frontend/src/Workspace.tsx`: route `#/investor-mvp` và nav.
- Backend hiện có: `companies`, `rooms`, upload/preview/version cho local VDR.
- Vercel frontend deployment.

### Chưa có trong code

- Backend persistence cho buyer request / deal gates / approval / Tech DD / finance.
- Auth/RBAC/MFA thật.
- VDR production, e-sign, watermark, antivirus/file scan.
- Audit log production cho view/download/approve/revoke.
- Real object storage hoặc provider VDR.

## Quy tắc không được claim quá mức

Khi demo, chỉ nói đây là **MVP chứng minh quy trình, vai trò và logic kiểm soát**. Không nói đây là hệ thống production cho dữ liệu mật thật.
