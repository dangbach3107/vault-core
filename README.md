# VAULT Core Engine — MVP Framework
> **Verified Access to Unlisted Listings & Transactions**  
> *Nền tảng kết nối vốn và thẩm định công nghệ M&A trong hệ sinh thái Rikkeisoft*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=Python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-MVP%20Ready-emerald.svg)]()

---

## 📖 GIỚI THIỆU TỔNG QUAN

**VAULT Core Engine** là khung mã nguồn mở đầu (MVP Framework) được thiết kế cho Giai đoạn Chứng minh (Proof Phase – Cổng 1 đến Cổng 4) của dự án VAULT thuộc hệ sinh thái **Rikkeisoft**.

Thay vì xây dựng các cổng thông tin cồng kềnh, repo này tập trung giải quyết **4 bài toán kỹ thuật cốt tử** trong các thương vụ M&A giữa doanh nghiệp Việt Nam và nhà đầu tư chiến lược Nhật Bản:

```
                  4 TRỤ CỘT KỸ THUẬT LÕI CỦA VAULT CORE
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ 1. TRUST PROFILE ENGINE (Khử định danh & Phân tầng dữ liệu)                 │
 │    - Tự động làm mờ số liệu (Range Binning) và khái quát địa lý (K-Anonymity)│
 │    - Xuất bản hồ sơ 3 phân tầng: Blind Teaser (Lớp 1) và CIM (Lớp 2).       │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ 2. SECURE VIRTUAL DATA ROOM (Phòng dữ liệu ảo an toàn - VDR)                │
 │    - Chuẩn hóa cây thư mục 6 phân hệ M&A (Pháp lý, Tài chính, Vận hành...).  │
 │    - Dynamic Watermarking theo thời gian thực (Email + IP + Timestamp UTC). │
 │    - Chế độ View-only DRM: Chặn chuột phải, chặn in ấn (Ctrl+P) và tải file.│
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ 3. NDA & TWO-PERSON APPROVAL GATE (Quy tắc Bốn con mắt)                     │
 │    - Tích hợp ký số e-Sign thỏa thuận bảo mật NDA (mã băm SHA-256).         │
 │    - Quyền mở Lớp 2/3 chỉ mở khi cả Founder Bên bán và Pháp chế cùng DUYỆT.  │
 ├─────────────────────────────────────────────────────────────────────────────┤
 │ 4. TECH DUE DILIGENCE ENGINE (Thẩm định công nghệ 6 trục độc quyền)         │
 │    - Đánh giá kiến trúc, chất lượng code, bản quyền mã nguồn mở (AGPL/GPL). │
 │    - Bảng lượng hóa chi phí khắc phục (Remediation Cost Model) tính bằng     │
 │      tiền VNĐ làm căn cứ đàm phán trừ lùi giá mua cổ phần.                  │
 └─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 KHỞI ĐỘNG NHANH TRONG 2 PHÚT (QUICKSTART)

### 1. Yêu cầu môi trường
- Python 3.10 trở lên
- Git

### 2. Cài đặt và khởi chạy Server

```bash
# 1. Clone repository
git clone https://github.com/dangbach3107/vault-core.git
cd vault-core

# 2. Tạo môi trường ảo (Virtual Environment)
python3 -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Khởi chạy server FastAPI
python3 -m app.main
```

### 3. Trải nghiệm hệ thống
- **Giao diện Demo trực quan (Live Dashboard):** Truy cập [http://localhost:8000](http://localhost:8000) trên trình duyệt để trải nghiệm toàn bộ 4 tính năng với giao diện tối hiện đại.
- **Tài liệu API Swagger (Interactive Docs):** Truy cập [http://localhost:8000/docs](http://localhost:8000/docs).
- **Kiểm tra Healthcheck:** `GET http://localhost:8000/health`.

### 4. Chạy bộ kiểm thử tự động (Unit Tests)

```bash
pytest tests/ -v
```

---

## 📂 CẤU TRÚC THƯ MỤC (PROJECT STRUCTURE)

```
vault-core/
├── app/
│   ├── main.py                  # Điểm khởi chạy ứng dụng FastAPI & Dashboard UI
│   ├── core/                    # Cấu hình bảo mật, sinh Token, mã băm SHA-256
│   ├── models/                  # Pydantic Schemas cho 4 Module
│   │   ├── profile.py           # Schema Hồ sơ doanh nghiệp & Trust Profile
│   │   ├── vdr.py               # Schema Phòng dữ liệu VDR, Watermark & Audit Log
│   │   ├── approval.py          # Schema Thỏa thuận NDA & Phê duyệt kép
│   │   └── techdd.py            # Schema Thẩm định công nghệ & Bảng trừ lùi giá
│   ├── services/                # Nghiệp vụ xử lý cốt lõi (Business Logic)
│   │   ├── profile_engine.py    # Module 1: Máy khử định danh & sinh Teaser
│   │   ├── vdr_service.py       # Module 2: Trạm VDR & Phủ Watermark động
│   │   ├── approval_gate.py     # Module 3: Luồng ký NDA & Cổng duyệt 2 bước
│   │   └── techdd_scanner.py    # Module 4: Khung Tech DD & Remediation Calculator
│   ├── api/                     # REST API Endpoints (/api/v1)
│   └── templates/
│       └── index.html           # Giao diện Dashboard Demo tương tác thời gian thực
├── sample_data/                 # Dữ liệu thử nghiệm mẫu (Case study WMS Bình Dương)
│   ├── sample_seller_input.json # Dữ liệu thô bên bán
│   └── sample_techdd_scan.json  # Dữ liệu quét mã nguồn SonarQube & Snyk
├── tests/                       # Bộ kiểm thử Unit test toàn diện
│   └── test_vault_modules.py
├── requirements.txt             # Danh mục thư viện phụ thuộc
├── .env.example                 # Mẫu biến môi trường
└── README.md
```

---

## 🛠️ CHI TIẾT 4 MODULE KỸ THUẬT

### Module 1: Trust Profile Engine
- **Endpoint:** `POST /api/v1/profile/generate`
- **Mục tiêu:** Nhận dữ liệu thô nhạy cảm của Bên bán (tên công ty, doanh thu chi tiết, danh sách khách hàng).
- **Thuật toán xử lý:**
  - *Range Binning:* Quy đổi doanh thu 72 tỷ VNĐ ➔ dải `50 – 100 tỷ VNĐ`.
  - *K-Anonymity:* Quy đổi địa bàn Bình Dương ➔ `Vùng kinh tế Đông Nam Bộ`.
  - *Bilingual Generation:* Tự động sinh tiêu đề tiếng Việt và tiếng Nhật phục vụ bên mua.

### Module 2: Secure Virtual Data Room (VDR)
- **Endpoints:**
  - `GET /api/v1/vdr/documents/{deal_id}`: Lấy danh mục 6 thư mục M&A chuẩn hóa.
  - `POST /api/v1/vdr/watermark`: Phủ watermark động định danh theo `Viewer Email`, `IP`, `Timestamp UTC`.
  - `GET /api/v1/vdr/audit-trail`: Truy xuất lịch sử kiểm toán bất biến ai đã xem tài liệu nào.

### Module 3: Two-Person Approval Gate
- **Endpoints:**
  - `POST /api/v1/approval/nda/submit`: Tiếp nhận sự kiện ký số NDA từ bên mua.
  - `POST /api/v1/approval/decision`: Tiếp nhận quyết định từ Founder bên bán (`SELLER_FOUNDER`) hoặc Pháp chế (`VAULT_COMPLIANCE`).
- **Quy tắc Bốn con mắt:** Quyền truy cập Lớp 2/3 chỉ được mở (`is_access_granted: true`) và cấp Token hiệu lực 14 ngày khi **cả hai bên cùng APPROVED**.

### Module 4: Tech DD & Remediation Cost Calculator
- **Endpoint:** `POST /api/v1/techdd/evaluate/{deal_id}`
- **Mục tiêu:** Rà soát 6 trục công nghệ (Kiến trúc, Nợ kỹ thuật, Bản quyền mã nguồn mở AGPL/GPL, An toàn thông tin, Rủi ro nhân sự, Tích hợp sau M&A).
- **Đầu ra tài chính:** Tự động tính toán chi phí sửa chữa CAPEX và quy đổi thành **Con số đề xuất trừ lùi vào định giá đàm phán M&A** (ví dụ: `-330.000.000 VNĐ`).

---

## 👥 ĐÓNG GÓP & LIÊN HỆ

Dự án phát triển bởi **Đội ngũ Công nghệ VAULT — Hệ sinh thái Rikkeisoft**.  
Mọi thắc mắc kỹ thuật vui lòng liên hệ Ban Kỹ thuật hoặc tạo Issue trên kho lưu trữ.
