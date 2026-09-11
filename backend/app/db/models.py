from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.session import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (CheckConstraint("revision >= 1", name="ck_company_revision"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    alias: Mapped[str] = mapped_column(String(40), unique=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    tax_id: Mapped[str | None] = mapped_column(String(30), unique=True)
    profile: Mapped[dict] = mapped_column(JSONB)
    revision: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (UniqueConstraint("company_id", "title", name="uq_room_company_title"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint("current_version >= 1", name="ck_document_current_version"),
        CheckConstraint("folder IN ('LEGAL_CORPORATE','FINANCIAL_TAX','COMMERCIAL_OPERATIONS','TECHNOLOGY_IP','HUMAN_RESOURCES','QA_TRACKER')", name="ck_document_folder"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    room_id: Mapped[UUID] = mapped_column(ForeignKey("rooms.id"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    folder: Mapped[str] = mapped_column(String(40))
    current_version: Mapped[int] = mapped_column(Integer, default=1)


class DocumentVersion(Base):
    __tablename__ = "document_versions"
    __table_args__ = (
        UniqueConstraint("document_id", "number", name="uq_document_version"),
        CheckConstraint("number >= 1 AND size_bytes > 0", name="ck_version_positive"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    document_id: Mapped[UUID] = mapped_column(ForeignKey("documents.id"), index=True)
    number: Mapped[int] = mapped_column(Integer)
    filename: Mapped[str] = mapped_column(String(255))
    media_type: Mapped[str] = mapped_column(String(100))
    size_bytes: Mapped[int] = mapped_column(BigInteger)
    sha256: Mapped[str] = mapped_column(String(64))
    storage_key: Mapped[str] = mapped_column(String(40), unique=True)
    note: Mapped[str] = mapped_column(String(1000), default="")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
