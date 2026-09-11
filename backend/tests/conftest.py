import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import Settings
from backend.app.db.session import build_engine
from backend.app.main import create_app
from backend.testing import migrate_test_database, test_database_url as database_url


@pytest.fixture(scope="session")
def postgres_engine():
    # Fail with setup instructions, rather than silently skipping persistence checks.
    migrate_test_database()
    engine = build_engine(Settings(_env_file=None, database_url=database_url()))
    yield engine
    engine.dispose()


@pytest.fixture
def client(postgres_engine, tmp_path):
    with postgres_engine.connect() as connection:
        transaction = connection.begin()
        app = create_app(Settings(_env_file=None, internal_preview_enabled=True, database_url="", upload_directory=tmp_path / "uploads", max_upload_bytes=1024))
        app.state.session_factory = sessionmaker(bind=connection, expire_on_commit=False, join_transaction_mode="create_savepoint")
        try:
            with TestClient(app) as api:
                yield api
        finally:
            transaction.rollback()
