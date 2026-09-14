# Hiện trạng VAULT

Cập nhật **2026-09-13**. Hai cụm **8 / 7** (Mở lớp 1–8 / VDR & đóng 9–15) — **chưa code**. Không commit/push.

## Đã có trong code

| Hạng mục | Thực tế | Giới hạn |
| --- | --- | --- |
| Hồ sơ / Trust Profile | CRUD, 3 nhãn, 3 tab xem trước | Không phải phát hành cho buyer |
| Phòng dữ liệu | 6 nhóm, upload, preview, version | Chưa grant / NDA / MFA |
| PostgreSQL | 0001–0002 | Chưa `introductions` / `engagements` |
| Work-flow | A = 1–8, B = 9–15 (giấy) | Chưa `#/disclosures` / `#/closings` |
| Design | SVG 01–13 cho hồ sơ/phòng | Chưa SVG tab persona |

## Kiểm thử (lần ghi nhận 2026-09-11)

Python 36; Vitest 8 (sau sửa selector UI); Playwright 3 (chưa chạy lại sau polish UI). OpenAPI mới có health / companies / rooms.

## Việc tiếp theo

Người dùng bảo A làm **Mở lớp** và/hoặc B làm **VDR & đóng** — song song. **Đừng code từ planning.**

Còn mở: D-02 / D-03 production; bốn tên field Buyer chính thức (A-07 tạm dùng); e2e chưa chạy lại.
