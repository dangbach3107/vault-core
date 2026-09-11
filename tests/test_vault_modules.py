import pytest
from app.models.profile import RawSellerInput, DealType
from app.services.profile_engine import profile_engine
from app.services.vdr_service import vdr_service
from app.services.approval_gate import approval_gate_service
from app.services.techdd_scanner import techdd_service
from app.models.vdr import WatermarkRequest
from app.models.approval import NDASubmission, ApprovalDecisionRequest, ApprovalStatus

def test_module_1_trust_profile_generation():
    raw_input = RawSellerInput(
        company_name="Công ty Phần mềm Kho vận Bình Dương",
        tax_id="0399887766",
        founding_year=2012,
        province="Bình Dương",
        industry_category="Warehouse Management System (WMS)",
        annual_revenue_vnd=72_000_000_000,
        ebitda_margin_pct=18.5,
        net_debt_vnd=2_000_000_000,
        employee_count=65,
        key_clients_description="Nhà máy điện tử",
        tech_stack=["Java", "React", "PostgreSQL"],
        deal_type=DealType.SECONDARY_SALE,
        target_stake_pct=30.0,
        expected_valuation_vnd=250_000_000_000,
        is_audited=True
    )
    result = profile_engine.process_raw_profile(raw_input)
    assert result.deal_id.startswith("deal_")
    assert "Bình Dương" not in result.layer_1_teaser.headline_vi
    assert "Đông Nam Bộ" in result.layer_1_teaser.macro_region
    assert "50 – 100 tỷ VNĐ" in result.layer_1_teaser.revenue_bracket
    assert result.layer_2_cim.company_name == "Công ty Phần mềm Kho vận Bình Dương"

def test_module_2_vdr_and_dynamic_watermark():
    deal_id = "deal_test_123"
    docs = vdr_service.get_documents_for_deal(deal_id)
    assert len(docs) == 6
    
    watermark_req = WatermarkRequest(
        deal_id=deal_id,
        doc_id=docs[0].doc_id,
        viewer_email="tanaka@sumitomo.jp",
        viewer_ip="118.69.182.44"
    )
    wm = vdr_service.generate_dynamic_watermark(watermark_req)
    assert "tanaka@sumitomo.jp" in wm.watermark_text
    assert "118.69.182.44" in wm.watermark_text

    logs = vdr_service.get_audit_trail(deal_id)
    assert len(logs) >= 1
    assert logs[-1].viewer_email == "tanaka@sumitomo.jp"

def test_module_3_two_person_approval_gate():
    sub = NDASubmission(
        deal_id="deal_test_456",
        buyer_company_name="Sumitomo Corp Japan",
        signer_name="Kenji Tanaka",
        signer_title="Investment Director",
        signer_email="tanaka@sumitomo.jp"
    )
    state = approval_gate_service.submit_nda(sub)
    assert state.is_access_granted is False
    assert state.seller_approval_status == ApprovalStatus.PENDING
    assert state.compliance_approval_status == ApprovalStatus.PENDING

    # Step 1: Seller Founder approves
    state = approval_gate_service.process_decision(ApprovalDecisionRequest(
        approval_id=state.approval_id,
        decision=ApprovalStatus.APPROVED,
        approver_role="SELLER_FOUNDER",
        approver_name="Nguyen Van Tan"
    ))
    assert state.is_access_granted is False

    # Step 2: Legal Compliance approves -> Access granted!
    state = approval_gate_service.process_decision(ApprovalDecisionRequest(
        approval_id=state.approval_id,
        decision=ApprovalStatus.APPROVED,
        approver_role="VAULT_COMPLIANCE",
        approver_name="Dang Minh Trang"
    ))
    assert state.is_access_granted is True
    assert state.access_token.startswith("vdr_auth_")

def test_module_4_techdd_evaluation_and_cost_remediation():
    deal_id = "deal_test_789"
    res = techdd_service.evaluate_tech_assets(deal_id)
    assert res.critical_p0_count >= 1
    assert res.high_p1_count >= 1
    assert res.total_capex_deduction_vnd > 0
    assert res.suggested_valuation_adjustment_vnd == res.total_capex_deduction_vnd
