# Phạm vi cơ sở VAULT

| Phiên bản | Ngày | Thay đổi |
| --- | --- | --- |
| 1.0 | 2026-10-15 | Bản đầu, sau góp ý GUI/Tech ngày 14/10/2026 |
| 1.1 | 2026-10-20 | Tech DD chỉ thấy phòng dữ liệu của deal đang thẩm định; Finance đọc chứng từ closing theo deal |
| 1.2 | 2026-10-20 | Form riêng cho nhu cầu mua, NDA, LOI, đề nghị chính thức, bàn giao; NDA/LOI giới hạn thời hạn quyền |
| 1.3 | 2026-10-20 | Quy trình duyệt dữ kiện: gửi duyệt kèm bằng chứng, Legal/Admin quyết định, người gửi không tự duyệt |

Tài liệu này nói rõ cái gì đã chạy được, cái gì chỉ ghi nhận, cái gì chưa làm. Khi phạm vi đổi, tăng phiên bản và ghi một dòng vào bảng trên.

## Giai đoạn 1 — Mua bán, chuyển nhượng (M&A)

### Đã có chức năng thật (lưu PostgreSQL, kiểm tra quyền ở backend)

| Hạng mục | Nội dung |
| --- | --- |
| Đăng nhập theo vai trò | 8 tài khoản tổng hợp (2 Buyer, 2 Seller, Admin, Legal, Tech DD, Finance). Không phải SSO/MFA. |
| Gán bên tham gia | Admin tạo deal, chọn hồ sơ seller và Buyer phụ trách. Buyer/Seller khác không thấy deal. |
| Dữ liệu tối thiểu theo vai trò | API chỉ trả phần dữ liệu vai trò đó cần (xem README). |
| Trust Profile | Dữ kiện có nhãn tự khai / đã đối chiếu / bên thứ ba xác nhận. Nhãn xác minh chỉ gắn qua yêu cầu duyệt (nguồn, ngày nguồn, file bằng chứng) do Legal/Admin khác người gửi quyết định; có lịch sử chấp thuận/từ chối. Số dữ kiện xác minh hiển thị đúng thực tế, 0 là 0. |
| Teaser (Lớp 1) | Buyer chỉ xem sau khi Seller duyệt Teaser trong deal. |
| Lớp 2, Lớp 3 | Mở khi có căn cứ (NDA cho Lớp 2, LOI sơ bộ cho Lớp 3) và Seller/Legal cấp quyền còn hiệu lực. Lớp 3 là "Tài liệu hạn chế theo quyền", không phải "đầy đủ". |
| Quyền tài liệu | Theo người, deal, từng file và phiên bản, căn cứ, xem hoặc tải, ngày hết hạn, thu hồi. Phiên bản mới không tự mở cho Buyer. Có nhật ký xem/tải. |
| Phòng dữ liệu | Thư mục, phiên bản, xem trước PDF/ảnh/văn bản. Word/Excel chỉ tải về. |
| Tech DD | Finding (mức độ, mô tả, khắc phục, ảnh hưởng), Seller phản hồi, Tech DD đóng hoặc chấp nhận rủi ro; ký xác nhận riêng, bị chặn khi còn finding mở. |
| Finance | Khoản phí → hóa đơn → từng lần thanh toán; tự tính chưa xuất hóa đơn / đã xuất / thanh toán một phần / đủ / quá hạn. Phí thành công chỉ sau Closing. |
| Ký và đóng | Hai bước riêng: Ký hợp đồng (Legal) và Đóng giao dịch (Admin, cần checklist điều kiện đóng). |
| Phạm vi phòng dữ liệu | Tech DD chỉ thấy phòng của seller trong deal đã mở phòng dữ liệu, chưa đóng/dừng. Finance chỉ đọc file chứng từ được đính kèm ở checklist điều kiện đóng, ký, đóng. |
| Quy trình 20 bước | Mỗi bước có người phụ trách, ghi chú, quyết định tiếp tục/dừng. |

### Có form nghiệp vụ riêng

Nhu cầu mua (năng lực, ngân sách, thời gian, mục tiêu), NDA (số hiệu, các bên, ngày ký, hết hạn, file), LOI sơ bộ và đề nghị chính thức (giá, cơ sở định giá EV/Equity, độc quyền, hạn hiệu lực, điều kiện), bàn giao (bên nhận, ngày, danh mục). NDA/LOI là căn cứ cấp quyền; quyền không vượt hạn căn cứ.

### Chỉ ghi nhận (ghi chú + người + thời gian)

Xác nhận hồ sơ Seller, ghép Buyer–Seller, đề nghị biết danh tính, các phê duyệt của Legal (Lớp 3, chuyển dữ liệu ra nước ngoài, không giữ tiền), checklist điều kiện đóng, ký và đóng (có đính kèm file chứng từ).

### Chưa làm

- Quốc gia/đơn vị tiền tệ (JPY), kỳ tài chính cho hồ sơ doanh nghiệp. (EV/Equity đã có trong LOI/đề nghị.)
- Ký điện tử, quét virus, watermark, VDR bên ngoài, chặn chụp màn hình. "Chỉ xem" nghĩa là ứng dụng không cấp nút tải; không ngăn được người xem tự lưu.
- Đăng nhập thật (SSO/MFA), quản lý tài khoản.
- Kiểm tra nguy cơ nhận diện Teaser tự động. Teaser vẫn cần người duyệt đọc trước khi chia sẻ.
- Không tuyên bố tuân thủ K-Anonymity hay Nghị định 13/2023; chưa có đánh giá pháp lý cho việc đó.

## Giai đoạn 2 — Gọi vốn (chưa triển khai)

Vòng gọi vốn, bảng cơ cấu cổ đông (cap table), nhà đầu tư theo vòng: **chưa triển khai** (Book B khóa). Giao diện và tài liệu giới thiệu phải ghi rõ điều này.

## Dữ liệu minh họa

Nút "Nạp dữ liệu minh họa" gắn cờ `is_sample`; mọi ghi chú trong đó có chữ "Dữ liệu minh họa". Không dùng làm bằng chứng nghiệm thu.
