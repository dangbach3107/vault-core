import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import make_url

from backend.app.core.config import Settings
from backend.app.db.session import Base, build_engine
from backend.app.main import create_app
from backend.export_openapi import CONTRACT, contract_text


def test_health_works_without_database_and_exposes_no_secret():
    settings = Settings(_env_file=None, project_name="VAULT test", database_url="")
    with TestClient(create_app(settings)) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
            "service": "VAULT test",
            "version": settings.version,
            "scope": "liveness",
        }
        assert client.post("/api/v1/profile/generate", json={}).status_code == 404


def test_environment_file_and_process_precedence(tmp_path, monkeypatch):
    example = tmp_path / ".env"
    example.write_text("PROJECT_NAME=From file\nDATABASE_URL=\n", encoding="utf-8")
    monkeypatch.delenv("PROJECT_NAME", raising=False)
    assert Settings(_env_file=example).project_name == "From file"
    monkeypatch.setenv("PROJECT_NAME", "From process")
    assert Settings(_env_file=example).project_name == "From process"


def test_shared_contract_matches_backend():
    assert json.loads(CONTRACT.read_text(encoding="utf-8")) == json.loads(contract_text())


def test_database_is_explicit_and_uses_postgresql_without_connecting():
    with pytest.raises(ValueError, match="Configure DATABASE_URL"):
        build_engine(Settings(_env_file=None, database_url=""))
    engine = build_engine(
        Settings(_env_file=None, database_url="postgresql+psycopg://vault@127.0.0.1/vault")
    )
    try:
        assert engine.url.drivername == make_url("postgresql+psycopg://").drivername
        assert "companies" in Base.metadata.tables
    finally:
        engine.dispose()
