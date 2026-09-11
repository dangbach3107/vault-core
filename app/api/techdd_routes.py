from typing import Dict, Any, Optional
from fastapi import APIRouter
from app.models.techdd import RemediationCostSummary
from app.services.techdd_scanner import techdd_service

router = APIRouter(prefix="/techdd", tags=["Module 4: Tech Due Diligence Engine"])

@router.post("/evaluate/{deal_id}", response_model=RemediationCostSummary)
def evaluate_deal_tech_assets(deal_id: str, scan_payload: Optional[Dict[str, Any]] = None):
    """
    Thực hiện Thẩm định Công nghệ 6 trục độc quyền của Rikkei.
    Phát hiện rủi ro P0/P1/P2 và tính toán Bảng chi phí khắc phục
    để quy đổi thành con số trừ lùi giá đàm phán M&A.
    """
    return techdd_service.evaluate_tech_assets(deal_id, scan_payload)
