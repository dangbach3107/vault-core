# VAULT Core — Bộ quy tắc ứng dụng và hướng dẫn demo luồng thương vụ A–Z

Ngày cập nhật: 14/09/2026  
Đường dẫn demo Vercel: `https://frontend-xi-eosin-36.vercel.app/#/investor-mvp`  
Đường dẫn local: `http://127.0.0.1:5174/#/investor-mvp` nếu Vite đang chạy ở cổng 5174, hoặc `http://127.0.0.1:5173/#/investor-mvp` nếu dùng cổng mặc định.  
Phạm vi: MVP dùng để trình diễn với nhà đầu tư/đồng nghiệp bằng dữ liệu giả lập. **Không dùng dữ liệu thật hoặc tài liệu mật thật.**

---

## 1. Mục tiêu của màn demo

Màn demo này cho thấy VAULT không phải là website đăng tin, không phải quỹ đầu tư, không phải sàn chứng khoán, và cũng không phải công cụ AI tự làm M&A. VAULT là một **nền tảng vận hành giao dịch có kiểm soát**, giúp các bên liên quan cùng đi qua một thương vụ mẫu từ đầu đến cuối:

1. Buyer nêu nhu cầu mua/góp vốn.
2. Seller tạo và duyệt hồ sơ.
3. VAULT ghi nhận doanh thu gói chuẩn bị ngay từ giai đoạn chuẩn hóa hồ sơ.
4. VAULT ghép buyer–seller bằng tiêu chí có giải thích.
5. Buyer nộp **Indicative LOI sơ bộ** trước khi được mở VDR sâu.
6. Legal/Compliance kiểm soát các điểm rủi ro trước khi mở Layer 3.
7. Tech DD đánh giá công nghệ và quy đổi rủi ro thành chi phí/tác động giao dịch.
8. Buyer gửi **Definitive Offer** sau khi đã có thông tin đầy đủ từ VDR/Tech DD.
9. Finance theo dõi phí, hóa đơn và dòng tiền thực tế.
10. VAULT đóng thương vụ giả lập và bàn giao cơ hội sau giao dịch cho Rikkei.

---

## 2. Bộ quy tắc ứng dụng trong MVP

### Quy tắc 1 — Buyer-first

Luồng demo chuẩn bắt đầu từ **Buyer**. Buyer phải tạo nhu cầu mua trước khi VAULT chuẩn bị ghép với Seller.

Buyer Request trong MVP có 4 trường tối thiểu:

1. Buyer đang thiếu hoặc muốn mua năng lực gì.
2. Mục tiêu trong 24 tháng sau khi mua/góp vốn.
3. Ngân sách hoặc khoảng quy mô giao dịch.
4. Timeline hoặc người/đường phê duyệt quyết định.

Trong MVP để trình diễn, thiếu trường vẫn có thể đi tiếp với cảnh báo. Khi sản phẩm thật, có thể siết theo định nghĩa đầy đủ hơn trong report.

---

### Quy tắc 2 — Một thương vụ mẫu đồng bộ trên tất cả các tab

Tất cả các tab đang nói về **cùng một thương vụ mẫu**:

- Buyer: một strategic buyer Nhật Bản ẩn danh.
- Seller: một công ty phần mềm quản lý kho/vận hành B2B tại Việt Nam.
- Mục tiêu giao dịch: strategic minority investment/acquisition path, khoảng 25–35% cổ phần.
- Trạng thái hoàn tất: SPA signed / deal closed giả lập, success fee được ghi nhận, và có post-deal handoff sang Rikkei.

Không demo rời rạc từng màn. Khi chuyển tab, trạng thái phải phản ánh cùng một deal.

---

### Quy tắc 3 — Các bên liên quan trong demo

MVP hiện có 6 tab vai trò:

1. **Buyer** — doanh nghiệp Nhật / strategic buyer.
2. **Seller** — founder/chủ doanh nghiệp Việt Nam.
3. **VAULT Admin** — deal lead điều phối toàn bộ.
4. **Legal** — Legal/Compliance kiểm soát rủi ro.
5. **Tech DD** — reviewer kỹ thuật của Rikkei.
6. **Finance** — theo dõi phí, invoice, collected/overdue.

VAULT Admin là trung tâm điều phối, nhưng demo phải cho thấy các bên khác có hành động và quyền phê duyệt riêng.

---

### Quy tắc 4 — Trust Profile có 3 lớp thông tin

Thông tin doanh nghiệp không được mở một lần toàn bộ. VAULT mở theo 3 lớp:

| Lớp | Nội dung | Điều kiện mở |
|---|---|---|
| Layer 1 — Teaser ẩn danh | Ngành, vùng, revenue band, employee band, deal intent | Seller duyệt teaser; buyer đã được VAULT xác minh ở mức phù hợp |
| Layer 2 — CIM định danh | Tên doanh nghiệp, sản phẩm, tài chính tóm tắt, khách hàng vẫn mã hóa Client A/B/C | Buyer request identity, NDA recorded, Seller approve buyer đó |
| Layer 3 — VDR/DD files | Tài liệu nhạy cảm, file thẩm định, dữ liệu phục vụ Tech DD | Buyer đã nộp Indicative LOI + Seller duyệt từng file + Legal/Compliance approve |

Layer 2 không tự động mở top customers thật. Layer 3 là theo từng file và từng buyer, không phải mở cả phòng dữ liệu một lần.

---

### Quy tắc 5 — Cam kết trước, mở VDR sau

Trước khi VAULT mở toàn bộ VDR và bỏ chi phí làm Tech DD, buyer phải nộp **Indicative LOI sơ bộ**:

- Không ràng buộc mua bán cuối cùng.
- Có thể kèm đề nghị độc quyền đàm phán ngắn hạn.
- Là bằng chứng buyer nghiêm túc trước khi seller mở tài liệu nhạy cảm.

Thông điệp chính:

> Cam kết trước, mở hồ sơ sau — không đánh cược chi phí thẩm định vào một buyer chưa ràng buộc gì.

---

### Quy tắc 6 — Các cổng phê duyệt bắt buộc

MVP thể hiện các cổng sau:

1. Seller approve Layer 1 teaser.
2. Buyer request identity / yêu cầu mở Layer 2.
3. VAULT record signed NDA.
4. Seller approve buyer mở Layer 2.
5. Buyer submit Indicative LOI trước VDR.
6. Legal approve Layer 3 access.
7. Legal approve cross-border data access.
8. Legal confirm VAULT does not hold money/shares.
9. Seller approve từng file Layer 3 cho buyer.

Không có chuyện buyer tự động xem Layer 2/Layer 3 chỉ vì đã quan tâm.

---

### Quy tắc 7 — VAULT có doanh thu từ giai đoạn chuẩn bị

Phí gói chuẩn bị được ghi nhận ngay khi Seller ký hợp đồng chuẩn hóa hồ sơ, không phụ thuộc deal sau này có đóng hay không.

Thông điệp chính:

> VAULT có doanh thu từ giai đoạn chuẩn bị, không chỉ ăn phí thành công — đây là điểm khác marketplace thuần túy.

---

### Quy tắc 8 — VAULT không giữ tiền giao dịch hoặc cổ phần

VAULT có thể theo dõi trạng thái escrow bên thứ ba, nhưng VAULT **không giữ tiền**, **không giữ cổ phần**, và **không đứng giữa dòng tiền mua bán vốn**.

Trong demo, Legal có bước xác nhận: “VAULT does not hold money/shares”.

---

### Quy tắc 9 — Matching là rule-based, không phải AI

MVP dùng scorecard theo quy tắc, không dùng AI matching.

Scorecard phải thể hiện:

- Tổng điểm phù hợp.
- Các tiêu chí cụ thể.
- Lý do match.
- 3 rủi ro/điểm chưa biết trước khi giới thiệu.

Thông điệp cần nói khi demo: VAULT kiểm soát lý do ghép nối, không dựa vào một mô hình AI hộp đen.

---

### Quy tắc 10 — Tech DD bắt đầu sau Indicative LOI và Layer 3/VDR

Tech DD chỉ bắt đầu sau khi buyer đã nộp Indicative LOI và Layer 3/VDR đã được mở đúng điều kiện.

Output MVP của Tech DD gồm:

- Finding/checklist.
- Severity.
- Remediation class.
- Chi phí hoặc tác động tới giao dịch.
- Reviewer sign-off.

MVP chưa cần report builder đầy đủ. Report builder là phase sau.

Các remediation class trong MVP:

1. Pre-closing must-fix.
2. 6-month fix.
3. Defer.
4. Growth investment.

---

### Quy tắc 11 — Finance theo dõi actuals, không sync Excel model

App không sync hai chiều với Excel model. Excel vẫn là mô hình tài chính/kế hoạch riêng.

Trong app, Finance theo dõi các sự kiện thực tế:

- Prep package fee.
- Success fee.
- Tech DD fee.
- Build-to-Buy opportunity.
- Invoice issued.
- Collected.
- Overdue.

---

### Quy tắc 12 — Khi nào một thương vụ được coi là hoàn tất A–Z

Một thương vụ demo được coi là hoàn tất khi đủ các bước:

1. Buyer request đã được tạo.
2. Seller profile đã được tạo.
3. Finance/VAULT ghi nhận prep package fee.
4. Seller approve Layer 1 teaser.
5. VAULT prepare match buyer–seller.
6. Buyer request identity.
7. VAULT record signed NDA.
8. Seller approve Layer 2 cho buyer.
9. Buyer submit Indicative LOI trước VDR.
10. Legal approve Layer 3.
11. Legal approve cross-border data access.
12. Legal confirm VAULT không giữ tiền/cổ phần.
13. Seller approve từng file Layer 3 cho buyer.
14. VAULT open approved VDR files.
15. Tech DD reviewer sign-off.
16. Buyer submit Definitive Offer.
17. Legal complete closing checklist.
18. VAULT mark SPA signed / deal closed.
19. Finance record success fee.
20. VAULT post-deal handoff to Rikkei.

---

## 3. Hướng dẫn demo một luồng hoàn chỉnh

### Chuẩn bị trước khi demo

1. Mở ứng dụng tại `#/investor-mvp`.
2. Bấm **Reset demo** để bắt đầu từ trạng thái sạch.
3. Nói rõ với người xem: đây là MVP dùng dữ liệu giả lập, chưa phải production cho dữ liệu mật thật.

---

### Bước 1 — Buyer tạo nhu cầu mua

Tab: **Buyer**

1. Chỉ cho người xem 4 trường Buyer Request.
2. Bấm **Lưu buyer request**.
3. Giải thích: VAULT bắt đầu từ nhu cầu thật của buyer, không bắt đầu bằng một kho hồ sơ đăng bán công khai.

Thông điệp chính:

> Buyer demand là điểm khởi đầu. VAULT không phải marketplace đăng tin hàng loạt.

---

### Bước 2 — Seller tạo hồ sơ doanh nghiệp

Tab: **Seller**

1. Chỉ cho người xem seller profile mẫu.
2. Bấm **Tạo seller profile từ sample data**.
3. Bấm **Approve L1 teaser**.
4. Giải thích: Seller kiểm soát những gì được đưa ra ngoài. Layer 1 là ẩn danh.

Thông điệp chính:

> Seller không bị lộ danh tính ngay từ đầu. VAULT chỉ mở thông tin theo lớp.

---

### Bước 2.5 — VAULT ghi nhận phí gói chuẩn bị

Tab: **Finance** hoặc **VAULT Admin**

1. Chuyển sang tab **Finance**.
2. Bấm **Record prep package fee**.
3. Giải thích: phí này thu ngay khi seller ký hợp đồng chuẩn hóa hồ sơ, không phụ thuộc deal sau này có đóng hay không.

Thông điệp chính:

> VAULT có doanh thu từ giai đoạn chuẩn bị, không chỉ ăn phí thành công — đây là điểm khác marketplace thuần túy.

---

### Bước 3 — VAULT chuẩn bị match

Tab: **VAULT Admin**

1. Chỉ task list theo role.
2. Chỉ matching score và lý do match.
3. Bấm **Prepare match buyer–seller**.
4. Giải thích: matching có tiêu chí, có lý do, có risk list.

Thông điệp chính:

> VAULT tạo một lời giới thiệu có kiểm soát, không gửi hồ sơ hàng loạt.

---

### Bước 4 — Buyer yêu cầu mở danh tính

Tab: **Buyer**

1. Chỉ rằng Layer 1 đã mở.
2. Bấm **Request identity / mở Layer 2**.
3. Giải thích: Buyer chỉ yêu cầu mở danh tính sau khi teaser ẩn danh đủ phù hợp.

Thông điệp chính:

> Layer 2 chỉ mở khi có nhu cầu cụ thể, không mở tự động.

---

### Bước 5 — VAULT ghi nhận NDA

Tab: **VAULT Admin**

1. Bấm **Record signed NDA**.
2. Giải thích: MVP hiện ghi nhận/upload signed NDA; e-sign integration là phase sau.

Thông điệp chính:

> NDA là cổng kỹ thuật/nghiệp vụ trước khi mở thông tin định danh.

---

### Bước 6 — Seller duyệt buyer mở Layer 2

Tab: **Seller**

1. Bấm **Approve buyer mở Layer 2**.
2. Giải thích: Seller duyệt từng buyer. Không phải buyer nào có NDA cũng tự động xem doanh nghiệp.

Thông điệp chính:

> Seller giữ quyền kiểm soát danh tính và thông tin định danh.

---

### Bước 6.5 — Buyer nộp thư quan tâm sơ bộ

Tab: **Buyer**

1. Bấm **Submit Indicative LOI (non-binding + đề nghị độc quyền đàm phán ngắn hạn)**.
2. Giải thích: trước khi VAULT mở toàn bộ VDR và bỏ chi phí làm Tech DD, buyer phải cam kết tối thiểu bằng văn bản.
3. Nói rõ bước này bảo vệ cả Seller và VAULT:
   - Seller không mở hồ sơ nhạy cảm cho buyer chưa nghiêm túc.
   - VAULT không đánh cược chi phí Tech DD vào buyer chưa ràng buộc gì.

Thông điệp chính:

> Cam kết trước, mở hồ sơ sau — không đánh cược chi phí thẩm định vào một buyer chưa ràng buộc gì.

---

### Bước 7 — Legal duyệt Layer 3 và cross-border data

Tab: **Legal**

1. Bấm **Approve Layer 3 access**.
2. Bấm **Approve cross-border data access**.
3. Bấm **Confirm VAULT does not hold money/shares**.
4. Giải thích: Legal xử lý các điểm rủi ro trước khi mở tài liệu nhạy cảm.

Thông điệp chính:

> VAULT kiểm soát pháp lý và dữ liệu trước khi mở VDR.

---

### Bước 8 — Seller duyệt file Layer 3

Tab: **Seller**

1. Bấm **Approve từng file Layer 3 cho buyer**.
2. Giải thích: Layer 3 không phải mở cả kho; mở theo file và theo buyer.

Thông điệp chính:

> File nhạy cảm chỉ mở đúng người, đúng phạm vi, đúng thời điểm.

---

### Bước 9 — VAULT mở VDR files

Tab: **VAULT Admin**

1. Bấm **Open approved VDR files**.
2. Giải thích: bản demo dùng local synthetic VDR. Production cần VDR/object storage thật, audit log, watermark, MFA, antivirus/file scan.

Thông điệp chính:

> MVP chứng minh flow; production sẽ thay local VDR bằng hạ tầng bảo mật phù hợp.

---

### Bước 10 — Tech DD review và sign-off

Tab: **Tech DD**

1. Chỉ bảng findings.
2. Giải thích các remediation class:
   - Pre-closing must-fix.
   - 6-month fix.
   - Defer.
   - Growth investment.
3. Bấm **Tech DD reviewer sign-off**.

Thông điệp chính:

> Tech DD là khác biệt của VAULT/Rikkei: biến rủi ro công nghệ thành chi phí và tác động giao dịch.

---

### Bước 11 — Buyer gửi Đề nghị chính thức (Definitive Offer)

Tab: **Buyer**

1. Bấm **Submit Definitive Offer**.
2. Giải thích: đây là đề nghị đã có đầy đủ thông tin từ VDR và Tech DD.
3. Nói rõ điểm khác biệt:
   - Indicative LOI ở bước 6.5 là cam kết sơ bộ trước khi mở hồ sơ nhạy cảm.
   - Definitive Offer ở bước 11 là đề nghị chính thức sau khi đã có thông tin thẩm định.

Thông điệp chính:

> Sau Tech DD, buyer không chỉ quan tâm nữa mà đưa ra đề nghị chính thức dựa trên dữ liệu đầy đủ.

---

### Bước 12 — Legal hoàn tất closing checklist

Tab: **Legal**

1. Bấm **Complete LOI/closing checklist**.
2. Giải thích: Legal vẫn đi cùng deal tới closing. MVP là checklist, chưa phải full legal document automation.

Thông điệp chính:

> Closing không chỉ là thao tác thương mại; phải có checklist pháp lý.

---

### Bước 13 — VAULT đánh dấu deal closed

Tab: **VAULT Admin**

1. Bấm **Mark SPA signed / deal closed**.
2. Giải thích: đây là trạng thái closing giả lập cho MVP.

Thông điệp chính:

> VAULT quản trị deal tới trạng thái đóng thương vụ, không chỉ tới lúc mở VDR.

---

### Bước 14 — Finance ghi nhận success fee và tổng hợp phí phát sinh khi đóng deal

Tab: **Finance**

1. Chỉ các dòng phí: prep package, success fee, Tech DD, Build-to-Buy opportunity.
2. Bấm **Record success fee**.
3. Giải thích: phí gói chuẩn bị đã ghi ở bước 2.5. Màn này chỉ tổng hợp thêm success fee/Tech DD/Build-to-Buy phát sinh khi đóng deal.
4. Nhắc lại: app tracking actuals; Excel vẫn là model kế hoạch.

Thông điệp chính:

> Finance nhìn được thương vụ chuyển thành phí thực tế, nhưng không gây hiểu lầm rằng mọi phí chỉ về khi deal thành công.

---

### Bước 15 — VAULT handoff sau giao dịch

Tab: **VAULT Admin**

1. Bấm **Post-deal handoff to Rikkei**.
2. Kiểm tra progress đạt 100%.
3. Kết luận demo.

Thông điệp chính:

> Sau closing, VAULT còn tạo cơ hội triển khai công nghệ/hậu giao dịch cho hệ sinh thái Rikkei, nhưng không cộng trùng doanh thu nếu chưa có hợp đồng riêng.

---

## 4. Kịch bản nói ngắn khi demo cho nhà đầu tư/đồng nghiệp

Có thể nói theo đoạn này:

> Đây là một thương vụ mẫu A–Z. Buyer Nhật bắt đầu bằng nhu cầu mua năng lực phần mềm kho vận. Seller Việt Nam tạo hồ sơ và kiểm soát thông tin theo 3 lớp. Ngay sau khi seller ký gói chuẩn hóa hồ sơ, VAULT đã ghi nhận phí gói chuẩn bị — tức là VAULT có doanh thu từ giai đoạn chuẩn bị, không chỉ ăn success fee. VAULT ghép hai bên bằng scorecard có lý do, không phải AI hộp đen. Trước khi mở VDR sâu, buyer phải nộp Indicative LOI sơ bộ để chứng minh mức nghiêm túc. Sau đó Legal kiểm Layer 3, cross-border data và xác nhận VAULT không giữ tiền/cổ phần. Tech DD đánh giá công nghệ và quy đổi rủi ro thành chi phí/tác động giao dịch. Khi đã có dữ liệu đầy đủ, buyer gửi Definitive Offer. Legal kiểm closing, Finance ghi nhận success fee, và VAULT handoff cơ hội sau giao dịch cho Rikkei. Đây là MVP dùng dữ liệu giả lập để chứng minh quy trình và vai trò của từng bên; chưa phải production cho dữ liệu thật.

---

## 5. Cách demo nhanh nếu thiếu thời gian

Nếu chỉ có vài phút:

1. Bấm **Reset demo**.
2. Giới thiệu 6 tab: Buyer, Seller, VAULT Admin, Legal, Tech DD, Finance.
3. Bấm **Hoàn tất mẫu**.
4. Chuyển từng tab để giải thích mỗi bên đã làm gì.
5. Nhấn mạnh: cùng một deal, cùng một trạng thái, nhiều bên phối hợp.
6. Nhấn riêng 2 điểm mới:
   - Prep package fee được ghi trước closing.
   - Indicative LOI phải có trước khi mở VDR/Tech DD.

Cách này phù hợp khi cần storytelling nhanh. Nếu muốn chứng minh sản phẩm có flow thật, nên đi theo toàn bộ các bước ở phần trên.

---

## 6. Những điều không được claim quá mức

Khi demo, không nói rằng MVP đã production-ready. Cần nói rõ:

- Dữ liệu đang là dữ liệu giả lập.
- Chưa dùng real Rikkei SSO.
- Chưa dùng MFA thật.
- Chưa dùng VDR provider thật.
- Chưa có watermark/audit/antivirus production-grade đầy đủ.
- Chưa dùng dữ liệu mật thật.
- Tech DD hiện là checklist/findings mẫu, chưa phải full report builder.
- Finance tracking là mô phỏng actuals, không sync Excel model.

Câu nên dùng:

> Đây là MVP chứng minh quy trình, vai trò và logic kiểm soát của VAULT. Trước khi dùng dữ liệu thật, cần hoàn thiện auth, MFA, audit log, VDR/storage production, watermark, antivirus/file scan, backup và retention policy.
