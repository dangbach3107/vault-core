PASSWORD = "vault-demo"
ACTION_USERS = {
    "buyerRequest": "buyer", "identityRequested": "buyer", "indicativeLoiSubmitted": "buyer", "loiSubmitted": "buyer",
    "sellerProfile": "seller", "sellerL1Approval": "seller", "sellerL2Approval": "seller", "sellerFileApproval": "seller",
    "matchPrepared": "admin", "ndaRecorded": "admin", "vdrOpened": "admin", "dealClosed": "admin", "postDealHandoff": "admin",
    "legalL3Approval": "legal", "crossBorderApproval": "legal", "noEscrowConfirmed": "legal", "legalClosingChecklist": "legal",
    "techDdSigned": "tech", "prepPackageFeeRecorded": "finance", "successFeeRecorded": "finance",
}


def headers(client, username):
    login = client.post("/api/v1/auth/login", json={"username": username, "password": PASSWORD})
    assert login.status_code == 200, login.text
    return {"Authorization": f'Bearer {login.json()["access_token"]}'}


def create_deal(client):
    response = client.post("/api/v1/deals", json={}, headers=headers(client, "admin"))
    assert response.status_code == 201, response.text
    return response.json()


def act(client, deal_id, action):
    return client.post(f"/api/v1/deals/{deal_id}/actions/{action}", json={}, headers=headers(client, ACTION_USERS[action]))


def test_deal_gate_order_and_complete_sample(client):
    deal = create_deal(client)
    assert act(client, deal["id"], "vdrOpened").status_code == 409
    for action in [
        "buyerRequest", "sellerProfile", "prepPackageFeeRecorded", "sellerL1Approval",
        "matchPrepared", "identityRequested", "ndaRecorded", "sellerL2Approval",
        "indicativeLoiSubmitted", "legalL3Approval", "crossBorderApproval",
        "noEscrowConfirmed", "sellerFileApproval", "vdrOpened", "techDdSigned",
        "loiSubmitted", "legalClosingChecklist", "dealClosed", "successFeeRecorded",
        "postDealHandoff",
    ]:
        response = act(client, deal["id"], action)
        assert response.status_code == 200, (action, response.text)
    state = response.json()["state"]
    assert all(state["steps"].values())
    assert state["buyer_request"]["capability"]
    assert state["indicative_loi"]["non_binding"] is True
    assert len(state["tech_dd"]["findings"]) == 2
    assert {fee["type"] for fee in state["fees"]} == {
        "PREP_PACKAGE", "SUCCESS_FEE", "TECH_DD", "BUILD_TO_BUY"
    }
    assert state["closing"]["status"] == "SPA_SIGNED"
    assert state["handoff"]["status"] == "HANDED_OFF"


def test_deal_reset_and_complete_sample(client):
    deal = create_deal(client)
    admin = headers(client, "admin")
    completed = client.post(f'/api/v1/deals/{deal["id"]}/complete-sample', headers=admin)
    assert completed.status_code == 200
    assert all(completed.json()["state"]["steps"].values())
    reset = client.post(f'/api/v1/deals/{deal["id"]}/reset', headers=admin)
    assert reset.status_code == 200
    assert not any(reset.json()["state"]["steps"].values())


def test_role_login_and_authorization(client):
    deal = create_deal(client)
    assert client.get("/api/v1/deals", headers={"Authorization": ""}).status_code == 401
    buyer = headers(client, "buyer")
    assert client.post("/api/v1/deals", json={"title": "Unauthorized deal"}, headers=buyer).status_code == 403
    assert client.get("/api/v1/auth/me", headers=buyer).json()["role"] == "BUYER"
    assert client.post(f'/api/v1/deals/{deal["id"]}/actions/sellerProfile', json={}, headers=buyer).status_code == 403
    assert client.post("/api/v1/auth/login", json={"username": "buyer", "password": "wrong"}).status_code == 401


def test_person_scoped_access_request_approval_and_revoke(client):
    deal = create_deal(client)
    path = f'/api/v1/deals/{deal["id"]}'
    requested = client.post(path + "/access-requests", json={
        "requested_level": "L2", "purpose": "Evaluate strategic investment fit"
    }, headers=headers(client, "buyer"))
    assert requested.status_code == 200, requested.text
    request_row = requested.json()["state"]["access_requests"][0]
    assert request_row["requester"] == "buyer"
    assert request_row["status"] == "PENDING"
    assert client.post(path + f'/access-requests/{request_row["id"]}/decision', json={
        "approved": True, "reason": "Approved without expiry"
    }, headers=headers(client, "seller")).status_code == 422
    decided = client.post(path + f'/access-requests/{request_row["id"]}/decision', json={
        "approved": True, "reason": "Approved for selected diligence purpose",
        "expires_at": "2030-01-01T00:00:00Z"
    }, headers=headers(client, "seller"))
    assert decided.status_code == 200, decided.text
    grant = decided.json()["state"]["access_grants"][0]
    assert grant["user"] == "buyer"
    assert grant["access_level"] == "L2"
    assert grant["purpose"] == "Evaluate strategic investment fit"
    assert grant["approved_by"] == "seller"
    assert client.post(path + f'/access-grants/{grant["id"]}/revoke', json={
        "reason": "Deal stopped"
    }, headers=headers(client, "buyer")).status_code == 403
    revoked = client.post(path + f'/access-grants/{grant["id"]}/revoke', json={
        "reason": "Deal stopped"
    }, headers=headers(client, "seller"))
    assert revoked.status_code == 200
    assert revoked.json()["state"]["access_grants"][0]["revoked_at"]
    assert [event["type"] for event in revoked.json()["state"]["access_events"]] == [
        "ACCESS_REQUESTED", "ACCESS_APPROVED", "ACCESS_REVOKED"
    ]


def test_twenty_step_workflow_tracks_owner_conditions_and_stop_reason(client):
    deal = create_deal(client)
    admin = headers(client, "admin")
    wrong = headers(client, "buyer")
    path = f'/api/v1/deals/{deal["id"]}/workflow/1/complete'
    assert client.post(path, json={"note": "Lead qualified"}, headers=wrong).status_code == 403
    first = client.post(path, json={"note": "Lead qualified", "opened_data": ["Lead brief"]}, headers=admin)
    assert first.status_code == 200, first.text
    workflow = first.json()["state"]["workflow"]
    assert workflow["current_step"] == 2
    assert workflow["opened_data"] == ["Lead brief"]
    legal = headers(client, "legal")
    stopped = client.post(
        f'/api/v1/deals/{deal["id"]}/workflow/2/complete',
        json={"note": "Không xác minh được người đại diện", "outcome": "STOP"},
        headers=legal,
    )
    assert stopped.status_code == 200
    assert stopped.json()["state"]["workflow"]["status"] == "STOPPED"
    assert "người đại diện" in stopped.json()["state"]["workflow"]["stop_reason"]
