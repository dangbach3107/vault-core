# Cấu trúc cơ sở dữ liệu VAULT

Cập nhật **2026-09-13**. PostgreSQL 17, schema `public`, UUID PK, thời gian `timestamptz` UTC.

- **Đã có (0001–0002):** `companies`, `rooms`, `documents`, `document_versions` — khớp `backend/app/db/models.py`.
- **P3b người A (0003, chưa tạo):** `disclosures`, `disclosure_events`, `disclosure_document_grants`.
- **P3b người B (0004, chưa tạo):** `closings`, `closing_events`, `closing_opened_documents`, `tech_dd_findings`, `fee_lines`.
- **Nối sau (0005, không nằm PR A/B):** `closings.disclosure_id` nullable.

Không có bảng `users` / session. `INTERNAL_PREVIEW_ENABLED` không lưu DB. Byte file nằm đĩa (`storage_key`), không phải BYTEA.

Tiền: `NUMERIC(18,2)` hoặc chuỗi số thập phân đã validate — **không** `float`. JSONB sự kiện (`Fact`) nằm trong `companies.profile`.

```
companies ──┬── rooms ── documents ── document_versions
            ├── disclosures ── disclosure_events
            │              └── disclosure_document_grants ──► documents.id
            └── closings ── closing_events
                         ├── closing_opened_documents ──► documents.id
                         ├── tech_dd_findings
                         └── fee_lines
```

---

## 1. Đã triển khai

### 1.1 `companies` — revision `0001`

| Cột | Kiểu | Null | Ràng buộc | Ý nghĩa |
| --- | --- | --- | --- | --- |
| `id` | UUID | không | PK, `gen` uuid4 | |
| `alias` | VARCHAR(40) | không | UNIQUE | Bí danh L1 (A-04) |
| `name` | VARCHAR(200) | không | INDEX | Tên hiện tại (copy từ fact) |
| `tax_id` | VARCHAR(30) | có | UNIQUE | Trùng → 409; không phải xác minh pháp lý |
| `profile` | JSONB | không | | Toàn bộ `CompanyInput` |
| `revision` | INTEGER | không | `>= 1` | Optimistic lock; sai → 409 |
| `created_at` | TIMESTAMPTZ | không | | |
| `updated_at` | TIMESTAMPTZ | không | | |

**`profile` (JSONB)** — mỗi trường nghiệp vụ là object `Fact` trừ `financials` (mảng ≤ 3):

```json
{
  "value": null,
  "verification": "SELF_DECLARED | DOCUMENT_VERIFIED | THIRD_PARTY_CONFIRMED",
  "issue": "NONE | CONFLICTED | EXPIRED",
  "source": "",
  "source_date": null,
  "entered_by": "",
  "reviewed_by": "",
  "reviewed_on": null,
  "notes": ""
}
```

| Khóa trong `profile` | `value` |
| --- | --- |
| `company_name` | string 1–200, **bắt buộc** khi lưu nháp |
| `tax_id` | string 3–30 hoặc null |
| `founded_year` | int 1800–năm hiện tại |
| `sector` | `SOFTWARE` `MANUFACTURING` `SERVICES` `OTHER` |
| `region` | `NORTH` `CENTRAL` `SOUTH` |
| `address` `description` `customer_groups` `technology` `shareholders` `decision_maker` `funds_destination` `objectives` `permitted_use` | string ≤ 2000 |
| `employees` | int 0–10_000_000 |
| `deal_type` | `PRIMARY` `SECONDARY` `MIXED` |
| `stake_percent` | decimal 0–100, 2 lẻ |
| `financials[]` | `{ year, revenue_vnd: Fact, ebitda_vnd: Fact }` — năm không trùng, không tương lai; tiền `NUMERIC` 18,2 |

Nhãn đã xác minh bắt buộc có `value`, `source`, `source_date`, `reviewed_by`, `reviewed_on`. `CONFLICTED`/`EXPIRED` phải `SELF_DECLARED`.

### 1.2 `rooms` — `0002`

| Cột | Kiểu | Null | Ràng buộc |
| --- | --- | --- | --- |
| `id` | UUID | không | PK |
| `company_id` | UUID | không | FK `companies.id`, INDEX |
| `title` | VARCHAR(200) | không | UNIQUE (`company_id`, `title`) |
| `created_at` | TIMESTAMPTZ | không | |

Không `ON DELETE CASCADE` trên company (xóa công ty chưa có API).

### 1.3 `documents` — `0002`

| Cột | Kiểu | Null | Ràng buộc |
| --- | --- | --- | --- |
| `id` | UUID | không | PK |
| `room_id` | UUID | không | FK `rooms.id`, INDEX |
| `title` | VARCHAR(200) | không | |
| `folder` | VARCHAR(40) | không | `LEGAL_CORPORATE` `FINANCIAL_TAX` `COMMERCIAL_OPERATIONS` `TECHNOLOGY_IP` `HUMAN_RESOURCES` `QA_TRACKER` |
| `current_version` | INTEGER | không | `>= 1` |

### 1.4 `document_versions` — `0002`

| Cột | Kiểu | Null | Ràng buộc |
| --- | --- | --- | --- |
| `id` | UUID | không | PK |
| `document_id` | UUID | không | FK `documents.id`, INDEX |
| `number` | INTEGER | không | UNIQUE (`document_id`, `number`), `>= 1` |
| `filename` | VARCHAR(255) | không | Tên gốc (hiển thị), không dùng làm path |
| `media_type` | VARCHAR(100) | không | |
| `size_bytes` | BIGINT | không | `> 0`; app giới hạn 10 MiB |
| `sha256` | CHAR/VARCHAR(64) | không | Hex |
| `storage_key` | VARCHAR(40) | không | UNIQUE; key trên đĩa |
| `note` | VARCHAR(1000) | không | Default `''` |
| `uploaded_at` | TIMESTAMPTZ | không | |

---

## 2. Người A — `0003_disclosures` (kế hoạch)

Chỉ A tạo/sửa file migration này. Không FK sang bảng B.

### 2.1 `disclosures`

Một hàng = một kịch bản mở lớp (bước 1–8).

| Cột | Kiểu | Null | Default | Ràng buộc / ghi chú |
| --- | --- | --- | --- | --- |
| `id` | UUID | không | uuid4 | PK |
| `company_id` | UUID | có | null | FK `companies.id` — điền ở bước 2 |
| `buyer_label` | VARCHAR(120) | không | `'buyer-demo'` | Nhãn buyer giả (không phải user id) |
| `capability_gap` | VARCHAR(2000) | không | `''` | Buyer field 1 (A-07) |
| `outcome_24m` | VARCHAR(2000) | không | `''` | Field 2 |
| `budget_band` | VARCHAR(120) | không | `''` | Field 3 — **không** số tiền chính xác |
| `close_window` | VARCHAR(120) | không | `''` | Field 4 |
| `request_saved` | BOOLEAN | không | false | FLOW-01 |
| `l1_approved` | BOOLEAN | không | false | FLOW-02 |
| `match_prepared` | BOOLEAN | không | false | FLOW-03 |
| `match_score` | SMALLINT | có | null | 1–5 khi đã match; CHECK |
| `match_reasons` | JSONB | không | `[]` | `string[]`, ≥ 3 khi `match_prepared` |
| `match_risks` | JSONB | không | `[]` | `string[]`, ≥ 3 khi match |
| `l2_requested` | BOOLEAN | không | false | FLOW-04 |
| `nda_recorded` | BOOLEAN | không | false | FLOW-05 |
| `nda_signer` | VARCHAR(120) | không | `''` | |
| `nda_signed_at` | TIMESTAMPTZ | có | null | |
| `nda_sha256` | VARCHAR(64) | không | `''` | |
| `nda_storage_key` | VARCHAR(40) | có | null | UNIQUE nếu không null; file local |
| `nda_filename` | VARCHAR(255) | không | `''` | |
| `l2_approved` | BOOLEAN | không | false | FLOW-06 |
| `legal_l3_approved` | BOOLEAN | không | false | FLOW-07 |
| `legal_cross_border` | BOOLEAN | không | false | FLOW-07 |
| `legal_no_custody` | BOOLEAN | không | false | FLOW-07 — VAULT không giữ tiền/cổ phần |
| `step` | SMALLINT | không | 0 | 0–8, số bước đã xong |
| `created_at` | TIMESTAMPTZ | không | now | |
| `updated_at` | TIMESTAMPTZ | không | now | |

CHECK gợi ý (service vẫn là chuẩn): `step BETWEEN 0 AND 8`; `match_score IS NULL OR match_score BETWEEN 1 AND 5`.

### 2.2 `disclosure_events`

Nhật ký append-only.

| Cột | Kiểu | Null | Ràng buộc |
| --- | --- | --- | --- |
| `id` | UUID | không | PK |
| `disclosure_id` | UUID | không | FK `disclosures.id`, INDEX |
| `flow_id` | VARCHAR(16) | không | `FLOW-01` … `FLOW-08` |
| `actor_persona` | VARCHAR(20) | không | `BUYER` `SELLER` `ADMIN` `LEGAL` |
| `payload` | JSONB | không | Default `{}` |
| `at` | TIMESTAMPTZ | không | |

Không xóa / không update hàng.

### 2.3 `disclosure_document_grants` — FLOW-08

| Cột | Kiểu | Null | Ràng buộc |
| --- | --- | --- | --- |
| `id` | UUID | không | PK |
| `disclosure_id` | UUID | không | FK `disclosures.id` |
| `document_id` | UUID | không | FK `documents.id` |
| `buyer_label` | VARCHAR(120) | không | Khớp `disclosures.buyer_label` |
| `approved_at` | TIMESTAMPTZ | không | |
| | | | UNIQUE (`disclosure_id`, `document_id`, `buyer_label`) |

A **không** có cột “đã mở VDR”.

---

## 3. Người B — `0004_closings` (kế hoạch)

Không FK `disclosures` ở 0004. Seed: `l3_precleared = true` (text giả định bước 1–8 xong).

### 3.1 `closings`

| Cột | Kiểu | Null | Default | Ghi chú |
| --- | --- | --- | --- | --- |
| `id` | UUID | không | uuid4 | PK |
| `company_id` | UUID | không | | FK `companies.id` |
| `room_id` | UUID | không | | FK `rooms.id` — phòng B tự tạo |
| `buyer_label` | VARCHAR(120) | không | `'buyer-demo'` | |
| `l3_precleared` | BOOLEAN | không | true | Fixture; không đọc bảng A |
| `vdr_opened` | BOOLEAN | không | false | FLOW-09 |
| `vdr_opened_at` | TIMESTAMPTZ | có | null | |
| `tech_dd_signed` | BOOLEAN | không | false | FLOW-10 |
| `tech_dd_reviewer` | VARCHAR(120) | không | `''` | Tên gõ tay |
| `tech_dd_signed_at` | TIMESTAMPTZ | có | null | |
| `loi_submitted` | BOOLEAN | không | false | FLOW-11 |
| `loi_amount_vnd` | VARCHAR(32) | không | `''` | Chuỗi decimal, 2 lẻ; rỗng = chưa nộp |
| `loi_non_binding` | BOOLEAN | không | true | Bắt buộc true khi nộp |
| `loi_submitted_at` | TIMESTAMPTZ | có | null | |
| `closing_checklist` | JSONB | không | `[]` | `[{ "id", "label", "done" }]` |
| `checklist_complete` | BOOLEAN | không | false | FLOW-12 |
| `spa_closed` | BOOLEAN | không | false | FLOW-13 |
| `spa_closed_at` | TIMESTAMPTZ | có | null | |
| `success_fee_recorded` | BOOLEAN | không | false | FLOW-14 |
| `handoff_done` | BOOLEAN | không | false | FLOW-15 |
| `handoff_note` | VARCHAR(2000) | không | `''` | |
| `handoff_at` | TIMESTAMPTZ | có | null | |
| `step` | SMALLINT | không | 0 | 0–7 (bước 9…15) |
| `created_at` | TIMESTAMPTZ | không | | |
| `updated_at` | TIMESTAMPTZ | không | | |

`disclosure_id` **chưa có** ở 0004.

### 3.2 `closing_events`

Giống `disclosure_events`; `flow_id` = `FLOW-09` … `FLOW-15`; `actor_persona` thêm `TECH_DD` `FINANCE` `BUYER` `LEGAL` `ADMIN`.

### 3.3 `closing_opened_documents` — FLOW-09

Danh sách file B cho phép mở trong demo (grant giả, **không** đọc `disclosure_document_grants`).

| Cột | Kiểu | Null | Ràng buộc |
| --- | --- | --- | --- |
| `id` | UUID | không | PK |
| `closing_id` | UUID | không | FK `closings.id` |
| `document_id` | UUID | không | FK `documents.id` |
| | | | UNIQUE (`closing_id`, `document_id`) |

API mở file: 404 nếu không có hàng này.

### 3.4 `tech_dd_findings` — FLOW-10

| Cột | Kiểu | Null | Ràng buộc |
| --- | --- | --- | --- |
| `id` | UUID | không | PK |
| `closing_id` | UUID | không | FK `closings.id`, INDEX |
| `title` | VARCHAR(300) | không | |
| `detail` | VARCHAR(4000) | không | `''` |
| `remediation_class` | VARCHAR(40) | không | `PRE_CLOSING_MUST_FIX` `SIX_MONTH_FIX` `DEFER` `GROWTH_INVESTMENT` |
| `sort_order` | INTEGER | không | default 0 |
| `created_at` | TIMESTAMPTZ | không | |

Sign-off nằm trên `closings`, không trên từng finding.

### 3.5 `fee_lines` — FLOW-14

| Cột | Kiểu | Null | Ràng buộc |
| --- | --- | --- | --- |
| `id` | UUID | không | PK |
| `closing_id` | UUID | không | FK `closings.id` |
| `kind` | VARCHAR(40) | không | `PREP_PACKAGE` `SUCCESS_FEE` `TECH_DD` `BUILD_TO_BUY` |
| `amount_vnd` | VARCHAR(32) | không | Chuỗi decimal ≥ 0, 2 lẻ |
| `counts_as_vault_revenue` | BOOLEAN | không | `false` với `TECH_DD` và `BUILD_TO_BUY` |
| `note` | VARCHAR(500) | không | `''` |
| | | | UNIQUE (`closing_id`, `kind`) |

Tổng doanh thu VAULT demo = cộng dòng có `counts_as_vault_revenue = true` bằng decimal, không JS `number`.

---

## 4. Nối sau — `0005` (không làm trong PR A/B)

```text
ALTER TABLE closings ADD COLUMN disclosure_id UUID NULL REFERENCES disclosures(id);
CREATE INDEX ix_closings_disclosure_id ON closings (disclosure_id);
```

Khi có: chỉ cho gắn nếu `disclosures.step = 8`. Trước 0005, B không đọc A.

---

## 5. Enum / persona (cột VARCHAR + CHECK, không TYPE Postgres — dễ Alembic)

| Tập | Giá trị |
| --- | --- |
| Folder tài liệu | như `documents.folder` |
| `verification` / `issue` | trong JSONB `Fact` |
| `remediation_class` | 4 lớp Tech DD |
| `fee.kind` | 4 loại phí |
| `actor_persona` | `BUYER` `SELLER` `ADMIN` `LEGAL` `TECH_DD` `FINANCE` |
| `flow_id` | `FLOW-01` … `FLOW-15` |

---

## 6. Sở hữu migration

| Revision | File | Người |
| --- | --- | --- |
| 0001 | `0001_company_profiles.py` | Đã có |
| 0002 | `0002_data_rooms.py` | Đã có |
| **0003** | `0003_disclosures.py` | **Chỉ A** |
| **0004** | `0004_closings.py` | **Chỉ B** (`down_revision = "0003"` sau khi 0003 đã merge, **hoặc** A merge 0003 trước một nhịp rồi B rebase — nếu song song ngày 1: B đặt `down_revision = "0002"` và **đổi thành 0003 khi rebase**; không sửa file 0003 của A) |
| 0005 | `0005_link_closing_disclosure.py` | PR nối |

Hai nhánh Alembic song song từ 0002 được phép nếu cả hai thống nhất merge linear trước khi deploy chung: ưu tiên **A merge 0003 trước**, B `down_revision = "0003"`.

Áp dụng: `alembic -c backend/alembic.ini upgrade head` — **không** chạy lúc app start.

---

## 7. Không có trong CSDL này

Bảng account, role production, watermark log, e-sign provider, invoice, Book B, marketplace listing. Xóa company/room/file hàng loạt. Mật khẩu / API key.
