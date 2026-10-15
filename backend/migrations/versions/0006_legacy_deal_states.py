"""Bring deals created before buyer assignment / signing-closing split into the current shape.

Legacy rows have no `buyer_username`. A row where a buyer already sent an access request is
given to that buyer, so the request stays visible to them; other rows get the buyer accounts
not used yet, in creation order. A legacy row completed with the old sample button (every step done,
closing "SPA_SIGNED") is rebuilt as labelled sample data, so signing and closing agree.
Other rows only gain the new keys; their progress is kept.
"""
import json

from alembic import op
import sqlalchemy as sa

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None

BUYERS = ["buyer", "buyer2"]  # the synthetic buyer accounts in core.auth.USERS


def upgrade():
    # Uses the app's own state helpers so the result matches what the API produces today.
    from backend.app.api.deals import normalize, sample_state

    connection = op.get_bind()
    rows = connection.execute(sa.text("SELECT id, state FROM deals ORDER BY created_at")).all()
    legacy = [(row.id, row.state) for row in rows if "buyer_username" not in row.state]
    owners = {}
    for deal_id, state in legacy:
        requesters = [item["requester"] for item in state.get("access_requests", []) if item.get("requester") in BUYERS]
        if requesters:
            owners[deal_id] = requesters[0]
    free = [name for name in BUYERS if name not in owners.values()] or BUYERS
    for index, deal_id in enumerate(deal_id for deal_id, _ in legacy if deal_id not in owners):
        owners[deal_id] = free[index % len(free)]
    for deal_id, state in legacy:
        old_sample = all(state.get("steps", {}).values()) and (state.get("closing") or {}).get("status") == "SPA_SIGNED"
        state = normalize(state)
        state["buyer_username"] = owners[deal_id]
        if old_sample:
            state = sample_state(state)
        connection.execute(
            sa.text("UPDATE deals SET state = CAST(:state AS jsonb), revision = revision + 1, updated_at = now() WHERE id = :id"),
            {"state": json.dumps(state), "id": deal_id},
        )


def downgrade():
    # Data-only change; the previous shape is not restored.
    pass
