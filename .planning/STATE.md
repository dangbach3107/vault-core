# Hiện trạng VAULT

Cập nhật: **2026-10-20**.

## Cập nhật 2026-10-20 — case demo đầy đủ qua API (bước 5 kế hoạch tiếp)

- `python -m backend.demo_case --base <url>` (cần `DEMO_ROLE_PASSWORD`) dựng một deal hoàn chỉnh qua API công khai, từng bước bằng đúng vai trò: hồ sơ + phòng dữ liệu với 5 PDF nội dung khác nhau (ĐKDN, BCTC, kiến trúc, NDA, hợp đồng), duyệt dữ kiện có bằng chứng, nhu cầu mua, NDA, LOI, cấp quyền Lớp 2/3 theo file, Tech DD (2 finding, phản hồi, đóng, ký), đề nghị chính thức, ký rồi đóng với file chứng từ, 3 khoản phí (thu một phần / quá hạn / đã xuất hóa đơn), bàn giao.
- Mọi tên, tài liệu và nội dung PDF ghi "Dữ liệu minh họa"; không dùng nút "hoàn tất mẫu".
- `backend/tests/test_demo_case.py` chạy cả case rồi kiểm tra từng vai trò chỉ thấy phần của mình (Buyer không thấy phí/Tech DD, Buyer 2 không thấy deal, Buyer chỉ đọc 2 file được cấp ở chế độ chỉ xem, Finance chỉ thấy chứng từ ký/đóng).
- Xác minh: 69 test Python.

## Cập nhật 2026-10-20 — quốc gia, đơn vị tiền, kỳ tài chính (bước 4 kế hoạch tiếp)

- Hồ sơ có `country` (VN/JP/khác), `currency` (VND hoặc JPY, áp dụng cho mọi số tiền của hồ sơ), `expected_valuation` + `valuation_basis` (EV/Equity) tách khỏi doanh thu; vùng Bắc/Trung/Nam chỉ cho doanh nghiệp Việt Nam.
- Năm tài chính có `period_end` (ví dụ 2026-03-31 cho FY2025 Nhật); trường đổi tên `revenue_vnd/ebitda_vnd` → `revenue/ebitda`. Migration `0009` đổi dữ liệu cũ (gắn `currency: VND`) và đường dẫn duyệt dữ kiện; có downgrade.
- Dải doanh thu Lớp 1 theo đơn vị tiền (nhãn VND/JPY riêng, không quy đổi); Lớp 1 hiện quốc gia; Lớp 2 trả `currency`.
- Giao diện: chọn đơn vị tiền và ngày kết thúc kỳ trong form; tiền hiển thị kèm VND/JPY; bộ lọc quốc gia ở danh sách hồ sơ.
- Tiền trong deal (phí, LOI, ngân sách) vẫn là VND.
- Xác minh: 67 test Python, 25 test frontend, 9 test Chromium, tsc, eslint, OpenAPI, alembic check; dry-run `0009` lên/xuống với dữ liệu dạng cũ.

## Cập nhật 2026-10-20 — quy trình duyệt dữ kiện (bước 3 kế hoạch tiếp)

- Migration `0008` thêm bảng `fact_reviews`. Seller (chủ hồ sơ) hoặc Admin gửi duyệt từng dữ kiện (kể cả doanh thu/EBITDA theo năm) kèm nguồn, ngày nguồn và file bằng chứng trong phòng dữ liệu của chính doanh nghiệp (phiên bản cố định lúc gửi).
- Legal/Admin duyệt ở `#/reviews`: chấp thuận (đã đối chiếu chứng từ / bên thứ ba xác nhận) hoặc từ chối kèm lý do. Người gửi không tự duyệt; dữ kiện đổi sau khi gửi → 409, cần gửi lại.
- Không ai gắn nhãn xác minh bằng cách sửa hồ sơ nữa (kể cả Admin) — chỉ qua quyết định duyệt; `reviewed_by` là tài khoản người duyệt.
- Giao diện: tab "Nguồn & xác minh" có bảng gửi duyệt và lịch sử; trang "Duyệt dữ kiện" cho Legal/Admin; ô nhãn xác minh trong form hồ sơ bị khóa.
- Xác minh: 61 test Python, 24 test frontend, 8 test Chromium, tsc, eslint, OpenAPI, alembic check.

## Cập nhật 2026-10-20 — form nghiệp vụ (bước 2 kế hoạch tiếp)

- Nhu cầu mua, NDA, LOI sơ bộ, đề nghị chính thức, bàn giao có form riêng (schema `BuyerRequestForm`, `NdaForm`, `OfferForm`, `HandoffForm` trong `DealActionInput`); thiếu form hoặc gửi form sai bước → 422.
- NDA (số hiệu, các bên, ngày ký, hết hạn, file tùy chọn) là căn cứ Lớp 2; LOI sơ bộ là căn cứ Lớp 3; đề nghị chính thức là căn cứ tài liệu closing. Căn cứ hết hạn → 409; quyền không được kéo dài quá hạn căn cứ → 422; số hiệu căn cứ tự gắn vào quyền.
- LOI/đề nghị có giá (khoảng), cơ sở định giá EV/Equity, số ngày độc quyền, hạn hiệu lực.
- Giao diện: form theo bước trong "Việc của bạn", khối "Nội dung đã ghi nhận", hộp duyệt quyền hiện căn cứ và giới hạn ngày.
- Migration `0007` dựng lại deal minh họa theo form mới (chỉ deal `is_sample`).
- Xác minh: 60 test Python, 24 test frontend, 7 test Chromium, tsc, eslint, OpenAPI, alembic check.

## Cập nhật 2026-10-20 — vá quyền phòng dữ liệu (bước 1 kế hoạch tiếp)

- Tech DD: `/rooms` chỉ trả phòng của seller có deal đã mở phòng dữ liệu, chưa đóng, chưa dừng; phòng khác trả 404.
- Finance: đọc chứng từ closing theo deal (`/deals/<id>/closing-evidence`) — đúng file và phiên bản Legal/Admin đính kèm ở checklist điều kiện đóng, ký, đóng. File đính kèm phải thuộc phòng dữ liệu của seller trong deal (422 nếu không). Finance vẫn không vào phòng dữ liệu.
- Giao diện: ô chọn file chứng từ ở các bước đó; mục "Chứng từ ký và đóng" trong khối Finance; ẩn nút tạo/tải lên/xóa với vai trò chỉ đọc.
- Xác minh: 57 test Python, 22 test frontend, 6 test Chromium, tsc, eslint, OpenAPI.

## Cập nhật 2026-10-15 — sửa theo góp ý GUI/Tech 14/10

- Phạm vi có phiên bản: [SCOPE_BASELINE.md](SCOPE_BASELINE.md) v1.0.
- Gỡ Investor MVP (`#/investor-mvp`, fallback Vercel). Thẻ deal mở `#/deals/<id>` với phần việc theo vai trò.
- Deal có Buyer phụ trách; API chiếu dữ liệu tối thiểu theo vai trò; thao tác của Buyer/Seller kiểm tra đúng bên của deal.
- Quyền tài liệu theo file + phiên bản + căn cứ + xem/tải + hạn + thu hồi; Buyer đọc file qua deal; Teaser cần Seller duyệt; NDA/LOI chỉ là điều kiện.
- Tech DD: finding tách khỏi ký xác nhận. Finance: phí → hóa đơn → thanh toán, trạng thái quá hạn/một phần. Tách Ký và Đóng (`spaSigned`, `dealClosed`).
- Seller không tự gắn nhãn xác minh. Bỏ số xác minh giả (12/15), bỏ tuyên bố K-Anonymity/NĐ13, Lớp 3 = "Tài liệu hạn chế theo quyền", sửa câu xem trước Office.
- Định dạng tiền VND bằng chuỗi/BigInt; sửa tràn ngang mobile (390/768px), lịch sử phiên bản xuống dòng, hộp thoại có Esc/giữ focus.
- Xác minh: 55 test Python, 22 test frontend, 6 test Chromium (gồm kiểm tra không tràn ngang 390/768px), tsc, eslint, OpenAPI.
- Migration dữ liệu `0006` chỉnh deal cũ khi deploy: gán Buyer phụ trách (ưu tiên người đã gửi yêu cầu truy cập), deal hoàn tất bằng nút mẫu cũ được dựng lại thành dữ liệu minh họa có Ký/Đóng khớp nhau; deal khác giữ tiến độ. Trên production: Aurora → `buyer2` (minh họa), Bamboo → `buyer`.


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

## Cập nhật 2026-10-14 — vận hành bản public

- Migration `0005`: bảng `document_blobs`. Tài liệu tải lên lưu trong PostgreSQL cùng giao dịch với `document_versions` (không còn ghi đĩa); file cũ trên đĩa vẫn đọc được. Xóa tài liệu/phòng xóa luôn blob trong cùng giao dịch.
- Giới hạn đăng nhập sai (5 lần/15 phút mỗi tài khoản, 30 lần mỗi IP, HTTP 429, bộ đếm trong bộ nhớ) và header bảo mật qua middleware ASGI.
- Trang pháp lý `#/terms`, `#/privacy`, `#/contact` (nội dung ở `frontend/src/features/legal/`), trang 404 trong app.
- `scripts/backup-db.sh` sao lưu DB gồm cả tài liệu.
- Chưa làm: đăng nhập email riêng từng người (vẫn 7 tài khoản dùng chung `DEMO_ROLE_PASSWORD`), email liên hệ thật trong `siteInfo.ts`, CSP, tên miền riêng.
