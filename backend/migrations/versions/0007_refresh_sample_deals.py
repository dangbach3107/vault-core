"""Rebuild sample deals so they carry the typed NDA/LOI/offer/handoff records.

Only rows flagged `is_sample` are touched; real deals keep their data. The responsible
buyer and seller link are preserved.
"""
import json

from alembic import op
import sqlalchemy as sa

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade():
    # Uses the app's own sample builder so the rows match what the API produces today.
    from backend.app.api.deals import normalize, sample_state

    connection = op.get_bind()
    rows = connection.execute(sa.text("SELECT id, state FROM deals WHERE state->>'is_sample' = 'true'")).all()
    for row in rows:
        connection.execute(
            sa.text("UPDATE deals SET state = CAST(:state AS jsonb), revision = revision + 1, updated_at = now() WHERE id = :id"),
            {"state": json.dumps(sample_state(normalize(row.state))), "id": row.id},
        )


def downgrade():
    # Data-only change; the previous sample content is not restored.
    pass
