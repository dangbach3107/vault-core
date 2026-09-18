from backend.app.db.models import Company
from backend.app.schemas.company import (
    AnonymousPreview, CompanyInput, CompanyResponse, CompanySummary, IdentifiedPreview, RestrictedPreview,
)

RESTRICTED = {"shareholders", "decision_maker", "permitted_use"}


def extract_summary(company: Company) -> CompanySummary:
    profile = company.profile or {}
    sector = (profile.get("sector") or {}).get("value")
    region = (profile.get("region") or {}).get("value")
    deal_type = (profile.get("deal_type") or {}).get("value")
    stake = (profile.get("stake_percent") or {}).get("value")
    employees = (profile.get("employees") or {}).get("value")

    revenue = None
    financials = profile.get("financials") or []
    if financials:
        latest = max(financials, key=lambda row: row.get("year", 0), default=None)
        if latest:
            rev_fact = latest.get("revenue_vnd") or {}
            revenue = rev_fact.get("value")
            if revenue is not None:
                try:
                    revenue = float(revenue)
                except (ValueError, TypeError):
                    revenue = None

    def band(value, boundaries, labels):
        if value is None:
            return None
        return next((labels[i] for i, limit in enumerate(boundaries) if value < limit), labels[-1])

    rev_band = band(
        revenue,
        [20e9, 50e9, 100e9, 200e9, 500e9],
        ["Dưới 20 tỷ", "20–dưới 50 tỷ", "50–dưới 100 tỷ", "100–dưới 200 tỷ", "200–dưới 500 tỷ", "Từ 500 tỷ"],
    )
    emp_band = band(employees, [50, 200, 1000], ["Dưới 50", "50–199", "200–999", "Từ 1.000"])

    verified_count = 0
    total_count = 0
    for k, v in profile.items():
        if isinstance(v, dict) and "verification" in v:
            total_count += 1
            if v.get("verification") in ("DOCUMENT_VERIFIED", "THIRD_PARTY_CONFIRMED") and v.get("value") is not None:
                verified_count += 1
        elif k == "financials" and isinstance(v, list):
            for fin in v:
                for f_k in ("revenue_vnd", "ebitda_vnd"):
                    sub_f = fin.get(f_k)
                    if isinstance(sub_f, dict) and "verification" in sub_f:
                        total_count += 1
                        if sub_f.get("verification") in ("DOCUMENT_VERIFIED", "THIRD_PARTY_CONFIRMED") and sub_f.get("value") is not None:
                            verified_count += 1

    return CompanySummary(
        id=company.id,
        alias=company.alias,
        name=company.name,
        tax_id=company.tax_id,
        updated_at=company.updated_at,
        sector=sector,
        region=region,
        revenue_band=rev_band,
        employee_band=emp_band,
        deal_type=deal_type,
        stake_percent=stake,
        verified_facts_count=verified_count,
        total_facts_count=total_count,
    )


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
