from backend.app.db.models import Company
from backend.app.schemas.company import (
    AnonymousPreview, CompanyInput, CompanyResponse, IdentifiedPreview, RestrictedPreview,
)

RESTRICTED = {"shareholders", "decision_maker", "permitted_use"}


def response(company: Company) -> CompanyResponse:
    return CompanyResponse(
        id=company.id, alias=company.alias, revision=company.revision,
        created_at=company.created_at, updated_at=company.updated_at, profile=company.profile,
    )


def changed_verified_facts(old: dict, new: dict) -> bool:
    """Changed values must be saved as self-declared before a fresh review."""
    if isinstance(new, dict):
        if "verification" in new:
            return old.get("value") != new.get("value") and new["verification"] != "SELF_DECLARED"
        return any(changed_verified_facts(old.get(key, {}), value) for key, value in new.items())
    if isinstance(new, list):
        old_years = {row["year"]: row for row in old} if isinstance(old, list) else {}
        return any(changed_verified_facts(old_years.get(row["year"], {}), row) for row in new)
    return False


def preview(company: Company, layer: int):
    profile = CompanyInput.model_validate(company.profile)
    if layer == 1:
        def safe(fact):
            return fact.value if fact.issue == "NONE" else None

        revenue = None
        if profile.financials:
            revenue = safe(max(profile.financials, key=lambda row: row.year).revenue_vnd)
        def band(value, boundaries, labels):
            if value is None:
                return None
            return next((labels[i] for i, limit in enumerate(boundaries) if value < limit), labels[-1])
        return AnonymousPreview(
            alias=company.alias, sector=safe(profile.sector), region=safe(profile.region),
            revenue_band_vnd=band(revenue, [20e9, 50e9, 100e9, 200e9, 500e9],
                ["Dưới 20 tỷ", "20–dưới 50 tỷ", "50–dưới 100 tỷ", "100–dưới 200 tỷ", "200–dưới 500 tỷ", "Từ 500 tỷ"]),
            employee_band=band(safe(profile.employees), [50, 200, 1000], ["Dưới 50", "50–199", "200–999", "Từ 1.000"]),
            deal_type=safe(profile.deal_type),
        )
    data = profile.model_dump(mode="json")
    if layer == 2:
        return IdentifiedPreview(facts={key: val for key, val in data.items() if key not in RESTRICTED | {"financials"}}, financials=profile.financials)
    return RestrictedPreview(facts={key: data[key] for key in RESTRICTED})
