from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TechDDAxis(str, Enum):
    ARCHITECTURE_SCALABILITY = "1_ARCHITECTURE_&_SCALABILITY"
    CODE_QUALITY_DEBT = "2_CODE_QUALITY_&_TECHNICAL_DEBT"
    IP_OSS_COMPLIANCE = "3_IP_&_OPEN_SOURCE_COMPLIANCE"
    CYBERSECURITY_PRIVACY = "4_CYBERSECURITY_&_DATA_PRIVACY"
    KEY_PERSON_DEPENDENCY = "5_KEY_PERSON_DEPENDENCY"
    POST_DEAL_INTEGRATION = "6_POST_DEAL_INTEGRATION"

class FindingSeverity(str, Enum):
    P0_CRITICAL = "P0_CRITICAL"   # Rủi ro làm đổ vỡ deal / Chặn pháp lý
    P1_HIGH = "P1_HIGH"           # Rủi ro cao cần sửa trước khi closing
    P2_MEDIUM = "P2_MEDIUM"       # Rủi ro kỹ thuật trung bình đưa vào kế hoạch 100 ngày
    P3_LOW = "P3_LOW"             # Khuyến nghị cải tiến

class CostClassification(str, Enum):
    CAPEX_ONE_TIME = "CAPEX"      # Đầu tư sửa chữa 1 lần (Trừ lùi giá mua)
    OPEX_ANNUAL = "OPEX"          # Chi phí vận hành phát sinh hằng năm
    ACCEPTABLE_DEBT = "TOLERABLE" # Nợ kỹ thuật có thể sống chung

class TechDDFinding(BaseModel):
    finding_id: str
    axis: TechDDAxis
    title: str
    description: str
    severity: FindingSeverity
    cost_type: CostClassification
    estimated_man_months: float
    estimated_cost_vnd: float
    recommended_deal_action: str  # Ví dụ: "Trừ lùi trực tiếp vào Giá mua" hoặc "Condition Precedent"

class ScanToolResult(BaseModel):
    tool_name: str                # "SonarQube", "Snyk", "OWASP ZAP"
    scan_timestamp: str
    summary_metrics: Dict[str, Any] = Field(default_factory=dict)
    high_vulnerabilities_count: int = 0
    copyleft_licenses_detected: List[str] = Field(default_factory=list)

class RemediationCostSummary(BaseModel):
    deal_id: str
    total_findings_count: int
    critical_p0_count: int
    high_p1_count: int
    total_capex_deduction_vnd: float
    total_opex_impact_vnd: float
    suggested_valuation_adjustment_vnd: float
    findings: List[TechDDFinding]
