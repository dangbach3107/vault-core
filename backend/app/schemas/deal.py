from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import Field, model_validator

from backend.app.schemas.company import StrictModel


DealAction = Literal[
    "buyerRequest", "sellerProfile", "prepPackageFeeRecorded", "sellerL1Approval",
    "matchPrepared", "identityRequested", "ndaRecorded", "sellerL2Approval",
    "indicativeLoiSubmitted", "legalL3Approval", "crossBorderApproval",
    "noEscrowConfirmed", "sellerFileApproval", "vdrOpened", "techDdSigned",
    "loiSubmitted", "legalClosingChecklist", "spaSigned", "dealClosed",
    "successFeeRecorded", "postDealHandoff",
]
PositiveMoney = Annotated[Decimal, Field(gt=0, max_digits=18, decimal_places=2)]


class DealCreate(StrictModel):
    title: str = Field(default="Japanese buyer × Vietnamese warehouse software seller", min_length=1, max_length=200)
    seller_company_id: UUID | None = None
    buyer_username: str | None = Field(default=None, min_length=1, max_length=80)


class BuyerRequestForm(StrictModel):
    capability: str = Field(min_length=3, max_length=500)
    goal: str = Field(default="", max_length=1000)
    budget_min_vnd: PositiveMoney | None = None
    budget_max_vnd: PositiveMoney | None = None
    timeline: str = Field(default="", max_length=200)

    @model_validator(mode="after")
    def budget_range(self):
        if self.budget_min_vnd and self.budget_max_vnd and self.budget_max_vnd < self.budget_min_vnd:
            raise ValueError("Ngân sách tối đa phải lớn hơn hoặc bằng tối thiểu.")
        return self


class NdaForm(StrictModel):
    reference: str = Field(min_length=1, max_length=60)
    parties: list[Annotated[str, Field(min_length=1, max_length=200)]] = Field(min_length=2, max_length=10)
    signed_on: date
    expires_on: date
    document_id: UUID | None = None

    @model_validator(mode="after")
    def dates(self):
        if self.signed_on > date.today():
            raise ValueError("Ngày ký NDA không được ở tương lai.")
        if self.expires_on <= self.signed_on:
            raise ValueError("Ngày hết hạn NDA phải sau ngày ký.")
        return self


ValuationBasis = Literal["EV", "EQUITY"]


class OfferForm(StrictModel):
    """LOI sơ bộ (không ràng buộc) hoặc đề nghị chính thức."""
    reference: str = Field(min_length=1, max_length=60)
    price_low_vnd: PositiveMoney
    price_high_vnd: PositiveMoney | None = None
    valuation_basis: ValuationBasis
    exclusivity_days: int = Field(default=0, ge=0, le=365)
    valid_until: date
    conditions: str = Field(default="", max_length=2000)

    @model_validator(mode="after")
    def price_and_validity(self):
        if self.price_high_vnd is not None and self.price_high_vnd < self.price_low_vnd:
            raise ValueError("Giá cao phải lớn hơn hoặc bằng giá thấp.")
        if self.valid_until < date.today():
            raise ValueError("Hạn hiệu lực không được ở quá khứ.")
        return self


class HandoffForm(StrictModel):
    recipient: str = Field(min_length=1, max_length=200)
    handed_on: date
    items: list[Annotated[str, Field(min_length=1, max_length=200)]] = Field(min_length=1, max_length=30)

    @model_validator(mode="after")
    def not_future(self):
        if self.handed_on > date.today():
            raise ValueError("Ngày bàn giao không được ở tương lai.")
        return self


class DealActionInput(StrictModel):
    note: str = Field(default="", max_length=1000)
    document_ids: list[UUID] = Field(default_factory=list, max_length=100)
    # Business steps carry a typed form instead of a free note (see FORM_ACTIONS in api/deals.py).
    buyer_request: BuyerRequestForm | None = None
    nda: NdaForm | None = None
    offer: OfferForm | None = None
    handoff: HandoffForm | None = None


AccessLevel = Literal["L0", "L1", "L2", "L3", "CLOSING"]


class AccessRequestInput(StrictModel):
    requested_level: AccessLevel
    purpose: str = Field(min_length=3, max_length=500)
    document_ids: list[UUID] = Field(default_factory=list, max_length=100)


class AccessDecisionInput(StrictModel):
    approved: bool
    expires_at: datetime | None = None
    reason: str = Field(min_length=3, max_length=500)
    can_download: bool = False
    basis_ref: str = Field(default="", max_length=200)
    # The approver picks the files; None keeps the files named in the request.
    document_ids: list[UUID] | None = Field(default=None, max_length=100)


class RevokeAccessInput(StrictModel):
    reason: str = Field(min_length=3, max_length=500)


class WorkflowStepInput(StrictModel):
    note: str = Field(min_length=1, max_length=1000)
    opened_data: list[str] = Field(default_factory=list, max_length=50)
    outcome: Literal["CONTINUE", "STOP"] = "CONTINUE"


FindingSeverity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
FindingStatus = Literal["OPEN", "RESPONDED", "RESOLVED", "ACCEPTED_RISK"]


class FindingInput(StrictModel):
    title: str = Field(min_length=3, max_length=200)
    severity: FindingSeverity
    description: str = Field(default="", max_length=2000)
    remediation: str = Field(default="", max_length=1000)
    impact_vnd: PositiveMoney | None = None


class FindingUpdate(StrictModel):
    status: FindingStatus
    note: str = Field(min_length=3, max_length=1000)


FeeType = Literal["PREP_PACKAGE", "TECH_DD", "SUCCESS_FEE"]


class FeeInput(StrictModel):
    type: FeeType
    amount_vnd: PositiveMoney
    due_on: date
    note: str = Field(default="", max_length=500)


class InvoiceInput(StrictModel):
    invoice_number: str = Field(min_length=1, max_length=60)
    issued_on: date


class PaymentInput(StrictModel):
    amount_vnd: PositiveMoney
    paid_on: date
    reference: str = Field(min_length=1, max_length=120)


class CatalogAction(StrictModel):
    key: DealAction
    label: str
    role: str
    requires: list[str]


class CatalogStage(StrictModel):
    number: int
    label: str
    owner: str


class DealCatalog(StrictModel):
    actions: list[CatalogAction]
    stages: list[CatalogStage]
    buyers: list[str]


class DealResponse(StrictModel):
    id: UUID
    title: str
    state: dict[str, Any]
    revision: int
    created_at: datetime
    updated_at: datetime


class DealDocument(StrictModel):
    grant_id: UUID
    document_id: UUID
    title: str
    filename: str
    media_type: str
    version_number: int
    latest_version: int
    can_download: bool
    expires_at: datetime


class ClosingEvidence(StrictModel):
    action: str
    action_label: str
    document_id: UUID
    title: str
    filename: str
    media_type: str
    version_number: int
