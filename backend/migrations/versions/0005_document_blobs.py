"""Store document bytes in PostgreSQL so uploads survive restarts on ephemeral-disk hosts."""
from alembic import op
import sqlalchemy as sa

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("document_blobs",
        sa.Column("storage_key", sa.String(40), primary_key=True),
        sa.Column("content", sa.LargeBinary(), nullable=False))


def downgrade():
    op.drop_table("document_blobs")
