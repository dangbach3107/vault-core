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


def test_disabled_preview_does_not_enable_business_routes():
    with TestClient(create_app(Settings(_env_file=None, internal_preview_enabled=False, database_url=""))) as api:
        assert api.get("/api/v1/health").status_code == 200
        assert api.get("/api/v1/companies").status_code == 503


def test_external_origin_and_host_rejected(client):
    assert client.post("/api/v1/companies", json=draft(), headers={"Origin": "https://external.example"}).status_code == 403
    assert client.get("/api/v1/companies", headers={"Host": "external.example"}).status_code == 403
