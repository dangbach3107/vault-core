from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import Field

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


class DealActionInput(StrictModel):
    note: str = Field(default="", max_length=1000)
    document_ids: list[UUID] = Field(default_factory=list, max_length=100)


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
