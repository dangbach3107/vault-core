from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.core.config import Settings


class Base(DeclarativeBase):
    """Metadata shared by authorized domain models and Alembic."""


def build_engine(settings: Settings) -> Engine:
    url = settings.database_url.get_secret_value()
    if not url:
        raise ValueError("Configure DATABASE_URL before using database tooling.")
    if url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url.removeprefix("postgresql://")
    elif url.startswith("postgres://"):
        url = "postgresql+psycopg://" + url.removeprefix("postgres://")
    if not url.startswith("postgresql+psycopg://"):
        raise ValueError("DATABASE_URL must use the postgresql+psycopg driver.")
    return create_engine(url, pool_pre_ping=True)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)
