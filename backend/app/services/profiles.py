from backend.app.db.models import Company
from backend.app.schemas.company import (
    AnonymousPreview, CompanyInput, CompanyResponse, CompanySummary, IdentifiedPreview, RestrictedPreview,
)

RESTRICTED = {"shareholders", "decision_maker", "permitted_use"}
FINANCIAL_METRICS = ("revenue", "ebitda")
# Layer-1 revenue bands per reporting currency; amounts never mix currencies.
REVENUE_BANDS = {
    "VND": ([20e9, 50e9, 100e9, 200e9, 500e9],
            ["Dưới 20 tỷ VND", "20–dưới 50 tỷ VND", "50–dưới 100 tỷ VND", "100–dưới 200 tỷ VND", "200–dưới 500 tỷ VND", "Từ 500 tỷ VND"]),
    "JPY": ([100e6, 300e6, 1e9, 3e9, 10e9],
            ["Dưới 100 triệu JPY", "100–dưới 300 triệu JPY", "300 triệu–dưới 1 tỷ JPY", "1–dưới 3 tỷ JPY", "3–dưới 10 tỷ JPY", "Từ 10 tỷ JPY"]),
}
EMPLOYEE_BANDS = ([50, 200, 1000], ["Dưới 50", "50–199", "200–999", "Từ 1.000"])


def band(value, boundaries, labels):
    if value is None:
        return None
    return next((labels[i] for i, limit in enumerate(boundaries) if value < limit), labels[-1])


def revenue_band(value, currency):
    return band(float(value) if value is not None else None, *REVENUE_BANDS[currency])


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
            rev_fact = latest.get("revenue") or {}
            revenue = rev_fact.get("value")
            if revenue is not None:
                try:
                    revenue = float(revenue)
                except (ValueError, TypeError):
                    revenue = None

    currency = profile.get("currency") or "VND"
    rev_band = revenue_band(revenue, currency)
    emp_band = band(employees, *EMPLOYEE_BANDS)

    verified_count = 0
    total_count = 0
    for k, v in profile.items():
        if isinstance(v, dict) and "verification" in v:
            total_count += 1
            if v.get("verification") in ("DOCUMENT_VERIFIED", "THIRD_PARTY_CONFIRMED") and v.get("value") is not None:
                verified_count += 1
        elif k == "financials" and isinstance(v, list):
            for fin in v:
                for f_k in FINANCIAL_METRICS:
                    sub_f = fin.get(f_k)
                    if isinstance(sub_f, dict) and "verification" in sub_f:
                        total_count += 1
                        if sub_f.get("verification") in ("DOCUMENT_VERIFIED", "THIRD_PARTY_CONFIRMED") and sub_f.get("value") is not None:
                            verified_count += 1

    return CompanySummary(
        id=company.id,
        alias=company.alias,
        owner_username=company.owner_username,
        name=company.name,
        tax_id=company.tax_id,
        updated_at=company.updated_at,
        sector=sector,
        country=(profile.get("country") or {}).get("value"),
        region=region,
        currency=currency,
        revenue_band=rev_band,
        employee_band=emp_band,
        deal_type=deal_type,
        stake_percent=stake,
        verified_facts_count=verified_count,
        total_facts_count=total_count,
    )


def response(company: Company) -> CompanyResponse:
    return CompanyResponse(
        id=company.id, alias=company.alias, owner_username=company.owner_username, revision=company.revision,
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


def verified_fact_changed(old, new) -> bool:
    """True when a verified label is added or edited; only reviewers may do that."""
    if isinstance(new, dict):
        if "verification" in new:
            return new["verification"] != "SELF_DECLARED" and old != new
        old = old if isinstance(old, dict) else {}
        return any(verified_fact_changed(old.get(key, {}), value) for key, value in new.items())
    if isinstance(new, list):
        old_years = {row["year"]: row for row in old} if isinstance(old, list) else {}
        return any(verified_fact_changed(old_years.get(row["year"], {}), row) for row in new)
    return False


def find_fact(profile: dict, path: str) -> dict | None:
    """A fact by review path: a top-level key, or financials.<year>.revenue|ebitda."""
    parts = path.split(".")
    if len(parts) == 1:
        fact = profile.get(path)
        return fact if isinstance(fact, dict) and "verification" in fact else None
    if len(parts) == 3 and parts[0] == "financials" and parts[1].isdigit() and parts[2] in FINANCIAL_METRICS:
        row = next((item for item in profile.get("financials") or [] if item.get("year") == int(parts[1])), None)
        return row.get(parts[2]) if row else None
    return None


def preview(company: Company, layer: int):
    profile = CompanyInput.model_validate(company.profile)
    if layer == 1:
        def safe(fact):
            return fact.value if fact.issue == "NONE" else None

        revenue = None
        if profile.financials:
            revenue = safe(max(profile.financials, key=lambda row: row.year).revenue)
        return AnonymousPreview(
            alias=company.alias, sector=safe(profile.sector), country=safe(profile.country), region=safe(profile.region),
            revenue_band=revenue_band(revenue, profile.currency),
            employee_band=band(safe(profile.employees), *EMPLOYEE_BANDS),
            deal_type=safe(profile.deal_type),
        )
    data = profile.model_dump(mode="json")
    if layer == 2:
        hidden = RESTRICTED | {"financials", "currency"}
        return IdentifiedPreview(facts={key: val for key, val in data.items() if key not in hidden}, currency=profile.currency, financials=profile.financials)
    return RestrictedPreview(facts={key: data[key] for key in RESTRICTED})
