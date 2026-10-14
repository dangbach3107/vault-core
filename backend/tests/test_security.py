def login(client, username, password):
    return client.post("/api/v1/auth/login", json={"username": username, "password": password})


def test_login_lockout_after_repeated_failures_is_per_user(client):
    for _ in range(5):
        assert login(client, "legal", "wrong-password").status_code == 401
    locked = login(client, "legal", "vault-demo")
    assert locked.status_code == 429
    assert int(locked.headers["retry-after"]) > 0
    assert login(client, "finance", "vault-demo").status_code == 200


def test_successful_login_clears_earlier_failures(client):
    for _ in range(4):
        assert login(client, "tech", "wrong-password").status_code == 401
    assert login(client, "tech", "vault-demo").status_code == 200
    for _ in range(4):
        assert login(client, "tech", "wrong-password").status_code == 401
    assert login(client, "tech", "vault-demo").status_code == 200


def test_security_headers_are_sent(client):
    response = client.get("/api/v1/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "SAMEORIGIN"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert "strict-transport-security" not in response.headers  # only in production
