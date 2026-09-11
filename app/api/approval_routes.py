from typing import List
from fastapi import APIRouter, HTTPException
from app.models.approval import (
    NDASubmission,
    DualApprovalState,
    ApprovalDecisionRequest
)
from app.services.approval_gate import approval_gate_service

router = APIRouter(prefix="/approval", tags=["Module 3: NDA & Two-Person Approval Gate"])

@router.post("/nda/submit", response_model=DualApprovalState)
def submit_signed_nda(sub: NDASubmission):
    """
    Tiếp nhận sự kiện Bên mua ký số NDA thành công.
    Khởi tạo phiên phê duyệt kép (Two-Person Approval Gate).
    """
    return approval_gate_service.submit_nda(sub)

@router.post("/decision", response_model=DualApprovalState)
def make_approval_decision(req: ApprovalDecisionRequest):
    """
    Xử lý quyết định phê duyệt từ Founder Bên bán (SELLER_FOUNDER)
    hoặc Cán bộ Pháp chế VAULT (VAULT_COMPLIANCE).
    Chỉ khi cả 2 cùng APPROVED thì Token mở VDR mới được cấp.
    """
    try:
        return approval_gate_service.process_decision(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/deal/{deal_id}", response_model=List[DualApprovalState])
def get_deal_approvals(deal_id: str):
    """Lấy danh sách các yêu cầu tiếp cận thông tin của deal."""
    return approval_gate_service.list_approvals_for_deal(deal_id)
