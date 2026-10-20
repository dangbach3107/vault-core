from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, LargeBinary, String, UniqueConstraint
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
    owner_username: Mapped[str] = mapped_column(String(80), index=True)
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


class Deal(Base):
    __tablename__ = "deals"
    __table_args__ = (CheckConstraint("revision >= 1", name="ck_deal_revision"),)
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(200))
    state: Mapped[dict] = mapped_column(JSONB)
    revision: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class DocumentBlob(Base):
    """File bytes live in PostgreSQL so uploads survive restarts on hosts with ephemeral disks."""
    __tablename__ = "document_blobs"
    storage_key: Mapped[str] = mapped_column(String(40), primary_key=True)
    content: Mapped[bytes] = mapped_column(LargeBinary)


class FactReview(Base):
    """A request to verify one fact, decided by a reviewer who is not the requester."""
    __tablename__ = "fact_reviews"
    __table_args__ = (
        CheckConstraint("status IN ('PENDING', 'APPROVED', 'REJECTED')", name="ck_fact_review_status"),
        Index("ix_fact_reviews_company_status", "company_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"))
    field: Mapped[str] = mapped_column(String(80))
    value: Mapped[object] = mapped_column(JSONB)
    source: Mapped[str] = mapped_column(String(500))
    source_date: Mapped[date] = mapped_column(Date)
    document: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    note: Mapped[str] = mapped_column(String(1000), default="")
    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    verification: Mapped[str | None] = mapped_column(String(30), nullable=True)
    requested_by: Mapped[str] = mapped_column(String(80))
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    decided_by: Mapped[str | None] = mapped_column(String(80), nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reason: Mapped[str] = mapped_column(String(500), default="")

