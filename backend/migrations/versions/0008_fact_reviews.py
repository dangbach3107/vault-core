"""Fact review requests: verification is a reviewer decision with evidence."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "fact_reviews",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("company_id", sa.Uuid(), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("field", sa.String(80), nullable=False),
        sa.Column("value", postgresql.JSONB(), nullable=False),
        sa.Column("source", sa.String(500), nullable=False),
        sa.Column("source_date", sa.Date(), nullable=False),
        sa.Column("document", postgresql.JSONB(), nullable=True),
        sa.Column("note", sa.String(1000), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("verification", sa.String(30), nullable=True),
        sa.Column("requested_by", sa.String(80), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("decided_by", sa.String(80), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reason", sa.String(500), nullable=False),
        sa.CheckConstraint("status IN ('PENDING', 'APPROVED', 'REJECTED')", name="ck_fact_review_status"),
    )
    op.create_index("ix_fact_reviews_company_status", "fact_reviews", ["company_id", "status"])


def downgrade():
    op.drop_index("ix_fact_reviews_company_status", table_name="fact_reviews")
    op.drop_table("fact_reviews")
