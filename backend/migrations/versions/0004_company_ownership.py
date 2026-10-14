"""Add row-level ownership to company profiles."""
from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("companies", sa.Column("owner_username", sa.String(80), nullable=True))
    op.execute("UPDATE companies SET owner_username = 'admin' WHERE owner_username IS NULL")
    op.alter_column("companies", "owner_username", nullable=False)
    op.create_index("ix_companies_owner_username", "companies", ["owner_username"])


def downgrade():
    op.drop_index("ix_companies_owner_username", table_name="companies")
    op.drop_column("companies", "owner_username")
