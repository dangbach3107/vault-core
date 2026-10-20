"""Build one complete synthetic deal through the public API, one role at a time.

    DEMO_ROLE_PASSWORD=... python -m backend.demo_case --base http://127.0.0.1:8001

Every step goes through the same endpoints and rules a real user hits, so this doubles as an
end-to-end acceptance run. Everything it creates is labelled "Dữ liệu minh họa": the deal and
company names, the document titles and the text inside each PDF. The seed never uses the
"complete sample" shortcut.
"""
import argparse
import io
import os
from datetime import date, timedelta

from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

LABEL = "Dữ liệu minh họa"
DOCUMENTS = [
    # (folder, title, filename, lines) — each file has its own content.
    ("LEGAL_CORPORATE", "Giấy đăng ký doanh nghiệp", "giay-dang-ky-doanh-nghiep.pdf",
     ["GIAY CHUNG NHAN DANG KY DOANH NGHIEP", "Ma so doanh nghiep: DEMO-0101", "Nguoi dai dien: Nguyen Van A (minh hoa)", "Von dieu le: 20 ty VND"]),
    ("FINANCIAL_TAX", "Báo cáo tài chính 2025", "bao-cao-tai-chinh-2025.pdf",
     ["BAO CAO TAI CHINH NAM 2025", "Doanh thu: 62 ty VND", "EBITDA: 11 ty VND", "Y kien kiem toan: chap nhan toan phan (minh hoa)"]),
    ("TECHNOLOGY_IP", "Kiến trúc hệ thống", "kien-truc-he-thong.pdf",
     ["TAI LIEU KIEN TRUC HE THONG", "Kien truc: monolith tach dan thanh dich vu", "Co so du lieu: PostgreSQL", "Phu thuoc ma nguon mo: 38 thu vien"]),
    ("LEGAL_CORPORATE", "NDA mẫu đã ký", "nda-da-ky.pdf",
     ["THOA THUAN BAO MAT (NDA)", "Cac ben: Buyer minh hoa va Seller minh hoa", "Hieu luc: 12 thang", "Pham vi: thong tin kinh doanh va ky thuat"]),
    ("LEGAL_CORPORATE", "Hợp đồng mua bán cổ phần (đã ký)", "hop-dong-mua-ban.pdf",
     ["HOP DONG MUA BAN CO PHAN", "Ty le chuyen nhuong: 30%", "Gia tri: 105 ty VND (EV)", "Dieu kien hoan tat: da dap ung (minh hoa)"]),
]


def make_pdf(heading: str, lines: list[str]) -> bytes:
    """A one-page PDF whose text differs per document (Helvetica, ASCII only)."""
    writer = PdfWriter()
    page = writer.add_blank_page(width=595, height=842)
    font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})
    page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
    text = [f"BT /F1 12 Tf 60 780 Td (DU LIEU MINH HOA - {heading}) Tj ET"]
    for index, line in enumerate(lines):
        text.append(f"BT /F1 12 Tf 60 {740 - index * 28} Td ({line.replace('(', '').replace(')', '')}) Tj ET")
    stream = DecodedStreamObject()
    stream.set_data("\n".join(text).encode("latin-1", "replace"))
    page[NameObject("/Contents")] = writer._add_object(stream)
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


class Demo:
    def __init__(self, api, password: str):
        self.api, self.password, self.tokens = api, password, {}

    def headers(self, user: str):
        if user not in self.tokens:
            login = self.api.post("/api/v1/auth/login", json={"username": user, "password": self.password})
            login.raise_for_status()
            self.tokens[user] = login.json()["access_token"]
        return {"Authorization": f"Bearer {self.tokens[user]}"}

    def call(self, user: str, method: str, path: str, **kwargs):
        response = self.api.request(method, f"/api/v1{path}", headers=self.headers(user), **kwargs)
        if response.status_code >= 400:
            raise RuntimeError(f"{user} {method} {path} -> {response.status_code}: {response.text[:300]}")
        return response.json() if response.content else None

    def run(self, buyer: str = "buyer", seller: str = "seller"):
        today = date.today()
        in_year, in_half = (today + timedelta(days=365)).isoformat(), (today + timedelta(days=180)).isoformat()
        suffix = today.strftime("%d%m%y")

        # 1. Seller: profile, data room with distinct documents.
        company = self.call(seller, "POST", "/companies", json={
            "company_name": {"value": f"Aurora Warehouse Software ({LABEL})"},
            "tax_id": {"value": f"DEMO-{suffix}-{os.urandom(2).hex()}"},
            "sector": {"value": "SOFTWARE"}, "country": {"value": "VN"}, "region": {"value": "SOUTH"},
            "employees": {"value": 120}, "deal_type": {"value": "SECONDARY"}, "stake_percent": {"value": "30"},
            "expected_valuation": {"value": "105000000000"}, "valuation_basis": {"value": "EV"},
            "description": {"value": f"{LABEL}: phần mềm quản lý kho cho doanh nghiệp sản xuất."},
            "currency": "VND",
            "financials": [{"year": 2025, "period_end": f"{today.year - 1}-12-31", "revenue": {"value": "62000000000"}, "ebitda": {"value": "11000000000"}}],
        })
        room = self.call(seller, "POST", "/rooms", json={"company_id": company["id"], "title": f"Phòng dữ liệu ({LABEL})"})
        docs = {}
        for folder, title, filename, lines in DOCUMENTS:
            docs[filename] = self.call(seller, "POST", f"/rooms/{room['id']}/documents",
                                       data={"folder": folder, "title": f"{title} ({LABEL})"},
                                       files={"file": (filename, make_pdf(title, lines), "application/pdf")})
        by_name = lambda filename: docs[filename]["id"]  # noqa: E731

        # 2. Verification: seller asks, legal decides with the evidence file.
        for field, source, evidence in [("tax_id", "Giấy đăng ký doanh nghiệp", "giay-dang-ky-doanh-nghiep.pdf"),
                                        ("financials.2025.revenue", "Báo cáo tài chính 2025", "bao-cao-tai-chinh-2025.pdf")]:
            review = self.call(seller, "POST", f"/companies/{company['id']}/reviews", json={
                "field": field, "source": source, "source_date": (today - timedelta(days=30)).isoformat(), "document_id": by_name(evidence)})
            self.call("legal", "POST", f"/reviews/{review['id']}/decision", json={"approved": True, "verification": "DOCUMENT_VERIFIED", "reason": f"Khớp {source.lower()}"})

        # 3. Deal and the gated steps, each by its own role.
        deal = self.call("admin", "POST", "/deals", json={"title": f"Aurora × Nhà đầu tư Nhật ({LABEL})", "seller_company_id": company["id"], "buyer_username": buyer})
        path = f"/deals/{deal['id']}"
        step = lambda user, action, **body: self.call(user, "POST", f"{path}/actions/{action}", json=body)  # noqa: E731
        offer = lambda ref, low, high: {"offer": {"reference": ref, "price_low_vnd": low, "price_high_vnd": high, "valuation_basis": "EV", "exclusivity_days": 60, "valid_until": in_year, "conditions": LABEL}}  # noqa: E731

        step(buyer, "buyerRequest", buyer_request={"capability": "Phần mềm quản lý kho B2B", "goal": "Mở rộng sang nhà máy Nhật", "budget_min_vnd": "70000000000", "budget_max_vnd": "150000000000", "timeline": "LOI trong 90 ngày"})
        step(seller, "sellerProfile", note="Hồ sơ đã rà soát")
        self.call("finance", "POST", f"{path}/fees", json={"type": "PREP_PACKAGE", "amount_vnd": "150000000", "due_on": (today + timedelta(days=30)).isoformat(), "note": LABEL})
        step("finance", "prepPackageFeeRecorded")
        step(seller, "sellerL1Approval", note="Teaser đã đọc, không lộ danh tính")
        step("admin", "matchPrepared", note="Khẩu vị phù hợp")
        step(buyer, "identityRequested", note="Cần biết danh tính để ký NDA")
        step("admin", "ndaRecorded", nda={"reference": f"NDA-{suffix}", "parties": ["Buyer minh họa", "Seller minh họa"], "signed_on": today.isoformat(), "expires_on": in_year, "document_id": by_name("nda-da-ky.pdf")})
        step(seller, "sellerL2Approval", note="Đồng ý mở Lớp 2 sau NDA")
        step(buyer, "indicativeLoiSubmitted", **offer(f"LOI-{suffix}", "90000000000", "120000000000"))

        # Access: the buyer asks for L2, then for L3 with two files; the approver picks versions and expiry.
        requested = self.call(buyer, "POST", f"{path}/access-requests", json={"requested_level": "L2", "purpose": "Đánh giá mức phù hợp"})
        self.call(seller, "POST", f"{path}/access-requests/{requested['state']['access_requests'][0]['id']}/decision",
                  json={"approved": True, "reason": "Có NDA", "expires_at": f"{in_half}T23:59:59Z"})
        step("legal", "legalL3Approval", note="Đủ điều kiện mở Lớp 3")
        step("legal", "crossBorderApproval", note="Chuyển dữ liệu ra nước ngoài: đã đánh giá")
        step("legal", "noEscrowConfirmed", note="VAULT không giữ tiền")
        step(seller, "sellerFileApproval", note="Danh sách file đã duyệt")
        requested = self.call(buyer, "POST", f"{path}/access-requests", json={"requested_level": "L3", "purpose": "Thẩm định tài chính và kỹ thuật"})
        self.call("legal", "POST", f"{path}/access-requests/{requested['state']['access_requests'][1]['id']}/decision",
                  json={"approved": True, "reason": "Hạn chế theo file", "expires_at": f"{in_half}T23:59:59Z",
                        "document_ids": [by_name("bao-cao-tai-chinh-2025.pdf"), by_name("kien-truc-he-thong.pdf")], "can_download": False})
        step("admin", "vdrOpened", note="Mở phòng dữ liệu cho thẩm định")

        # 4. Tech DD: findings handled one by one, then the separate sign-off.
        for title, severity, impact in [("Khả năng mở rộng kiến trúc", "HIGH", "180000000"), ("Thiếu bằng chứng giấy phép mã nguồn mở", "MEDIUM", "90000000")]:
            self.call("tech", "POST", f"{path}/tech-dd/findings", json={"title": title, "severity": severity, "impact_vnd": impact, "description": LABEL, "remediation": "Theo kế hoạch 6 tháng"})
        findings = self.call("tech", "GET", path)["state"]["tech_dd"]["findings"]
        for finding, final in zip(findings, ["ACCEPTED_RISK", "RESOLVED"]):
            self.call(seller, "POST", f"{path}/tech-dd/findings/{finding['id']}/status", json={"status": "RESPONDED", "note": "Đã gửi bằng chứng và kế hoạch"})
            self.call("tech", "POST", f"{path}/tech-dd/findings/{finding['id']}/status", json={"status": final, "note": "Đã kiểm tra phản hồi"})
        step("tech", "techDdSigned", note="Kết thúc thẩm định kỹ thuật")
        self.call("finance", "POST", f"{path}/fees", json={"type": "TECH_DD", "amount_vnd": "90000000", "due_on": (today - timedelta(days=2)).isoformat(), "note": LABEL})

        # 5. Offer, closing conditions, signing, closing — with the cited evidence files.
        step(buyer, "loiSubmitted", **offer(f"OFFER-{suffix}", "105000000000", None))
        step("legal", "legalClosingChecklist", note="Điều kiện đóng đã đủ", document_ids=[by_name("hop-dong-mua-ban.pdf")])
        step("legal", "spaSigned", note=f"HĐ-{suffix}", document_ids=[by_name("hop-dong-mua-ban.pdf")])
        step("admin", "dealClosed", note="Hoàn tất điều kiện đóng")

        # 6. Fees: one part-paid, one overdue, one invoiced; then the handoff.
        fees = {fee["type"]: fee for fee in self.call("finance", "GET", path)["state"]["fees"]}
        self.call("finance", "POST", f"{path}/fees", json={"type": "SUCCESS_FEE", "amount_vnd": "2100000000", "due_on": (today + timedelta(days=25)).isoformat(), "note": LABEL})
        fees = {fee["type"]: fee for fee in self.call("finance", "GET", path)["state"]["fees"]}
        for kind, number in [("PREP_PACKAGE", "HD-01"), ("TECH_DD", "HD-02"), ("SUCCESS_FEE", "HD-03")]:
            self.call("finance", "POST", f"{path}/fees/{fees[kind]['id']}/invoice", json={"invoice_number": f"{number}-{suffix}", "issued_on": today.isoformat()})
        self.call("finance", "POST", f"{path}/fees/{fees['PREP_PACKAGE']['id']}/payments", json={"amount_vnd": "50000000", "paid_on": today.isoformat(), "reference": "UNC-minh-hoa"})
        step("finance", "successFeeRecorded")
        step("admin", "postDealHandoff", handoff={"recipient": "Đội tích hợp minh họa", "handed_on": today.isoformat(), "items": ["Mã nguồn", "Tài khoản hạ tầng", "Danh sách khách hàng"]})
        return {"company": company["id"], "deal": deal["id"], "documents": [doc["id"] for doc in docs.values()]}


def main():
    import httpx
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="http://127.0.0.1:8001")
    parser.add_argument("--buyer", default="buyer")
    parser.add_argument("--seller", default="seller")
    args = parser.parse_args()
    password = os.environ.get("DEMO_ROLE_PASSWORD")
    if not password:
        raise SystemExit("Set DEMO_ROLE_PASSWORD to the demo account password.")
    with httpx.Client(base_url=args.base, timeout=60) as api:
        result = Demo(api, password).run(args.buyer, args.seller)
    print(f"Created deal {result['deal']} for company {result['company']} with {len(result['documents'])} documents.")


if __name__ == "__main__":
    main()
