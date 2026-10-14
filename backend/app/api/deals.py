from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.api.companies import ApiError
from backend.app.api.dependencies import database_session
from backend.app.db.models import Company, Deal, utcnow
from backend.app.schemas.deal import AccessDecisionInput, AccessRequestInput, DealAction, DealActionInput, DealCreate, DealResponse, RevokeAccessInput, WorkflowStepInput
from backend.app.core.auth import current_user
from backend.app.schemas.auth import UserResponse

router = APIRouter(prefix="/deals", tags=["Synthetic deal workspace"], responses={404: {"model": ApiError}, 409: {"model": ApiError}, 503: {"model": ApiError}})
DB = Annotated[Session, Depends(database_session)]

ACTIONS = [
    "buyerRequest", "sellerProfile", "prepPackageFeeRecorded", "sellerL1Approval",
    "matchPrepared", "identityRequested", "ndaRecorded", "sellerL2Approval",
    "indicativeLoiSubmitted", "legalL3Approval", "crossBorderApproval",
    "noEscrowConfirmed", "sellerFileApproval", "vdrOpened", "techDdSigned",
    "loiSubmitted", "legalClosingChecklist", "dealClosed", "successFeeRecorded",
    "postDealHandoff",
]
REQUIRES = {
    "prepPackageFeeRecorded": ["sellerProfile"], "sellerL1Approval": ["sellerProfile"],
    "matchPrepared": ["buyerRequest", "sellerL1Approval"], "identityRequested": ["matchPrepared"],
    "ndaRecorded": ["identityRequested"], "sellerL2Approval": ["identityRequested", "ndaRecorded"],
    "indicativeLoiSubmitted": ["sellerL2Approval"],
    "legalL3Approval": ["sellerL2Approval", "indicativeLoiSubmitted"],
    "crossBorderApproval": ["sellerL2Approval", "indicativeLoiSubmitted"],
    "sellerFileApproval": ["sellerL2Approval", "indicativeLoiSubmitted"],
    "vdrOpened": ["legalL3Approval", "crossBorderApproval", "noEscrowConfirmed", "sellerFileApproval", "indicativeLoiSubmitted"],
    "techDdSigned": ["vdrOpened"], "loiSubmitted": ["techDdSigned"],
    "legalClosingChecklist": ["loiSubmitted"], "dealClosed": ["loiSubmitted", "legalClosingChecklist"],
    "successFeeRecorded": ["dealClosed"], "postDealHandoff": ["dealClosed"],
}
ACTION_ROLES = {
    "buyerRequest": "BUYER", "identityRequested": "BUYER", "indicativeLoiSubmitted": "BUYER", "loiSubmitted": "BUYER",
    "sellerProfile": "SELLER", "sellerL1Approval": "SELLER", "sellerL2Approval": "SELLER", "sellerFileApproval": "SELLER",
    "matchPrepared": "VAULT_ADMIN", "ndaRecorded": "VAULT_ADMIN", "vdrOpened": "VAULT_ADMIN", "dealClosed": "VAULT_ADMIN", "postDealHandoff": "VAULT_ADMIN",
    "legalL3Approval": "LEGAL", "crossBorderApproval": "LEGAL", "noEscrowConfirmed": "LEGAL", "legalClosingChecklist": "LEGAL",
    "techDdSigned": "TECH_DD", "prepPackageFeeRecorded": "FINANCE", "successFeeRecorded": "FINANCE",
}
WORKFLOW_STAGES = [
    (1, "Nhận lead / cơ hội giao dịch", "VAULT_ADMIN"),
    (2, "Xác minh bên tham gia", "LEGAL"),
    (3, "Xác định mục tiêu giao dịch", "VAULT_ADMIN"),
    (4, "Legal & eligibility screening", "LEGAL"),
    (5, "Ký mandate / xác nhận phạm vi", "VAULT_ADMIN"),
    (6, "Thu thập hồ sơ ban đầu của seller", "SELLER"),
    (7, "Đánh giá mức độ sẵn sàng", "VAULT_ADMIN"),
    (8, "Chuẩn hóa hồ sơ seller", "SELLER"),
    (9, "Tạo Teaser ẩn danh", "SELLER"),
    (10, "Xây Buyer Thesis", "BUYER"),
    (11, "Tìm và shortlist buyer phù hợp", "VAULT_ADMIN"),
    (12, "Seller duyệt buyer được tiếp cận", "SELLER"),
    (13, "Buyer gửi yêu cầu tiếp cận", "BUYER"),
    (14, "Ký NDA", "LEGAL"),
    (15, "Mở Data Room theo quyền", "VAULT_ADMIN"),
    (16, "Management Meeting / Q&A", "VAULT_ADMIN"),
    (17, "Due Diligence / Tech DD", "TECH_DD"),
    (18, "Xử lý findings & đàm phán", "VAULT_ADMIN"),
    (19, "LOI → hợp đồng → Signing/Closing", "LEGAL"),
    (20, "Post-deal Integration / đóng hồ sơ", "VAULT_ADMIN"),
]


def initial_state(seller_company_id=None):
    return {
        "steps": {key: False for key in ACTIONS},
        "buyer_request": None, "seller_profile": {"company_id": str(seller_company_id) if seller_company_id else None},
        "approvals": [], "indicative_loi": None, "vdr_opening": None,
        "tech_dd": {"findings": [], "signed_off_at": None}, "definitive_offer": None,
        "legal_closing_checklist": None, "fees": [], "closing": None, "handoff": None,
        "access_requests": [], "access_grants": [], "access_events": [],
        "workflow": {
            "status": "ACTIVE", "current_step": 1, "stop_reason": None,
            "opened_data": [], "unmet_conditions": ["Hoàn tất bước 1"],
            "history": [],
        },
    }


def response(row):
    return DealResponse(
        id=row.id, title=row.title, state=row.state, revision=row.revision,
        created_at=row.created_at, updated_at=row.updated_at,
    )


def find_deal(session, deal_id, lock=False):
    query = select(Deal).where(Deal.id == deal_id)
    row = session.scalar(query.with_for_update() if lock else query)
    if row is None:
        raise HTTPException(404, "Không tìm thấy thương vụ.")
    return row


@router.get("", response_model=list[DealResponse], operation_id="list_deals")
def list_deals(session: DB, user: UserResponse = Depends(current_user)):
    return [response(row) for row in session.scalars(select(Deal).order_by(Deal.updated_at.desc()))]


@router.post("", response_model=DealResponse, status_code=201, operation_id="create_deal")
def create_deal(body: DealCreate, session: DB, user: UserResponse = Depends(current_user)):
    if user.role != "VAULT_ADMIN":
        raise HTTPException(403, "Chỉ VAULT Admin được tạo lead/deal mới.")
    if body.seller_company_id and session.get(Company, body.seller_company_id) is None:
        raise HTTPException(404, "Không tìm thấy seller profile để liên kết.")
    row = Deal(title=body.title, state=initial_state(body.seller_company_id))
    session.add(row); session.commit()
    return response(row)


@router.get("/{deal_id}", response_model=DealResponse, operation_id="get_deal")
def get_deal(deal_id: UUID, session: DB, user: UserResponse = Depends(current_user)):
    return response(find_deal(session, deal_id))


def event(action, note=""):
    return {"action": action, "at": datetime.now(timezone.utc).isoformat(), "note": note}


def access_collections(state):
    state["access_requests"] = list(state.get("access_requests", []))
    state["access_grants"] = list(state.get("access_grants", []))
    state["access_events"] = list(state.get("access_events", []))


@router.post("/{deal_id}/access-requests", response_model=DealResponse, operation_id="request_deal_access")
def request_deal_access(deal_id: UUID, body: AccessRequestInput, session: DB, user: UserResponse = Depends(current_user)):
    if user.role != "BUYER": raise HTTPException(403, "Chỉ Buyer được gửi yêu cầu truy cập.")
    if body.requested_level == "L0": raise HTTPException(409, "L0 là teaser; không cần tạo access request.")
    row = find_deal(session, deal_id, lock=True); state = dict(row.state); access_collections(state)
    now = datetime.now(timezone.utc).isoformat(); request_id = str(uuid4())
    state["access_requests"].append({"id": request_id, "requester": user.username, "requested_level": body.requested_level, "purpose": body.purpose, "document_ids": [str(value) for value in body.document_ids], "status": "PENDING", "requested_at": now, "decided_at": None, "decided_by": None, "reason": None})
    state["access_events"].append({"type": "ACCESS_REQUESTED", "actor": user.username, "at": now, "request_id": request_id, "level": body.requested_level})
    row.state = state; row.revision += 1; row.updated_at = utcnow(); session.commit(); return response(row)


@router.post("/{deal_id}/access-requests/{request_id}/decision", response_model=DealResponse, operation_id="decide_deal_access")
def decide_deal_access(deal_id: UUID, request_id: UUID, body: AccessDecisionInput, session: DB, user: UserResponse = Depends(current_user)):
    if user.role not in {"SELLER", "LEGAL"}: raise HTTPException(403, "Chỉ Seller hoặc Legal được duyệt quyền truy cập.")
    if body.approved and body.expires_at is None: raise HTTPException(422, "Quyền được duyệt phải có thời hạn hết hiệu lực.")
    if body.approved and body.expires_at <= datetime.now(timezone.utc): raise HTTPException(422, "Thời hạn truy cập phải nằm trong tương lai.")
    row = find_deal(session, deal_id, lock=True); state = dict(row.state); access_collections(state)
    item = next((value for value in state["access_requests"] if value["id"] == str(request_id)), None)
    if item is None: raise HTTPException(404, "Không tìm thấy yêu cầu truy cập.")
    if item["status"] != "PENDING": raise HTTPException(409, "Yêu cầu truy cập đã được xử lý.")
    now = datetime.now(timezone.utc).isoformat(); item.update({"status": "APPROVED" if body.approved else "REJECTED", "decided_at": now, "decided_by": user.username, "reason": body.reason})
    if body.approved:
        state["access_grants"].append({"id": str(uuid4()), "request_id": item["id"], "user": item["requester"], "deal_id": str(deal_id), "access_level": item["requested_level"], "document_ids": item["document_ids"], "purpose": item["purpose"], "approved_by": user.username, "granted_at": now, "expires_at": body.expires_at.isoformat(), "revoked_at": None, "revoke_reason": None})
    state["access_events"].append({"type": "ACCESS_APPROVED" if body.approved else "ACCESS_REJECTED", "actor": user.username, "at": now, "request_id": item["id"], "reason": body.reason})
    row.state = state; row.revision += 1; row.updated_at = utcnow(); session.commit(); return response(row)


@router.post("/{deal_id}/access-grants/{grant_id}/revoke", response_model=DealResponse, operation_id="revoke_deal_access")
def revoke_deal_access(deal_id: UUID, grant_id: UUID, body: RevokeAccessInput, session: DB, user: UserResponse = Depends(current_user)):
    if user.role not in {"SELLER", "LEGAL", "VAULT_ADMIN"}: raise HTTPException(403, "Vai trò hiện tại không được thu hồi quyền.")
    row = find_deal(session, deal_id, lock=True); state = dict(row.state); access_collections(state)
    grant = next((value for value in state["access_grants"] if value["id"] == str(grant_id)), None)
    if grant is None: raise HTTPException(404, "Không tìm thấy quyền truy cập.")
    if grant["revoked_at"]: raise HTTPException(409, "Quyền truy cập đã bị thu hồi.")
    now = datetime.now(timezone.utc).isoformat(); grant.update({"revoked_at": now, "revoke_reason": body.reason})
    state["access_events"].append({"type": "ACCESS_REVOKED", "actor": user.username, "at": now, "grant_id": grant["id"], "reason": body.reason})
    row.state = state; row.revision += 1; row.updated_at = utcnow(); session.commit(); return response(row)


def apply_sample(state, action, body):
    now = datetime.now(timezone.utc).isoformat()
    if action == "buyerRequest": state["buyer_request"] = {"capability": "Warehouse B2B software", "goal_24_months": "Localize and expand to Japanese factories", "budget": "70–150 tỷ VND EV", "timeline": "LOI 90 days; closing 9–12 months"}
    elif action == "sellerProfile": state["seller_profile"].update({"sample_case": "Vietnamese warehouse software seller", "linked": True})
    elif action in {"sellerL1Approval", "identityRequested", "ndaRecorded", "sellerL2Approval", "legalL3Approval", "crossBorderApproval", "noEscrowConfirmed", "sellerFileApproval"}: state["approvals"].append(event(action, body.note))
    elif action == "indicativeLoiSubmitted": state["indicative_loi"] = {"submitted_at": now, "non_binding": True, "exclusivity": "short-term requested"}
    elif action == "vdrOpened": state["vdr_opening"] = {"opened_at": now, "document_ids": [str(value) for value in body.document_ids]}
    elif action == "techDdSigned":
        state["tech_dd"] = {"findings": [{"title": "Architecture scalability", "severity": "MAJOR", "remediation": "6-month fix", "impact_vnd": 180000000}, {"title": "OSS license evidence", "severity": "HIGH", "remediation": "pre-closing must-fix", "impact_vnd": 90000000}], "signed_off_at": now}
        state["fees"].append({"type": "TECH_DD", "status": "RECORDED", "recorded_at": now})
    elif action == "loiSubmitted": state["definitive_offer"] = {"submitted_at": now, "status": "SUBMITTED"}
    elif action == "legalClosingChecklist": state["legal_closing_checklist"] = {"completed_at": now, "items_complete": True}
    elif action == "dealClosed": state["closing"] = {"closed_at": now, "status": "SPA_SIGNED"}
    elif action in {"prepPackageFeeRecorded", "successFeeRecorded"}: state["fees"].append({"type": "PREP_PACKAGE" if action.startswith("prep") else "SUCCESS_FEE", "status": "RECORDED", "recorded_at": now})
    elif action == "postDealHandoff":
        state["handoff"] = {"created_at": now, "recipient": "Rikkei", "status": "HANDED_OFF"}
        state["fees"].append({"type": "BUILD_TO_BUY", "status": "OPPORTUNITY", "recorded_at": now})


def workflow_view(state):
    workflow = state.setdefault("workflow", initial_state()["workflow"])
    current = min(int(workflow.get("current_step", 1)), 20)
    number, label, owner = WORKFLOW_STAGES[current - 1]
    return workflow, {"number": number, "label": label, "owner": owner}


@router.post("/{deal_id}/workflow/{step}/complete", response_model=DealResponse, operation_id="complete_workflow_step")
def complete_workflow_step(deal_id: UUID, step: int, body: WorkflowStepInput, session: DB, user: UserResponse = Depends(current_user)):
    if not 1 <= step <= 20: raise HTTPException(422, "Bước workflow phải từ 1 đến 20.")
    row = find_deal(session, deal_id, lock=True); state = dict(row.state); workflow, current = workflow_view(state)
    if workflow["status"] != "ACTIVE": raise HTTPException(409, "Deal đã dừng hoặc đóng.")
    if step != current["number"]: raise HTTPException(409, f"Bước hiện tại là {current['number']}.")
    if user.role != current["owner"]: raise HTTPException(403, f"Bước này thuộc vai trò {current['owner']}.")
    now = datetime.now(timezone.utc).isoformat()
    workflow = dict(workflow); workflow["history"] = list(workflow.get("history", []))
    workflow["history"].append({"step": step, "label": current["label"], "owner": user.role, "outcome": body.outcome, "note": body.note, "opened_data": body.opened_data, "completed_at": now})
    workflow["opened_data"] = sorted(set(workflow.get("opened_data", []) + body.opened_data))
    if body.outcome == "STOP":
        workflow.update({"status": "STOPPED", "stop_reason": body.note, "unmet_conditions": []})
    elif step == 20:
        workflow.update({"status": "CLOSED", "current_step": 20, "unmet_conditions": []})
    else:
        workflow.update({"current_step": step + 1, "unmet_conditions": [f"Hoàn tất bước {step + 1}: {WORKFLOW_STAGES[step][1]}"]})
    state["workflow"] = workflow; row.state = state; row.revision += 1; row.updated_at = utcnow(); session.commit()
    return response(row)


@router.post("/{deal_id}/actions/{action}", response_model=DealResponse, operation_id="complete_deal_action")
def complete_action(deal_id: UUID, action: DealAction, body: DealActionInput, session: DB, user: UserResponse = Depends(current_user)):
    if user.role != ACTION_ROLES[action]:
        raise HTTPException(403, f"Action này thuộc vai trò {ACTION_ROLES[action]}.")
    row = find_deal(session, deal_id, lock=True); state = dict(row.state); state["steps"] = dict(state["steps"])
    if state["steps"][action]: return response(row)
    missing = [key for key in REQUIRES.get(action, []) if not state["steps"].get(key)]
    if missing: raise HTTPException(409, f"Chưa đủ điều kiện: {', '.join(missing)}.")
    apply_sample(state, action, body); state["steps"][action] = True
    row.state = state; row.revision += 1; row.updated_at = utcnow(); session.commit()
    return response(row)


@router.post("/{deal_id}/reset", response_model=DealResponse, operation_id="reset_deal")
def reset_deal(deal_id: UUID, session: DB, user: UserResponse = Depends(current_user)):
    if user.role != "VAULT_ADMIN": raise HTTPException(403, "Chỉ VAULT Admin được reset thương vụ.")
    row = find_deal(session, deal_id, lock=True); seller_id = row.state.get("seller_profile", {}).get("company_id")
    row.state = initial_state(seller_id); row.revision += 1; row.updated_at = utcnow(); session.commit()
    return response(row)


@router.post("/{deal_id}/complete-sample", response_model=DealResponse, operation_id="complete_sample_deal")
def complete_sample(deal_id: UUID, session: DB, user: UserResponse = Depends(current_user)):
    if user.role != "VAULT_ADMIN": raise HTTPException(403, "Chỉ VAULT Admin được hoàn tất dữ liệu mẫu.")
    row = find_deal(session, deal_id, lock=True); state = initial_state(row.state.get("seller_profile", {}).get("company_id")); body = DealActionInput()
    for action in ACTIONS: apply_sample(state, action, body); state["steps"][action] = True
    state["workflow"] = {"status": "CLOSED", "current_step": 20, "stop_reason": None, "opened_data": ["L1 teaser", "L2 CIM", "L3 VDR", "Tech DD findings"], "unmet_conditions": [], "history": [{"step": number, "label": label, "owner": owner, "outcome": "CONTINUE", "note": "Hoàn tất dữ liệu mẫu", "opened_data": [], "completed_at": datetime.now(timezone.utc).isoformat()} for number, label, owner in WORKFLOW_STAGES]}
    row.state = state; row.revision += 1; row.updated_at = utcnow(); session.commit()
    return response(row)
