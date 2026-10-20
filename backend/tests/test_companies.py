from copy import deepcopy
from datetime import date
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from backend.app.core.config import Settings
from backend.app.main import create_app


def draft():
    return {
        "company_name": {"value": "Công ty Tổng hợp Giả lập"},
        "tax_id": {"value": "SYNTH-010101"},
        "address": {"value": "123 Đường Bí mật"},
        "description": {"value": "Khách hàng Secret Brand"},
        "technology": {"value": "Secret architecture"},
        "shareholders": {"value": "Sensitive shareholder"},
        "region": {"value": "NORTH", "notes": "Must never disclose"},
        "sector": {"value": "SOFTWARE"},
        "employees": {"value": 120},
        "financials": [{"year": 2025, "revenue": {"value": "25000000000.01"}, "ebitda": {"value": "-1000.50"}}],
    }


def create(client, body=None):
    response = client.post("/api/v1/companies", json=body or draft())
    assert response.status_code == 201, response.text
    return response.json()


def auth_headers(client, username):
    login = client.post("/api/v1/auth/login", json={"username": username, "password": "vault-demo"})
    assert login.status_code == 200, login.text
    return {"Authorization": f'Bearer {login.json()["access_token"]}'}


def test_persistence_edit_and_stale_revision(client):
    company = create(client)
    path = f'/api/v1/companies/{company["id"]}'
    loaded = client.get(path).json()
    assert loaded == company
    assert loaded["profile"]["financials"][0]["revenue"]["value"] == "25000000000.01"
    assert loaded["profile"]["financials"][0]["ebitda"]["value"] == "-1000.50"
    loaded["profile"]["company_name"]["value"] = "Doanh nghiệp đã sửa"
    update = {"expected_revision": 1, "profile": loaded["profile"]}
    assert client.put(path, json=update).json()["revision"] == 2
    assert client.get(path).json()["profile"]["company_name"]["value"] == "Doanh nghiệp đã sửa"
    assert client.put(path, json=update).status_code == 409
    assert client.get("/api/v1/companies?q=SYNTH-010101").json()[0]["id"] == company["id"]
    assert client.get("/api/v1/companies?q=%").json() == []
    assert client.post("/api/v1/companies", json=draft()).status_code == 409


def test_delete_draft_company(client):
    company = create(client)
    path = f'/api/v1/companies/{company["id"]}'
    assert client.delete(path).status_code == 204
    assert client.get(path).status_code == 404
    assert client.delete(path).status_code == 404


def test_delete_company_with_room_is_blocked(client):
    company = create(client)
    room = client.post(
        "/api/v1/rooms",
        json={"company_id": company["id"], "title": "Phòng dữ liệu cần giữ"},
    )
    assert room.status_code == 201, room.text
    response = client.delete(f'/api/v1/companies/{company["id"]}')
    assert response.status_code == 409
    assert "phòng dữ liệu" in response.json()["detail"]


def test_company_and_room_routes_enforce_login_role(client):
    login = client.post("/api/v1/auth/login", json={"username": "buyer", "password": "vault-demo"})
    buyer = {"Authorization": f'Bearer {login.json()["access_token"]}'}
    assert client.get("/api/v1/companies", headers=buyer).status_code == 403
    assert client.post("/api/v1/companies", json={"company_name": {"value": "Not allowed"}}, headers=buyer).status_code == 403
    assert client.get("/api/v1/rooms", headers=buyer).status_code == 403


def test_sellers_only_access_their_own_company_and_rooms(client):
    seller = auth_headers(client, "seller")
    other_seller = auth_headers(client, "seller2")
    body = draft()
    body["tax_id"]["value"] = "SYNTH-OWNER-01"
    created = client.post("/api/v1/companies", json=body, headers=seller)
    assert created.status_code == 201, created.text
    company = created.json()
    company_path = f'/api/v1/companies/{company["id"]}'
    assert company["owner_username"] == "seller"
    assert [row["id"] for row in client.get("/api/v1/companies", headers=seller).json()] == [company["id"]]
    assert client.get("/api/v1/companies", headers=other_seller).json() == []
    assert client.get(company_path, headers=other_seller).status_code == 404
    assert client.get(company_path + "/preview/1", headers=other_seller).status_code == 404
    assert client.put(company_path, json={"expected_revision": 1, "profile": company["profile"]}, headers=other_seller).status_code == 404
    assert client.delete(company_path, headers=other_seller).status_code == 404
    assert client.get(company_path).status_code == 200

    created_room = client.post(
        "/api/v1/rooms",
        json={"company_id": company["id"], "title": "Seller private room"},
        headers=seller,
    )
    assert created_room.status_code == 201, created_room.text
    room = created_room.json()
    room_path = f'/api/v1/rooms/{room["id"]}'
    assert [row["id"] for row in client.get("/api/v1/rooms", headers=seller).json()] == [room["id"]]
    assert client.get("/api/v1/rooms", headers=other_seller).json() == []
    assert client.get(room_path, headers=other_seller).status_code == 404
    assert client.post(
        "/api/v1/rooms",
        json={"company_id": company["id"], "title": "Forbidden room"},
        headers=other_seller,
    ).status_code == 404
    assert client.delete(room_path, headers=other_seller).status_code == 404


def test_preview_backend_allowlist_and_missing_vs_zero(client):
    company = create(client)
    path = f'/api/v1/companies/{company["id"]}/preview'
    anonymous = client.get(f"{path}/1")
    assert anonymous.status_code == 200, anonymous.text
    assert set(anonymous.json()) == {"layer", "alias", "sector", "region", "country", "revenue_band", "employee_band", "deal_type", "notice"}
    assert anonymous.json()["revenue_band"] == "20–dưới 50 tỷ VND"
    for private in ["Giả lập", "SYNTH-010101", "Bí mật", "Secret", "Sensitive", "Must never", "25000000000", "notes", "company_name"]:
        assert private not in anonymous.text
    identified = client.get(f"{path}/2").json()
    assert identified["facts"]["company_name"]["value"] == draft()["company_name"]["value"]
    assert "shareholders" not in identified["facts"]
    assert client.get(f"{path}/3").json()["facts"]["shareholders"]["value"] == "Sensitive shareholder"
    blank = create(client, {"company_name": {"value": "Blank"}, "employees": {"value": 0}})
    preview = client.get(f'/api/v1/companies/{blank["id"]}/preview/1').json()
    assert preview["revenue_band"] is None
    assert preview["employee_band"] == "Dưới 50"
    assert client.get(f"{path}/4").status_code == 422
    assert client.get(f"/api/v1/companies/{uuid4()}").status_code == 404


@pytest.mark.parametrize("patch", [
    {"company_name": {"value": "  "}},
    {"employees": {"value": -1}},
    {"stake_percent": {"value": "101"}},
    {"founded_year": {"value": date.today().year + 1}},
    {"sector": {"value": "identifying free text"}},
    {"financials": [{"year": 2025}, {"year": 2025}]},
    {"financials": [{"year": 2025, "revenue": {"value": "-1"}}]},
    {"financials": [{"year": 2025, "revenue": {"value": "1.001"}}]},
    {"company_name": {"value": "Unsupported", "verification": "DOCUMENT_VERIFIED"}},
    {"is_audited": True},
    {"currency": "USD"},
    {"country": {"value": "JP"}},  # draft() has a Vietnamese region
    {"expected_valuation": {"value": "100000000000"}},  # no EV/Equity basis
    {"financials": [{"year": 2025, "period_end": "2027-03-31"}]},
    {"financials": [{"year": date.today().year, "period_end": date.today().replace(month=12, day=31).isoformat()}]} if date.today().month < 12 else {"is_audited": True},
])
def test_validation(client, patch):
    body = draft() | patch
    assert client.post("/api/v1/companies", json=body).status_code == 422
    assert client.get("/api/v1/companies?q=SYNTH-010101").json() == []


def test_japanese_profile_uses_jpy_bands_and_fiscal_period(client):
    body = draft() | {
        "country": {"value": "JP"}, "region": {"value": None}, "currency": "JPY",
        "expected_valuation": {"value": "2500000000"}, "valuation_basis": {"value": "EQUITY"},
        "financials": [{"year": 2024, "period_end": "2025-03-31", "revenue": {"value": "450000000"}}],
    }
    company = create(client, body)
    assert company["profile"]["currency"] == "JPY"
    assert company["profile"]["financials"][0]["period_end"] == "2025-03-31"
    path = f'/api/v1/companies/{company["id"]}/preview'
    teaser = client.get(f"{path}/1").json()
    assert teaser["country"] == "JP" and teaser["revenue_band"] == "300 triệu–dưới 1 tỷ JPY"
    identified = client.get(f"{path}/2").json()
    assert identified["currency"] == "JPY" and "currency" not in identified["facts"]
    assert identified["facts"]["valuation_basis"]["value"] == "EQUITY"
    summary = next(row for row in client.get("/api/v1/companies?limit=200").json() if row["id"] == company["id"])
    assert summary["currency"] == "JPY" and summary["country"] == "JP" and summary["revenue_band"] == "300 triệu–dưới 1 tỷ JPY"


def review(client, company_id, field, requester="seller", **extra):
    body = {"field": field, "source": "Giấy đăng ký doanh nghiệp mẫu", "source_date": "2025-01-01", **extra}
    return client.post(f"/api/v1/companies/{company_id}/reviews", json=body, headers=auth_headers(client, requester))


def decide(client, review_id, reviewer="legal", **body):
    return client.post(f"/api/v1/reviews/{review_id}/decision", json={"approved": True, "verification": "DOCUMENT_VERIFIED", "reason": "Khớp chứng từ", **body}, headers=auth_headers(client, reviewer))


def seller_company(client):
    response = client.post("/api/v1/companies", json=draft(), headers=auth_headers(client, "seller"))
    assert response.status_code == 201, response.text
    return response.json()


def test_nobody_sets_verified_labels_by_editing_the_profile(client):
    evidence = {"verification": "DOCUMENT_VERIFIED", "source": "Giấy phép mẫu", "source_date": "2025-01-01", "reviewed_by": "admin", "reviewed_on": "2025-02-01"}
    body = draft()
    body["company_name"] |= evidence
    assert client.post("/api/v1/companies", json=body, headers=auth_headers(client, "seller")).status_code == 403
    assert client.post("/api/v1/companies", json=body).status_code == 403  # default client is VAULT Admin
    company = seller_company(client)
    update = {"expected_revision": 1, "profile": deepcopy(company["profile"])}
    update["profile"]["company_name"] |= evidence
    assert client.put(f'/api/v1/companies/{company["id"]}', json=update).status_code == 403


def test_review_flow_verifies_with_evidence_and_keeps_lineage(client):
    company = seller_company(client)
    path = f'/api/v1/companies/{company["id"]}'
    seller = auth_headers(client, "seller")
    room = client.post("/api/v1/rooms", json={"company_id": company["id"], "title": "Hồ sơ pháp lý"}, headers=seller).json()
    document = client.post(f'/api/v1/rooms/{room["id"]}/documents', data={"folder": "LEGAL_CORPORATE", "title": "Giấy ĐKDN"},
                           files={"file": ("dkdn.txt", b"synthetic registration", "text/plain")}, headers=seller).json()
    assert review(client, company["id"], "unknown_field").status_code == 422
    assert review(client, company["id"], "founded_year").status_code == 409  # no value yet
    requested = review(client, company["id"], "employees", document_id=document["id"])
    assert requested.status_code == 201, requested.text
    item = requested.json()
    assert item["value"] == 120 and item["document"]["version_number"] == 1 and item["status"] == "PENDING"
    assert review(client, company["id"], "employees").status_code == 409  # already pending
    queue = client.get("/api/v1/reviews", headers=auth_headers(client, "legal")).json()
    assert item["id"] in {row["id"] for row in queue}
    assert client.get("/api/v1/reviews", headers=seller).status_code == 403
    assert decide(client, item["id"], reviewer="seller").status_code == 403
    assert decide(client, item["id"], verification=None).status_code == 422
    approved = decide(client, item["id"])
    assert approved.status_code == 200, approved.text
    fact = client.get(path, headers=seller).json()["profile"]["employees"]
    assert fact["verification"] == "DOCUMENT_VERIFIED" and fact["reviewed_by"] == "legal" and fact["source"] == "Giấy đăng ký doanh nghiệp mẫu"
    assert client.get("/api/v1/companies", headers=seller).json()[0]["verified_facts_count"] == 1
    assert decide(client, item["id"]).status_code == 409  # already decided
    # Editing a verified value must go back to self-declared; conflict cannot stay verified.
    profile = client.get(path, headers=seller).json()
    update = {"expected_revision": profile["revision"], "profile": deepcopy(profile["profile"])}
    update["profile"]["employees"]["value"] = 150
    assert client.put(path, json=update, headers=seller).status_code == 422
    update["profile"]["employees"] |= {"verification": "SELF_DECLARED", "issue": "CONFLICTED"}
    assert client.put(path, json=update, headers=seller).status_code == 200
    assert review(client, company["id"], "employees").status_code == 409  # conflicted


def test_review_rejection_self_review_and_stale_value(client):
    company = seller_company(client)
    path = f'/api/v1/companies/{company["id"]}'
    rejected = decide(client, review(client, company["id"], "tax_id").json()["id"], approved=False, verification=None, reason="Thiếu chứng từ")
    assert rejected.json()["status"] == "REJECTED" and rejected.json()["reason"] == "Thiếu chứng từ"
    own = review(client, company["id"], "sector", requester="admin").json()
    assert decide(client, own["id"], reviewer="admin").status_code == 409  # requester cannot decide
    stale = review(client, company["id"], "financials.2025.revenue").json()
    assert stale["value"] == "25000000000.01"
    seller = auth_headers(client, "seller")
    profile = client.get(path, headers=seller).json()
    update = {"expected_revision": profile["revision"], "profile": deepcopy(profile["profile"])}
    update["profile"]["financials"][0]["revenue"]["value"] = "26000000000"
    assert client.put(path, json=update, headers=seller).status_code == 200
    assert decide(client, stale["id"]).status_code == 409
    other_seller = auth_headers(client, "seller2")
    assert client.get(path + "/reviews", headers=other_seller).status_code == 404
    assert [row["field"] for row in client.get(path + "/reviews", headers=seller).json()] == ["financials.2025.revenue", "sector", "tax_id"]


def test_disabled_preview_does_not_enable_business_routes():
    with TestClient(create_app(Settings(_env_file=None, internal_preview_enabled=False, database_url=""))) as api:
        assert api.get("/api/v1/health").status_code == 200
        assert api.get("/api/v1/companies").status_code == 503


def test_external_origin_and_host_rejected(client):
    assert client.post("/api/v1/companies", json=draft(), headers={"Origin": "https://external.example"}).status_code == 403
    assert client.get("/api/v1/companies", headers={"Host": "external.example"}).status_code == 403
