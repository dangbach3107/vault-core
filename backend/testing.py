"""Configuration for synthetic integration tests, never the application's database."""
import json
import os

from sqlalchemy import make_url

from backend.app.core.config import REPOSITORY_ROOT


def test_database_url() -> str:
    configured = os.environ.get("TEST_DATABASE_URL")
    local = REPOSITORY_ROOT / ".tmp" / "database.json"
    if not configured and local.exists():
        configured = json.loads(local.read_text(encoding="utf-8"))["test_database_url"]
    if not configured:
        raise RuntimeError("Run scripts/start-database.ps1 or set TEST_DATABASE_URL to an isolated vault_test database.")
    url = make_url(configured)
    if url.drivername != "postgresql+psycopg" or url.database != "vault_test":
        raise RuntimeError("Integration tests require PostgreSQL database named vault_test; refusing another database.")
    return configured


def migrate_test_database():
    from alembic import command
    from alembic.config import Config
    previous = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = test_database_url()
    try:
        command.upgrade(Config(str(REPOSITORY_ROOT / "backend" / "alembic.ini")), "head")
    finally:
        if previous is None:
            os.environ.pop("DATABASE_URL", None)
        else:
            os.environ["DATABASE_URL"] = previous


if __name__ == "__main__":
    migrate_test_database()
    print("Isolated vault_test database migrated to head.")
