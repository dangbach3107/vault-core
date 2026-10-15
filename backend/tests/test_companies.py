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
        "financials": [{"year": 2025, "revenue_vnd": {"value": "25000000000.01"}, "ebitda_vnd": {"value": "-1000.50"}}],
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
    assert loaded["profile"]["financials"][0]["revenue_vnd"]["value"] == "25000000000.01"
    assert loaded["profile"]["financials"][0]["ebitda_vnd"]["value"] == "-1000.50"
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
    assert set(anonymous.json()) == {"layer", "alias", "sector", "region", "revenue_band_vnd", "employee_band", "deal_type", "notice"}
    assert anonymous.json()["revenue_band_vnd"] == "20–dưới 50 tỷ"
    for private in ["Giả lập", "SYNTH-010101", "Bí mật", "Secret", "Sensitive", "Must never", "25000000000", "notes", "company_name"]:
        assert private not in anonymous.text
    identified = client.get(f"{path}/2").json()
    assert identified["facts"]["company_name"]["value"] == draft()["company_name"]["value"]
    assert "shareholders" not in identified["facts"]
    assert client.get(f"{path}/3").json()["facts"]["shareholders"]["value"] == "Sensitive shareholder"
    blank = create(client, {"company_name": {"value": "Blank"}, "employees": {"value": 0}})
    preview = client.get(f'/api/v1/companies/{blank["id"]}/preview/1').json()
    assert preview["revenue_band_vnd"] is None
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
    {"financials": [{"year": 2025, "revenue_vnd": {"value": "-1"}}]},
    {"financials": [{"year": 2025, "revenue_vnd": {"value": "1.001"}}]},
    {"company_name": {"value": "Unsupported", "verification": "DOCUMENT_VERIFIED"}},
    {"is_audited": True},
])
def test_validation(client, patch):
    body = draft() | patch
    assert client.post("/api/v1/companies", json=body).status_code == 422
    assert client.get("/api/v1/companies?q=SYNTH-010101").json() == []


def test_verification_lineage_and_conflicted_projection(client):
    body = draft()
    body["company_name"] |= {"verification": "THIRD_PARTY_CONFIRMED", "source": "Synthetic reviewer report", "source_date": "2025-01-01", "reviewed_by": "Reviewer sample", "reviewed_on": "2025-02-01"}
    company = create(client, body)
    assert company["profile"]["company_name"]["verification"] == "THIRD_PARTY_CONFIRMED"
    update = {"expected_revision": 1, "profile": deepcopy(company["profile"])}
    update["profile"]["company_name"]["value"] = "Changed after review"
    path = f'/api/v1/companies/{company["id"]}'
    assert client.put(path, json=update).status_code == 422
    update["profile"]["company_name"]["verification"] = "SELF_DECLARED"
    update["profile"]["region"]["issue"] = "CONFLICTED"
    assert client.put(path, json=update).status_code == 200
    assert client.get(path + "/preview/1").json()["region"] is None
    update["expected_revision"] = 2
    update["profile"]["company_name"]["verification"] = "DOCUMENT_VERIFIED"
    update["profile"]["company_name"]["issue"] = "EXPIRED"
    assert client.put(path, json=update).status_code == 422


def test_only_reviewer_marks_facts_verified(client):
    seller = auth_headers(client, "seller")
    evidence = {"verification": "DOCUMENT_VERIFIED", "source": "Giấy phép mẫu", "source_date": "2025-01-01", "reviewed_by": "seller", "reviewed_on": "2025-02-01"}
    body = draft()
    body["company_name"] |= evidence
    assert client.post("/api/v1/companies", json=body, headers=seller).status_code == 403
    company = client.post("/api/v1/companies", json=draft(), headers=seller).json()
    path = f'/api/v1/companies/{company["id"]}'
    update = {"expected_revision": 1, "profile": deepcopy(company["profile"])}
    update["profile"]["company_name"] |= evidence
    assert client.put(path, json=update, headers=seller).status_code == 403
    reviewed = client.put(path, json=update)  # the default client is VAULT Admin, the reviewer
    assert reviewed.status_code == 200
    # The seller may still save other self-declared edits without touching the reviewed fact.
    again = {"expected_revision": 2, "profile": deepcopy(reviewed.json()["profile"])}
    again["profile"]["employees"]["value"] = 12
    assert client.put(path, json=again, headers=seller).status_code == 200


def test_disabled_preview_does_not_enable_business_routes():
    with TestClient(create_app(Settings(_env_file=None, internal_preview_enabled=False, database_url=""))) as api:
        assert api.get("/api/v1/health").status_code == 200
        assert api.get("/api/v1/companies").status_code == 503


def test_external_origin_and_host_rejected(client):
    assert client.post("/api/v1/companies", json=draft(), headers={"Origin": "https://external.example"}).status_code == 403
    assert client.get("/api/v1/companies", headers={"Host": "external.example"}).status_code == 403
