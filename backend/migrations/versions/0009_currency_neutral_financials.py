"""Financial facts become currency-neutral: revenue_vnd/ebitda_vnd -> revenue/ebitda.

The profile now states its reporting currency (VND or JPY). Existing profiles were all
entered in VND, so they get currency "VND". Fact review paths are renamed to match.
"""
import json

from alembic import op
import sqlalchemy as sa

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None

RENAMES = {"revenue_vnd": "revenue", "ebitda_vnd": "ebitda"}


def rename_rows(profile, renames):
    for row in profile.get("financials") or []:
        for old, new in renames.items():
            if old in row:
                row[new] = row.pop(old)
    return profile


def migrate(renames, currency):
    connection = op.get_bind()
    for row in connection.execute(sa.text("SELECT id, profile FROM companies")).all():
        profile = rename_rows(dict(row.profile), renames)
        if currency:
            profile.setdefault("currency", currency)
        else:
            profile.pop("currency", None)
        connection.execute(sa.text("UPDATE companies SET profile = CAST(:profile AS jsonb) WHERE id = :id"),
                           {"profile": json.dumps(profile), "id": row.id})
    for old, new in renames.items():
        connection.execute(sa.text("UPDATE fact_reviews SET field = regexp_replace(field, :pattern, :replacement) WHERE field LIKE :like"),
                           {"pattern": f"\\.{old}$", "replacement": f".{new}", "like": f"financials.%.{old}"})


def upgrade():
    migrate(RENAMES, "VND")


def downgrade():
    migrate({new: old for old, new in RENAMES.items()}, None)
