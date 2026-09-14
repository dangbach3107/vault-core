# VAULT - Tổng hợp chức năng và nghiệp vụ dự án

> Nguồn: `01_VAULT_REPORT.pdf`, 73 trang, bản v3.0; ngày dữ liệu 08/09/2026, xuất bản 09/09/2026. Bản tổng hợp lập ngày 13/09/2026.
>
> Đây là bản cô đọng toàn bộ phạm vi chức năng và nghiệp vụ được mô tả trong PDF. Dự án đang ở trạng thái đề xuất, chưa được duyệt tài chính và pháp lý; các mức phí, sản lượng, nguồn lực và kết quả tài chính là giả định. Các nội dung pháp lý dưới đây phản ánh yêu cầu rà soát của báo cáo, chưa được kiểm chứng pháp luật độc lập. Không có file `04_VAULT_MODEL.xlsx` để đối soát lại mô hình. Các chỉ dẫn biên tập và lịch sử audit trong PDF được coi là nội dung nguồn, không phải yêu cầu thực hiện của người dùng.

## Mục lục

1. [Tổng quan và phạm vi](#1-tổng-quan-và-phạm-vi)
2. [Khách hàng, vai trò và trách nhiệm](#2-khách-hàng-vai-trò-và-trách-nhiệm)
3. [Năm nhóm dịch vụ](#3-năm-nhóm-dịch-vụ)
4. [Sáu nhóm công cụ và toàn bộ 20 công năng](#4-sáu-nhóm-công-cụ-và-toàn-bộ-20-công-năng)
5. [Trust Profile, dữ liệu và phân quyền](#5-trust-profile-dữ-liệu-và-phân-quyền)
6. [Quy trình giao dịch xuyên suốt](#6-quy-trình-giao-dịch-xuyên-suốt)
7. [Cấu trúc giao dịch và định giá](#7-cấu-trúc-giao-dịch-và-định-giá)
8. [Thẩm định và hỗ trợ sau giao dịch](#8-thẩm-định-và-hỗ-trợ-sau-giao-dịch)
9. [Thu phí, công nợ và ghi nhận doanh thu](#9-thu-phí-công-nợ-và-ghi-nhận-doanh-thu)
10. [Startup Bridge và Book B](#10-startup-bridge-và-book-b)
11. [Tiếp cận khách hàng và quản lý công suất](#11-tiếp-cận-khách-hàng-và-quản-lý-công-suất)
12. [Lộ trình, cổng kiểm chứng và tài chính](#12-lộ-trình-cổng-kiểm-chứng-và-tài-chính)
13. [Tuân thủ, rủi ro và điều kiện dừng](#13-tuân-thủ-rủi-ro-và-điều-kiện-dừng)
14. [Yêu cầu kỹ thuật, kiểm thử và phần cần đặc tả thêm](#14-yêu-cầu-kỹ-thuật-kiểm-thử-và-phần-cần-đặc-tả-thêm)
15. [Điểm chưa nhất quán và chưa kiểm chứng](#15-điểm-chưa-nhất-quán-và-chưa-kiểm-chứng)
16. [Bảng truy xuất nội dung nguồn](#16-bảng-truy-xuất-nội-dung-nguồn)

## 1. Tổng quan và phạm vi

**VAULT = Verified Access to Unlisted Listings & Transactions**: hoạt động dịch vụ kết hợp nền tảng dữ liệu để kết nối vốn và hỗ trợ giao dịch doanh nghiệp chưa niêm yết tại Việt Nam, bắt đầu từ bên mua Nhật Bản, đặt trong hệ sinh thái Rikkei.

Giá trị cốt lõi là chuẩn hóa hồ sơ có bằng chứng, bảo vệ thông tin bán vốn, xác định nhu cầu mua thực tế, ghép đối tác có lý do, điều phối thẩm định và đàm phán, rồi chuyển tiếp sang hỗ trợ sau đầu tư nếu khách hàng có nhu cầu.

### 1.1. Bài toán và khách hàng trọng tâm

- Bên bán Việt Nam cần vốn tăng trưởng, đối tác chiến lược, chuyển giao thế hệ hoặc thoái vốn; hồ sơ tài chính, pháp lý và công nghệ có thể chưa đủ chuẩn để bên mua nước ngoài đánh giá.
- Bên mua Nhật cần năng lực sản xuất, công nghệ, nhà cung ứng, khách hàng hoặc thị trường, nhưng thiếu thông tin đáng tin cậy và khả năng đánh giá doanh nghiệp mục tiêu.
- Phân khúc trọng tâm được báo cáo nhấn mạnh là **giá trị doanh nghiệp 200-500 tỷ đồng**; nhận chọn lọc nhóm 50-200 tỷ khi có lý do phù hợp. Một số bảng dùng dải 100-300 tỷ để minh họa giao dịch cỡ vừa; cần chốt lại khi lập tiêu chí tuyển chọn.
- Hướng phù hợp gồm doanh nghiệp có tài sản công nghệ, phần mềm B2B, giải pháp phục vụ sản xuất, tự động hóa và chuỗi cung ứng. Báo cáo chưa chốt một danh sách ngành đủ chi tiết để áp dụng máy móc.
- Doanh nghiệp được xếp loại vừa theo tiêu chí hành chính không tự động thuộc phân khúc giá trị mục tiêu; thiếu nợ vay cũng không chứng minh nhu cầu bán vốn.

Theo số liệu được dẫn trong báo cáo, M&A Việt Nam năm 2025 có 367 thương vụ, giá trị công bố khoảng 8,715 tỷ USD; phía Nhật có 22 thương vụ và 461,6 triệu USD. Nửa đầu 2026 có 9 thương vụ Nhật - Việt theo một nguồn khác. Đây là bối cảnh để kiểm tra mức tham vọng, không phải số khách hàng VAULT có thể phục vụ. Quan hệ công khai của Rikkei và ý định mở rộng của doanh nghiệp Nhật chưa phải bằng chứng có nhu cầu mua vốn hay trả phí.

### 1.2. Phân biệt giai đoạn với Book

| Cách phân loại | Phạm vi | Trạng thái theo đề xuất |
|---|---|---|
| Giai đoạn 1 | Giao dịch vốn chiến lược giữa doanh nghiệp Việt Nam và bên mua xác định, trước hết là Nhật Bản | Trọng tâm khởi động |
| Giai đoạn 2 | Bổ sung startup gọi vốn, quản lý vòng vốn và quan hệ nhà đầu tư; xem xét nhánh huy động rộng có điều kiện riêng | Chưa hợp nhất vào vận hành giai đoạn 1 |
| Book A | Giao dịch vốn giữa các bên xác định, gồm cả startup gọi vốn với quỹ ở giai đoạn 2 | Cơ chế giao dịch trực tiếp, không cam kết lợi suất |
| Book B | Huy động rộng hơn kèm cam kết chi trả cổ tức/mua lại | Nghiên cứu, đang khóa, doanh thu bằng 0 |

**Book A không đồng nghĩa riêng giai đoạn 1; Book B không đồng nghĩa toàn bộ giai đoạn 2.** Một khách hàng có thể chỉ sử dụng Book A.

## 2. Khách hàng, vai trò và trách nhiệm

Nguồn: mục 3.3, 3.6, 4.1 và sơ đồ S03, trang 24, 27, 31-32.

| Chủ thể/vai trò | Trách nhiệm nghiệp vụ |
|---|---|
| Bên bán/cổ đông hiện hữu | Cung cấp thông tin, chứng minh quyền sở hữu và đại diện, xác định mục tiêu thoái vốn, ký hợp đồng, duyệt hồ sơ và việc chia sẻ |
| Doanh nghiệp nhận vốn/ban điều hành | Xây kế hoạch tăng trưởng, sử dụng vốn, cung cấp dữ liệu và tham gia thẩm định; phối hợp cổ đông có quyền quyết định |
| Bên mua Nhật/nhà đầu tư/quỹ | Cung cấp tiêu chí mua, ngân sách, người quyết định và lịch; ký NDA, yêu cầu truy cập, hỏi đáp, thẩm định, đàm phán |
| Điều phối giao dịch | Chủ trì hồ sơ từ đầu mối đến hoàn tất; điều phối các bên và theo dõi đầu ra mỗi bước |
| Phân tích và định giá | Chuẩn hóa dữ kiện, lập mô hình, cấu trúc vốn, bảng sở hữu và tài liệu đàm phán |
| Đầu mối Nhật Bản | Tiếp cận bên mua, xác nhận nhu cầu, dịch và theo dõi quá trình phê duyệt phía Nhật |
| Thẩm định công nghệ | Kiểm tra kiến trúc, mã nguồn, bảo mật, nhân sự, chi phí khắc phục và tích hợp |
| Pháp lý và tuân thủ | Rà điều kiện giao dịch, hợp đồng, dữ liệu, xung đột lợi ích; cấp quyền phòng dữ liệu theo quy trình |
| Tài chính và kiểm soát | Phí, hóa đơn, công nợ, dòng tiền, ngân sách, kiểm tra ghi nhận doanh thu |
| Chuyên gia bên ngoài | Luật sư, kiểm toán, thuế, chuyên gia ngành; ký và chịu trách nhiệm theo từng phạm vi chuyên môn |
| Khối triển khai Rikkei | Ký hợp đồng riêng cho thẩm định công nghệ/triển khai thuộc phạm vi của mình, tích hợp hệ thống và chuyển đổi số |
| Rikkeisoft, người bảo trợ và hội đồng | Cấp thương hiệu, quan hệ, vốn, người; duyệt cổng, hạn mức, quyền ký và quyết định tiếp tục/dừng |

Sáu bộ phận vận hành là điều phối, phân tích, đầu mối Nhật, thẩm định công nghệ, pháp lý, tài chính. Mỗi vai trò phải có người cụ thể, số giờ cam kết theo tháng và người dự phòng.

Các nguyên tắc phân tách trách nhiệm:

- Người đàm phán và người/cơ quan có quyền phê duyệt phải được ghi thành hai thông tin riêng ở cả hai phía.
- Người điều phối giao dịch không đồng thời quyết định kết luận thẩm định công nghệ của cùng hồ sơ.
- Người bán hồ sơ không tự cấp quyền phòng dữ liệu; quyền do pháp lý và tuân thủ xử lý, có phê duyệt hai người khi cấp mới.
- Người thẩm định tách khỏi người bán dịch vụ khắc phục; khách hàng có quyền chọn nhà cung cấp khác.
- VAULT là tên sản phẩm; đơn vị vận hành có thể là bộ phận nội bộ hoặc pháp nhân riêng. Bên ký hợp đồng, nhận phí và chịu trách nhiệm dữ liệu cần được xác định trước khi vận hành.

## 3. Năm nhóm dịch vụ

Nguồn: mục 3.1, trang 22-23.

| Dịch vụ | Phạm vi nghiệp vụ | Người trả tiền | Phạm vi triển khai |
|---|---|---|---|
| Giao dịch vốn chiến lược - Book A | Chuẩn hóa bên bán, xác định bên mua, ghép đối tác, điều phối thẩm định, đàm phán và hoàn tất | Bên bán trả gói chuẩn bị; bên ký ủy nhiệm trả phí thành công | Giai đoạn 1 |
| Startup Bridge | Hồ sơ gọi vốn, data pack, đối chiếu với quỹ, quản lý vòng vốn | Startup theo hợp đồng | Giai đoạn 2, kinh tế riêng |
| Distribution & Licensing | Kết nối phân phối/cấp phép khi chưa cần mua vốn; có thể là bước trước giao dịch vốn | Doanh nghiệp hoặc đối tác thương mại | Mở rộng, chưa dự phóng doanh thu |
| Deal Creation Studio | Tìm mục tiêu và chuẩn bị năng lực theo đơn đặt hàng của bên mua Nhật; phạm vi và nghiệm thu riêng | Bên mua | Mở rộng, chưa dự phóng doanh thu |
| Roll-up Studio | Tìm nhiều mục tiêu và hỗ trợ hợp nhất khi bên mua đã có chiến lược, vốn và năng lực tích hợp | Nhà mua hoặc bên tài trợ vốn | Tầm nhìn, chưa dự phóng doanh thu |

## 4. Sáu nhóm công cụ và toàn bộ 20 công năng

Nguồn: mục 3.2 và Phụ lục C, trang 23-24, 61-62. Sáu nhóm là các lớp công việc hỗ trợ dịch vụ, không phải sáu sản phẩm phần mềm độc lập.

### 4.1. Nhóm 1 - Hồ sơ doanh nghiệp và Trust Profile

| Mã | Công năng | Đầu vào | Xử lý và đầu ra | Cách triển khai được nêu |
|---|---|---|---|---|
| F01 | Hồ sơ pháp nhân và quyền đại diện | Đăng ký kinh doanh, điều lệ, biên bản họp, sổ cổ đông | Làm rõ chuỗi sở hữu tới cá nhân và danh sách người có quyền ký/quyết định bán | Biểu mẫu kiểm tra trường bắt buộc, tài liệu có phiên bản; không cần phần mềm riêng |
| F02 | Hồ sơ bằng chứng và trạng thái kiểm tra | BCTC, hợp đồng khách hàng, tờ khai thuế, hồ sơ nhân sự | Gắn từng dữ kiện với nguồn, ngày/kỳ và trạng thái: khách hàng khai, đã đối chiếu tài liệu, đã kiểm toán | Tái sử dụng nền tảng nội bộ, bổ sung lớp trạng thái kiểm tra |
| F03 | Sàng lọc mục tiêu bán vốn | Ngành, doanh thu, cơ cấu sở hữu, mục tiêu giao dịch | Kết luận đủ/không đủ điều kiện, kèm mã lý do | Bảng tiêu chí có trọng số; ban đầu xử lý thủ công |
| F04 | Chuẩn hóa hồ sơ và bản giới thiệu | Dữ kiện từ F01 và F02 | Bản giới thiệu ẩn danh và hồ sơ định danh song ngữ Việt - Nhật | Mẫu tài liệu chuẩn, công cụ dịch có người kiểm tra |

### 4.2. Nhóm 2 - Danh mục cơ hội và ghép đối tác

| Mã | Công năng | Đầu vào | Xử lý và đầu ra | Cách triển khai được nêu |
|---|---|---|---|---|
| F05 | Hồ sơ nhu cầu bên mua | Trao đổi trực tiếp với đơn vị kinh doanh phía mua | Yêu cầu mua đủ sáu thông tin bắt buộc; thiếu một thông tin thì chưa được tính là yêu cầu mua đạt chuẩn | Biểu mẫu bắt buộc, xác nhận nhu cầu thực tế |
| F06 | Ghép nối có lý do lựa chọn | Hồ sơ bên bán và yêu cầu mua | Danh sách ngắn, giải thích mức phù hợp theo từng tiêu chí; tránh phát tán hàng loạt | Bảng so khớp, chưa cần thuật toán |
| F07 | Duyệt tiếp cận hai phía | Bên mua yêu cầu mở danh tính | Chấp thuận bằng văn bản của bên bán, có thời điểm; chỉ mở khi hai phía đã đồng ý theo quy trình | Phê duyệt lưu vết, tích hợp phòng dữ liệu |

Sáu thông tin bắt buộc của F05:

1. Bên mua thiếu năng lực gì.
2. Kết quả muốn đạt trong hai năm sau khi mua.
3. Loại hồ sơ có thể xem xét.
4. Người/cấp ký quyết định.
5. Dải ngân sách dự kiến.
6. Khoảng thời gian muốn hoàn tất.

Tiêu chí so khớp còn phải thể hiện ngành, quy mô vốn, tỷ lệ sở hữu mong muốn, năng lực cần có và địa bàn khi phù hợp. Cuộc gặp hoặc sự quan tâm chung không được đếm thành yêu cầu mua đủ điều kiện.

### 4.3. Nhóm 3 - NDA, phòng dữ liệu và tiến độ

| Mã | Công năng | Đầu vào | Xử lý và đầu ra | Cách triển khai được nêu |
|---|---|---|---|---|
| F08 | Thỏa thuận bảo mật và phòng dữ liệu | Tài liệu theo ba lớp thông tin | Quản lý NDA, quyền xem/tải riêng, thời hạn, thu hồi, phiên bản và nhật ký truy cập | Mua sản phẩm thương mại; bắt buộc có nhật ký và thủy vân |
| F09 | Hỏi đáp và theo dõi tiến độ | Câu hỏi/vấn đề phát sinh trong thẩm định | Mỗi vấn đề có trạng thái, người phụ trách, hạn trả lời và lịch sử xử lý | Công cụ quản lý công việc thông thường |

### 4.4. Nhóm 4 - Thẩm định và mạng lưới chuyên môn

| Mã | Công năng | Đầu vào | Xử lý và đầu ra | Cách triển khai được nêu |
|---|---|---|---|---|
| F10 | Thẩm định công nghệ | Mã nguồn, kiến trúc, nhân sự kỹ thuật, hợp đồng thư viện | Báo cáo sáu hạng mục, rủi ro và chi phí khắc phục/tích hợp | Chuẩn hóa phương pháp và báo cáo; dùng công cụ quét mã có sẵn |
| F11 | Điều phối pháp lý, tài chính và thuế | Phạm vi đã ký với từng đơn vị chuyên môn | Theo dõi hạn bàn giao, tổng hợp bộ báo cáo thẩm định và tóm tắt cho hội đồng | Danh sách đối tác đã thẩm định, hợp đồng khung |

### 4.5. Nhóm 5 - Tài chính, giao dịch và mở rộng

| Mã | Công năng | Đầu vào | Xử lý và đầu ra | Phạm vi/cách triển khai |
|---|---|---|---|---|
| F12 | Theo dõi phí, hóa đơn và công nợ | Điều khoản phí của từng hợp đồng | Phí theo hồ sơ, mốc ghi nhận, xuất hóa đơn, thu tiền và dư nợ | Bảng tính ban đầu; số hóa khi vượt vài chục hồ sơ |
| F13 | Hỗ trợ sau giao dịch | Kết quả thẩm định, kế hoạch tích hợp | Bàn giao sang khối triển khai; hợp đồng riêng và thông tin nguồn giới thiệu | Quy tắc ghi nhận doanh thu, không cần công cụ mới |
| F14 | Phân phối và cấp phép | Nhu cầu thương mại hai phía | Hợp đồng phân phối hoặc cấp phép | Ngoài giai đoạn 1 |
| F15 | Nâng cấp doanh nghiệp trước giao dịch | Vấn đề có thể khắc phục từ sàng lọc | Chương trình khắc phục có mốc và chi phí, đưa doanh nghiệp về trạng thái sẵn sàng đầu tư | Ngoài giai đoạn 1 |
| F16 | Startup gọi vốn quỹ | Tăng trưởng, kinh tế đơn vị, cơ cấu sở hữu | Data pack và bảng mức phù hợp với từng quỹ | Giai đoạn 2 |
| F17 | Gọi vốn công chúng | Điều kiện tổ chức phát hành | Hồ sơ chào bán theo kênh được pháp lý xác nhận | Đang khóa; phụ thuộc mục 7.3 của PDF |
| F18 | Theo dõi nghĩa vụ mua lại | Cam kết chi trả và dòng tiền tổ chức phát hành | Lịch nghĩa vụ, nguồn trả, thiếu hụt và cảnh báo | Đang khóa; phụ thuộc thiết kế Book B |
| F19 | Hợp nhất nhiều doanh nghiệp | Luận điểm hợp nhất của bên mua | Danh sách mục tiêu theo thứ tự và kế hoạch tích hợp | Tầm nhìn |

Ngoài các tên công năng trên, nhóm 5 còn bao gồm mô hình cấu trúc vốn, tỷ lệ sở hữu trước/sau, bảng điều kiện hoàn tất và bộ số dùng chung cho đàm phán.

### 4.6. Nhóm 6 - Trợ lý AI

| Mã | Công năng | Đầu vào | Xử lý và đầu ra | Cách triển khai được nêu |
|---|---|---|---|---|
| F20 | Trợ lý phân tích và trí tuệ nhân tạo | Tài liệu trong phòng dữ liệu | Bản dịch nháp, tóm tắt tài liệu, danh sách dữ kiện thiếu | Dùng công cụ sẵn có, không xây mô hình riêng; mọi kết quả phải được người có trách nhiệm kiểm tra |

AI hỗ trợ công việc lặp lại. Kết quả không được dùng trực tiếp làm kết luận thẩm định, định giá hoặc tư vấn khi chưa được chuyên gia duyệt.

## 5. Trust Profile, dữ liệu và phân quyền

Nguồn: mục 3.3, 6.3, 7.4 và Phụ lục C, trang 24, 49, 52-53, 61.

### 5.1. Ba lớp thông tin

| Lớp | Thông tin | Người được xem | Điều kiện mở |
|---|---|---|---|
| 1 - Ẩn danh | Ngành, tỉnh/thành, dải doanh thu, dải nhân sự, loại khách hàng, mục tiêu giao dịch, dải tỷ lệ muốn bán | Bên mua đăng ký và đã được VAULT xác minh danh tính | Bên bán duyệt một lần khi lập hồ sơ |
| 2 - Định danh có kiểm soát | Tên doanh nghiệp, sản phẩm cụ thể, cơ cấu sở hữu, tài chính tóm tắt ba năm, khách hàng theo nhóm | Bên mua đã ký NDA và được bên bán chấp thuận riêng | Duyệt từng bên mua; ghi ai được mở và thời điểm mở |
| 3 - Nhạy cảm | Hợp đồng khách hàng, bảng lương, mã nguồn, kiến trúc, thuế, tranh chấp | Bên mua đã xác nhận nhu cầu và vào thẩm định chính thức | Bên bán duyệt từng tài liệu; giới hạn thời gian, tự thu hồi khi hết hạn |

Quyền xem và tải là hai quyền riêng. Thu hồi quyền chỉ ngăn truy cập tiếp, không xóa được bản đã tải/chụp màn hình. Tài liệu lớp 3 chỉ được mở ở mức cần thiết và có thủy vân theo người xem. Lịch sử audit còn nêu nhu cầu kiểm tra khả năng nhận diện lại doanh nghiệp từ teaser quá cụ thể; đây là điểm cần đưa vào đặc tả trước khi phát hành hồ sơ.

### 5.2. Kiểm chứng theo từng dữ kiện

- Mỗi dữ kiện cần nguồn, ngày/kỳ dữ liệu, trạng thái kiểm tra và bằng chứng đối chiếu.
- Ba trạng thái là **khách hàng khai**, **đã đối chiếu tài liệu**, **đã kiểm toán**.
- Nhãn đã kiểm toán chỉ áp dụng đúng dữ kiện thuộc phạm vi báo cáo kiểm toán, kèm đơn vị, kỳ và loại ý kiến; không gắn cho toàn hồ sơ.
- Không gom Trust Profile thành một điểm tín nhiệm tổng hợp khiến người đọc hiểu nhầm là bảo đảm chất lượng đầu tư.
- Dữ kiện mâu thuẫn hoặc hết hạn phải có quy trình xử lý; PDF chưa chốt chi tiết vòng đời trạng thái và thời hạn hiệu lực.

### 5.3. Quản trị toàn vòng đời dữ liệu

| Công đoạn | Yêu cầu nghiệp vụ/kỹ thuật |
|---|---|
| Thu thập | Ghi nguồn từng trường; xác định căn cứ xử lý và mục đích được đồng ý |
| Lưu trữ | Mã hóa khi lưu và truyền; xác định nơi lưu, bên vận hành, hợp đồng bảo mật hạ tầng |
| Chia sẻ | Phân quyền theo lớp và vai trò; xác thực nhiều lớp cho tài khoản xem lớp 2/3; hai người duyệt quyền mới; nhật ký đầy đủ, xuất được |
| Truy cập từ nước ngoài | Kiểm tra điều kiện chuyển dữ liệu trước khi cho bên mua Nhật truy cập |
| Lưu giữ và xóa | Thời hạn trong hợp đồng; quy trình xóa có xác nhận và xử lý yêu cầu xóa |
| Sự cố | Người chịu trách nhiệm, hạn báo cáo, danh sách liên hệ, mẫu thông báo được duyệt |
| Nhà cung cấp | Danh mục bên thứ ba tiếp cận dữ liệu, hợp đồng xử lý dữ liệu và rà định kỳ |
| Tái sử dụng | Chỉ dùng trong phạm vi quyền đã cấp; không mang hồ sơ riêng, khách hàng, giá mua, nhân sự sang giao dịch khác; dữ liệu tổng hợp phải không nhận ra doanh nghiệp cụ thể |

Vai trò bên kiểm soát/bên xử lý dữ liệu, hồ sơ đánh giá tác động và thời hạn thực hiện cần pháp chế xác nhận trên hệ thống thật.

## 6. Quy trình giao dịch xuyên suốt

Nguồn: mục 3.5, sơ đồ S01, mục 6.1, trang 25-26, 46-47. Bảng dưới tổ chức lại luồng mô tả trong phần văn bản; thứ tự ký ủy nhiệm và chuẩn hóa trong sơ đồ chưa hoàn toàn khớp, được ghi tại mục 15.

| Bước | Công việc | Đầu ra/điều kiện chuyển bước |
|---|---|---|
| 1. Xác nhận phía mua | Thu đủ sáu thông tin F05, làm rõ người đàm phán, cấp phê duyệt và lịch nội bộ | Yêu cầu mua đủ chuẩn; có căn cứ đi tìm mục tiêu |
| 2. Tạo và sàng lọc đầu mối bán | Thu thập dữ liệu hợp lệ; rà ngành, quy mô, sở hữu, thẩm quyền, mục tiêu | Hồ sơ đủ điều kiện hoặc bị loại có mã lý do |
| 3. Ký và chốt phạm vi dịch vụ | Thống nhất gói chuẩn bị/ủy nhiệm, phí, thời hạn, nghiệm thu, giới thiệu, hoàn phí và quyền dữ liệu | Hợp đồng/phạm vi được ký; thu tạm ứng theo hợp đồng |
| 4. Chuẩn hóa phía bán | F01-F04; rà tài liệu bên bán cấp, dựng hồ sơ ẩn danh và định danh | Bên bán duyệt hồ sơ bằng văn bản; bàn giao và nghiệm thu gói |
| 5. Ghép và giới thiệu | So khớp hồ sơ với yêu cầu mua; lập danh sách ngắn có lý do; xin chấp thuận | Hai phía đồng ý tiếp cận theo cơ chế phân lớp |
| 6. NDA và cấp quyền | Ký bảo mật, phê duyệt lớp 2/3 và từng tài liệu theo điều kiện | Người được phép có quyền đúng lớp, đúng hạn và nhật ký |
| 7. Thẩm định chính thức | Công nghệ, pháp lý, tài chính, thuế; quản lý hỏi đáp, hạn và người phụ trách | Bộ báo cáo, vấn đề cần xử lý và ảnh hưởng tới giao dịch |
| 8. Đàm phán và phê duyệt | Cấu trúc vốn, giá, quyền quản trị, điều kiện hoàn tất; phê duyệt nội bộ hai bên | Điều khoản được các cấp có thẩm quyền chấp thuận |
| 9. Hoàn tất | Kiểm tra điều kiện, thủ tục, thanh toán/chuyển quyền qua các bên có chức năng | Bằng chứng hoàn tất và điều kiện phát sinh phí thành công |
| 10. Đối soát và thu phí | Xác định cơ sở phí, phần chia đối tác, hóa đơn, công nợ, thực thu | Bảng đối soát theo hợp đồng; không nhận giữ tiền giao dịch của khách hàng |
| 11. Sau giao dịch | Bàn giao kế hoạch tích hợp, theo dõi hợp đồng triển khai riêng nếu phát sinh | Chuyển tiếp sang Rikkei; ghi nhận đúng pháp nhân; xử lý quyền truy cập và lưu giữ dữ liệu |

Rà soát phía bán trong gói chuẩn bị phục vụ bên bán và giới hạn trong dữ liệu họ cấp. Thẩm định đầy đủ của bên mua chỉ bắt đầu sau NDA và cấp quyền hợp lệ.

Mỗi bước phải có đầu ra cụ thể mới được chuyển tiếp. Hồ sơ dừng phải ghi bước dừng và mã nguyên nhân: không đủ điều kiện, không ghép được, dừng sau thẩm định hoặc không hoàn tất. Chi phí hồ sơ thất bại vẫn phải ghi nhận; thu được tiền gói không mặc nhiên bù được toàn bộ chi phí theo đuổi giao dịch.

## 7. Cấu trúc giao dịch và định giá

Nguồn: mục 3.6-3.7, trang 27-28; Phụ lục B, trang 59-60.

| Nội dung | Chuyển nhượng vốn hiện hữu | Phát hành mới để tăng trưởng |
|---|---|---|
| Mục tiêu | Cổ đông thoái/chuyển giao vốn | Doanh nghiệp nhận vốn và năng lực đối tác |
| Tiền đi đâu | Về cổ đông bán; doanh nghiệp không nhận tiền mới | Vào doanh nghiệp; cổ đông hiện hữu bị pha loãng |
| Bên quyết định | Cổ đông/cấp có thẩm quyền | Ban điều hành cùng cổ đông có quyền phê duyệt |
| Hồ sơ cần làm rõ | Sở hữu thực, phụ thuộc người sáng lập, nghĩa vụ tiềm ẩn | Sử dụng vốn, năng lực đối tác ngoài tiền, quyền quản trị |
| Cơ sở đàm phán giá | Lợi nhuận và mức phụ thuộc người sáng lập | Kế hoạch tăng trưởng và điều kiện vốn mới |

Ví dụ của PDF giữ giá trị vốn chủ sau đầu tư 300 tỷ và sở hữu bên mua 30%: khoản đầu tư là 90 tỷ. Nếu chuyển nhượng toàn bộ, 90 tỷ về cổ đông, giá trị vốn chủ trước giao dịch vẫn 300 tỷ. Nếu toàn bộ là phát hành mới, 90 tỷ vào công ty, giá trị vốn chủ trước đầu tư là 210 tỷ.

Các phân biệt bắt buộc khi lập bộ số:

- Giá trị doanh nghiệp (EV), nợ ròng (ND), giá trị vốn chủ, giá trị phần vốn giao dịch và giá trị vốn chủ trước/sau đầu tư.
- Giá trị vốn chủ được suy từ EV trừ ND; tỷ lệ chuyển nhượng vốn hiện hữu và tỷ lệ sở hữu sau phát hành mới có mẫu số khác nhau.
- Biến `PRIMARY = 50%` của mô hình là tỷ trọng **số giao dịch phát hành mới** trong tập giao dịch, không mô tả một thương vụ hỗn hợp 50% tiền mới/50% chuyển nhượng.
- Phí thành công tính trên giá trị phần vốn giao dịch, không tự lấy 2% toàn bộ EV.
- Không được nhân tỷ lệ sở hữu lần nữa nếu dữ liệu đầu vào đã là giá trị phần vốn được mua.

Tỷ lệ sở hữu không tự quyết định quyền. Bộ điều khoản phải làm rõ ghế hội đồng, vấn đề cần đồng thuận, quyền thông tin, chuyển nhượng và lối ra, giữ người sáng lập, cam kết thương mại. Tất cả cần đàm phán và pháp lý rà soát.

## 8. Thẩm định và hỗ trợ sau giao dịch

Nguồn: mục 3.4, 6.4, trang 24-25, 50.

### 8.1. Sáu hạng mục thẩm định công nghệ

1. **Kiến trúc và khả năng mở rộng:** khả năng chịu tải, nút thắt, chi phí đáp ứng quy mô bên mua.
2. **Mã nguồn và nợ kỹ thuật:** trùng lặp, độ phủ kiểm thử, tài liệu, công sức đưa về mức bảo trì được.
3. **Sở hữu trí tuệ:** thư viện bên thứ ba, giấy phép, điều khoản chuyển giao quyền; chuyên gia kỹ thuật cung cấp phát hiện, luật sư ký kết luận quyền sở hữu hợp lệ.
4. **An toàn thông tin và dữ liệu cá nhân:** phân quyền, nhật ký, mã hóa, điều kiện xử lý/chuyển dữ liệu.
5. **Phụ thuộc nhân sự chủ chốt:** kiến thức tập trung, rủi ro nghỉ việc, giữ người và chuyển giao tri thức.
6. **Tích hợp với bên mua:** khả năng kết nối và chi phí nâng cấp/tích hợp để phục vụ đàm phán.

### 8.2. Đầu ra và quy tắc sử dụng

- Báo cáo gồm tóm tắt cho hội đồng, chi tiết cho đội kỹ thuật và bảng chi phí khắc phục.
- Phát hiện trình bày theo chuỗi: rủi ro → ảnh hưởng tiền → người chịu → thời điểm → tác động vào giá hoặc điều khoản → mức chắc chắn.
- Phân thời hạn xử lý: bắt buộc trước hoàn tất; nên làm trong sáu tháng đầu; có thể hoãn.
- Tách chi phí sửa một lần, chi phí vận hành tăng hằng năm, nợ kỹ thuật có thể chấp nhận và đầu tư phục vụ tăng trưởng. Theo cách tiếp cận của báo cáo, chi phí sửa một lần và giá trị hiện tại của chi phí vận hành tăng thêm mới là căn cứ điều chỉnh giá; tránh trừ cùng một khoản cả trong EV lẫn dự phóng dòng tiền.
- Ghi rõ người được dựa vào báo cáo, mục đích, ngày hiệu lực, hệ thống/mẫu đã kiểm, phần không kiểm, cách xử lý phát hiện mới, giới hạn trách nhiệm và khiếu nại.

### 8.3. Hỗ trợ sau giao dịch

Có thể gồm đồng bộ khách hàng/đơn hàng, hợp nhất báo cáo, bản địa hóa tiếng Nhật, thay phần mềm quản trị, tích hợp hệ thống và chuyển đổi số. Chỉ thực hiện khi khách hàng có nhu cầu và ký hợp đồng riêng; đầu tư thiểu số không mặc nhiên kéo theo hợp nhất hệ thống.

Theo dõi giá trị hợp đồng phát sinh, pháp nhân Rikkei nhận hợp đồng và phí giới thiệu nếu có. Doanh thu triển khai không cộng lần thứ hai vào VAULT.

## 9. Thu phí, công nợ và ghi nhận doanh thu

Nguồn: mục 2.3, 3.9, 5.1-5.3, trang 22, 29-30, 37-39.

### 9.1. Nguồn thu

| Nguồn thu | Người trả | Cơ sở giả định | Mốc thu/ghi nhận | Trong dự phóng VAULT giai đoạn 1 |
|---|---|---|---|---|
| Gói chuẩn bị | Bên bán | 90 triệu/gói; phạm vi theo độ phức tạp | Tạm ứng khi ký, còn lại theo nghiệm thu, dự kiến cách 6-8 tuần | Có; mô hình hiện đơn giản hóa thu và ghi nhận cùng tháng |
| Phí thành công | Bên ký ủy nhiệm | 2% giá trị phần vốn giao dịch; chia đối tác giới thiệu 20% | Giao dịch hoàn tất, đủ điều kiện hợp đồng; thu trễ bình quân 2 tháng | Có; giả định thực thu 90%, tổn thất dự kiến 10% |
| Thẩm định công nghệ | Bên mua hoặc bên bán | 250 triệu/hợp đồng cơ sở, theo phạm vi | Theo nghiệm thu báo cáo | Không; thuộc hợp đồng Rikkei |
| Thuê bao công cụ | Bên bán | Theo tháng hoặc thương vụ | Kích hoạt/gia hạn | Không; phần lớn đã nằm trong gói chuẩn bị |

Hợp đồng gói phải quy định sản phẩm bàn giao, tiêu chí nghiệm thu, số vòng chỉnh sửa và giới thiệu tối thiểu, điều kiện hoàn phí khi không thực hiện cam kết, và có cấn trừ phí gói vào phí thành công hay không. Hồ sơ chuẩn hóa phải có giá trị sử dụng độc lập cho bên bán, kể cả khi không bán được vốn.

Phụ lục B còn có giả định chia **10% phí gói** cho đối tác ở kịch bản cơ sở. Vì vậy không dùng phép tính đơn giản 90 triệu trừ 15 triệu làm lợi nhuận cuối cùng của gói: còn phần chia phí, giờ công và các chi phí liên quan.

### 9.2. Nguyên tắc kiểm soát phí

- Quản lý theo từng hồ sơ và hợp đồng: người trả, cơ sở phí, tỷ lệ, phần chia đối tác, mốc nghiệm thu, hóa đơn, đến hạn, thực thu và dư nợ.
- Tách doanh thu đã ghi nhận, tiền thực thu, tổn thất phí và công nợ.
- Không thu trùng công cụ đã nằm trong gói; không tính phí hai phía cho cùng công việc khi hợp đồng chưa có cơ sở.
- Chi phí trực tiếp mỗi ủy nhiệm áp dụng cả hồ sơ thất bại. Giả định cơ sở: 15 triệu/gói, 35 triệu/ủy nhiệm, 70 triệu/lần hoàn tất.
- Mỗi hợp đồng chỉ được ghi nhận ở một nơi; đối soát VAULT với các pháp nhân Rikkei định kỳ.
- VAULT thu phí dịch vụ của mình, không nhận giữ tiền thanh toán mua vốn hoặc cổ phần thay khách hàng.

### 9.3. Phương án chủ trì và hợp tác

| Nội dung | VAULT chủ trì | Đối tác chủ trì |
|---|---|---|
| Ký ủy nhiệm và giữ quan hệ mua | VAULT | Đối tác |
| Phần giữ lại từ phí thành công theo giả định | 80% sau chia 20% cho đầu mối | 20% phí giới thiệu |
| Vai trò chủ yếu của Rikkei/VAULT | Toàn bộ chuỗi điều phối, chuẩn bị và chuyên môn liên quan | Chuẩn hóa hồ sơ, thẩm định công nghệ, giới thiệu |
| Giờ minh họa một giao dịch | 615 giờ | Khoảng 200 giờ |

Báo cáo đề xuất thử bằng hợp tác, rồi chỉ chuyển sang tự chủ sau cổng 4. Mô hình 60 tháng lại dự phóng theo **VAULT chủ trì**; không áp nguyên kết quả đó cho mô hình đối tác chủ trì. Quyền tiếp cận khách hàng, dùng lại dữ liệu, chia phí, không đi vòng, chấm dứt và chuyển đổi mô hình phải được đàm phán bằng hợp đồng.

Phương án mua/góp vốn vào công ty tư vấn có sẵn chỉ cân nhắc sau khi hợp tác chứng minh nhu cầu thực tế.

## 10. Startup Bridge và Book B

Nguồn: mục 2.2, 3.8, 5.6-5.7, 7.3, trang 16-18, 28-29, 43-46, 51-52.

### 10.1. Startup Bridge - giao dịch với quỹ vẫn thuộc Book A

- Sàng lọc theo bốn trục: giai đoạn gọi vốn, cỡ vé, ngành, tăng trưởng đã chứng minh.
- Hồ sơ cần luận điểm tăng trưởng, kinh tế đơn vị, cơ cấu sở hữu và kế hoạch sử dụng vốn.
- Lập data pack, đối chiếu từng quỹ theo luận điểm đầu tư, giai đoạn, cỡ vé, ngành, danh mục trùng lặp và người quyết định.
- Quản lý vòng vốn, quan hệ nhà đầu tư; dùng chung hạ tầng và dữ liệu chỉ trong phạm vi được phép.
- Danh sách Genesia Ventures, CyberAgent Capital, Do Ventures trong báo cáo là đầu mối nghiên cứu, chưa phải bên nhận hồ sơ VAULT hay đối tác đã cam kết.
- Kinh tế nhánh đứng riêng: giả định 80 triệu chi phí cố định/tháng, 60 triệu/gói, 25 triệu chi phí trực tiếp/gói, thêm phí vốn huy động khi hoàn tất. PDF chưa đủ chi tiết để coi đây là biểu phí đã chốt.
- Theo phép thử của báo cáo, 24 gói/năm cần ít nhất hai vòng hoàn tất để dương; 12 gói thì bốn vòng hoàn tất vẫn chưa bù chi phí nhóm. Các cách thử thủ công, qua đối tác hoặc tuyển dần chưa được định lượng.

### 10.2. Book B - huy động kèm nghĩa vụ chi trả

Nhánh này đang nghiên cứu; F17 và F18 bị khóa, không mở trong giai đoạn 1 kể cả thử nhỏ theo đề xuất của PDF.

Thiết kế minh họa: doanh nghiệp huy động 10 tỷ, trả 10%/năm trên vốn ban đầu, mua lại 100% cuối năm 5. Lịch nghĩa vụ là 1 tỷ/năm trong bốn năm đầu và 11 tỷ năm 5, tổng 15 tỷ. Nghĩa vụ thuộc tổ chức phát hành; VAULT và Rikkei không bảo lãnh.

F18 cần theo dõi vốn huy động, cổ tức đến hạn/đã trả/còn nợ, dự trữ, nguồn trả, nghĩa vụ mua lại, thiếu hụt và cảnh báo. Nếu doanh nghiệp có 2 tỷ tiền tự do/năm, năm 5 chỉ có 6 tỷ trước khi chi so với 11 tỷ nghĩa vụ, thiếu 5 tỷ. Ngưỡng tự tích lũy trong ví dụ là 3 tỷ/năm khi cổ tức 10%, hoặc 3,5 tỷ/năm khi cổ tức 15%.

Tiền tự do phải là phần còn lại sau đầu tư tài sản, vốn lưu động, thuế, nghĩa vụ nợ và tiền vận hành tối thiểu. Cần thử doanh thu suy giảm, dòng tiền không đều, giới hạn phân phối và thực hiện quyền mua lại 100%, kể cả quyền sớm nếu hợp đồng cho phép.

Trước khi thiết kế sản phẩm phải có kết luận pháp lý bằng văn bản theo năm bước:

1. Xác định tổ chức phát hành và chủ thể chịu nghĩa vụ.
2. Phân loại công cụ: cổ phần phổ thông/ưu đãi hoặc công cụ nợ.
3. Xác định nhóm nhà đầu tư.
4. Chọn kênh phân phối phù hợp.
5. Xác định tổ chức có chức năng thực hiện phần cần giấy phép; không có thì bỏ nhánh đó.

Điều khoản cần chốt gồm bên ký với nhà đầu tư, điều kiện/thứ tự chi trả khi thiếu tiền, mua lại sớm, công bố định kỳ, xung đột lợi ích, ngoại hối và thuế. Giấy phép đối tác không chứng minh công cụ hợp lệ hay doanh nghiệp đủ tiền trả.

## 11. Tiếp cận khách hàng và quản lý công suất

Nguồn: mục 4.2-4.5, 6.1, trang 32-36, 46-47.

### 11.1. Tạo nguồn hai phía

Ưu tiên bên mua theo thứ tự: khách hàng Nhật hiện hữu của Rikkei → quan hệ đã công bố → JETRO/hiệp hội/trung gian → tiếp cận trực tiếp có chọn lọc. Bốn tháng đầu tập trung hai kênh đầu. Quan hệ phải được xin quyền tiếp cận nội bộ để bảo vệ hợp đồng dịch vụ đang có.

Ma trận tiếp cận mỗi tổ chức cần: đơn vị kinh doanh cụ thể, người có thẩm quyền, người Rikkei có thể giới thiệu, trạng thái liên hệ. Bốn mức trạng thái là chưa liên hệ, đã liên hệ chưa trả lời, đã trao đổi, đã xác nhận tiêu chí bằng văn bản. Sumitomo/MISUMI là đầu mối cần kiểm chứng; RK Tsunagu là tham chiếu vận hành liên doanh; trung gian/hiệp hội không phải bên mua.

Phía bán được sàng lọc từ đăng ký doanh nghiệp, dữ liệu tài chính thực sự công bố hoặc mua hợp lệ, tài liệu doanh nghiệp cung cấp và dấu hiệu nguồn mở. BCTC nộp thuế không mặc nhiên là dữ liệu công khai. Dấu hiệu thay đổi đại diện/cơ cấu vốn/tuyển dụng chỉ giúp ưu tiên tiếp cận, không khẳng định ý định bán.

Liên hệ đầu phải nêu nguồn và mục đích, dừng khi doanh nghiệp từ chối. Máy tạo thứ tự ưu tiên; người phụ trách quyết định nhận hồ sơ sau trao đổi. Nhật ký thử nghiệm ghi phân khúc, nguồn đầu mối, giá niêm yết/thực thu, người có quyền ký và lý do từ chối; tách khách trả tiền độc lập với hồ sơ nội bộ/tài trợ.

### 11.2. Công suất theo tháng

| Cỡ giao dịch minh họa | Giá trị doanh nghiệp | Chu kỳ từ ủy nhiệm đến hoàn tất | Tổng giờ nhóm |
|---|---|---|---|
| Nhỏ | 50-100 tỷ | 9 tháng | 365 |
| Vừa | 100-300 tỷ | 12 tháng | 615 |
| Lớn | 300-500 tỷ | 15 tháng | 950 |

615 giờ của giao dịch vừa gồm: trưởng giao dịch 140, phân tích 240, đầu mối Nhật 110, công nghệ 80, pháp lý 45. Đây là giờ cả nhóm, chưa phải giờ thực đo và không bao gồm giai đoạn tìm/sàng lọc.

Theo dõi độc lập giờ phân tích, giờ đầu mối Nhật, hồ sơ đang chạy và cơ hội mua đủ điều kiện. Hồ sơ tồn tiếp tục chiếm giờ; phải trừ giờ phục vụ hồ sơ đang chạy trước khi nhận việc mới. Dư giờ một vai trò không bù được thiếu vai trò khác. Khi hồ sơ đã vào đàm phán, báo cáo đề nghị ưu tiên xử lý thay vì chỉ ưu tiên gói mới như mô hình.

Chỉ số vận hành cần đo: đầu mối, tỷ lệ đủ điều kiện, tỷ lệ mua gói, gói thành ủy nhiệm, tuổi hồ sơ, hoàn tất theo lứa ký, lý do dừng, độ tương thích hai phía, giờ từng vai trò và tháng cao điểm, phí/phần thực thu, công nợ, hợp đồng triển khai sau đầu tư.

## 12. Lộ trình, cổng kiểm chứng và tài chính

Nguồn: chương 5-6 và Phụ lục B, trang 37-50, 59-60. Toàn bộ số là kịch bản trong PDF, chưa đối soát workbook.

### 12.1. Bốn cổng trước vận hành

| Cổng | Thời gian dự kiến | Điều kiện tối thiểu | Ngân sách | Khi không đạt |
|---|---|---|---|---|
| 1 - Phạm vi pháp lý | 90 ngày | Ý kiến pháp lý về dịch vụ/dữ liệu; 8 trao đổi bên bán, 4 bên mua | 90 triệu | Dừng |
| 2 - Nhu cầu hai phía | 120 ngày | 2 ủy nhiệm bán đã ký; 3 hồ sơ chuẩn được bên bán duyệt; 2 yêu cầu mua đủ sáu thông tin | 120 triệu | Điều chỉnh hoặc dừng |
| 3 - Khách trả tiền | 120 ngày | Ít nhất 1 hợp đồng gói đã thu tiền, có khách ngoài hệ sinh thái; 2 NDA đã ký | 120 triệu | Dừng mở rộng, giữ năng lực thẩm định công nghệ |
| 4 - Khả năng lặp lại | 120 ngày | 3 gói đã thu tiền; 1 thư bày tỏ ý định (LOI); giờ công thực tế ít nhất 3 hồ sơ | 120 triệu | Trình hội đồng quyết định |

Tổng 450 triệu trong khoảng 450 ngày, nằm **trước tháng 1 của lịch vận hành 60 tháng**. Chỉ cần một chỉ tiêu không đạt là phải trình lại; không cần mọi chỉ tiêu cùng không đạt. Không cổng nào yêu cầu đã hoàn tất một thương vụ M&A. Điều kiện dừng thương mại ở mục 7.6 của PDF còn yêu cầu phải có ít nhất một yêu cầu mua đủ sáu thông tin tại cổng 4; cần đọc cùng bảng trên.

### 12.2. Nguồn lực và nhu cầu vốn

- Vận hành cơ sở cần 1,74 tỷ tiền mặt, gồm đáy âm khoảng 1,43 tỷ tại tháng 20 và đệm ba tháng chi tiền cố định.
- Tổng đề nghị gồm 0,45 tỷ giai đoạn bằng chứng + 1,74 tỷ vận hành = **2,19 tỷ đồng**.
- Nếu không có người nội bộ hỗ trợ, phần tiền mặt vận hành tăng lên 3,15 tỷ; tổng cộng hai giai đoạn là 3,60 tỷ, phép cộng từ số trong PDF.
- Chi phí cố định cơ sở năm đầu 140 triệu/tháng, tăng giả định 20%/năm; 40% trả bằng nguồn lực nội bộ, 60% bằng tiền. Chi phí nội bộ khoảng 5 tỷ trong năm năm vẫn tính vào hiệu quả kinh tế.
- Chi trực tiếp năm đầu 1,35 tỷ được phân về 870 triệu thiết lập rải sáu tháng, 390 triệu đã trong chi phí cố định, 90 triệu trong biến phí; không cộng lại lần nữa vào tổng chi phí.
- Ước tính tổn thất khi dừng giai đoạn bằng chứng là 415 triệu = 355 triệu đã cam kết + 60 triệu đóng cửa; còn phụ thuộc điều khoản thật, không phải trần lỗ được bảo đảm.
- Cần chốt bản chất khoản cấp, sở hữu phần mềm/quy trình/dữ liệu, pháp nhân ghi nhận và thước đo hiệu quả trước giải ngân.

### 12.3. Kết quả cơ sở và giới hạn

| Chỉ tiêu | Giá trị được PDF nêu |
|---|---|
| Sản lượng năm năm | 157 gói; 11 giao dịch hoàn tất |
| Doanh thu năm năm | 35,77 tỷ |
| Lợi nhuận trước/sau thuế năm năm | 8,64 tỷ / 6,91 tỷ |
| Dòng tiền kinh tế lũy kế 60 tháng | 5,14 tỷ; chưa trừ 450 triệu giai đoạn bằng chứng |
| Riêng năm 5 | 47 gói, 23 ủy nhiệm mới, 4 hoàn tất; doanh thu 12,10 tỷ |
| Hoàn tất và thu phí thương vụ đầu | Tháng vận hành 19 và 21 |
| Tiền mặt dương liên tục đến hết kỳ | Từ tháng 27; lần đầu dương tháng 21 chưa bền |
| Dòng tiền kinh tế dương liên tục đến hết kỳ | Từ tháng 37; lần đầu dương tháng 32 chưa bền |
| Phần còn lại tại tháng 60 | 23 ủy nhiệm chưa hết chu kỳ; khoảng 1,77 tỷ phí phải thu |

Không lấy hoàn tất của cùng năm chia ủy nhiệm năm đó để coi là xác suất thành công; chúng có thể thuộc các lứa khác nhau. Các con số 0/11/42 giao dịch của ba kịch bản là kết quả mô hình tất định được làm tròn, không phải xác suất hoặc trung vị.

Theo bảng chính trang 43: miễn phí gói làm dòng tiền kinh tế năm năm còn -5,85 tỷ; không có bên mua đủ điều kiện -3,01 tỷ; không có giao dịch hoàn tất -5,74 tỷ. Chu kỳ 18 tháng còn 3,05 tỷ; phí 1,5% còn 2,55 tỷ; thu trễ 5 tháng còn 3,37 tỷ trong kỳ, một phần tiền bị đẩy sau tháng 60. Downside kết hợp cho -6,48 tỷ và nhu cầu vận hành 7,35 tỷ theo cách tính đệm tại tháng đáy của bảng; đây không phải trần xấu nhất.

Nhánh startup, Book B và cơ hội triển khai Rikkei không dùng để bù kết quả giai đoạn 1. Phép thử triển khai sau đầu tư của PDF cho 6,6 tỷ doanh thu và 1,8 tỷ đóng góp ròng minh họa, giữ ngoài kịch bản cơ sở.

### 12.4. Toàn bộ 34 biến của động cơ 60 tháng - giá trị cơ sở năm 1

| Nhóm | Mã và giá trị |
|---|---|
| Cấu trúc vốn | `EV` 300.000 triệu; `ND` 30.000 triệu; `ST` 30%; `NEW` 30%; `PRIMARY` 50% số giao dịch |
| Phí và chi phí trực tiếp | `FEE` 2%; `SHARE` 20%; `PREP` 90 triệu; `PSHARE` 10%; `PCOST` 15 triệu; `DCOST` 35 triệu; `CCOST` 70 triệu |
| Hoàn tất và thu tiền | `PROB` 20%; `CYCLE` 12 tháng; `COLL` 90%; `LAG` 2 tháng |
| Phễu bán | `LEADS` 10/tháng; `QUAL` 40%; `PAY` 40%; `MAND` 50% |
| Giờ công | `AH` 160 giờ phân tích/tháng; `PH` 28 giờ/gói; `DH` 6 giờ phân tích/hồ sơ đang chạy/tháng; `BH` 80 giờ đầu mối Nhật/tháng; `BM` 5 giờ đầu mối Nhật/hồ sơ đang chạy/tháng |
| Chi phí và tài trợ | `FIX` 140 triệu/tháng; `SETUP` 870 triệu; `SETUPM` 6 tháng; `TAX` 20% mô phỏng; `INT` 40% chi phí cố định bằng nguồn lực nội bộ; `BUFFER` 3 tháng |
| Cầu mua và phép thử | `BUYER` 1 cơ hội phù hợp/tháng; `PREPON` 1, bật thu phí gói; `NOCLOSE` 0 tháng chặn hoàn tất |

Ngoài 34 biến còn có đầu vào riêng cho Book B, mở rộng và dữ liệu thị trường. Đây là tham số mô hình kinh doanh, không mặc nhiên là danh mục cấu hình phần mềm phải xây.

## 13. Tuân thủ, rủi ro và điều kiện dừng

Nguồn: chương 7, trang 50-55. Phần này tổng hợp yêu cầu trong báo cáo, không xác nhận tính hợp pháp của một giao dịch cụ thể.

### 13.1. Các cửa kiểm tra

- Phân loại hoạt động thực tế: chuẩn bị/tư vấn, môi giới/tư vấn chào bán, nhận lệnh, phân phối, giữ tiền/tài sản; tên gọi hợp đồng không tự quyết định phạm vi giấy phép.
- Điều kiện nhà đầu tư nước ngoài: ngành có điều kiện, thay đổi nhóm kiểm soát do tỷ lệ sở hữu, quyền sử dụng đất tại địa bàn nhạy cảm.
- Thủ tục góp vốn/mua cổ phần và sở hữu trước/sau.
- Tập trung kinh tế: quy mô tất cả các bên và nhóm công ty liên quan, lịch thông báo/thẩm định trước hoàn tất.
- Loại cổ phần, quyền cổ đông, điều kiện chia cổ tức và mua lại.
- Ngoại hối, loại tài khoản vốn và chuyển lợi nhuận.
- Vai trò xử lý dữ liệu, căn cứ xử lý, hồ sơ đánh giá tác động, chuyển dữ liệu xuyên biên giới.
- Pháp luật Nhật do chuyên gia Nhật kiểm tra riêng.

### 13.2. Sổ 11 rủi ro

| Mã | Rủi ro | Kiểm soát chính | Chủ trì theo PDF |
|---|---|---|---|
| R01 | Book B bị coi là chào bán sai kênh/bảo đảm lợi nhuận | Ý kiến pháp lý, đơn vị có phép, duyệt truyền thông | Pháp lý và hội đồng |
| R02 | Tổ chức phát hành thiếu tiền cổ tức/mua lại | Stress test thực hiện quyền 100%, đệm, ràng buộc | Tài chính và pháp lý |
| R03 | Giữ tiền/cổ phần ngoài phạm vi | Thanh toán/lưu ký qua bên có chức năng, sơ đồ dòng tiền | Pháp lý |
| R04 | Rò rỉ dữ liệu mật | MFA, phân quyền, hai người duyệt, log, thủy vân | Bảo mật |
| R05 | Phụ thuộc người, quá tải | Người dự phòng, giới hạn hồ sơ, giờ công tháng | Người bảo trợ |
| R06 | Không có nhu cầu hoặc không trả phí | Ủy nhiệm ký, yêu cầu mua đủ chuẩn, cổng kiểm chứng | Trưởng giao dịch |
| R07 | Xung đột lợi ích dịch vụ liên đới | Công bố, rút khỏi quyết định, duyệt độc lập, tách phạm vi | Người bảo trợ và pháp lý |
| R08 | Dự báo tiền sớm, che nguồn lực nội bộ | Tách dòng tiền mặt/kinh tế, công nợ và độ trễ | Tài chính |
| R09 | Đối tác thiếu chất lượng/giấy phép/trách nhiệm | Thẩm định đối tác, phạm vi, SLA, hợp đồng | Pháp lý và mua sắm |
| R10 | Vướng sở hữu nước ngoài, cạnh tranh, thuế, ngoại hối | Luật sư từng vụ và checklist trước ký | Pháp lý và tài chính |
| R11 | Trùng doanh thu VAULT/Rikkei | Một nơi ghi nhận mỗi hợp đồng, đối chiếu định kỳ | Tài chính |

Điểm rủi ro sau kiểm soát trong PDF là mục tiêu, chưa phải hiện trạng. R01-R04 vẫn có mức tác động tối đa theo thang của báo cáo; khóa Book B không loại được rủi ro giữ tiền và dữ liệu của Book A.

### 13.3. Bốn điều kiện dừng theo logic HOẶC

1. Hoạt động thuộc phạm vi cần giấy phép nhưng chưa có: dừng ngay, báo hội đồng.
2. Rò tài liệu lớp 3 hoặc công bố trái phép danh tính: dừng chia sẻ dữ liệu đến khi điều tra xong.
3. Tại cổng 4 chưa đủ ba hợp đồng gói đã thu tiền **hoặc** chưa có yêu cầu mua đủ sáu thông tin: dừng mở rộng, trình hội đồng.
4. Mất người phụ trách chính mà chưa có thay thế: dừng nhận hồ sơ mới.

Pháp lý, bảo mật, người bảo trợ có quyền kích hoạt theo phạm vi; tài chính có quyền yêu cầu dừng khi đáy tiền vượt hạn mức. Không cần tất cả các vai trò cùng đồng ý mới được yêu cầu dừng.

## 14. Yêu cầu kỹ thuật, kiểm thử và phần cần đặc tả thêm

Nguồn: mục 3.2, 7.4 và Phụ lục C, trang 23-24, 52-53, 61-62.

### 14.1. Xây, mua và vận hành thủ công

| Cách làm | Phạm vi |
|---|---|
| Tái sử dụng và xây bổ sung | Hồ sơ doanh nghiệp, bằng chứng và trạng thái kiểm tra; tiêu chí bên mua và so khớp tạo tài sản dữ liệu dùng lại được |
| Mua và tích hợp | Phòng dữ liệu, chữ ký số, CRM; công cụ quét mã; công cụ AI sẵn có |
| Thủ công/bảng tính ban đầu | Sàng lọc, ghép nối, tài chính, điều kiện hoàn tất, theo dõi phí, danh sách đầu mối |
| Chuẩn hóa chuyên môn | Phương pháp Tech DD, mẫu báo cáo, hợp đồng và mạng lưới chuyên gia |

Nguyên tắc đề xuất: chỉ số hóa quy trình sau khi đã chạy bằng người ít nhất 10 lần. Đây là quy tắc thiết kế của báo cáo, không phải chuẩn ngành. Mức tái sử dụng hạ tầng Rikkei vẫn cần kiểm kê kỹ thuật và quyền khai thác.

### 14.2. Kiểm soát chất lượng AI

- Từ điển thuật ngữ Việt - Nhật thống nhất.
- Dẫn tới đúng trang nguồn; đánh dấu số và đơn vị để người kiểm soát đối chiếu.
- Ghi người duyệt và lịch sử kiểm tra.
- Đo thời gian tiết kiệm sau khi trừ thời gian kiểm/sửa, tỷ lệ lỗi trọng yếu và sai lệch số liệu.
- Không lấy tốc độ tạo nháp làm thước đo duy nhất; không dùng AI làm kết luận thẩm định.

### 14.3. Mười tình huống nghiệp vụ phải có kết quả mong đợi bằng văn bản

1. Dữ liệu mâu thuẫn hoặc hết hạn.
2. Hai ủy nhiệm trùng một doanh nghiệp.
3. Hai bên mua cạnh tranh trên cùng hồ sơ.
4. Người không đủ quyền vẫn truy cập được tài liệu.
5. Thu hồi quyền sau khi tài liệu đã tải xuống.
6. Điều khoản giao dịch thay đổi sau khi hồ sơ phát hành.
7. Thu phí một phần rồi hồ sơ dừng.
8. Hủy giao dịch sau khi ký.
9. Người phụ trách nghỉ giữa quy trình.
10. Dịch tự động sai điều khoản.

PDF liệt kê các trường hợp trên nhưng chưa cung cấp đầy đủ cách xử lý và tiêu chí pass/fail, nên không được coi chúng là test case hoàn chỉnh.

### 14.4. Phần cần bổ sung để giao đội sản phẩm

Mỗi công năng F01-F20 cần thêm sáu trường mà PDF xác định còn thiếu: người dùng/người chịu trách nhiệm, trạng thái đầu vào, quyền truy cập, phụ thuộc công năng, quyết định xây/mua kèm tổng chi phí sở hữu ba năm, và ước tính giờ.

Các đối tượng dữ liệu được tổng hợp từ nghiệp vụ để thuận tiện đặc tả tiếp, **chưa phải schema đã được PDF phê duyệt**: tổ chức và người đại diện; chuỗi sở hữu; dữ kiện/bằng chứng; yêu cầu mua; hồ sơ cơ hội; hợp đồng gói/ủy nhiệm; NDA và quyết định cấp quyền; tài liệu/phiên bản/log; cặp ghép; hỏi đáp; báo cáo thẩm định; cấu trúc vốn/điều kiện hoàn tất; phí/hóa đơn/công nợ; giờ công; hợp đồng triển khai; vòng vốn startup; lịch nghĩa vụ Book B; quyết định cổng và sự kiện dừng.

PDF chưa phải BRD/SRS đủ để ước tính phát triển. Chưa chốt màn hình, API, schema, ma trận quyền đầy đủ, thời hạn hiệu lực, quy tắc xử lý ngoại lệ, SLA và chi phí từng công năng. Không tự bổ sung những phần này thành yêu cầu đã được duyệt.

## 15. Điểm chưa nhất quán và chưa kiểm chứng

### 15.1. Điểm cần đối soát trong chính PDF

| Vấn đề | Nội dung chưa khớp | Cách đọc trong bản tổng hợp |
|---|---|---|
| Thứ tự chuẩn hóa và ủy nhiệm | S01 trang 26 vẽ chuẩn hóa trước ký ủy nhiệm; văn bản ngay dưới yêu cầu ký ủy nhiệm trước dựng hồ sơ | Trình bày luồng theo văn bản và yêu cầu chốt riêng hợp đồng gói/ủy nhiệm trước triển khai |
| Định nghĩa Book A | Mục 3.8 và S02 gồm startup gọi vốn riêng; CA-030 tại trang 67 lại chỉ ghi giai đoạn 1 | Dùng định nghĩa phần chính: Book A gồm giao dịch giữa các bên xác định ở cả hai giai đoạn |
| Bộ ngưỡng cổng 4 | Bảng 6.2 có ba gói, LOI, dữ liệu giờ; mục 7.6 thêm điều kiện yêu cầu mua đủ chuẩn | Giữ cả hai, chưa tự coi bảng cổng đã đủ |
| Số stress test tại Phụ lục E | Trang 65 nêu không buyer -2,39 tỷ, chu kỳ 18 tháng 3,54 tỷ, phí 1,5% 3,05 tỷ; bảng trang 43 lần lượt -3,01; 3,05; 2,55 tỷ | Dùng bảng chính trang 43, ghi nhận chưa có workbook xác minh |
| Downside kết hợp | Văn xuôi có 6,90 tỷ; bảng trang 43 dùng 7,35 tỷ do cách tính đệm | Nêu 7,35 tỷ theo đệm tại tháng đáy, không coi là trần lỗ |
| Dòng tiền kinh tế âm trở lại | Văn xuôi trang 41 nói hai tháng sau lần dương đầu; bảng cụ thể ghi tháng 35-36 | Dùng mốc dương bền tháng 37; không suy mốc hoàn vốn từ lần đầu dương |
| Quỹ phí thị trường | Trang 15 nói hai phép ước lượng 235,4 và 70,6 tỷ không chứng minh là cận; tiêu đề và Phụ lục E/F vẫn dùng cách gọi hai cận | Không dùng làm quy mô thị trường phục vụ được đã xác nhận |
| Phân khúc | Trọng tâm 200-500 tỷ nhưng nhiều bảng dùng 100-300 tỷ | Giữ trọng tâm được nhấn mạnh, ghi bảng cỡ vừa là minh họa |
| Lợi nhuận gói chuẩn bị | Trang 26 tính đóng góp khoảng 63 triệu từ phí, chi trực tiếp và giờ; Phụ lục B có thêm chia 10% phí gói | Không sử dụng 63 triệu như đóng góp đầy đủ đã đối soát |
| Lịch sử audit | Phụ lục F tự ghi đã sửa nhưng còn số/diễn giải cũ; bìa và phụ lục cũng mô tả khác nhau về bình luận audit | Không dùng trạng thái đã sửa làm bằng chứng độc lập; không chuyển chỉ dẫn biên tập thành yêu cầu dự án |
| Mức hoàn thiện phần mở đầu | Trang 5 còn mục/đoạn dang dở | Tổng quan được gom từ các chương nghiệp vụ đầy đủ hơn; không tự điền nội dung còn trống |

### 15.2. Giả định chưa được chứng minh

Chưa xác nhận khách trả giá gói 90 triệu, chấp nhận phí 2%, mức chia phí, tỷ lệ hoàn tất 20%, chu kỳ 12 tháng, lịch thu 90% sau hai tháng, số buyer đạt chuẩn, khả năng ghép đúng phân khúc, nguồn lực nội bộ, giờ công, quyền dùng lại tài sản/hạ tầng, điều khoản đối tác và cấu trúc khoản cấp. Năng lực thiết kế của VAULT chưa phải năng lực đã vận hành; không dùng bảng so đối thủ để khẳng định VAULT đã vượt trội.

Sáu đơn giản hóa mô hình cần nhớ: dùng tham số năm hiện hành cho hồ sơ cũ; thu tiền gói và ghi nhận cùng tháng; nhu cầu mua tích lũy không hết hạn; chỉ giới hạn số lượng mà chưa kiểm tương thích từng cặp; ưu tiên gói trước ủy nhiệm; dùng định mức giờ cố định không có phân tán. Cần bổ sung thời hạn hồ sơ/cơ hội, theo dõi lứa và kiểm tra nguồn lực thực khi chuyển sang đặc tả vận hành.

Phụ lục F ghi lịch sử 150 phát hiện với 133 đã sửa, 8 sửa một phần, 8 ghi giới hạn, 1 chờ xác nhận. Đây là tự đánh giá của tài liệu. Bản tổng hợp giữ những nội dung ảnh hưởng chức năng/nghiệp vụ và các điểm còn vướng, không chép lại toàn bộ lịch sử sửa biên tập.

## 16. Bảng truy xuất nội dung nguồn

Số trang dưới đây là số trang PDF, không lấy số mục lục cũ làm tham chiếu.

| Phạm vi tổng hợp | Vị trí trong PDF |
|---|---|
| Trạng thái đề xuất, nguồn số liệu | Trang 1 |
| Bài toán, thị trường, phân khúc, cạnh tranh | Chương 1-2, trang 3-22 |
| Dịch vụ, công cụ, Trust Profile | Mục 3.1-3.3, trang 22-24 |
| Tech DD, luồng giao dịch, cấu trúc vốn, Book | Mục 3.4-3.8, trang 24-29; S01 trang 26, S02 trang 29 |
| Phí và phạm vi doanh thu | Mục 3.9, trang 29-31 |
| Tổ chức, quan hệ, công suất, chi phí | Chương 4, trang 31-37; S03 trang 31 |
| Kết quả tài chính, startup, nghĩa vụ Book B | Chương 5, trang 37-46 |
| Tiếp cận khách hàng, cổng, cấp vốn và giá trị Rikkei | Chương 6, trang 46-50 |
| Pháp lý, dữ liệu, 11 rủi ro và điều kiện dừng | Chương 7, trang 50-55 |
| Phương pháp, sáu đơn giản hóa, danh mục nguồn | Phụ lục A, trang 56-58 |
| Toàn bộ 34 biến mô hình | Phụ lục B, trang 59-60 |
| Toàn bộ 20 công năng, AI, tình huống lỗi | Phụ lục C, trang 61-62 |
| Danh mục biểu đồ H01-H36 và sơ đồ S01-S03 | Phụ lục D, trang 63-64 |
| Giả định chưa kiểm chứng | Phụ lục E, trang 65 |
| Lịch sử audit và các điểm cần đọc thận trọng | Phụ lục F, trang 66-73 |

Tài liệu nguồn định vị VAULT là một hoạt động dịch vụ chuyên môn có công cụ hỗ trợ. Phạm vi khởi động tập trung vào hồ sơ, xác minh, ghép nối có kiểm soát, thẩm định, điều phối và thu phí; các nhánh mở rộng vẫn được giữ đầy đủ trong danh mục với trạng thái tương ứng.
