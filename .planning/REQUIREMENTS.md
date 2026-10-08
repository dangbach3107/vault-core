# Yêu cầu VAULT

<<<<<<< Updated upstream
Cập nhật **2026-09-13**. Nguồn kịch bản: [Work-flow.txt](../VAULT_text/Work-flow.txt). Quyết định D-13 trong [PROJECT.md](PROJECT.md).
=======
Cập nhật: **2026-10-08**.

## P1 — Deal workspace MVP có persistence

| ID | Acceptance MVP |
| --- | --- |
| P1-01 | Deal aggregate được lưu PostgreSQL và reload giữ nguyên state |
| P1-02 | API action bao phủ buyer request, seller link/sample, L1/L2/NDA/L3/file grant, hai offer, VDR opening, Tech DD, closing, fees và handoff |
| P1-03 | Backend từ chối action khi thiếu gate bắt buộc; reset và complete-sample cũng được persist |
| P1-04 | Fee records có đủ prep package, success fee, Tech DD và Build-to-Buy opportunity |
| P1-05 | Frontend `#/investor-mvp` đọc/ghi deal qua API thay vì chỉ giữ React state |
| P1-06 | Sáu tài khoản synthetic đăng nhập theo role; backend xác thực session và từ chối action không thuộc role |
| P1-07 | 20 bước là khung tham chiếu; trạng thái dashboard phải được suy ra từ dữ liệu nghiệp vụ thực, không yêu cầu người dùng vận hành một tracker riêng |
| P1-08 | MVP có module nghiệp vụ cho lead/deal, participant, mandate, seller readiness, teaser, buyer thesis/matching, disclosure/NDA/access, Q&A, DD/findings, closing, fee và post-deal |
| P1-09 | Mỗi module lưu dữ liệu, người chịu trách nhiệm, bằng chứng và trạng thái riêng; dashboard chỉ tổng hợp current state, blockers và next action |
| P1-10 | Access grant gắn với user + deal + level + document scope + purpose + approver + granted/expiry/revoked timestamps + reason; matching không tự mở dữ liệu |
| P1-11 | Buyer gửi access request; Seller/Legal duyệt hoặc từ chối và bắt buộc expiry khi duyệt; Seller/Legal/VAULT Admin được revoke; mọi thay đổi sinh access event |
| P1-12 | Chức năng mới có route/component độc lập và xuất hiện theo role trên VAULT module hub; không triển khai thêm nghiệp vụ trong màn synthetic A–Z |
| P1-13 | RBAC đăng nhập lọc navigation/route theo role và backend từ chối mutation trái role; disclosure approval là nghiệp vụ trong deal, không đồng nhất với RBAC |
>>>>>>> Stashed changes

V1-01–V1-12 (pilot vận hành: MFA, VDR mua ngoài, ma trận đã ký) **vẫn chưa đạt**. MVP-01 / MVP-02 **đã làm** (hồ sơ + phòng local). FLOW-01–15 là increment **kế tiếp khi được phép code**.

## Lõi đã có

| ID | Chức năng | Trạng thái |
| --- | --- | --- |
| MVP-01 | Tạo/sửa/danh sách hồ sơ; 3 nhãn sự kiện; xem trước L1/L2/L3 nội bộ | Xong, dữ liệu giả |
| MVP-02 | Phòng theo deal, 6 nhóm tài liệu, tải lên, xem trước, phiên bản | Xong, file local. Không MFA/watermark |

## Kịch bản 15 bước (Work-flow)

Một deal giả. Nút sau **khóa** và nêu bước thiếu (tiếng Việt). Toast đúng thông điệp dưới đây. Chrome hồ sơ/phòng theo `VAULT-Canva-SVG` (`13-states`: trống, lỗi, 10 MiB, bản cũ, đã lưu nháp).

| ID | Tab | Nút (giữ nguyên chữ) | Phải có trước | Lưu gì | Thông điệp / ý nghĩa |
| --- | --- | --- | --- | --- | --- |
| FLOW-01 | Buyer | **Lưu buyer request** | — | Đúng 4 trường. Tab này **không** danh sách seller. | “Đã lưu buyer request. Chưa mở marketplace.” Bắt đầu từ nhu cầu, không kho tin đăng. |
| FLOW-02 | Seller | **Tạo seller profile từ sample data** rồi **Approve L1 teaser** | — (độc lập 01) | Một công ty giả + cờ L1 đã duyệt. L1 ẩn danh. | “Đã tạo hồ sơ mẫu.” / “Đã duyệt teaser Lớp 1 (ẩn danh).” Seller kiểm soát lớp mở. |
| FLOW-03 | VAULT Admin | **Prepare match buyer–seller** | 01 + 02 | Task theo vai; điểm; ≥3 lý do; ≥3 rủi ro. | “Đã chuẩn bị match. Điểm và lý do đã lưu.” Giới thiệu có kiểm soát, không gửi hàng loạt. |
| FLOW-04 | Buyer | **Request identity / mở Layer 2** | 02 L1 + 03 | Yêu cầu L2; **chưa** mở định danh. Hiện L1 đã mở. | “Đã gửi yêu cầu mở Lớp 2 (định danh).” Không tự mở. |
| FLOW-05 | Admin | **Record signed NDA** | 04 | File + người ký + giờ + hash. | “Đã ghi nhận NDA đã ký (bản ghi file, chưa e-sign).” Cổng trước thông tin định danh. |
| FLOW-06 | Seller | **Approve buyer mở Layer 2** | 04 + 05 | Duyệt **từng** buyer trên deal này. | “Đã duyệt buyer này mở Lớp 2.” NDA không đủ để xem doanh nghiệp. |
| FLOW-07 | Legal | **Approve Layer 3 access** · **Approve cross-border data access** · **Confirm VAULT does not hold money/shares** | 06 (khuyến nghị; L3 mở ở 09 cần đủ 3 cờ) | Ba cờ độc lập. | “Legal đã duyệt L3 / xuyên biên giới / VAULT không giữ tiền hay cổ phần.” |
| FLOW-08 | Seller | **Approve** từng file L3 cho buyer | 07 (cả 3) | Một dòng grant / (file × buyer). | “Đã duyệt từng tệp Lớp 3 cho buyer này.” Không mở cả kho. |
| FLOW-09 | Admin | **Open approved VDR files** | 08 ≥1 file | Lọc phòng local theo grant. Banner môi trường minh họa. | “Đã mở các tệp VDR đã được duyệt (môi trường minh họa).” Production: VDR thật, audit, watermark, MFA, quét file. |
| FLOW-10 | Tech DD | **Tech DD reviewer sign-off** | 09 | Findings + 4 lớp: *Pre-closing must-fix* · *6-month fix* · *Defer* · *Growth investment*. | “Tech DD đã sign-off. Ước lượng không phải định giá.” |
| FLOW-11 | Buyer | **Submit LOI / indicative offer** | 09 + 10 | Số tiền chuỗi VND thập phân; cờ không ràng buộc. | “Đã nộp LOI / chào mua sơ bộ (không ràng buộc).” Quan tâm → hành động giao dịch. |
| FLOW-12 | Legal | **Complete LOI/closing checklist** | 11 | Checklist đủ mới được đóng. | “Checklist LOI/closing đã đủ.” Chưa tự động hóa hồ sơ pháp lý. |
| FLOW-13 | Admin | **Mark SPA signed / deal closed** | 11 + 12 + 07 no-custody | Trạng thái đóng (giả lập). | “Đã đánh dấu SPA ký / deal closed.” Quản trị tới đóng, không dừng ở VDR. |
| FLOW-14 | Finance | **Record success fee** | 13 | Dòng: prep package, success fee, Tech DD, Build-to-Buy. Hai dòng sau không cộng doanh thu VAULT. | “Đã ghi success fee. Không cộng trùng Tech DD / Build-to-Buy.” App = actuals; Excel = kế hoạch. |
| FLOW-15 | Admin | **Post-deal handoff to Rikkei** | 14 | Ghi chú bàn giao. Thanh tiến độ kịch bản = 15/15 (không phải 100% V1). | “Đã bàn giao post-deal cho Rikkei. Doanh thu khác cần hợp đồng riêng.” |

**ENG-04 (khi code):** hai aggregate — `disclosures` (A, `0003`, FLOW-01–08) và `closings` (B, `0004`, FLOW-09–15). Không bảng `deals` chung. Chi tiết: [ROADMAP.md](ROADMAP.md).

<<<<<<< Updated upstream
Nghiệm thu A trên `#/disclosures` (8/8). Nghiệm thu B trên `#/closings` (7/7, seed L3 xong). Không e2e 15 bước trong PR của A hoặc B.
=======
| ID | Yêu cầu | Ghi chú |
| --- | --- | --- |
| BE-01 | Persist A–Z deal state vào PostgreSQL | Đã có ở mức synthetic MVP (`deals`, revision `0003`) |
| BE-02 | API cho buyer request, approvals, grants, Tech DD, fee lines | Đã có action API với gate và dữ liệu mẫu có cấu trúc |
| BE-03 | Audit log view/download/approve/revoke | Chưa có audit bảo mật production; MVP chỉ giữ timestamp/note trong aggregate |
| SEC-01 | Auth/RBAC/Rikkei SSO | Có role login/RBAC synthetic cho MVP; chưa có Rikkei SSO production |
| SEC-02 | MFA cho L2/L3 | Chưa có |
| VDR-01 | VDR/object storage production | Chưa có |
| VDR-02 | Người dùng có thể xóa tài liệu (gồm mọi phiên bản) hoặc cả phòng dữ liệu sau bước xác nhận; metadata và blob local tương ứng được dọn | MVP local |
| FILE-01 | Watermark + antivirus/file scan | Chưa có |
| LEGAL-01 | Retention/deletion policy | Chưa chốt |
>>>>>>> Stashed changes

## V1 vận hành (giữ để khỏi nhầm MVP)

V1-01 brief đủ field · V1-06 từ chối buyer giả / thiếu NDA / sai file · V1-07 chữ ký thật · V1-08 MFA + watermark · V1-10 playbook 6 trục đã chốt D-06. **P3b không đóng các mục này.**

## Data ownership

- `SEC-03`: Seller chỉ được liệt kê, xem, sửa và xóa hồ sơ doanh nghiệp do chính tài khoản seller đó tạo.
- `SEC-04`: Phòng dữ liệu và tài liệu kế thừa chủ sở hữu từ doanh nghiệp; seller khác không thể đọc hoặc thay đổi bằng cách gọi API trực tiếp.
- API trả `404` khi seller truy cập tài nguyên của seller khác để không làm lộ sự tồn tại của bản ghi.
