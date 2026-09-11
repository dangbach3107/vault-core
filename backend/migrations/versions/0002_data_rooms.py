"""Local synthetic deal rooms and immutable document versions."""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("rooms",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("company_id", sa.Uuid(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("company_id", "title", name="uq_room_company_title"))
    op.create_index("ix_rooms_company_id", "rooms", ["company_id"])
    op.create_table("documents",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("room_id", sa.Uuid(), sa.ForeignKey("rooms.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("folder", sa.String(40), nullable=False),
        sa.Column("current_version", sa.Integer(), nullable=False),
        sa.CheckConstraint("current_version >= 1", name="ck_document_current_version"),
        sa.CheckConstraint("folder IN ('LEGAL_CORPORATE','FINANCIAL_TAX','COMMERCIAL_OPERATIONS','TECHNOLOGY_IP','HUMAN_RESOURCES','QA_TRACKER')", name="ck_document_folder"))
    op.create_index("ix_documents_room_id", "documents", ["room_id"])
    op.create_table("document_versions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("document_id", sa.Uuid(), sa.ForeignKey("documents.id"), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("media_type", sa.String(100), nullable=False),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("storage_key", sa.String(40), nullable=False, unique=True),
        sa.Column("note", sa.String(1000), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("document_id", "number", name="uq_document_version"),
        sa.CheckConstraint("number >= 1 AND size_bytes > 0", name="ck_version_positive"))
    op.create_index("ix_document_versions_document_id", "document_versions", ["document_id"])


def downgrade():
    op.drop_table("document_versions")
    op.drop_table("documents")
    op.drop_table("rooms")
