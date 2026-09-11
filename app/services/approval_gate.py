import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from app.models.approval import (
    NDASubmission,
    DualApprovalState,
    ApprovalStatus,
    ApprovalDecisionRequest
)
from app.core.security import generate_secure_token, hash_document_content

class ApprovalGateService:
    """
    Module 3: Thỏa thuận bảo mật (NDA) & Cổng phê duyệt 2 bước (Two-Person Rule).
    Nguyên tắc: Quyền xem tài liệu nhạy cảm chỉ mở khi cả Founder Bên bán và Pháp chế VAULT cùng phê duyệt.
    """

    def __init__(self):
        # In-memory store cho MVP
        self._approvals: Dict[str, DualApprovalState] = {}

    def submit_nda(self, sub: NDASubmission) -> DualApprovalState:
        """Nhận sự kiện bên mua đã ký NDA điện tử và khởi tạo phiên phê duyệt kép."""
        approval_id = f"appr_{uuid.uuid4().hex[:8]}"
        
        # Tạo mã băm hợp đồng điện tử giả lập
        mock_nda_bytes = f"{sub.deal_id}_{sub.buyer_company_name}_{sub.signer_email}_{datetime.utcnow()}".encode()
        doc_hash = hash_document_content(mock_nda_bytes)

        state = DualApprovalState(
            approval_id=approval_id,
            deal_id=sub.deal_id,
            buyer_company_name=sub.buyer_company_name,
            buyer_email=sub.signer_email,
            nda_signed_at=datetime.utcnow(),
            nda_document_hash=doc_hash,
            seller_approval_status=ApprovalStatus.PENDING,
            compliance_approval_status=ApprovalStatus.PENDING,
            is_access_granted=False
        )
        self._approvals[approval_id] = state
        return state

    def process_decision(self, req: ApprovalDecisionRequest) -> DualApprovalState:
        """Xử lý quyết định phê duyệt từ Bên bán hoặc Cán bộ Pháp chế."""
        if req.approval_id not in self._approvals:
            raise ValueError(f"Approval ID {req.approval_id} không tồn tại.")
        
        state = self._approvals[req.approval_id]
        now = datetime.utcnow()

        if req.approver_role == "SELLER_FOUNDER":
            state.seller_approval_status = req.decision
            state.seller_approved_by = req.approver_name
            state.seller_approved_at = now
        elif req.approver_role == "VAULT_COMPLIANCE":
            state.compliance_approval_status = req.decision
            state.compliance_approved_by = req.approver_name
            state.compliance_approved_at = now
        else:
            raise ValueError(f"Vai trò phê duyệt không hợp lệ: {req.approver_role}")

        # Kiểm tra điều kiện mở quyền (Two-Person Rule: Cả 2 đều phải APPROVED)
        if (state.seller_approval_status == ApprovalStatus.APPROVED and 
            state.compliance_approval_status == ApprovalStatus.APPROVED):
            state.is_access_granted = True
            state.access_token = generate_secure_token(prefix="vdr_auth_")
            state.token_expires_at = now + timedelta(days=14)
        elif (state.seller_approval_status == ApprovalStatus.REJECTED or 
              state.compliance_approval_status == ApprovalStatus.REJECTED):
            state.is_access_granted = False
            state.access_token = None

        return state

    def get_approval_state(self, approval_id: str) -> Optional[DualApprovalState]:
        return self._approvals.get(approval_id)

    def list_approvals_for_deal(self, deal_id: str) -> List[DualApprovalState]:
        return [a for a in self._approvals.values() if a.deal_id == deal_id]

approval_gate_service = ApprovalGateService()
