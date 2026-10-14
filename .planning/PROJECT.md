# Định nghĩa dự án VAULT

<<<<<<< Updated upstream
Cập nhật **2026-09-13**. Kịch bản ứng dụng lấy từ [VAULT_text/Work-flow.txt](../VAULT_text/Work-flow.txt) (15 bước). Planning này **không** tự cho phép viết code tính năng, commit hay đẩy remote.
=======
Cập nhật: **2026-10-08**.

## Quyết định phạm vi 2026-10-08

Theo xác nhận trực tiếp của người dùng, MVP bao gồm backend persistence cho toàn bộ 11 nhóm chức năng P1: buyer request, seller profile link/sample case, disclosure approvals, Indicative LOI, VDR opening, Tech DD, Definitive Offer, legal closing, deal closed, bốn loại fee line và post-deal handoff. Đây vẫn là synthetic MVP; auth/RBAC/MFA, e-sign, scanner và VDR production không nằm trong tuyên bố hoàn thành.

Quyết định D-20: danh sách 20 bước từ nhận lead đến post-deal/đóng hồ sơ là khung tham chiếu để thiết kế các module nghiệp vụ, không phải một tính năng workflow riêng cho người dùng bấm chuyển bước. Sản phẩm phải tập trung vào dữ liệu và thao tác thật của lead/deal, participant/KYB, mandate, seller intake/readiness, teaser, buyer thesis/matching, approvals/NDA/access, Q&A, DD/findings, offer-contract-closing, fee và post-deal. Trạng thái/owner/next step là projection từ các module này, không phải nguồn dữ liệu thay thế chúng.

Quyết định D-21: theo `pasted-text.txt` do người dùng cung cấp ngày 2026-10-08, controlled access là lõi phân quyền. Grant không gắn chung với company mà phải chứa person/user, deal, access level L0/L1/L2/L3/Closing, document scope, purpose, approver, thời điểm cấp, hết hạn, thu hồi và lý do. Matching chỉ đề xuất; không tự cấp quyền. Buyer tạo request; Seller/Legal quyết định; Seller/Legal/VAULT Admin có thể revoke theo phạm vi MVP.

Quyết định D-22: các chức năng sản phẩm mới phải nằm trong feature/module/route độc lập và điều hướng theo role; không tiếp tục nhồi vào `A–Z Deal Workspace · synthetic investor demo`. Route A–Z chỉ được giữ như demo tham khảo legacy. Điểm vào sau đăng nhập là VAULT module hub.

Quyết định D-23: “phân quyền” nghĩa là RBAC theo tài khoản đăng nhập. Menu/route được lọc theo Buyer, Seller, VAULT Admin, Legal, Tech DD và Finance; backend vẫn phải kiểm tra role cho mutation. Access request/approval L1–L3 được gọi là nghiệp vụ `Disclosure approvals`, không gọi là chức năng phân quyền tài khoản.

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
>>>>>>> Stashed changes

## Mục đích

VAULT (Verified Access to Unlisted Listings & Transactions) hỗ trợ giới thiệu và thẩm định giữa doanh nghiệp Việt Nam và bên mua/đầu tư chiến lược Nhật trong hệ sinh thái Rikkeisoft. Giá trị cốt lõi: hồ sơ có bằng chứng, mở thông tin theo lớp, Tech DD.

**Điểm khởi đầu là nhu cầu buyer — không phải marketplace đăng tin hàng loạt** (Work-flow bước 1).

## Người dùng (vai trò nghiệp vụ)

| Vai trò | Việc chính trên deal |
| --- | --- |
| **Buyer** | Lưu nhu cầu (4 trường), xem teaser L1, xin mở L2, nộp LOI |
| **Seller** | Tạo hồ sơ mẫu, duyệt teaser L1, duyệt từng buyer mở L2, duyệt từng file L3 |
| **VAULT Admin** | Task theo vai, chuẩn bị match, ghi NDA, mở file VDR đã duyệt, đánh dấu đóng deal, bàn giao Rikkei |
| **Legal** | Duyệt L3, duyệt chuyển dữ liệu xuyên biên giới, xác nhận VAULT không giữ tiền/cổ phần, checklist closing |
| **Tech DD** | Bảng findings + 4 lớp khắc phục + sign-off |
| **Finance** | Dòng phí: gói chuẩn bị, success fee, Tech DD, cơ hội Build-to-Buy |

Kỹ thuật/IT **không** mặc định đọc nội dung deal.

## Nguồn

- **S14 / S16 / S17:** file trong `VAULT_text/` (hướng dẫn kỹ thuật, tổng hợp F01–F20). Đề xuất, chưa phải chính sách đã duyệt.
- **S18 / Work-flow:** [Work-flow.txt](../VAULT_text/Work-flow.txt) — **kịch bản MVP trong app**.
- **S19:** [VAULT-Canva-SVG/](../VAULT-Canva-SVG/) (`01`–`13`) — giao diện hồ sơ / phòng dữ liệu. Tab persona chưa có trong bộ SVG.
- Code cũ `app/`, `sample_data/` là prototype, không phải chính sách.

Không lấy ngân sách / số deal / tháng trong nguồn làm mốc dự án.

## Phạm vi phiên bản này (MVP demo)

Hai lõi dữ liệu đã có: **Hồ sơ doanh nghiệp (Trust Profile)** và **phòng dữ liệu local**. Việc mới tách **hai cụm độc lập, khối lượng 8 / 7**:

- **Mở lớp (người A):** Work-flow **1–8** — nhu cầu, L1, match, NDA, L2, Legal ×3, duyệt từng file L3.
- **VDR & đóng (người B):** **9–15** — mở VDR, Tech DD, LOI, checklist, closed, phí, handoff; seed “L3 file đã duyệt”.

<<<<<<< Updated upstream
Nối bằng `closings.disclosure_id` là PR **sau**. Tab persona chỉ trên màn từng cụm.
=======
- Auth/RBAC/MFA và audit bảo mật production cho deal workspace.
- Auth/RBAC/MFA thật.
- VDR production, e-sign, watermark, antivirus/file scan.
- Audit log production cho view/download/approve/revoke.
- Real object storage hoặc provider VDR.
>>>>>>> Stashed changes

**Trong scope**

- Tab 6 persona + đúng tên nút trong Work-flow.
- Lưu trạng thái cổng; nút sau khóa đến khi bước trước xong.
- VDR local đã có; thêm duyệt theo file × buyer và “mở file đã duyệt”.
- Ghi NDA bằng upload (chưa e-sign).
- Phí thực tế trên deal; không cộng trùng Tech DD / Build-to-Buy vào doanh thu VAULT nếu chưa HĐ riêng.

**Ngoài scope**

- Đăng nhập / MFA / RBAC production.
- Marketplace, Book B, e-sign, VDR thương mại, watermark, quét virus.
- Chuyển tiền, giữ cổ phần, hệ thống pháp nhân Rikkei.
- Thuật toán xếp hạng match, tự động hóa DD.

## Phân quyền — hai tầng (đừng gộp)

### 1) Demo (làm ngay khi implement P3b)

Tab persona **đổi giao diện**, không phải tài khoản. Ai bật `INTERNAL_PREVIEW_ENABLED` đều đổi tab được.

| Tab thấy | Được bấm | Không được (ẩn/khóa) |
| --- | --- | --- |
| Buyer | Lưu request, xin L2, nộp LOI | Duyệt L1/L2/L3, NDA, match, phí, đóng deal |
| Seller | Tạo hồ sơ mẫu, duyệt L1, duyệt buyer L2, duyệt từng file L3 | Ghi NDA, mở VDR, Legal, phí |
| VAULT Admin | Task list, Prepare match, Record NDA, Open VDR, Mark closed, Handoff | Sign-off Tech DD, Record success fee (Finance), ba nút Legal |
| Legal | Approve L3, cross-border, no-custody, checklist closing | Mở file VDR, ghi phí |
| Tech DD | Bảng findings, sign-off | Đóng deal, phí |
| Finance | Xem 4 dòng phí, Record success fee | Đổi cổng pháp lý / VDR |

Cổng **tuần tự trên một deal** (backend từ chối nhảy bước, 422). Đây **không** phải kiểm thử V1-06 (buyer giả, thiếu NDA, sai deal).

### 2) Production (chưa quyết — D-02)

S14: seller duyệt từng buyer (L2) và từng tài liệu (L3). S16: có chỗ thêm Compliance đồng duyệt L3. **Chưa chốt.** Demo chỉ làm đúng thứ tự nút Work-flow.

## Quyết định (trích)

| ID | Nội dung |
| --- | --- |
| D-01 | Ba nhãn sự kiện: tự khai / đối chiếu chứng từ / bên thứ ba xác nhận |
| D-02 | **Mở** — ma trận production |
| D-03 | **Mở** — watermark, MFA, log VDR production |
| D-04 | File MVP nằm local (đã chọn) |
| D-11 / D-12 | React+Vite; PostgreSQL+Alembic (đã chọn) |
| **D-13** | **15 bước Work-flow = kịch bản MVP** (2026-09-13) |

## Giả định triển khai

- **A-04:** L1 ẩn danh (bí danh, ngành/vùng thô, dải số) — không tên, không số tiền đúng.
- **A-06:** Tab ≠ đăng nhập.
- **A-07:** Bốn trường Buyer (chưa đặt tên chính thức): khoảng trống năng lực; kết quả 24 tháng; dải ngân sách; cửa sổ đóng deal. Người quyết định + loại hồ sơ: panel Admin.
- **A-08:** Nút tạo hồ sơ seller lấy fixture tổng hợp trong repo — không công ty thật.
- **A-09:** Match có điểm + lý do + rủi ro do người sửa — không model.
- **A-10:** NDA = file + người ký + thời điểm + hash.
- **A-11:** Tech DD và Build-to-Buy gắn nhãn “không tính doanh thu VAULT” trừ khi có HĐ riêng. “Không giữ tiền/cổ phần” là checkbox Legal, không phải cổng thanh toán.

Chi tiết chấp nhận: [REQUIREMENTS.md](REQUIREMENTS.md). Chia việc: [ROADMAP.md](ROADMAP.md). Cột/bảng: [DATABASE.md](DATABASE.md).
