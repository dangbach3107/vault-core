# Cập nhật UI — branch `bach-ui`

Dựa trên `DucNT` (commit `df49a11`). Chỉ sửa frontend, không đụng backend/API/DB.

## Vấn đề

`workspace.css` (~2.200 dòng) có nhiều lớp theme ghi đè lẫn nhau. Hậu quả: banner xanh lá giữa theme đỏ, nút hai kiểu khác nhau, nội dung dính sát sidebar. `styles.css` còn lỗi cú pháp (thiếu `}`, thuộc tính khai báo trùng), nên font Be Vietnam Pro không được áp dụng.

## Thay đổi

- **Một design system duy nhất:** viết lại `frontend/src/styles.css` theo token (màu, khoảng cách, bo góc). Xóa `workspace.css`. Giữ nguyên tên class nên logic React không đổi.
- **Khung trang:**
  - Một thanh trên cùng có breadcrumb và nhãn "Demo nội bộ".
  - Mỗi trang chỉ một tiêu đề chính.
  - Nút đăng xuất nằm ở chân sidebar.
  - Trang đăng nhập riêng, không kèm sidebar.
- **Chi tiết UI:**
  - Icon SVG thay ký tự unicode.
  - Bảng có header cố định.
  - Tab dạng segmented control.
  - Hộp thoại xác nhận có nút xóa màu đỏ.
  - Focus ring rõ khi dùng bàn phím.
  - Responsive mobile.
- **Màn A–Z cũ** (`#/investor-mvp`): CSS riêng tách sang `features/investor-mvp/investor-mvp.css`.
- **Tiêu đề trùng:** các `h1` lặp trong trang (Tổng quan, Deals, Disclosure, Tài liệu) đổi thành `h2`.

Giữ tone đỏ rượu. Tham khảo bộ quy tắc của skill ui-ux-pro-max.

## Đã kiểm tra

- `npm run build`, `eslint` và `vitest` (8/8) đạt.
- Đã xem từng màn: đăng nhập, tổng quan, deals, doanh nghiệp, phòng dữ liệu, disclosure (admin/buyer), mobile 390px.
- **Chưa chạy** e2e Playwright: config hiện chỉ chạy trên Windows.
