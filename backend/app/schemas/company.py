"""Internal draft profiles. Verification describes individual facts, never a company."""

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Verification(StrEnum):
    SELF_DECLARED = "SELF_DECLARED"
    DOCUMENT_VERIFIED = "DOCUMENT_VERIFIED"
    THIRD_PARTY_CONFIRMED = "THIRD_PARTY_CONFIRMED"


class Issue(StrEnum):
    NONE = "NONE"
    CONFLICTED = "CONFLICTED"
    EXPIRED = "EXPIRED"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


T = TypeVar("T")
Text = Annotated[str, Field(min_length=1, max_length=2000)]
Money = Annotated[Decimal, Field(ge=0, max_digits=18, decimal_places=2)]
SignedMoney = Annotated[Decimal, Field(max_digits=18, decimal_places=2)]


class Fact(StrictModel, Generic[T]):
    value: T | None = None
    verification: Verification = Verification.SELF_DECLARED
    issue: Issue = Issue.NONE
    source: str = Field(default="", max_length=500)
    source_date: date | None = None
    entered_by: str = Field(default="", max_length=120)
    reviewed_by: str = Field(default="", max_length=120)
    reviewed_on: date | None = None
    notes: str = Field(default="", max_length=1000)

    @model_validator(mode="after")
    def evidence_for_review(self):
        if self.verification != Verification.SELF_DECLARED:
            if self.value is None or not all((self.source, self.source_date, self.reviewed_by, self.reviewed_on)):
                raise ValueError("Nhãn đã xác minh cần giá trị, nguồn, ngày nguồn, người và ngày đối chiếu.")
            if self.issue != Issue.NONE:
                raise ValueError("Dữ kiện mâu thuẫn hoặc hết hạn phải trở về nhãn tự khai.")
        if any(day and day > date.today() for day in (self.source_date, self.reviewed_on)):
            raise ValueError("Ngày nguồn/đối chiếu không được ở tương lai.")
        return self


class Sector(StrEnum):
    SOFTWARE = "SOFTWARE"
    MANUFACTURING = "MANUFACTURING"
    SERVICES = "SERVICES"
    OTHER = "OTHER"


class Region(StrEnum):
    NORTH = "NORTH"
    CENTRAL = "CENTRAL"
    SOUTH = "SOUTH"


class DealType(StrEnum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    MIXED = "MIXED"


class FinancialYear(StrictModel):
    year: int = Field(ge=1900, le=2100)
    revenue_vnd: Fact[Money] = Field(default_factory=Fact)
    ebitda_vnd: Fact[SignedMoney] = Field(default_factory=Fact)


class CompanyInput(StrictModel):
    company_name: Fact[Annotated[str, Field(min_length=1, max_length=200)]]
    source_url: Fact[Annotated[str, Field(min_length=8, max_length=2000, pattern=r"https?://\S+")]] = Field(default_factory=Fact)
    tax_id: Fact[Annotated[str, Field(min_length=3, max_length=30)]] = Field(default_factory=Fact)
    founded_year: Fact[Annotated[int, Field(ge=1800, le=2100)]] = Field(default_factory=Fact)
    sector: Fact[Sector] = Field(default_factory=Fact)
    region: Fact[Region] = Field(default_factory=Fact)
    address: Fact[Text] = Field(default_factory=Fact)
    description: Fact[Text] = Field(default_factory=Fact)
    customer_groups: Fact[Text] = Field(default_factory=Fact)
    employees: Fact[Annotated[int, Field(ge=0, le=10000000)]] = Field(default_factory=Fact)
    technology: Fact[Text] = Field(default_factory=Fact)
    shareholders: Fact[Text] = Field(default_factory=Fact)
    decision_maker: Fact[Text] = Field(default_factory=Fact)
    deal_type: Fact[DealType] = Field(default_factory=Fact)
    stake_percent: Fact[Annotated[Decimal, Field(ge=0, le=100, decimal_places=2)]] = Field(default_factory=Fact)
    funds_destination: Fact[Text] = Field(default_factory=Fact)
    objectives: Fact[Text] = Field(default_factory=Fact)
    permitted_use: Fact[Text] = Field(default_factory=Fact)
    financials: list[FinancialYear] = Field(default_factory=list, max_length=3)

    @model_validator(mode="after")
    def valid_draft(self):
        if self.company_name.value is None:
            raise ValueError("Tên doanh nghiệp là bắt buộc để lưu bản nháp.")
        years = [row.year for row in self.financials]
        if len(years) != len(set(years)):
            raise ValueError("Không được nhập trùng năm tài chính.")
        if any(year > date.today().year for year in years):
            raise ValueError("Năm tài chính không được ở tương lai.")
        if self.founded_year.value and self.founded_year.value > date.today().year:
            raise ValueError("Năm thành lập không được ở tương lai.")
        return self


class CompanyUpdate(StrictModel):
    expected_revision: int = Field(ge=1)
    profile: CompanyInput


class CompanyResponse(StrictModel):
    id: UUID
    alias: str
    revision: int
    created_at: datetime
    updated_at: datetime
    profile: CompanyInput


class CompanySummary(StrictModel):
    id: UUID
    alias: str
    name: str
    tax_id: str | None
    updated_at: datetime


class AnonymousPreview(StrictModel):
    layer: int = 1
    alias: str
    sector: Sector | None
    region: Region | None
    revenue_band_vnd: str | None
    employee_band: str | None
    deal_type: DealType | None
    notice: str = "Bản xem trước nội bộ; cần người duyệt nguy cơ nhận diện trước khi chia sẻ."


class IdentifiedPreview(StrictModel):
    layer: int = 2
    facts: dict[str, Fact[Text | Decimal | int]]
    financials: list[FinancialYear]
    notice: str = "Bản xem trước nội bộ; không phải quyền chia sẻ cho buyer."


class RestrictedPreview(StrictModel):
    layer: int = 3
    facts: dict[str, Fact[Text]]
    notice: str = "Nội dung hạn chế và phòng dữ liệu; chưa triển khai NDA/phê duyệt hay quyền buyer."
