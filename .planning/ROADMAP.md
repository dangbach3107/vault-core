# Lộ trình — hai người, khối lượng gần bằng nhau

Cập nhật **2026-09-13**. **Chưa được phép code** cho đến khi người dùng bảo làm.

Hai cụm **độc lập**: không chung bảng, route, thư mục UI; không lần lượt sửa cùng `Workspace.tsx` / cùng file Alembic / `openapi.json`. Mỗi người demo **sản phẩm của mình** (tự seed). Nối 15 bước là PR **sau**.

**Chia 8 / 7** (Work-flow 15 bước):

| | **Người A — Mở lớp** | **Người B — VDR & đóng** |
| --- | --- | --- |
| Bước | **1–8** | **9–15** |
| Số nút/cổng chính | 8 (L1, match, NDA, L2, Legal ×3, duyệt file) | 7 (mở VDR, Tech DD, LOI, checklist, closed, phí, handoff) |
| Nặng tương đương | Nhiều cổng nhỏ + 1 bảng grant file | Ít bước hơn nhưng nặng file/phí/findings |

## Pha

| Pha | Việc | Trạng thái |
| --- | --- | --- |
| P2a / P3a | Hồ sơ + phòng local | Xong |
| **P3b-A** | Mở lớp (1–8) | Kế hoạch |
| **P3b-B** | VDR & đóng (9–15) | Kế hoạch |

## Ranh giới file

| | **A — `#/disclosures` · nhãn Mở lớp** | **B — `#/closings` · nhãn VDR & đóng** |
| --- | --- | --- |
| API | `/api/v1/disclosures` | `/api/v1/closings` |
| Alembic | **`0003_disclosures.py`** chỉ A | **`0004_closings.py`** chỉ B |
| Backend | `api/disclosures.py` `schemas/disclosure.py` `db/disclosure.py` `services/disclosure.py` `tests/test_disclosures.py` | `api/closings.py` `schemas/closing.py` `db/closing.py` `services/closing.py` `tests/test_closings.py` |
| Frontend | `features/disclosures/` `e2e/disclosures.spec.ts` | `features/closings/` `e2e/closings.spec.ts` |
| `Workspace.tsx` | A thêm **một** mục `disclosures` | B thêm **một** mục `closings` |
| Tab trên màn mình | Buyer · Seller · Admin · Legal | Admin · Tech DD · Buyer (LOI) · Legal (checklist) · Finance |
| Seed | Tự tạo company (MVP-01) + disclosure | Tự tạo company + room + vài file (MVP-02) + closing **đã giả định L3 file đã duyệt** |

Cấm import / chờ API người kia. OpenAPI: mỗi người chỉ thêm prefix của mình; đừng export cùng lúc.

## Người A — bước 1–8 (tiến độ 8/8 mở lớp)

| Bước | Tab | Nút | Lưu (của A) |
| --- | --- | --- | --- |
| 1 | Buyer | **Lưu buyer request** | 4 field |
| 2 | Seller | **Tạo seller profile từ sample data** · **Approve L1 teaser** | `company_id`, `l1_approved` |
| 3 | Admin | **Prepare match buyer–seller** | điểm, ≥3 lý do, ≥3 rủi ro |
| 4 | Buyer | **Request identity / mở Layer 2** | `l2_requested` |
| 5 | Admin | **Record signed NDA** | file + signer + hash + giờ |
| 6 | Seller | **Approve buyer mở Layer 2** | `l2_approved` (cần 4+5) |
| 7 | Legal | 3 nút L3 / cross-border / no-custody | 3 boolean |
| 8 | Seller | Approve từng file L3 cho buyer | `disclosure_document_grants` |

Không làm mở VDR, Tech DD, phí. Toast/khóa nút: REQUIREMENTS FLOW-01–08.

**A xong:** e2e 1→8; nhảy bước 422; Buyer không marketplace.

## Người B — bước 9–15 (tiến độ 7/7 đóng)

Fixture mở đầu (text, **không** đọc bảng A): “Legal đã duyệt + đã có grant file”. Room/file do B tạo.

| Bước | Tab | Nút | Lưu (của B) |
| --- | --- | --- | --- |
| 9 | Admin | **Open approved VDR files** | `vdr_opened`; chỉ file trong fixture grant của B |
| 10 | Tech DD | Findings + **Tech DD reviewer sign-off** | `tech_dd_findings` + 4 lớp |
| 11 | Buyer | **Submit LOI / indicative offer** | VND chuỗi, không ràng buộc |
| 12 | Legal | **Complete LOI/closing checklist** | checklist jsonb |
| 13 | Admin | **Mark SPA signed / deal closed** | `status=closed` (cần 11+12) |
| 14 | Finance | **Record success fee** | 4 dòng; Tech DD / B2B không vào tổng VAULT |
| 15 | Admin | **Post-deal handoff to Rikkei** | ghi chú; 7/7 |

**B xong:** e2e 9→15; file ngoài grant 404; tổng phí đúng nhãn.

## Nối sau (không nằm trong PR A hay B)

`closings.disclosure_id` nullable khi cả hai đã merge.

Cột đúng tên: [DATABASE.md](DATABASE.md) — A chỉ tạo bảng mục 2; B chỉ mục 3.

## Việc nhỏ nhất khi được lệnh code

- A: `0003` + `POST /disclosures` + trang 8 bước.  
- B: `0004` + `POST /closings` (seed L3 xong) + trang 7 bước.  
Song song ngày 1.
