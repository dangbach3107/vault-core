"""Pre-deployment verification script for VAULT Core."""
import sys
from fastapi.testclient import TestClient
from backend.app.core.config import Settings
from backend.app.main import create_app

def test_readiness():
    print("1. Testing settings defaults...")
    settings = Settings(_env_file=None, allow_public_access=True, internal_preview_enabled=True)
    assert settings.allow_public_access is True
    assert settings.cors_origins == "*"
    print("   [PASS] Settings initialized successfully.")

    print("2. Testing FastAPI application initialization...")
    app = create_app(settings)
    client = TestClient(app)
    
    print("3. Testing /api/v1/health endpoint...")
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    print(f"   [PASS] Health check OK: {res.json()}")

    print("4. Testing CORS headers on preflight...")
    res = client.options(
        "/api/v1/health",
        headers={
            "Origin": "https://vault-preview.vercel.app",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert res.status_code == 200
    assert res.headers.get("access-control-allow-origin") == "https://vault-preview.vercel.app" or res.headers.get("access-control-allow-origin") == "*"
    print("   [PASS] CORS configured properly.")

    print("5. Testing public access without localhost guard...")
    # Health and routes accessible under cloud Host
    res = client.get("/api/v1/health", headers={"Host": "vault-api.onrender.com"})
    assert res.status_code == 200
    print("   [PASS] Host check passed.")

    print("\nALL PRE-DEPLOYMENT CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_readiness()
