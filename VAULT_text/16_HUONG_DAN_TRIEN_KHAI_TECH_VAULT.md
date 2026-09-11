# HƯỚNG DẪN TRIỂN KHAI KỸ THUẬT DỰ ÁN VAULT
## Xử lý Hồ sơ Doanh nghiệp, Trust Profile, Virtual Data Room, Phân quyền Bảo mật & Khung Thẩm định Công nghệ (Tech DD)

---

### THÔNG TIN TÀI LIỆU KỸ THUẬT

| Hạng mục | Nội dung chi tiết |
| :--- | :--- |
| **Dự án** | **VAULT** (*Verified Access to Unlisted Listings & Transactions*) |
| **Căn cứ nghiệp vụ** | Báo cáo chiến lược `01_VAULT_REPORT.md` & Mô hình tài chính `04_VAULT_MODEL.xlsx` |
| **Đối tượng áp dụng** | Solution Architects, Tech Leads, Product Managers, Kỹ sư Bảo mật & Đội ngũ Chuyên gia Thẩm định Công nghệ (Tech DD) thuộc Rikkeisoft |
| **Phạm vi trọng tâm** | 4 Trụ cột Kỹ thuật: (1) Hồ sơ Doanh nghiệp & Trust Profile; (2) Phòng Dữ liệu Ảo (VDR); (3) Thỏa thuận Bảo mật & Ma trận Phân quyền; (4) Khung Thẩm định Công nghệ (Tech DD) |
| **Nguyên tắc kỹ thuật** | **Lean MVP – Bảo mật tối thượng – Thực dụng trong tích hợp (Build Core, Buy Commodity)** |

---

## 0. NGUYÊN TẮC CỐT LÕI DÀNH CHO ĐỘI NGŨ TECH

Trước khi bắt tay vào thiết kế hay viết mã, toàn bộ đội ngũ kỹ thuật phải thống nhất 4 nguyên lý sống còn của hệ thống VAULT:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       4 NGUYÊN LÝ KỸ THUẬT BẤT BIẾN                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. TECH VỪA LÀ NỀN TẢNG (PLATFORM) VỪA LÀ DỊCH VỤ CỐT LÕI (TECH DD SERVICE) │
│    Hệ thống phần mềm chỉ là công cụ hỗ trợ. Năng lực "đọc vị" mã nguồn,     │
│    kiến trúc hệ thống và quy đổi rủi ro kỹ thuật thành tiền mới là vũ khí   │
│    cạnh tranh giúp VAULT vượt qua các đối thủ tư vấn tài chính truyền thống.│
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. TRIẾT LÝ BUILD VS BUY: KHÔNG PHÁT MINH LẠI BÁNH XE                       │
│    - BUY/INTEGRATE: Virtual Data Room (VDR), Chữ ký số điện tử (e-Sign),    │
│      Hạ tầng lưu trữ đám mây (Cloud), Công cụ quét mã nguồn tĩnh (SAST/SCA).│
│    - BUILD: Cấu trúc dữ liệu hồ sơ (Data Schema), Cơ chế phân lớp dữ liệu   │
│      (Trust Profile Engine), Thuật toán ghép nối (Matching) & Workflow.     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. CHỈ SỐ HÓA NHỮNG GÌ ĐÃ VẬN HÀNH THỦ CÔNG ỔN ĐỊNH                         │
│    Trong Giai đoạn Chứng minh (Proof Phase – Cổng 1 đến Cổng 4), ưu tiên     │
│    sử dụng bảng biểu chuẩn hóa, quy trình có kiểm soát (Excel/Google Sheet  │
│    bảo mật cao, dịch vụ SaaS chuyên dụng) trước khi viết code phức tạp.     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. ZERO-TRUST & DEFENSE-IN-DEPTH (BẢO MẬT PHÂN TẦNG ĐỘC LẬP)                │
│    Dữ liệu rò rỉ là án tử cho thương vụ M&A. Hệ thống phải bảo đảm: dù lộ   │
│    thông tin Lớp 1 cũng không thể truy ra Lớp 2; truy cập Lớp 3 phải được   │
│    chấp thuận kép (Dual-Approval) và đóng dấu thủy vân vết danh tính.       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PHẦN 1: HỒ SƠ DOANH NGHIỆP & CƠ CHẾ TRUST PROFILE

### 1.1. Cấu trúc Mô hình Dữ liệu (Data Schema & Ingestion)

Mọi thông tin doanh nghiệp đưa vào hệ thống phải được chuẩn hóa thành các thực thể dữ liệu có định danh, nguồn gốc và trạng thái xác minh.

```
                    MÔ HÌNH THỰC THỂ DỮ LIỆU VAULT
 ┌──────────────────────┐        ┌──────────────────────┐
 │    CompanyProfile    │───1:N──│   FinancialRecord    │ (Doanh thu, EBITDA, Nợ ròng)
 └──────────┬───────────┘        └──────────────────────┘
            │
            ├───1:N──┌──────────────────────┐
            │        │     LegalRecord      │ (Giấy phép, Cổ đông, Tranh chấp)
            │        └──────────────────────┘
            │
            ├───1:N──┌──────────────────────┐
            │        │   TechAssetRecord    │ (Repo, Kiến trúc, Tech Stack)
            │        └──────────────────────┘
            │
            └───1:1──┌──────────────────────┐
                     │     TrustProfile     │ (Cơ chế phân lớp 1 - 2 - 3)
                     └──────────────────────┘
```

#### 3 Trạng thái Kiểm tra Bắt buộc cho từng Dữ kiện (Data Verification Status)
Mỗi trường thông tin (Field-level Metadata) phải gắn 1 trong 3 nhãn sau:

| Nhãn Trạng thái | Mã | Ý nghĩa kỹ thuật | Bằng chứng kiểm tra kèm theo |
| :--- | :---: | :--- | :--- |
| **Self-Reported** | `VER_01` | Dữ liệu do bên bán tự kê khai trên biểu mẫu | Form nhập liệu, email từ Founder |
| **Document-Verified** | `VER_02` | Đã được Chuyên viên VAULT đối soát với hồ sơ gốc | Bản chụp Báo cáo tài chính nội bộ, Hợp đồng kinh tế |
| **Audited / Certified** | `VER_03` | Đã được xác nhận bởi bên thứ ba độc lập có thẩm quyền | Báo cáo kiểm toán độc lập (Big4/Hãng kiểm toán), Giấy chứng nhận ĐKKD |

> **Quy tắc hiển thị UI/UX:** Tuyệt đối **không** gắn nhãn "Đã kiểm toán" cho toàn bộ hồ sơ công ty. Nhãn `VER_03` chỉ được hiển thị ở đúng các trường số liệu được ghi nhận trong Báo cáo kiểm toán có đóng dấu pháp lý.

---

### 1.2. Cơ chế Sinh Hồ sơ 3 Phân tầng (Trust Profile Generator)

Trust Profile là bộ lọc tự động phân chia dữ liệu doanh nghiệp thành 3 lớp thông tin, giải quyết triệt để rủi ro rò rỉ bí mật kinh doanh:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     KIẾN TRÚC PHÂN LỚP DỮ LIỆU TRUST PROFILE                │
├─────────────────────────────────────────────────────────────────────────────┤
│  LỚP 1: BLIND TEASER (Bản giới thiệu ẩn danh)                               │
│  - Thuật toán Masking & Generalization tự động che giấu định danh.          │
│  - Phân quyền: Công khai có kiểm soát cho Buyer đã xác thực (Level 1).      │
├─────────────────────────────────────────────────────────────────────────────┤
│  LỚP 2: CONFIDENTIAL INFORMATION MEMORANDUM (CIM - Hồ sơ định danh)         │
│  - Mở tên pháp nhân, báo cáo tóm tắt 3 năm, sản phẩm cụ thể.                │
│  - Phân quyền: Cần ký NDA + Bên bán DUYỆT ĐÍCH DANH (Level 2).              │
├─────────────────────────────────────────────────────────────────────────────┤
│  LỚP 3: VIRTUAL DATA ROOM (Phòng dữ liệu chuyên sâu)                        │
│  - Toàn bộ tài liệu mật: Hợp đồng, Mã nguồn, Bảng lương, Báo cáo thuế.     │
│  - Phân quyền: Đang thẩm định chính thức + Phê duyệt 2 bước (Level 3).       │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Chi tiết Kỹ thuật Phân tầng Dữ liệu:

| Nhóm thông tin | Lớp 1: Blind Teaser (Ẩn danh) | Lớp 2: CIM (Định danh có NDA) | Lớp 3: VDR (Thẩm định sâu) |
| :--- | :--- | :--- | :--- |
| **Tên & Pháp nhân** | *"Doanh nghiệp phần mềm kho vận B2B"* (Masked) | Tên đầy đủ, Mã số thuế, Năm thành lập | Toàn bộ Giấy phép ĐKKD, Điều lệ, Biên bản họp HĐQT |
| **Địa bàn hoạt động** | *"Vùng kinh tế Đông Nam Bộ"* (Không nêu tỉnh cụ thể nếu chỉ có 1 đối thủ) | Tỉnh/Thành phố, Địa chỉ văn phòng chính | Bản vẽ mặt bằng, Hợp đồng thuê trụ sở/nhà xưởng |
| **Tài chính** | Doanh thu quy về dải: `50 - 100 tỷ VNĐ`; Biên EBITDA: `15 - 20%` | Bảng P&L tóm tắt 3 năm gần nhất, Nợ vay ngân hàng | Sổ phụ ngân hàng, Tờ khai thuế VAT/TNDN, Chi tiết công nợ |
| **Khách hàng** | Phân loại theo ngành: *"Hơn 40 khách hàng nhà máy chế tạo điện tử"* | Danh sách Top 10 khách hàng mã hóa tên (Client A, B...) | Toàn bộ Hợp đồng thương mại gốc, Phụ lục đơn giá |
| **Tài sản Công nghệ** | Ngôn ngữ/Tech Stack chính: `Java, React, AWS, On-premise` | Danh mục Module sản phẩm, Sơ đồ khối kiến trúc hệ thống | Báo cáo quét mã nguồn, Quyền truy cập Repo Git (Read-only), API Docs |
| **Nhân sự & Lương** | Quy mô nhân sự: `50 - 100 nhân sự` | Cơ cấu tổ chức (Org Chart), Hồ sơ ban điều hành | Bảng lương chi tiết từng nhân sự, Hợp đồng lao động, NDA nhân viên |

#### Quy tắc Kỹ thuật chống "Nhận diện ngược" (De-identification & Anti-Reidentification Rules):
1. **Quy tắc K-Anonymity cho Teaser (Lớp 1):** Nếu một doanh nghiệp có đặc điểm quá độc tôn trong một tỉnh (ví dụ: công ty phần mềm duy nhất tại một tỉnh miền núi có doanh thu >50 tỷ), hệ thống phải tự động nâng cấp mức khái quát địa lý lên cấp Vùng (ví dụ: *"Khu vực Trung du & Miền núi phía Bắc"*).
2. **Làm mờ số liệu (Range Binning):** Doanh thu và lợi nhuận tại Lớp 1 tuyệt đối không để số lẻ. Bắt buộc làm tròn thành các dải chuẩn: `20–50 tỷ`, `50–100 tỷ`, `100–200 tỷ`, `200–500 tỷ VNĐ`.
3. **Kiểm duyệt tự động văn bản (Text Sanitization):** Quét và tự động lọc bỏ các từ khóa thương hiệu riêng, tên sản phẩm độc quyền, tên khách hàng lớn xuất hiện trong phần mô tả chung của Teaser.

---

## PHẦN 2: THIẾT KẾ VÀ TÍCH HỢP VIRTUAL DATA ROOM (VDR)

### 2.1. Chiến lược Tích hợp: Build vs Buy

Việc tự xây dựng một phòng dữ liệu VDR đạt chuẩn quốc tế từ đầu đòi hỏi chi phí bảo mật cực lớn và mất ít nhất 9–12 tháng. Do đó, Tech áp dụng chiến lược **Hybrid-Buy**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KIẾN TRÚC HYBRID VDR                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  [ LỚP TRẢI NGHIỆM - BUILT BY VAULT ]                                       │
│  - Portal quản lý giao dịch, Danh mục thương vụ, Cổng duyệt mở quyền.       │
│  - Tích hợp qua REST API / Webhook.                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  [ LỚP DỮ LIỆU & BẢO MẬT - COMMODITY VDR ENGINE ]                           │
│  - Giai đoạn Cổng 1 - 2: Sử dụng Google Workspace Enterprise bảo mật cao     │
│    (Chặn tải, chặn in, phân quyền Folder, mã hóa ổ đĩa).                    │
│  - Giai đoạn Cổng 3 - 4 & Thương mại: Tích hợp SaaS VDR chuyên nghiệp       │
│    (iDeals, ShareVault, Digify hoặc AWS S3 + Dynamic DRM Viewer).           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2. Cấu trúc Cây Thư mục Chuẩn Hóa cho VDR (Standard M&A Data Room Index)

Mọi VDR khởi tạo cho một thương vụ M&A tại VAULT phải tuân thủ đúng cấu trúc 6 thư mục gốc (Root Folders) sau:

```
VDR_[Deal_Code]_[Company_Alias]/
├── 01_LEGAL_&_CORPORATE/             # Hồ sơ Pháp lý & Tư cách Doanh nghiệp
│   ├── 01.1_Incorporation_Docs/       # ĐKKD, Điều lệ các lần sửa đổi
│   ├── 01.2_Shareholder_Register/    # Sổ cổ đông, Danh sách góp vốn
│   ├── 01.3_Board_Resolutions/       # Biên bản họp & Nghị quyết ĐHĐCĐ/HĐQT
│   └── 01.4_Material_Contracts/      # Hợp đồng trọng yếu, Vay nợ, Thế chấp
├── 02_FINANCIAL_&_TAX/               # Hồ sơ Tài chính & Thuế
│   ├── 02.1_Audited_FS_3_Years/      # Báo cáo kiểm toán 3 năm gần nhất
│   ├── 02.2_Monthly_Management_P&L/  # Báo cáo quản trị nội bộ 12 tháng qua
│   ├── 02.3_Tax_Filings_&_Finals/    # Quyết toán thuế, Biên bản thanh tra thuế
│   └── 02.4_Debt_&_Bank_Statements/  # Sao kê tài khoản, Khế ước nhận nợ
├── 03_COMMERCIAL_&_OPERATIONS/       # Hồ sơ Kinh doanh & Vận hành
│   ├── 03.1_Customer_Contracts/      # Hợp đồng khách hàng (Masked tên nếu cần)
│   ├── 03.2_Supplier_Agreements/     # Hợp đồng nhà cung cấp linh kiện/dịch vụ
│   └── 03.3_Standard_Operating_SOP/  # Quy trình vận hành, Chứng chỉ ISO
├── 04_TECHNOLOGY_&_IP/               # Hồ sơ Công nghệ & Sở hữu Trí tuệ (TECH CORE)
│   ├── 04.1_Architecture_&_Design/   # Sơ đồ kiến trúc phần mềm, CSDL, Dataflow
│   ├── 04.2_Source_Code_Audits/      # Báo cáo quét bảo mật, Báo cáo SonarQube
│   ├── 04.3_Open_Source_Licenses/    # Danh mục thư viện OSS (Software BOM)
│   ├── 04.4_IP_Patents_Copyrights/   # Bằng sáng chế, Giấy chứng nhận bản quyền
│   └── 04.5_Infra_&_DevOps_Specs/    # Cấu hình Cloud AWS/GCP, Quy trình CI/CD
├── 05_HUMAN_RESOURCES/               # Hồ sơ Nhân sự & Tổ chức
│   ├── 05.1_Org_Chart_&_Key_Bios/    # Sơ đồ tổ chức, CV nhân sự chủ chốt
│   ├── 05.2_Labor_Contracts_Sample/  # Mẫu hợp đồng lao động, Thỏa thuận NDA/NCA
│   └── 05.3_Payroll_&_Comp_Summary/  # Bảng lương tóm tắt, Chính sách ESOP
└── 06_Q&A_TRACKER/                   # Nhật ký hỏi đáp thẩm định (Q&A Log)
```

### 2.3. Các Tính năng Kỹ thuật Bắt buộc của VDR (Mandatory Security Features)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       YÊU CẦU BẢO MẬT KỸ THUẬT VDR                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. DYNAMIC WATERMARKING (Thủy vân động theo thời gian thực)                 │
│    Mọi tài liệu PDF, hình ảnh hiển thị trên trình duyệt phải được phủ       │
│    watermark chìm bán trong suốt: "CONFIDENTIAL - [User_Email] - [User_IP]  │
│    - [Timestamp_UTC] - ACCESS FOR DUE DILIGENCE ONLY".                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. DRM & RESTRICTED ACCESS (Chống tải & sao chép)                           │
│    - Chặn chức năng Copy/Paste văn bản trên trình xem.                      │
│    - Vô hiệu hóa tính năng In ấn (Print) và Chụp màn hình (Screen capture)   │
│      ở mức tối đa mà trình duyệt cho phép.                                  │
│    - Quyền "Chỉ xem trên web" (View-only via HTML5 Sandbox viewer) là mặc   │
│      định. Quyền Tải tệp (Download) phải được cấp riêng từng tài liệu.      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. REMOTE ACCESS REVOCATION (Thu hồi quyền từ xa)                           │
│    Khi người dùng hết hạn quyền truy cập hoặc bị khóa tài khoản, toàn bộ    │
│    phiên làm việc lập tức bị hủy bỏ (Token Revocation).                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. GRANULAR AUDIT LOGGING (Ghi nhật ký chi tiết)                            │
│    Ghi nhận log bất biến (Immutable Audit Trail) cho từng thao tác:         │
│    User nào, mở tệp nào, xem trang mấy, trong bao nhiêu giây, từ địa chỉ    │
│    IP nào, bằng thiết bị gì. Xuất log phục vụ tranh chấp pháp lý.           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PHẦN 3: THỎA THUẬN BẢO MẬT (NDA) & MA TRẬN PHÂN QUYỀN

### 3.1. Luồng Tự động hóa Ký kết Bảo mật (e-Sign Integration Workflow)

Bảo mật không thể thực hiện bằng "lời hứa". Hệ thống phải thiết lập luồng chặn cứng kỹ thuật (Technical Gatekeeper):

```
 [ Buyer quan tâm Deal ]
          │
          ▼
 [ Trình ký NDA điện tử ] ──► (Tích hợp DocuSign / Adobe Sign / FPT.eSign)
          │
          ├───► Buyer ký số (Xác thực SMS OTP / Email OTP / Chữ ký số)
          │
          ▼
 [ Lưu trữ bản NDA có chữ ký điện tử hợp pháp ]
          │
          ├───► Ghi nhận mã băm tài liệu (SHA-256 Hash) vào Audit Log
          │
          ▼
 [ BÊN BÁN DUYỆT (Dual Approval Gate) ]
          │
          ├───► Bên bán nhấn "Chấp thuận mở Lớp 2 cho Bên mua X"
          │
          ▼
 [ KÍCH HOẠT QUYỀN MỞ LỚP 2 TỰ ĐỘNG ]
 (Hệ thống tự động cấp Token truy cập CIM trong thời hạn 14 ngày)
```

---

### 3.2. Ma trận Phân quyền Theo Vai trò (Role-Based Access Control - RBAC)

Hệ thống thiết lập 6 vai trò tiêu chuẩn với ma trận quyền hạn tuyệt đối như sau:

| Đối tượng / Vai trò | Xem Lớp 1 (Teaser) | Ký NDA | Xem Lớp 2 (CIM) | Xem Lớp 3 (VDR Docs) | Xem Mã nguồn (Repo) | Duyệt mở quyền | Xem Nhật ký Audit Log |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Guest / Unverified Buyer** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Verified Buyer (Đã xác minh)**| ✅ | ✅ | ❌ (Chờ ký NDA) | ❌ | ❌ | ❌ | ❌ |
| **NDA Signed Buyer (Đang DD)** | ✅ | ✅ | ✅ | ✅ (Chỉ xem) | ❌ | ❌ | ❌ |
| **Seller Admin (Chủ sở hữu)** | ✅ | ❌ | ✅ | ✅ (Toàn quyền) | ✅ | ✅ (Duyệt mở) | ✅ (Xem log của deal mình) |
| **VAULT Deal Lead** | ✅ | ✅ | ✅ | ✅ (Điều phối) | ❌ | ❌ | ✅ |
| **Rikkei Tech DD Specialist** | ✅ | ❌ | ✅ | ✅ (Xem kỹ thuật)| ✅ (Audit tool)| ❌ | ✅ |
| **VAULT Security Admin** | ✅ | ❌ | ❌ | ❌ (Không can thiệp)| ❌ | ✅ (Cấp quyền) | ✅ (Toàn quyền hệ thống) |

> **Nguyên tắc "Bốn con mắt" (Two-Person Rule):**
> Quyền truy cập Lớp 3 (VDR) của một bên mua không bao giờ do một cá nhân tự quyết định. Phải có đủ **2 chữ ký số phê duyệt trên hệ thống**:
> 1. Chữ ký chấp thuận của **Chủ doanh nghiệp bên bán (Seller)**.
> 2. Chữ ký xác nhận đủ điều kiện pháp lý của **Bộ phận Pháp lý & Tuân thủ VAULT (Compliance Officer)**.

---

## PHẦN 4: KHUNG THẨM ĐỊNH CÔNG NGHỆ (TECH DUE DILIGENCE PLAYBOOK)

Thẩm định công nghệ là năng lực tạo ra sự khác biệt sống còn của VAULT. Đội ngũ Tech Rikkeisoft cần chuẩn hóa quy trình thẩm định từ trực giác cá nhân thành **Khung đánh giá định lượng 6 trục chuẩn mực**.

```
                   6 TRỤC THẨM ĐỊNH CÔNG NGHỆ CỐT LÕI (TECH DD)
 ┌──────────────────────────────────────┬──────────────────────────────────────┐
 │ 1. KIẾN TRÚC & NĂNG LỰC MỞ RỘNG      │ 2. CHẤT LƯỢNG CODE & NỢ KỸ THUẬT     │
 │    (Architecture & Scalability)      │    (Code Quality & Technical Debt)   │
 ├──────────────────────────────────────┼──────────────────────────────────────┤
 │ 3. AN TOÀN THÔNG TIN & BẢO VỆ DỮ LIỆU│ 4. BẢN QUYỀN IP & THƯ VIỆN NGUỒN MỞ  │
 │    (Security & Data Privacy)         │    (IP Rights & OSS Compliance)      │
 ├──────────────────────────────────────┼──────────────────────────────────────┤
 │ 5. PHỤ THUỘC ĐỘI NGŨ & CON NGƯỜI     │ 6. CHI PHÍ TÍCH HỢP HỆ THỐNG POST-DEAL│
 │    (Key-Person Risk & Team Agility)  │    (Post-Deal Integration Cost)      │
 └──────────────────────────────────────┴──────────────────────────────────────┘
```

---

### 4.1. Chi tiết 6 Trục Thẩm định & Bộ Công cụ Đo kiểm

#### Trục 1: Kiến trúc Hệ thống & Khả năng Mở rộng (Architecture & Scalability)
- **Hạng mục kiểm tra:**
  - Mô hình kiến trúc: Monolithic, Microservices, Event-driven hay Serverless? Có tách biệt Frontend, Backend và Database không?
  - Khả năng chịu tải: Điểm nghẽn (Bottleneck) nằm ở đâu khi số lượng người dùng đồng thời (CCU) tăng gấp 5 lần?
  - Cơ chế dự phòng (High Availability) và Kế hoạch khắc phục sự cố (Disaster Recovery - RPO, RTO).
- **Công cụ kỹ thuật sử dụng:** Phân tích sơ đồ kiến trúc, kịch bản kiểm thử tải (Apache JMeter, k6), rà soát cấu hình hạ tầng Terraform/CloudFormation.

#### Trục 2: Chất lượng Mã nguồn & Nợ Kỹ thuật (Code Quality & Technical Debt)
- **Hạng mục kiểm tra:**
  - Tỷ lệ trùng lặp code (Code Duplication), độ phức tạp mã nguồn (Cyclomatic Complexity).
  - Độ bao phủ kiểm thử tự động (Unit Test / Integration Test Coverage). Ngưỡng chấp nhận: Test coverage > 60%.
  - Mức độ tài liệu hóa (Documentation): Có Swagger/OpenAPI cho API không? Code có chuẩn Clean Code không?
- **Công cụ kỹ thuật sử dụng:** **SonarQube Enterprise** (quét chỉ số Maintainability, Bugs, Code Smells), SonarLint.

#### Trục 3: Bản quyền Sở hữu Trí tuệ (IP) & Tuân thủ Mã nguồn mở (OSS Compliance)
- **Hạng mục kiểm tra:**
  - Kiểm tra xem sản phẩm có đang sử dụng các thư viện mã nguồn mở "dính virus bản quyền" (Copyleft licenses như **GPL v2/v3, AGPL**) hay không. *Nếu một phần mềm thương mại đóng gói vô tình nhúng thư viện AGPL, bên mua có nguy cơ bị buộc phải mở toàn bộ mã nguồn ra cộng đồng.*
  - Kiểm tra điều khoản chuyển giao quyền sở hữu trí tuệ giữa công ty và các kỹ sư lập trình (hợp đồng lao động, hợp đồng thầu phụ outsource).
- **Công cụ kỹ thuật sử dụng:** **Snyk Open Source**, **Black Duck**, **FOSSA** (quét Software Bill of Materials - SBOM).

#### Trục 4: An toàn Thông tin & Bảo vệ Dữ liệu Cá nhân (Cybersecurity & Data Privacy)
- **Hạng mục kiểm tra:**
  - Kiểm tra lỗ hổng bảo mật ứng dụng theo chuẩn OWASP Top 10 (SQL Injection, XSS, Broken Auth...).
  - Mã hóa dữ liệu: Dữ liệu nhạy cảm có được mã hóa khi lưu trữ (At-Rest - AES 256) và khi truyền tải (In-Transit - TLS 1.3) không?
  - Quản lý định danh và truy cập (IAM): Có phân quyền RBAC và xác thực 2 lớp (2FA) cho tài khoản quản trị không?
  - Tuân thủ Luật Bảo vệ dữ liệu cá nhân Việt Nam (Nghị định 356/2025/NĐ-CP) và chuẩn bị cho việc truyền dữ liệu xuyên biên giới sang Nhật Bản.
- **Công cụ kỹ thuật sử dụng:** **OWASP ZAP**, **Burp Suite Professional**, **Trivy** (quét lỗ hổng Container/Docker), AWS Security Hub.

#### Trục 5: Mức độ Phụ thuộc Nhân sự Chủ chốt (Key-Person Dependency)
- **Hạng mục kiểm tra:**
  - Phân tích đóng góp mã nguồn (Git Commit History): Có hiện tượng 80% mã nguồn chỉ do 1–2 cá nhân viết và nắm giữ không?
  - Mức độ chuẩn hóa quy trình onboarding kỹ sư mới: Mất bao lâu để một lập trình viên mới vào có thể build và release được code?
  - Rủi ro thất thoát tri thức (Bus Factor Analysis): Nếu CTO nghỉ việc, hệ thống có vận hành được tiếp không?
- **Công cụ kỹ thuật sử dụng:** GitPrime, GitKraken Insights, Phỏng vấn trực tiếp 1-on-1 với Tech Lead bên bán.

#### Trục 6: Dự toán Chi phí Tích hợp Sau Giao dịch (Post-deal Integration Costing)
- **Hạng mục kiểm tra:**
  - Dự toán khối lượng công việc kết nối hệ thống của doanh nghiệp mục tiêu với hệ thống của Bên mua Nhật Bản: Đồng bộ ERP (SAP/Oracle), chuẩn hóa API Gateway, Single Sign-On (SSO).
  - Bản địa hóa ngôn ngữ: Chuyển đổi giao diện, tài liệu vận hành và hệ thống cảnh báo sang tiếng Nhật/tiếng Anh.

---

### 4.2. Khung Báo cáo Kết quả Tech DD & Mô hình Lượng hóa Chi phí Khắc phục (Remediation Cost Model)

Kết quả cuối cùng của Tech DD **không phải là bản liệt kê lỗi kỹ thuật thuần túy**, mà là một Báo cáo Chiến lược kèm **Bảng quy đổi chi phí lượng hóa bằng tiền (Remediation Budget)**.

#### Bảng Mẫu Lượng hóa Chi phí Khắc phục Kỹ thuật trong Báo cáo Tech DD:

| Hạng mục phát hiện | Mức độ rủi ro | Phân loại chi phí | Hành động khắc phục đề xuất | Dự toán chi phí (Triệu VNĐ) | Đề xuất xử lý trong Đàm phán M&A |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **Nhúng thư viện AGPL v3 vào module lõi** | **Critical (P0)** | Chi phí đầu tư sửa chữa (CAPEX) | Viết lại toàn bộ module bằng thư viện giấy phép MIT (Ước tính 3 người-tháng) | **180** | **Điều kiện tiên quyết trước khi ký (Condition Precedent): Bên bán bắt buộc phải sửa xong mới giải ngân** |
| **Không có hệ thống sao lưu dự phòng tự động (Backup/DR)** | **High (P1)** | Chi phí đầu tư sửa chữa (CAPEX) | Thiết lập kiến trúc Multi-AZ trên AWS, cấu hình snapshot tự động | **70** | **Trừ lùi trực tiếp vào Giá mua cổ phần (Price Deduction)** |
| **Nợ kỹ thuật: Test coverage chỉ đạt 15%** | **Medium (P2)** | Chi phí vận hành tăng thêm (OPEX) | Bổ sung chuyên viên QA viết bổ sung Unit Test trong 6 tháng đầu sau sáp nhập | **120** | **Đưa vào Kế hoạch tích hợp 100 ngày đầu sau đầu tư (Post-deal 100-day Plan)** |
| **Thiếu chứng chỉ mã hóa dữ liệu người dùng** | **High (P1)** | Chi phí đầu tư sửa chữa (CAPEX) | Nâng cấp TLS 1.3, triển khai mã hóa AES-256 cho CSDL | **50** | **Trừ lùi trực tiếp vào Giá mua cổ phần** |
| **TỔNG CHI PHÍ KHẮC PHỤC** | | | | **420** | **Căn cứ đàm phán trừ lùi 300 triệu VNĐ vào định giá vốn** |

---

## PHẦN 5: LỘ TRÌNH TRIỂN KHAI VÀ PHÂN KỲ KỸ THUẬT (TECH ROADMAP)

Để đồng bộ hoàn hảo với mô hình giải ngân theo 4 Cổng tại `01_VAULT_REPORT.md`, kế hoạch hành động của Tech được chia làm 3 chặng cụ thể:

```
                  LỘ TRÌNH KỸ THUẬT THEO CỔNG KIỂM SOÁT
 ─────────────────────────────────────────────────────────────────────────────
  [ CHẶNG 1: CỔNG 1 & 2 ]   ► BẢO MẬT & MẪU BIỂU LEAN (Proof of Concept)
  (Tháng 1 - Tháng 7)         - Thiết lập bộ form Buyer Brief & Seller Intake chuẩn.
                              - Quy chuẩn Google Workspace Enterprise bảo mật cao.
                              - Ban hành Tech DD Checklist v1.0.
                              - Ngân sách Tech: ~90 triệu VNĐ.
 ─────────────────────────────────────────────────────────────────────────────
  [ CHẶNG 2: CỔNG 3 & 4 ]   ► TÍCH HỢP NỀN TẢNG VDR & AUTOMATION (MVP Pilot)
  (Tháng 8 - Tháng 15)        - Mua bản quyền SaaS VDR bảo mật chuyên nghiệp.
                              - Triển khai Dynamic Watermark & e-Sign tự động.
                              - Thực hiện 03 Báo cáo Tech DD thực địa đầu tiên.
                              - Ngân sách Tech: ~150 triệu VNĐ.
 ─────────────────────────────────────────────────────────────────────────────
  [ CHẶNG 3: GIAI ĐOẠN VẬN HÀNH THƯƠNG MẠI ] ► SỐ HÓA TOÀN DIỆN (Scale-up)
  (Tháng 16 - Tháng 60)       - Hoàn thiện cổng VAULT Portal nội bộ (React + Python/Node).
                              - Tự động hóa Matching Engine dựa trên dữ liệu.
                              - Đội ngũ Tech DD chuyên trách phục vụ 10–15 deal/năm.
 ─────────────────────────────────────────────────────────────────────────────
```

### Kế hoạch Hành động Ngay trong 30 Ngày Đầu tiên:

- [ ] **Đầu việc 1 (Ngày 1–7):** Ban hành bộ biểu mẫu thu thập dữ liệu chuẩn:
  - `Buyer_Brief_Form.xlsx` (Phiếu 6 tiêu chí xác thực người mua Nhật).
  - `Seller_Intake_TrustProfile.xlsx` (Phiếu khai báo và gắn nhãn 3 trạng thái dữ liệu).
- [ ] **Đầu việc 2 (Ngày 8–15):** Thiết lập môi trường VDR dùng thử (Sandbox VDR) đáp ứng tiêu chuẩn Dynamic Watermark và chặn tải file.
- [ ] **Đầu việc 3 (Ngày 16–22):** Hoàn thiện và ban hành quy trình nội bộ: `Tech_DD_Standard_Playbook_v1.0.pdf` kèm Bảng tính lượng hóa chi phí khắc phục.
- [ ] **Đầu việc 4 (Ngày 23–30):** Tiến hành diễn tập (Dry-run Test) quy trình thẩm định công nghệ giả lập trên 01 sản phẩm nội bộ của Rikkeisoft để đo lường số giờ công thực tế.

---

### KẾT LUẬN

Tài liệu này xác lập kim chỉ nam rõ ràng cho đội ngũ công nghệ: **Chúng ta không xây dựng một hệ thống phần mềm cồng kềnh để phô trương, mà xây dựng một cỗ máy bảo mật nghiêm ngặt và một quy trình thẩm định công nghệ chuẩn xác.**

Bằng việc kết hợp hài hòa giữa các công cụ sẵn có trên thị trường và năng lực kỹ thuật đỉnh cao của các kỹ sư Rikkeisoft, khối Tech sẽ trở thành đòn bẩy vững chắc nhất giúp VAULT hoàn thành xuất sắc sứ mệnh kết nối dòng vốn đầu tư Nhật Bản cho các doanh nghiệp Việt Nam.
