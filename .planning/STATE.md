# Hiện trạng VAULT

Cập nhật: **2026-10-08**.

## Cập nhật 2026-10-08 — P1 deal persistence

- Thêm migration `0003` và aggregate `deals` JSONB cho synthetic MVP.
- Thêm API list/create/get, action có gate, reset và complete-sample.
- Persist đủ 11 nhóm chức năng đã xác nhận, gồm bốn fee line.
- `#/investor-mvp` tải/tạo deal và lưu từng action qua backend; không còn chỉ là React state khi backend khả dụng.
- Đã thêm `#/deals` làm màn quản lý lead/deal thật: liệt kê nhiều deal, hiển thị mức hoàn thiện, VAULT Admin tạo deal và mở đúng workspace bằng `#/deals/{id}`. Đăng nhập local chuyển tới màn này thay vì tự chọn deal đầu tiên.
- Phòng dữ liệu local hỗ trợ xóa từng tài liệu (kèm mọi phiên bản/blob) và xóa cả phòng (kèm toàn bộ tài liệu/blob), có hộp xác nhận và phản hồi lỗi trên UI. Backend tests: 40 passed; riêng room tests: 15 passed (2026-10-08).
- Đây chưa phải production readiness: chưa có auth/RBAC/MFA, audit bảo mật, e-sign, antivirus hay external VDR.
- Đã áp dụng migration `0003` vào database local. Xác minh đạt: 40 test Python, 8 test frontend, frontend build/lint, OpenAPI check và generated API type check.
- `format:check` toàn frontend vẫn báo các file cũ chưa theo Prettier; các file thay đổi trong lượt này đã được format riêng, không rewrite hàng loạt file không liên quan.
- Thêm đăng nhập synthetic cho Buyer, Seller, VAULT Admin, Legal, Tech DD và Finance. Session ký HMAC hết hạn sau 8 giờ; mọi route database yêu cầu token và deal action kiểm tra role owner. Đây không phải Rikkei SSO/MFA production.
- Tinh chỉnh UI/UX theo tone đỏ rượu: Workflow A–Z là màn mặc định sau login, có directory 8 giai đoạn/11 nhóm chức năng, timeline/gate/sidebar theo role, navigation sticky và responsive desktop/mobile. Browser QA đã kiểm tra login, workflow và room download có auth.
- Đính chính D-20 theo phản hồi người dùng: 20 bước chỉ là mẫu tham chiếu, không phải chức năng chính. Tracker 20 bước đã được gỡ khỏi màn chính; bước tiếp theo là tách các action mẫu thành module nghiệp vụ có form và dữ liệu riêng.
- Bắt đầu D-21 controlled access theo tài liệu người dùng: Buyer có API tạo request L1/L2/L3/Closing với purpose/scope; Seller/Legal duyệt hoặc từ chối (approval bắt buộc expiry); Seller/Legal/VAULT Admin revoke; aggregate lưu grant theo person + deal và access event. UI role-specific và enforcement khi xem/tải tài liệu vẫn là bước kế tiếp.
- Sửa kiến trúc theo phản hồi D-22: gỡ Controlled Access khỏi `InvestorMvp.tsx`; thêm module độc lập `#/access`, module hub `#/vault` theo role; đăng nhập và logo đi tới hub; Deal List mở chức năng deal thay vì A–Z. A–Z chỉ còn liên kết demo riêng.
- Đính chính D-23: thay menu “Phân quyền” bằng `Disclosure approvals` (`#/disclosures`); navigation và route guard lọc theo role đăng nhập; backend giới hạn tạo lead/deal cho VAULT Admin. RBAC tài khoản và disclosure theo deal được tách thành hai khái niệm.
- RBAC backend được siết thêm: Company read dành cho Seller/VAULT Admin/Legal, Company mutation cho Seller/VAULT Admin; Room read dành cho Seller/VAULT Admin/Legal/Tech DD, Room mutation cho Seller/VAULT Admin. Buyer chưa được vào local room cho tới khi room–deal grant được enforce đúng scope.

## Đã có trong code

| Hạng mục | Thực tế | Giới hạn |
| --- | --- | --- |
| Hồ sơ / Trust Profile | CRUD, 3 nhãn, 3 tab xem trước | Không phải phát hành cho buyer |
| Phòng dữ liệu | 6 nhóm, upload, preview, version | Chưa grant / NDA / MFA |
| PostgreSQL | 0001–0002 | Chưa `introductions` / `engagements` |
| Work-flow | A = 1–8, B = 9–15 (giấy) | Chưa `#/disclosures` / `#/closings` |
| Design | SVG 01–13 cho hồ sơ/phòng | Chưa SVG tab persona |

## Kiểm thử (lần ghi nhận 2026-09-11)

| Hạng mục | Trạng thái |
| --- | --- |
| Backend deal persistence cho A–Z flow | Đã có ở mức synthetic MVP; chưa có auth/audit production |
| Auth/RBAC/Rikkei SSO | Chưa có |
| MFA thật | Chưa có |
| VDR production/object storage | Chưa có |
| Watermark/audit/antivirus production-grade | Chưa có |
| Real data readiness | Chưa đạt |

## Việc tiếp theo

Người dùng bảo A làm **Mở lớp** và/hoặc B làm **VDR & đóng** — song song. **Đừng code từ planning.**

Còn mở: D-02 / D-03 production; bốn tên field Buyer chính thức (A-07 tạm dùng); e2e chưa chạy lại.

## Cập nhật 2026-10-08 — seller data isolation

- Thêm ownership theo `owner_username` cho hồ sơ doanh nghiệp qua migration `0004`; dữ liệu cũ được gán cho `admin`.
- Seller chỉ thấy và thao tác hồ sơ/phòng dữ liệu thuộc chính tài khoản đó; truy cập chéo trả `404`.
- Bổ sung tài khoản synthetic `seller2` và kiểm thử truy cập chéo ở company, preview và room.
- Xác minh: 47 Python tests, 8 frontend tests, frontend build/lint, OpenAPI và generated API type check đều đạt.
