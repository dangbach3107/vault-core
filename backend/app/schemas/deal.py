from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import Field

from backend.app.schemas.company import StrictModel


DealAction = Literal[
    "buyerRequest", "sellerProfile", "prepPackageFeeRecorded", "sellerL1Approval",
    "matchPrepared", "identityRequested", "ndaRecorded", "sellerL2Approval",
    "indicativeLoiSubmitted", "legalL3Approval", "crossBorderApproval",
    "noEscrowConfirmed", "sellerFileApproval", "vdrOpened", "techDdSigned",
    "loiSubmitted", "legalClosingChecklist", "dealClosed", "successFeeRecorded",
    "postDealHandoff",
]


class DealCreate(StrictModel):
    title: str = Field(default="Japanese buyer × Vietnamese warehouse software seller", min_length=1, max_length=200)
    seller_company_id: UUID | None = None


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


class RevokeAccessInput(StrictModel):
    reason: str = Field(min_length=3, max_length=500)


class WorkflowStepInput(StrictModel):
    note: str = Field(min_length=1, max_length=1000)
    opened_data: list[str] = Field(default_factory=list, max_length=50)
    outcome: Literal["CONTINUE", "STOP"] = "CONTINUE"


class DealResponse(StrictModel):
    id: UUID
    title: str
    state: dict[str, Any]
    revision: int
    created_at: datetime
    updated_at: datetime
