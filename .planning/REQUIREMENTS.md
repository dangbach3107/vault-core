# Yêu cầu VAULT

Cập nhật **2026-09-13**. Nguồn kịch bản: [Work-flow.txt](../VAULT_text/Work-flow.txt). Quyết định D-13 trong [PROJECT.md](PROJECT.md).

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

Nghiệm thu A trên `#/disclosures` (8/8). Nghiệm thu B trên `#/closings` (7/7, seed L3 xong). Không e2e 15 bước trong PR của A hoặc B.

## V1 vận hành (giữ để khỏi nhầm MVP)

V1-01 brief đủ field · V1-06 từ chối buyer giả / thiếu NDA / sai file · V1-07 chữ ký thật · V1-08 MFA + watermark · V1-10 playbook 6 trục đã chốt D-06. **P3b không đóng các mục này.**
