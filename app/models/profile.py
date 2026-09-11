from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class VerificationStatus(str, Enum):
    SELF_REPORTED = "VER_01_SELF_REPORTED"
    DOCUMENT_VERIFIED = "VER_02_DOCUMENT_VERIFIED"
    AUDITED = "VER_03_AUDITED"

class DealType(str, Enum):
    SECONDARY_SALE = "SECONDARY"      # Thoái vốn (tiền về cổ đông)
    PRIMARY_CAPITAL = "PRIMARY"       # Phát hành mới (tiền vào công ty)
    MIXED = "MIXED"

class VerifiedField(BaseModel):
    value: Any
    status: VerificationStatus = VerificationStatus.SELF_REPORTED
    evidence_source: Optional[str] = None
    verified_at: Optional[str] = None

class RawSellerInput(BaseModel):
    company_name: str = Field(...)
    tax_id: str = Field(...)
    founding_year: int = Field(...)
    province: str = Field(...)
    industry_category: str = Field(...)
    annual_revenue_vnd: float = Field(..., description="Doanh thu hằng năm (VNĐ)")
    ebitda_margin_pct: float = Field(..., description="Biên EBITDA (%)")
    net_debt_vnd: float = Field(default=0)
    employee_count: int = Field(...)
    key_clients_description: str = Field(...)
    tech_stack: List[str] = Field(...)
    deal_type: DealType = Field(default=DealType.SECONDARY_SALE)
    target_stake_pct: float = Field(..., description="Tỷ lệ cổ phần chào bán (%)")
    expected_valuation_vnd: Optional[float] = Field(default=250_000_000_000)
    is_audited: bool = Field(default=True)
    auditor_name: Optional[str] = Field(default="A&C Auditing Company")

# Lớp 1: Blind Teaser (Ẩn danh hóa)
class BlindTeaser(BaseModel):
    project_code: str
    headline_vi: str
    headline_ja: str
    industry_category: str
    macro_region: str
    revenue_bracket: str
    ebitda_bracket: str
    employee_bracket: str
    tech_stack: List[str]
    deal_type: str
    target_stake_bracket: str
    verification_summary: Dict[str, str]

# Lớp 2: Confidential Information Memorandum (CIM)
class ConfidentialMemo(BaseModel):
    project_code: str
    company_name: str
    tax_id: str
    established_year: int
    headquarters: str
    financial_summary_3yr: Dict[str, Any]
    detailed_tech_stack: List[str]
    org_structure: Dict[str, Any]
    client_clusters: List[str]
    valuation_guide: Dict[str, Any]
    verification_badges: Dict[str, VerificationStatus]

# Lớp 3: Trust Profile tổng hợp
class TrustProfileResponse(BaseModel):
    deal_id: str
    layer_1_teaser: BlindTeaser
    layer_2_cim: ConfidentialMemo
    available_layer_3_folders: List[str]
