from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class NDAStatus(str, Enum):
    PENDING_SIGNATURE = "PENDING_SIGNATURE"
    SIGNED = "SIGNED"
    REJECTED = "REJECTED"

class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class NDASubmission(BaseModel):
    deal_id: str
    buyer_company_name: str
    signer_name: str
    signer_title: str
    signer_email: str
    buyer_country: str = "Japan"
    nda_contract_version: str = "VAULT_NDA_VI_JA_2026_V1"

class DualApprovalState(BaseModel):
    approval_id: str
    deal_id: str
    buyer_company_name: str
    buyer_email: str
    nda_signed_at: datetime
    nda_document_hash: str
    
    # Bốn con mắt (Two-person rule)
    seller_approval_status: ApprovalStatus = ApprovalStatus.PENDING
    seller_approved_by: Optional[str] = None
    seller_approved_at: Optional[datetime] = None
    
    compliance_approval_status: ApprovalStatus = ApprovalStatus.PENDING
    compliance_approved_by: Optional[str] = None
    compliance_approved_at: Optional[datetime] = None
    
    # Kết quả mở khóa
    is_access_granted: bool = False
    access_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None

class ApprovalDecisionRequest(BaseModel):
    approval_id: str
    decision: ApprovalStatus  # APPROVED or REJECTED
    approver_role: str        # "SELLER_FOUNDER" or "VAULT_COMPLIANCE"
    approver_name: str
    rejection_reason: Optional[str] = None
