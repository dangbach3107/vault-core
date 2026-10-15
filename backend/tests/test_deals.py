import io
from datetime import date, timedelta

PASSWORD = "vault-demo"
ACTION_USERS = {
    "buyerRequest": "buyer", "identityRequested": "buyer", "indicativeLoiSubmitted": "buyer", "loiSubmitted": "buyer",
    "sellerProfile": "seller", "sellerL1Approval": "seller", "sellerL2Approval": "seller", "sellerFileApproval": "seller",
    "matchPrepared": "admin", "ndaRecorded": "admin", "vdrOpened": "admin", "dealClosed": "admin", "postDealHandoff": "admin",
    "legalL3Approval": "legal", "crossBorderApproval": "legal", "noEscrowConfirmed": "legal", "legalClosingChecklist": "legal", "spaSigned": "legal",
    "techDdSigned": "tech", "prepPackageFeeRecorded": "finance", "successFeeRecorded": "finance",
}
ORDER = [
    "buyerRequest", "sellerProfile", "sellerL1Approval", "matchPrepared", "identityRequested", "ndaRecorded",
    "sellerL2Approval", "indicativeLoiSubmitted", "legalL3Approval", "crossBorderApproval", "noEscrowConfirmed",
    "sellerFileApproval", "vdrOpened", "techDdSigned", "loiSubmitted", "legalClosingChecklist", "spaSigned",
    "dealClosed",
]
FUTURE = "2030-01-01T00:00:00Z"


def headers(client, username):
    login = client.post("/api/v1/auth/login", json={"username": username, "password": PASSWORD})
    assert login.status_code == 200, login.text
    return {"Authorization": f'Bearer {login.json()["access_token"]}'}


def seller_company(client):
    response = client.post("/api/v1/companies", json={"company_name": {"value": "Synthetic Seller"}}, headers=headers(client, "seller"))
    assert response.status_code == 201, response.text
    return response.json()


def create_deal(client, buyer="buyer", company=None):
    company = company or seller_company(client)
    response = client.post("/api/v1/deals", json={"seller_company_id": company["id"], "buyer_username": buyer}, headers=headers(client, "admin"))
    assert response.status_code == 201, response.text
    return response.json()


def act(client, deal_id, action, note="Ghi chú bằng chứng mẫu"):
    return client.post(f"/api/v1/deals/{deal_id}/actions/{action}", json={"note": note}, headers=headers(client, ACTION_USERS[action]))


def run_until(client, deal_id, stop):
    for action in ORDER[:ORDER.index(stop)]:
        response = act(client, deal_id, action)
        assert response.status_code == 200, (action, response.text)


def upload(client, company_id, content=b"synthetic text v1"):
    seller = headers(client, "seller")
    room = client.post("/api/v1/rooms", json={"company_id": company_id, "title": "Deal room"}, headers=seller).json()
    document = client.post(f'/api/v1/rooms/{room["id"]}/documents', data={"folder": "LEGAL_CORPORATE", "title": "Sample contract"},
                           files={"file": ("contract.txt", io.BytesIO(content), "text/plain")}, headers=seller)
    assert document.status_code == 201, document.text
    return room, document.json()


def test_gate_order_records_evidence_and_splits_signing_from_closing(client):
    deal = create_deal(client)
    assert act(client, deal["id"], "vdrOpened").status_code == 409
    assert act(client, deal["id"], "buyerRequest", note="").status_code == 422
    run_until(client, deal["id"], "dealClosed")
    signed = client.get(f'/api/v1/deals/{deal["id"]}', headers=headers(client, "admin")).json()["state"]
    # Signed but not yet closed is a real, visible state.
    assert signed["signing"]["status"] == "SIGNED"
    assert signed["closing"] is None
    closed = act(client, deal["id"], "dealClosed").json()["state"]
    assert closed["closing"]["status"] == "CLOSED"
    # Nothing is invented: the buyer request is exactly what the buyer wrote.
    assert closed["buyer_request"]["summary"] == "Ghi chú bằng chứng mẫu"
    assert closed["buyer_request"]["by"] == "buyer"
    assert closed["tech_dd"]["findings"] == []
    assert closed["fees"] == [] and closed["opportunities"] == []
    assert act(client, deal["id"], "successFeeRecorded").status_code == 409  # no fee line yet


def test_deal_visibility_is_minimal_per_role(client):
    deal = create_deal(client)
    other = create_deal(client, buyer="buyer2")
    path = f'/api/v1/deals/{deal["id"]}'
    visible = {row["id"] for row in client.get("/api/v1/deals", headers=headers(client, "buyer")).json()}
    assert deal["id"] in visible and other["id"] not in visible
    assert client.get(f'/api/v1/deals/{other["id"]}', headers=headers(client, "buyer")).status_code == 404
    assert client.get(path, headers=headers(client, "seller2")).status_code == 404
    assert act(client, other["id"], "buyerRequest").status_code == 404
    buyer_state = client.get(path, headers=headers(client, "buyer")).json()["state"]
    for hidden in ("fees", "tech_dd", "approvals", "seller_profile", "records", "legal_closing_checklist"):
        assert hidden not in buyer_state
    assert "history" not in buyer_state["workflow"]
    seller_state = client.get(path, headers=headers(client, "seller")).json()["state"]
    assert "tech_dd" in seller_state and "fees" not in seller_state
    finance_state = client.get(path, headers=headers(client, "finance")).json()["state"]
    assert set(finance_state) == {"steps", "buyer_username", "is_sample", "workflow", "signing", "closing", "fees"}
    tech_state = client.get(path, headers=headers(client, "tech")).json()["state"]
    assert "fees" not in tech_state and "access_grants" not in tech_state and "tech_dd" in tech_state


def test_create_deal_requires_buyer_account(client):
    admin = headers(client, "admin")
    assert client.post("/api/v1/deals", json={"buyer_username": "seller"}, headers=admin).status_code == 422
    assert client.post("/api/v1/deals", json={"title": "x"}, headers=headers(client, "buyer")).status_code == 403
    catalog = client.get("/api/v1/deals/catalog", headers=admin).json()
    assert catalog["buyers"] == ["buyer", "buyer2"]
    assert [row["key"] for row in catalog["actions"]].index("spaSigned") < [row["key"] for row in catalog["actions"]].index("dealClosed")
    assert client.get("/api/v1/deals/catalog", headers=headers(client, "buyer")).json()["buyers"] == []


def test_teaser_needs_seller_approval_and_l2_needs_nda_and_grant(client):
    deal = create_deal(client)
    path = f'/api/v1/deals/{deal["id"]}'
    buyer = headers(client, "buyer")
    assert client.get(path + "/teaser", headers=buyer).status_code == 409
    run_until(client, deal["id"], "matchPrepared")
    assert client.get(path + "/teaser", headers=buyer).json()["layer"] == 1
    assert client.get(path + "/profile/2", headers=buyer).status_code == 403
    request_id = client.post(path + "/access-requests", json={"requested_level": "L2", "purpose": "Đánh giá phù hợp"}, headers=buyer).json()["state"]["access_requests"][0]["id"]
    decision = {"approved": True, "reason": "Đủ điều kiện", "expires_at": FUTURE}
    # NDA is a precondition, not an automatic opening.
    assert client.post(path + f"/access-requests/{request_id}/decision", json=decision, headers=headers(client, "seller")).status_code == 409
    run_until(client, deal["id"], "sellerL2Approval")
    assert client.get(path + "/profile/2", headers=buyer).status_code == 403
    granted = client.post(path + f"/access-requests/{request_id}/decision", json=decision, headers=headers(client, "seller"))
    assert granted.status_code == 200, granted.text
    assert granted.json()["state"]["access_grants"][0]["basis"] == "NDA"
    assert client.get(path + "/profile/2", headers=buyer).json()["layer"] == 2
    assert client.get(path + "/profile/3", headers=buyer).status_code == 403


def test_file_version_grant_view_download_expiry_and_revoke(client):
    company = seller_company(client)
    deal = create_deal(client, company=company)
    path = f'/api/v1/deals/{deal["id"]}'
    room, document = upload(client, company["id"])
    run_until(client, deal["id"], "sellerL2Approval")
    buyer = headers(client, "buyer")
    request_body = {"requested_level": "L2", "purpose": "Đọc hợp đồng", "document_ids": [document["id"]]}
    assert client.post(path + "/access-requests", json={**request_body, "document_ids": ["00000000-0000-0000-0000-000000000000"]}, headers=buyer).status_code == 422
    request_id = client.post(path + "/access-requests", json=request_body, headers=buyer).json()["state"]["access_requests"][0]["id"]
    assert client.post(path + f"/access-requests/{request_id}/decision", json={"approved": True, "reason": "Không hạn"}, headers=headers(client, "legal")).status_code == 422
    granted = client.post(path + f"/access-requests/{request_id}/decision", json={"approved": True, "reason": "Chỉ xem", "expires_at": FUTURE, "basis_ref": "NDA-001"}, headers=headers(client, "legal")).json()
    grant = granted["state"]["access_grants"][0]
    assert grant["documents"][0]["version_number"] == 1 and grant["can_download"] is False
    files = client.get(path + "/documents", headers=buyer).json()
    assert len(files) == 1 and files[0]["version_number"] == 1
    # The approver may narrow the files when deciding a later request.
    later = client.post(path + "/access-requests", json={"requested_level": "L2", "purpose": "Thêm tài liệu"}, headers=buyer).json()["state"]["access_requests"][1]["id"]
    narrowed = client.post(path + f"/access-requests/{later}/decision", json={"approved": True, "reason": "Chọn file", "expires_at": FUTURE, "document_ids": [document["id"]], "can_download": True}, headers=headers(client, "seller")).json()
    assert narrowed["state"]["access_grants"][1]["documents"][0]["document_id"] == document["id"]
    content = f'{path}/documents/{grant["id"]}/{document["id"]}/content'
    assert client.get(content, headers=buyer).content == b"synthetic text v1"
    assert client.get(content + "?download=true", headers=buyer).status_code == 403
    # A new upload does not widen the grant; the buyer keeps seeing the approved version.
    client.post(f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}/versions', files={"file": ("contract.txt", io.BytesIO(b"synthetic text v2"), "text/plain")}, headers=headers(client, "seller"))
    files = client.get(path + "/documents", headers=buyer).json()
    assert {row["version_number"] for row in files} == {1} and {row["latest_version"] for row in files} == {2}
    assert client.get(content, headers=buyer).content == b"synthetic text v1"
    assert client.get(content, headers=headers(client, "buyer2")).status_code in {403, 404}
    events = client.get(path, headers=buyer).json()["state"]["access_events"]
    assert "FILE_VIEWED" in [event["type"] for event in events]
    revoked = client.post(path + f'/access-grants/{grant["id"]}/revoke', json={"reason": "Deal dừng"}, headers=headers(client, "seller"))
    assert revoked.json()["state"]["access_grants"][0]["status"] == "REVOKED"
    assert client.get(content, headers=buyer).status_code == 403
    assert [row["grant_id"] for row in client.get(path + "/documents", headers=buyer).json()] == [narrowed["state"]["access_grants"][1]["id"]]


def test_expired_grant_closes_access(client, monkeypatch):
    from backend.app.api import deals
    deal = create_deal(client)
    path = f'/api/v1/deals/{deal["id"]}'
    run_until(client, deal["id"], "sellerL2Approval")
    buyer = headers(client, "buyer")
    request_id = client.post(path + "/access-requests", json={"requested_level": "L2", "purpose": "Đánh giá"}, headers=buyer).json()["state"]["access_requests"][0]["id"]
    client.post(path + f"/access-requests/{request_id}/decision", json={"approved": True, "reason": "Đồng ý", "expires_at": FUTURE}, headers=headers(client, "seller"))
    assert client.get(path + "/profile/2", headers=buyer).status_code == 200
    original = deals.grant_status
    monkeypatch.setattr(deals, "grant_status", lambda grant, at=None: original(grant, at) if grant.get("revoked_at") else "EXPIRED")
    assert client.get(path + "/profile/2", headers=buyer).status_code == 403
    assert client.get(path, headers=buyer).json()["state"]["access_grants"][0]["status"] == "EXPIRED"


def test_tech_dd_findings_are_separate_from_sign_off(client):
    deal = create_deal(client)
    path = f'/api/v1/deals/{deal["id"]}'
    tech = headers(client, "tech")
    finding = {"title": "Giấy phép mã nguồn mở", "severity": "HIGH", "impact_vnd": "90000000"}
    assert client.post(path + "/tech-dd/findings", json=finding, headers=tech).status_code == 409
    run_until(client, deal["id"], "techDdSigned")
    assert client.post(path + "/tech-dd/findings", json=finding, headers=headers(client, "buyer")).status_code == 403
    added = client.post(path + "/tech-dd/findings", json=finding, headers=tech)
    assert added.status_code == 201, added.text
    finding_id = added.json()["state"]["tech_dd"]["findings"][0]["id"]
    assert act(client, deal["id"], "techDdSigned").status_code == 409  # open finding blocks sign-off
    status = path + f"/tech-dd/findings/{finding_id}/status"
    assert client.post(status, json={"status": "RESOLVED", "note": "Tự đóng"}, headers=headers(client, "seller")).status_code == 403
    assert client.post(status, json={"status": "RESPONDED", "note": "Đã bổ sung giấy phép"}, headers=headers(client, "seller")).status_code == 200
    assert act(client, deal["id"], "techDdSigned").status_code == 409
    assert client.post(status, json={"status": "RESOLVED", "note": "Đã kiểm tra"}, headers=tech).status_code == 200
    signed = act(client, deal["id"], "techDdSigned").json()["state"]["tech_dd"]
    assert signed["signed_off_by"] == "tech"
    assert [row["status"] for row in signed["findings"][0]["history"]] == ["OPEN", "RESPONDED", "RESOLVED"]


def test_fee_invoice_partial_overdue_and_paid(client):
    deal = create_deal(client)
    path = f'/api/v1/deals/{deal["id"]}'
    finance = headers(client, "finance")
    today = date.today()
    assert client.post(path + "/fees", json={"type": "PREP_PACKAGE", "amount_vnd": "100", "due_on": today.isoformat()}, headers=headers(client, "admin")).status_code == 403
    assert client.post(path + "/fees", json={"type": "SUCCESS_FEE", "amount_vnd": "100", "due_on": today.isoformat()}, headers=finance).status_code == 409
    fee = client.post(path + "/fees", json={"type": "PREP_PACKAGE", "amount_vnd": "150000000", "due_on": (today + timedelta(days=10)).isoformat()}, headers=finance).json()["state"]["fees"][0]
    assert fee["status"] == "DRAFT"
    fee_path = path + f'/fees/{fee["id"]}'
    assert client.post(fee_path + "/payments", json={"amount_vnd": "1", "paid_on": today.isoformat(), "reference": "x"}, headers=finance).status_code == 409
    assert client.post(fee_path + "/invoice", json={"invoice_number": "HD-1", "issued_on": today.isoformat()}, headers=finance).json()["state"]["fees"][0]["status"] == "INVOICED"
    partial = client.post(fee_path + "/payments", json={"amount_vnd": "50000000", "paid_on": today.isoformat(), "reference": "UNC-1"}, headers=finance).json()["state"]["fees"][0]
    assert partial["status"] == "PARTIALLY_PAID" and partial["balance_vnd"] == "100000000"
    assert client.post(fee_path + "/payments", json={"amount_vnd": "100000001", "paid_on": today.isoformat(), "reference": "UNC-2"}, headers=finance).status_code == 409
    paid = client.post(fee_path + "/payments", json={"amount_vnd": "100000000", "paid_on": today.isoformat(), "reference": "UNC-2"}, headers=finance).json()["state"]["fees"][0]
    assert paid["status"] == "PAID"
    from backend.app.api.deals import fee_view
    overdue = {**fee, "invoice": {"number": "HD-2"}, "payments": [{"amount_vnd": "1"}], "due_on": (today - timedelta(days=1)).isoformat()}
    assert fee_view(overdue)["status"] == "OVERDUE"


def test_reset_and_sample_are_labelled(client):
    deal = create_deal(client)
    admin = headers(client, "admin")
    completed = client.post(f'/api/v1/deals/{deal["id"]}/complete-sample', headers=admin).json()["state"]
    assert completed["is_sample"] is True and all(completed["steps"].values())
    assert completed["signing"]["status"] == "SIGNED" and completed["closing"]["status"] == "CLOSED"
    assert all("minh họa" in row["note"] for row in completed["opportunities"])
    assert {fee["status"] for fee in completed["fees"]} == {"PAID", "OVERDUE", "INVOICED"}
    reset = client.post(f'/api/v1/deals/{deal["id"]}/reset', headers=admin).json()["state"]
    assert not any(reset["steps"].values()) and reset["is_sample"] is False and reset["buyer_username"] == "buyer"


def test_role_login_and_authorization(client):
    deal = create_deal(client)
    assert client.get("/api/v1/deals", headers={"Authorization": ""}).status_code == 401
    buyer = headers(client, "buyer")
    assert client.get("/api/v1/auth/me", headers=buyer).json()["role"] == "BUYER"
    assert client.post(f'/api/v1/deals/{deal["id"]}/actions/sellerProfile', json={}, headers=buyer).status_code == 403
    assert client.post(f'/api/v1/deals/{deal["id"]}/actions/sellerProfile', json={}, headers=headers(client, "seller2")).status_code == 404
    assert client.post("/api/v1/auth/login", json={"username": "buyer", "password": "wrong"}).status_code == 401


def test_rejected_request_and_revoke_events(client):
    deal = create_deal(client)
    path = f'/api/v1/deals/{deal["id"]}'
    run_until(client, deal["id"], "sellerL2Approval")
    buyer = headers(client, "buyer")
    first = client.post(path + "/access-requests", json={"requested_level": "L3", "purpose": "Đọc tài liệu hạn chế"}, headers=buyer).json()["state"]["access_requests"][0]["id"]
    rejected = client.post(path + f"/access-requests/{first}/decision", json={"approved": False, "reason": "Chưa có LOI"}, headers=headers(client, "seller"))
    assert rejected.json()["state"]["access_requests"][0]["status"] == "REJECTED"
    second = client.post(path + "/access-requests", json={"requested_level": "L2", "purpose": "Đánh giá"}, headers=buyer).json()["state"]["access_requests"][1]["id"]
    grant = client.post(path + f"/access-requests/{second}/decision", json={"approved": True, "reason": "Đồng ý", "expires_at": FUTURE}, headers=headers(client, "seller")).json()["state"]["access_grants"][0]
    assert client.post(path + f'/access-grants/{grant["id"]}/revoke', json={"reason": "Deal dừng"}, headers=buyer).status_code == 403
    revoked = client.post(path + f'/access-grants/{grant["id"]}/revoke', json={"reason": "Deal dừng"}, headers=headers(client, "seller")).json()["state"]
    assert [event["type"] for event in revoked["access_events"]] == ["ACCESS_REQUESTED", "ACCESS_REJECTED", "ACCESS_REQUESTED", "ACCESS_APPROVED", "ACCESS_REVOKED"]


def test_twenty_step_workflow_tracks_owner_conditions_and_stop_reason(client):
    deal = create_deal(client)
    admin = headers(client, "admin")
    path = f'/api/v1/deals/{deal["id"]}/workflow/1/complete'
    assert client.post(path, json={"note": "Lead qualified"}, headers=headers(client, "buyer")).status_code == 403
    first = client.post(path, json={"note": "Lead qualified", "opened_data": ["Lead brief"]}, headers=admin)
    assert first.status_code == 200, first.text
    workflow = first.json()["state"]["workflow"]
    assert workflow["current_step"] == 2
    assert workflow["opened_data"] == ["Lead brief"]
    stopped = client.post(
        f'/api/v1/deals/{deal["id"]}/workflow/2/complete',
        json={"note": "Không xác minh được người đại diện", "outcome": "STOP"},
        headers=headers(client, "legal"),
    )
    assert stopped.status_code == 200
    assert stopped.json()["state"]["workflow"]["status"] == "STOPPED"
    assert "người đại diện" in stopped.json()["state"]["workflow"]["stop_reason"]
