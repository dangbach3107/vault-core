from datetime import date, datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import Field, model_validator

from backend.app.schemas.company import StrictModel


class ReviewRequestInput(StrictModel):
    # A top-level fact key (e.g. "employees") or "financials.<year>.revenue_vnd|ebitda_vnd".
    field: str = Field(min_length=1, max_length=80)
    source: str = Field(min_length=1, max_length=500)
    source_date: date
    document_id: UUID | None = None
    note: str = Field(default="", max_length=1000)

    @model_validator(mode="after")
    def not_future(self):
        if self.source_date > date.today():
            raise ValueError("Ngày nguồn không được ở tương lai.")
        return self


class ReviewDecisionInput(StrictModel):
    approved: bool
    verification: Literal["DOCUMENT_VERIFIED", "THIRD_PARTY_CONFIRMED"] | None = None
    reason: str = Field(min_length=3, max_length=500)


class ReviewDocument(StrictModel):
    document_id: UUID
    room_id: UUID
    title: str
    version_number: int
    filename: str


class ReviewResponse(StrictModel):
    id: UUID
    company_id: UUID
    company_alias: str
    company_name: str
    field: str
    value: Any
    source: str
    source_date: date
    document: ReviewDocument | None
    note: str
    status: Literal["PENDING", "APPROVED", "REJECTED"]
    verification: str | None
    requested_by: str
    requested_at: datetime
    decided_by: str | None
    decided_at: datetime | None
    reason: str
