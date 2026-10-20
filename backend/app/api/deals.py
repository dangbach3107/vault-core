import copy
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Annotated
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.api.companies import ApiError
from backend.app.api.dependencies import database_session
from backend.app.api.rooms import version_file
from backend.app.core.auth import USERS, current_user
from backend.app.db.models import Company, Deal, Document, DocumentVersion, Room, utcnow
from backend.app.schemas.auth import UserResponse
from backend.app.schemas.company import AnonymousPreview, IdentifiedPreview, RestrictedPreview
from backend.app.schemas.deal import (
    AccessDecisionInput, AccessRequestInput, CatalogAction, ClosingEvidence, CatalogStage, DealAction, DealActionInput,
    DealCatalog, DealCreate, DealDocument, DealResponse, FeeInput, FindingInput, FindingUpdate,
    InvoiceInput, PaymentInput, RevokeAccessInput, WorkflowStepInput,
)
from backend.app.services.profiles import preview

router = APIRouter(prefix="/deals", tags=["Synthetic deal workspace"], responses={404: {"model": ApiError}, 409: {"model": ApiError}, 503: {"model": ApiError}})
DB = Annotated[Session, Depends(database_session)]
User = Annotated[UserResponse, Depends(current_user)]

ACTION_LABELS = {
    "buyerRequest": "Buyer gửi nhu cầu mua",
    "sellerProfile": "Seller hoàn tất hồ sơ",
    "prepPackageFeeRecorded": "Finance xác nhận phí chuẩn bị hồ sơ",
    "sellerL1Approval": "Seller duyệt Teaser ẩn danh",
    "matchPrepared": "Admin ghép Buyer với Seller",
    "identityRequested": "Buyer đề nghị biết danh tính",
    "ndaRecorded": "Ghi nhận NDA đã ký",
    "sellerL2Approval": "Seller đồng ý mở Lớp 2",
    "indicativeLoiSubmitted": "Buyer gửi LOI sơ bộ (không ràng buộc)",
    "legalL3Approval": "Legal đồng ý mở Lớp 3",
    "crossBorderApproval": "Legal duyệt chuyển dữ liệu ra nước ngoài",
    "noEscrowConfirmed": "Legal xác nhận VAULT không giữ tiền",
    "sellerFileApproval": "Seller duyệt danh sách tài liệu",
    "vdrOpened": "Mở phòng dữ liệu theo quyền",
    "techDdSigned": "Tech DD ký xác nhận kết thúc thẩm định",
    "loiSubmitted": "Buyer gửi đề nghị chính thức",
    "legalClosingChecklist": "Legal hoàn tất điều kiện đóng",
    "spaSigned": "Ký hợp đồng (Signing)",
    "dealClosed": "Đóng giao dịch (Closing)",
    "successFeeRecorded": "Finance xác nhận phí thành công",
    "postDealHandoff": "Bàn giao sau giao dịch",
}
ACTIONS = list(ACTION_LABELS)
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
    "legalClosingChecklist": ["loiSubmitted"], "spaSigned": ["loiSubmitted"],
    "dealClosed": ["spaSigned", "legalClosingChecklist"],
    "successFeeRecorded": ["dealClosed"], "postDealHandoff": ["dealClosed"],
}
ACTION_ROLES = {
    "buyerRequest": "BUYER", "identityRequested": "BUYER", "indicativeLoiSubmitted": "BUYER", "loiSubmitted": "BUYER",
    "sellerProfile": "SELLER", "sellerL1Approval": "SELLER", "sellerL2Approval": "SELLER", "sellerFileApproval": "SELLER",
    "matchPrepared": "VAULT_ADMIN", "ndaRecorded": "VAULT_ADMIN", "vdrOpened": "VAULT_ADMIN", "dealClosed": "VAULT_ADMIN", "postDealHandoff": "VAULT_ADMIN",
    "legalL3Approval": "LEGAL", "crossBorderApproval": "LEGAL", "noEscrowConfirmed": "LEGAL", "legalClosingChecklist": "LEGAL", "spaSigned": "LEGAL",
    "techDdSigned": "TECH_DD", "prepPackageFeeRecorded": "FINANCE", "successFeeRecorded": "FINANCE",
}
# Business steps that need a typed form; the value is the DealActionInput field holding it.
FORM_ACTIONS = {
    "buyerRequest": ("buyer_request", "Cần điền form nhu cầu mua."),
    "ndaRecorded": ("nda", "Cần điền form NDA (số hiệu, các bên, ngày ký, ngày hết hạn)."),
    "indicativeLoiSubmitted": ("offer", "Cần điền form LOI sơ bộ."),
    "loiSubmitted": ("offer", "Cần điền form đề nghị chính thức."),
    "postDealHandoff": ("handoff", "Cần điền form bàn giao."),
}
FORM_FIELDS = {"buyer_request", "nda", "offer", "handoff"}
# Steps without a form whose record is the evidence itself, so an empty note is not enough.
NOTE_REQUIRED = {
    "spaSigned": "Ghi số/ngày hợp đồng đã ký.",
    "dealClosed": "Ghi bằng chứng hoàn tất điều kiện đóng.",
}
WORKFLOW_STAGES = [
    (1, "Nhận lead / cơ hội giao dịch", "VAULT_ADMIN"),
    (2, "Xác minh bên tham gia", "LEGAL"),
    (3, "Xác định mục tiêu giao dịch", "VAULT_ADMIN"),
    (4, "Sàng lọc pháp lý & điều kiện tham gia", "LEGAL"),
    (5, "Ký mandate / xác nhận phạm vi", "VAULT_ADMIN"),
    (6, "Thu thập hồ sơ ban đầu của seller", "SELLER"),
    (7, "Đánh giá mức độ sẵn sàng", "VAULT_ADMIN"),
    (8, "Chuẩn hóa hồ sơ seller", "SELLER"),
    (9, "Tạo Teaser ẩn danh", "SELLER"),
    (10, "Xây nhu cầu mua của buyer", "BUYER"),
    (11, "Tìm và chọn buyer phù hợp", "VAULT_ADMIN"),
    (12, "Seller duyệt buyer được tiếp cận", "SELLER"),
    (13, "Buyer gửi yêu cầu tiếp cận", "BUYER"),
    (14, "Ký NDA", "LEGAL"),
    (15, "Mở phòng dữ liệu theo quyền", "VAULT_ADMIN"),
    (16, "Gặp ban điều hành / hỏi đáp", "VAULT_ADMIN"),
    (17, "Thẩm định / Tech DD", "TECH_DD"),
    (18, "Xử lý phát hiện & đàm phán", "VAULT_ADMIN"),
    (19, "LOI → hợp đồng → Ký → Đóng", "LEGAL"),
    (20, "Bàn giao sau giao dịch / đóng hồ sơ", "VAULT_ADMIN"),
]
LEVEL_ORDER = ["L0", "L1", "L2", "L3", "CLOSING"]
# Approval never follows automatically from the basis; the basis only makes approval possible.
# level -> (state key of the basis record, basis code, field holding its expiry, document name)
LEVEL_BASIS = {
    "L2": ("nda", "NDA", "expires_on", "NDA"),
    "L3": ("indicative_loi", "INDICATIVE_LOI", "valid_until", "LOI sơ bộ"),
    "CLOSING": ("definitive_offer", "LOI", "valid_until", "đề nghị chính thức"),
}
FULL_VIEW = {"VAULT_ADMIN", "LEGAL"}
# Files cited on these steps are the closing evidence Finance may read.
EVIDENCE_ACTIONS = ["legalClosingChecklist", "spaSigned", "dealClosed"]
EVIDENCE_ROLES = {"FINANCE", "LEGAL", "VAULT_ADMIN"}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def initial_state(seller_company_id=None, buyer_username=None):
    return {
        "steps": {key: False for key in ACTIONS},
        "records": {},
        "buyer_username": buyer_username,
        "is_sample": False,
        "buyer_request": None, "seller_profile": {"company_id": str(seller_company_id) if seller_company_id else None},
        "approvals": [], "indicative_loi": None, "vdr_opening": None,
        "tech_dd": {"findings": [], "signed_off_at": None, "signed_off_by": None}, "definitive_offer": None,
        "legal_closing_checklist": None, "fees": [], "signing": None, "closing": None, "handoff": None, "nda": None,
        "opportunities": [],
        "access_requests": [], "access_grants": [], "access_events": [],
        "workflow": {
            "status": "ACTIVE", "current_step": 1, "stop_reason": None,
            "opened_data": [], "unmet_conditions": ["Hoàn tất bước 1"],
            "history": [],
        },
    }


def normalize(state):
    """Fill keys added after a deal was created, so old rows keep working."""
    base = initial_state()
    state = copy.deepcopy(state)
    for key, value in base.items():
        state.setdefault(key, value)
    state["steps"] = {key: bool(state["steps"].get(key)) for key in ACTIONS}
    state["tech_dd"] = {**base["tech_dd"], **(state.get("tech_dd") or {})}
    # Rows written before fee lines/finding ids existed: placeholders are dropped, findings get stable ids.
    state["fees"] = [fee for fee in state["fees"] if "amount_vnd" in fee]
    state["tech_dd"]["findings"] = [
        {"status": "OPEN", "history": [], **finding, "id": finding.get("id") or str(uuid5(NAMESPACE_URL, finding.get("title", "")))}
        for finding in state["tech_dd"]["findings"]
    ]
    return state


def seller_company_id(state):
    return (state.get("seller_profile") or {}).get("company_id")


def is_seller_owner(session, state, user):
    company_id = seller_company_id(state)
    if user.role != "SELLER" or not company_id:
        return False
    company = session.get(Company, UUID(company_id))
    return company is not None and company.owner_username == user.username


def can_view(session, state, user):
    if user.role == "BUYER":
        return state.get("buyer_username") == user.username
    if user.role == "SELLER":
        return is_seller_owner(session, state, user)
    return True


def grant_status(grant, at=None):
    if grant.get("revoked_at"):
        return "REVOKED"
    if datetime.fromisoformat(grant["expires_at"]) <= (at or datetime.now(timezone.utc)):
        return "EXPIRED"
    return "ACTIVE"


def fee_view(fee, today=None):
    amount = Decimal(fee["amount_vnd"])
    paid = sum((Decimal(row["amount_vnd"]) for row in fee.get("payments", [])), Decimal(0))
    if paid >= amount:
        status = "PAID"
    elif not fee.get("invoice"):
        status = "DRAFT"
    elif date.fromisoformat(fee["due_on"]) < (today or date.today()):
        status = "OVERDUE"
    elif paid > 0:
        status = "PARTIALLY_PAID"
    else:
        status = "INVOICED"
    return {**fee, "paid_vnd": str(paid), "balance_vnd": str(max(amount - paid, Decimal(0))), "status": status}


def latest_versions(session, grants):
    ids = {UUID(item["document_id"]) for grant in grants for item in grant.get("documents", [])}
    if not ids:
        return {}
    return {str(row.id): row.current_version for row in session.scalars(select(Document).where(Document.id.in_(ids)))}


def grant_view(grant, latest):
    documents = [{**item, "latest_version": latest.get(item["document_id"], item["version_number"])} for item in grant.get("documents", [])]
    return {**grant, "documents": documents, "status": grant_status(grant)}


def project(session, row, user):
    """Minimal state per role: each role only receives what its work needs."""
    state = normalize(row.state)
    workflow = state["workflow"]
    summary = {key: workflow.get(key) for key in ("status", "current_step", "stop_reason", "unmet_conditions")}
    base = {
        "steps": state["steps"], "buyer_username": state["buyer_username"], "is_sample": state["is_sample"],
        "workflow": summary, "signing": state["signing"],
        "closing": {"status": state["closing"].get("status"), "closed_at": state["closing"].get("closed_at")} if state["closing"] else None,
    }
    role = user.role
    if role in FULL_VIEW or role == "SELLER":
        view = dict(state)
        if role == "SELLER":  # fees and Build-to-Buy are VAULT business, not the seller's
            view.pop("fees"); view.pop("opportunities")
    elif role == "BUYER":
        mine = lambda item, key: item.get(key) == user.username  # noqa: E731
        requests = [item for item in state["access_requests"] if mine(item, "requester")]
        grants = [item for item in state["access_grants"] if mine(item, "user")]
        own_ids = {item["id"] for item in requests} | {item["id"] for item in grants}
        view = {
            **base, "buyer_request": state["buyer_request"], "nda": state["nda"], "indicative_loi": state["indicative_loi"],
            "definitive_offer": state["definitive_offer"], "access_requests": requests, "access_grants": grants,
            "access_events": [item for item in state["access_events"] if item.get("request_id") in own_ids or item.get("grant_id") in own_ids],
        }
    elif role == "TECH_DD":
        view = {**base, "seller_profile": state["seller_profile"], "vdr_opening": state["vdr_opening"], "tech_dd": state["tech_dd"]}
    else:  # FINANCE
        view = {**base, "fees": state["fees"]}
    if "access_grants" in view:
        latest = latest_versions(session, view["access_grants"])
        view["access_grants"] = [grant_view(item, latest) for item in view["access_grants"]]
    if "fees" in view:
        view["fees"] = [fee_view(item) for item in view["fees"]]
    return view


def response(session, row, user):
    return DealResponse(
        id=row.id, title=row.title, state=project(session, row, user), revision=row.revision,
        created_at=row.created_at, updated_at=row.updated_at,
    )


def find_deal(session, deal_id, user, lock=False):
    query = select(Deal).where(Deal.id == deal_id)
    row = session.scalar(query.with_for_update() if lock else query)
    if row is None or not can_view(session, row.state, user):
        raise HTTPException(404, "Không tìm thấy thương vụ.")
    return row


def save(session, row, state, user):
    row.state = state; row.revision += 1; row.updated_at = utcnow(); session.commit()
    return response(session, row, user)


def record(user, note="", **extra):
    return {"by": user.username, "at": now_iso(), "note": note, **extra}


@router.get("/catalog", response_model=DealCatalog, operation_id="get_deal_catalog")
def get_catalog(user: User):
    return DealCatalog(
        actions=[CatalogAction(key=key, label=label, role=ACTION_ROLES[key], requires=REQUIRES.get(key, [])) for key, label in ACTION_LABELS.items()],
        stages=[CatalogStage(number=number, label=label, owner=owner) for number, label, owner in WORKFLOW_STAGES],
        buyers=sorted(name for name, (role, _) in USERS.items() if role == "BUYER") if user.role == "VAULT_ADMIN" else [],
    )


@router.get("", response_model=list[DealResponse], operation_id="list_deals")
def list_deals(session: DB, user: User):
    rows = session.scalars(select(Deal).order_by(Deal.updated_at.desc()))
    return [response(session, row, user) for row in rows if can_view(session, row.state, user)]


@router.post("", response_model=DealResponse, status_code=201, operation_id="create_deal")
def create_deal(body: DealCreate, session: DB, user: User):
    if user.role != "VAULT_ADMIN":
        raise HTTPException(403, "Chỉ VAULT Admin được tạo lead/deal mới.")
    if body.seller_company_id and session.get(Company, body.seller_company_id) is None:
        raise HTTPException(404, "Không tìm thấy seller profile để liên kết.")
    buyer = body.buyer_username.lower() if body.buyer_username else None
    if buyer and USERS.get(buyer, (None,))[0] != "BUYER":
        raise HTTPException(422, "Buyer phụ trách phải là một tài khoản Buyer.")
    row = Deal(title=body.title, state=initial_state(body.seller_company_id, buyer))
    session.add(row); session.commit()
    return response(session, row, user)


@router.get("/{deal_id}", response_model=DealResponse, operation_id="get_deal")
def get_deal(deal_id: UUID, session: DB, user: User):
    return response(session, find_deal(session, deal_id, user), user)


def check_party(session, state, user, owner_role):
    """Role alone is not enough: Buyer/Seller must be the party of this deal."""
    if user.role != owner_role:
        raise HTTPException(403, f"Bước này thuộc vai trò {owner_role}.")
    if owner_role == "BUYER" and state.get("buyer_username") != user.username:
        raise HTTPException(403, "Deal này giao cho Buyer khác.")
    if owner_role == "SELLER" and not is_seller_owner(session, state, user):
        raise HTTPException(403, "Chỉ Seller sở hữu hồ sơ của deal được thực hiện bước này.")


# --- Access requests: per person, level, file version, basis and expiry -------------------------

def seller_documents(session, state, document_ids):
    company_id = seller_company_id(state)
    if not document_ids:
        return []
    if not company_id:
        raise HTTPException(409, "Deal chưa liên kết hồ sơ seller nên chưa có tài liệu để cấp quyền.")
    rows = session.execute(
        select(Document, Room).join(Room, Room.id == Document.room_id)
        .where(Document.id.in_(document_ids), Room.company_id == UUID(company_id))
    ).all()
    if len(rows) != len(set(document_ids)):
        raise HTTPException(422, "Có tài liệu không thuộc phòng dữ liệu của seller trong deal này.")
    return [document for document, _ in rows]


def version_snapshot(session, documents):
    snapshot = []
    for document in documents:
        version = session.scalar(select(DocumentVersion).where(DocumentVersion.document_id == document.id, DocumentVersion.number == document.current_version))
        snapshot.append({"document_id": str(document.id), "title": document.title, "version_id": str(version.id), "version_number": version.number, "filename": version.filename, "media_type": version.media_type})
    return snapshot


@router.post("/{deal_id}/access-requests", response_model=DealResponse, operation_id="request_deal_access")
def request_deal_access(deal_id: UUID, body: AccessRequestInput, session: DB, user: User):
    if user.role != "BUYER": raise HTTPException(403, "Chỉ Buyer được gửi yêu cầu truy cập.")
    if body.requested_level == "L0": raise HTTPException(409, "L0 là teaser; không cần tạo access request.")
    row = find_deal(session, deal_id, user, lock=True); state = normalize(row.state)
    seller_documents(session, state, body.document_ids)
    now = now_iso(); request_id = str(uuid4())
    state["access_requests"].append({"id": request_id, "requester": user.username, "requested_level": body.requested_level, "purpose": body.purpose, "document_ids": [str(value) for value in body.document_ids], "status": "PENDING", "requested_at": now, "decided_at": None, "decided_by": None, "reason": None})
    state["access_events"].append({"type": "ACCESS_REQUESTED", "actor": user.username, "at": now, "request_id": request_id, "level": body.requested_level})
    return save(session, row, state, user)


def access_basis(state, level, expires_at):
    """The record that allows this level, checked for validity; the grant may not outlive it."""
    if level == "L1":
        if not state["steps"]["sellerL1Approval"]: raise HTTPException(409, "Seller chưa duyệt Teaser.")
        return "SELLER_L1_APPROVAL", ""
    key, basis, expiry_field, name = LEVEL_BASIS[level]
    record_ = state.get(key) or {}
    if not record_.get(expiry_field):  # missing, or recorded before forms existed
        raise HTTPException(409, f"Chưa có {name} được ghi nhận theo form; không thể mở {level}.")
    valid_until = date.fromisoformat(record_[expiry_field])
    if valid_until < date.today(): raise HTTPException(409, f"{name} đã hết hạn ngày {valid_until:%d/%m/%Y}; không thể cấp quyền mới.")
    if expires_at.date() > valid_until:
        raise HTTPException(422, f"Quyền không được kéo dài quá hạn {name} ({valid_until:%d/%m/%Y}).")
    return basis, record_.get("reference", "")


@router.post("/{deal_id}/access-requests/{request_id}/decision", response_model=DealResponse, operation_id="decide_deal_access")
def decide_deal_access(deal_id: UUID, request_id: UUID, body: AccessDecisionInput, session: DB, user: User):
    if user.role not in {"SELLER", "LEGAL"}: raise HTTPException(403, "Chỉ Seller hoặc Legal được duyệt quyền truy cập.")
    if body.approved and body.expires_at is None: raise HTTPException(422, "Quyền được duyệt phải có thời hạn hết hiệu lực.")
    if body.approved and body.expires_at <= datetime.now(timezone.utc): raise HTTPException(422, "Thời hạn truy cập phải nằm trong tương lai.")
    row = find_deal(session, deal_id, user, lock=True); state = normalize(row.state)
    item = next((value for value in state["access_requests"] if value["id"] == str(request_id)), None)
    if item is None: raise HTTPException(404, "Không tìm thấy yêu cầu truy cập.")
    if item["status"] != "PENDING": raise HTTPException(409, "Yêu cầu truy cập đã được xử lý.")
    now = now_iso()
    if body.approved:
        basis, basis_ref = access_basis(state, item["requested_level"], body.expires_at)
        chosen = body.document_ids if body.document_ids is not None else [UUID(value) for value in item["document_ids"]]
        documents = seller_documents(session, state, chosen)
        snapshot = version_snapshot(session, documents)  # the version the approver saw, not later uploads
        state["access_grants"].append({"id": str(uuid4()), "request_id": item["id"], "user": item["requester"], "deal_id": str(deal_id), "access_level": item["requested_level"], "documents": snapshot, "document_ids": [str(value) for value in chosen], "purpose": item["purpose"], "basis": basis, "basis_ref": basis_ref or body.basis_ref, "can_download": body.can_download, "approved_by": user.username, "approver_role": user.role, "granted_at": now, "expires_at": body.expires_at.isoformat(), "revoked_at": None, "revoke_reason": None})
    item.update({"status": "APPROVED" if body.approved else "REJECTED", "decided_at": now, "decided_by": user.username, "reason": body.reason})
    state["access_events"].append({"type": "ACCESS_APPROVED" if body.approved else "ACCESS_REJECTED", "actor": user.username, "at": now, "request_id": item["id"], "reason": body.reason})
    return save(session, row, state, user)


@router.post("/{deal_id}/access-grants/{grant_id}/revoke", response_model=DealResponse, operation_id="revoke_deal_access")
def revoke_deal_access(deal_id: UUID, grant_id: UUID, body: RevokeAccessInput, session: DB, user: User):
    if user.role not in {"SELLER", "LEGAL", "VAULT_ADMIN"}: raise HTTPException(403, "Vai trò hiện tại không được thu hồi quyền.")
    row = find_deal(session, deal_id, user, lock=True); state = normalize(row.state)
    grant = next((value for value in state["access_grants"] if value["id"] == str(grant_id)), None)
    if grant is None: raise HTTPException(404, "Không tìm thấy quyền truy cập.")
    if grant["revoked_at"]: raise HTTPException(409, "Quyền truy cập đã bị thu hồi.")
    now = now_iso(); grant.update({"revoked_at": now, "revoke_reason": body.reason})
    state["access_events"].append({"type": "ACCESS_REVOKED", "actor": user.username, "at": now, "grant_id": grant["id"], "reason": body.reason})
    return save(session, row, state, user)


def active_grants(state, user):
    return [grant for grant in state["access_grants"] if grant["user"] == user.username and grant_status(grant) == "ACTIVE"]


def deal_company(session, state):
    company_id = seller_company_id(state)
    company = session.get(Company, UUID(company_id)) if company_id else None
    if company is None:
        raise HTTPException(409, "Deal chưa liên kết hồ sơ seller.")
    return company


@router.get("/{deal_id}/teaser", response_model=AnonymousPreview, operation_id="get_deal_teaser")
def get_deal_teaser(deal_id: UUID, session: DB, user: User):
    """Layer 1 for the deal's buyer, only after the seller approved the teaser."""
    state = normalize(find_deal(session, deal_id, user).state)
    if user.role not in FULL_VIEW | {"BUYER", "SELLER"}: raise HTTPException(403, "Vai trò hiện tại không xem Teaser.")
    if user.role == "BUYER" and not state["steps"]["sellerL1Approval"]: raise HTTPException(409, "Seller chưa duyệt Teaser cho deal này.")
    return preview(deal_company(session, state), 1)


@router.get("/{deal_id}/profile/{layer}", response_model=IdentifiedPreview | RestrictedPreview, operation_id="get_deal_profile")
def get_deal_profile(deal_id: UUID, layer: Annotated[int, Path(ge=2, le=3)], session: DB, user: User):
    state = normalize(find_deal(session, deal_id, user).state)
    if user.role not in FULL_VIEW | {"BUYER", "SELLER"}: raise HTTPException(403, "Vai trò hiện tại không xem hồ sơ theo lớp.")
    if user.role == "BUYER":
        needed = "L2" if layer == 2 else "L3"
        if not any(LEVEL_ORDER.index(grant["access_level"]) >= LEVEL_ORDER.index(needed) for grant in active_grants(state, user)):
            raise HTTPException(403, f"Chưa có quyền {needed} còn hiệu lực cho deal này.")
    return preview(deal_company(session, state), layer)


@router.get("/{deal_id}/documents", response_model=list[DealDocument], operation_id="list_deal_documents")
def list_deal_documents(deal_id: UUID, session: DB, user: User):
    """Files the current buyer may open: exactly the version that was approved."""
    if user.role != "BUYER": raise HTTPException(403, "Danh sách này dành cho Buyer; vai trò nội bộ dùng Phòng dữ liệu.")
    state = normalize(find_deal(session, deal_id, user).state)
    grants = active_grants(state, user); latest = latest_versions(session, grants)
    return [DealDocument(
        grant_id=grant["id"], document_id=item["document_id"], title=item["title"], filename=item["filename"],
        media_type=item["media_type"], version_number=item["version_number"],
        latest_version=latest.get(item["document_id"], item["version_number"]),
        can_download=grant.get("can_download", False), expires_at=grant["expires_at"],
    ) for grant in grants for item in grant.get("documents", [])]


@router.get("/{deal_id}/documents/{grant_id}/{document_id}/content", response_class=FileResponse, operation_id="get_deal_document_content")
def get_deal_document_content(deal_id: UUID, grant_id: UUID, document_id: UUID, request: Request, session: DB, user: User, download: bool = False):
    if user.role != "BUYER": raise HTTPException(403, "Chỉ Buyer mở tài liệu qua quyền của deal.")
    row = find_deal(session, deal_id, user, lock=True); state = normalize(row.state)
    grant = next((value for value in active_grants(state, user) if value["id"] == str(grant_id)), None)
    if grant is None: raise HTTPException(403, "Quyền truy cập không tồn tại, đã hết hạn hoặc đã bị thu hồi.")
    item = next((value for value in grant.get("documents", []) if value["document_id"] == str(document_id)), None)
    if item is None: raise HTTPException(403, "Tài liệu này không nằm trong quyền đã duyệt.")
    if download and not grant.get("can_download"): raise HTTPException(403, "Quyền này chỉ cho xem, không cho tải xuống.")
    version = session.get(DocumentVersion, UUID(item["version_id"]))
    if version is None: raise HTTPException(404, "Phiên bản được duyệt không còn tồn tại.")
    if not download and version.media_type not in {"application/pdf", "image/png", "image/jpeg", "text/plain"} and not grant.get("can_download"):
        raise HTTPException(403, "File Office không xem trực tiếp được và quyền này không cho tải xuống.")
    file = version_file(request, session, version, inline=not download)
    state["access_events"].append({"type": "FILE_DOWNLOADED" if download else "FILE_VIEWED", "actor": user.username, "at": now_iso(), "grant_id": grant["id"], "document_id": item["document_id"], "version_number": item["version_number"]})
    row.state = state; session.commit()
    return file


# --- Tech DD: findings are handled separately from the sign-off ---------------------------------

def find_finding(state, finding_id):
    finding = next((value for value in state["tech_dd"]["findings"] if value["id"] == str(finding_id)), None)
    if finding is None: raise HTTPException(404, "Không tìm thấy finding.")
    return finding


@router.post("/{deal_id}/tech-dd/findings", response_model=DealResponse, status_code=201, operation_id="add_tech_dd_finding")
def add_finding(deal_id: UUID, body: FindingInput, session: DB, user: User):
    if user.role != "TECH_DD": raise HTTPException(403, "Chỉ Tech DD ghi nhận finding.")
    row = find_deal(session, deal_id, user, lock=True); state = normalize(row.state)
    if not state["steps"]["vdrOpened"]: raise HTTPException(409, "Phòng dữ liệu chưa mở cho thẩm định.")
    if state["steps"]["techDdSigned"]: raise HTTPException(409, "Tech DD đã ký xác nhận; không thêm finding.")
    now = now_iso()
    state["tech_dd"]["findings"].append({
        "id": str(uuid4()), "title": body.title, "severity": body.severity, "description": body.description,
        "remediation": body.remediation, "impact_vnd": str(body.impact_vnd) if body.impact_vnd is not None else None,
        "status": "OPEN", "created_by": user.username, "created_at": now,
        "history": [{"status": "OPEN", "by": user.username, "role": user.role, "at": now, "note": "Ghi nhận finding"}],
    })
    return save(session, row, state, user)


@router.post("/{deal_id}/tech-dd/findings/{finding_id}/status", response_model=DealResponse, operation_id="update_tech_dd_finding")
def update_finding(deal_id: UUID, finding_id: UUID, body: FindingUpdate, session: DB, user: User):
    row = find_deal(session, deal_id, user, lock=True); state = normalize(row.state)
    finding = find_finding(state, finding_id)
    if state["steps"]["techDdSigned"]: raise HTTPException(409, "Tech DD đã ký xác nhận; finding đã khóa.")
    # Seller/Admin answer a finding; only Tech DD decides whether it is resolved or an accepted risk.
    if body.status == "RESPONDED":
        if user.role == "SELLER": check_party(session, state, user, "SELLER")
        elif user.role != "VAULT_ADMIN": raise HTTPException(403, "Seller hoặc Admin phản hồi finding.")
    elif user.role != "TECH_DD":
        raise HTTPException(403, "Chỉ Tech DD đóng, chấp nhận rủi ro hoặc mở lại finding.")
    finding["status"] = body.status
    finding["history"] = [*finding.get("history", []), {"status": body.status, "by": user.username, "role": user.role, "at": now_iso(), "note": body.note}]
    return save(session, row, state, user)


# --- Finance: fee line → invoice → payments ------------------------------------------------------

def find_fee(state, fee_id):
    fee = next((value for value in state["fees"] if value.get("id") == str(fee_id)), None)
    if fee is None: raise HTTPException(404, "Không tìm thấy khoản phí.")
    return fee


def finance_deal(session, deal_id, user):
    if user.role != "FINANCE": raise HTTPException(403, "Chỉ Finance quản lý phí, hóa đơn và thanh toán.")
    row = find_deal(session, deal_id, user, lock=True)
    return row, normalize(row.state)


@router.post("/{deal_id}/fees", response_model=DealResponse, status_code=201, operation_id="add_deal_fee")
def add_fee(deal_id: UUID, body: FeeInput, session: DB, user: User):
    row, state = finance_deal(session, deal_id, user)
    if body.type == "SUCCESS_FEE" and not state["steps"]["dealClosed"]: raise HTTPException(409, "Phí thành công chỉ lập sau khi deal đã đóng (Closing).")
    if body.type == "TECH_DD" and not state["steps"]["vdrOpened"]: raise HTTPException(409, "Phí Tech DD chỉ lập khi đã mở phòng dữ liệu.")
    state["fees"].append({"id": str(uuid4()), "type": body.type, "amount_vnd": str(body.amount_vnd), "due_on": body.due_on.isoformat(), "note": body.note, "invoice": None, "payments": [], "created_by": user.username, "created_at": now_iso()})
    return save(session, row, state, user)


@router.post("/{deal_id}/fees/{fee_id}/invoice", response_model=DealResponse, operation_id="issue_fee_invoice")
def issue_invoice(deal_id: UUID, fee_id: UUID, body: InvoiceInput, session: DB, user: User):
    row, state = finance_deal(session, deal_id, user)
    fee = find_fee(state, fee_id)
    if fee.get("invoice"): raise HTTPException(409, "Khoản phí đã có hóa đơn.")
    if body.issued_on > date.today(): raise HTTPException(422, "Ngày xuất hóa đơn không được ở tương lai.")
    fee["invoice"] = {"number": body.invoice_number, "issued_on": body.issued_on.isoformat(), "by": user.username}
    return save(session, row, state, user)


@router.post("/{deal_id}/fees/{fee_id}/payments", response_model=DealResponse, operation_id="record_fee_payment")
def record_payment(deal_id: UUID, fee_id: UUID, body: PaymentInput, session: DB, user: User):
    row, state = finance_deal(session, deal_id, user)
    fee = find_fee(state, fee_id)
    if not fee.get("invoice"): raise HTTPException(409, "Cần xuất hóa đơn trước khi ghi nhận thanh toán.")
    if body.paid_on > date.today(): raise HTTPException(422, "Ngày thanh toán không được ở tương lai.")
    if body.amount_vnd > Decimal(fee_view(fee)["balance_vnd"]): raise HTTPException(409, "Số tiền vượt quá số còn phải thu.")
    fee["payments"] = [*fee.get("payments", []), {"amount_vnd": str(body.amount_vnd), "paid_on": body.paid_on.isoformat(), "reference": body.reference, "by": user.username}]
    return save(session, row, state, user)


# --- 20-step workflow and gated actions ----------------------------------------------------------

def workflow_view(state):
    workflow = state["workflow"]
    current = min(int(workflow.get("current_step", 1)), 20)
    number, label, owner = WORKFLOW_STAGES[current - 1]
    return workflow, {"number": number, "label": label, "owner": owner}


@router.post("/{deal_id}/workflow/{step}/complete", response_model=DealResponse, operation_id="complete_workflow_step")
def complete_workflow_step(deal_id: UUID, step: int, body: WorkflowStepInput, session: DB, user: User):
    if not 1 <= step <= 20: raise HTTPException(422, "Bước workflow phải từ 1 đến 20.")
    row = find_deal(session, deal_id, user, lock=True); state = normalize(row.state); workflow, current = workflow_view(state)
    if workflow["status"] != "ACTIVE": raise HTTPException(409, "Deal đã dừng hoặc đóng.")
    if step != current["number"]: raise HTTPException(409, f"Bước hiện tại là {current['number']}.")
    check_party(session, state, user, current["owner"])
    now = now_iso()
    workflow = dict(workflow); workflow["history"] = list(workflow.get("history", []))
    workflow["history"].append({"step": step, "label": current["label"], "owner": user.role, "by": user.username, "outcome": body.outcome, "note": body.note, "opened_data": body.opened_data, "completed_at": now})
    workflow["opened_data"] = sorted(set(workflow.get("opened_data", []) + body.opened_data))
    if body.outcome == "STOP":
        workflow.update({"status": "STOPPED", "stop_reason": body.note, "unmet_conditions": []})
    elif step == 20:
        workflow.update({"status": "CLOSED", "current_step": 20, "unmet_conditions": []})
    else:
        workflow.update({"current_step": step + 1, "unmet_conditions": [f"Hoàn tất bước {step + 1}: {WORKFLOW_STAGES[step][1]}"]})
    state["workflow"] = workflow
    return save(session, row, state, user)


def action_blocker(state, action):
    """Business conditions beyond step order; None when the action may proceed."""
    if action == "sellerProfile" and not seller_company_id(state):
        return "Deal chưa liên kết hồ sơ seller."
    if action in {"buyerRequest", "identityRequested"} and not state["buyer_username"]:
        return "Deal chưa có Buyer phụ trách."
    if action == "prepPackageFeeRecorded" and not any(fee["type"] == "PREP_PACKAGE" for fee in state["fees"]):
        return "Chưa lập khoản phí chuẩn bị hồ sơ."
    if action == "successFeeRecorded" and not any(fee["type"] == "SUCCESS_FEE" for fee in state["fees"]):
        return "Chưa lập khoản phí thành công."
    if action == "techDdSigned":
        unresolved = [finding["title"] for finding in state["tech_dd"]["findings"] if finding["status"] in {"OPEN", "RESPONDED"}]
        if unresolved: return f"Còn finding chưa xử lý: {', '.join(unresolved)}."
    return None


def apply_action(state, action, body, user, documents, form):
    """Store who did what, the form/note they entered and the file versions they cite; never invent content."""
    entry = record(user, body.note, document_ids=[str(value) for value in body.document_ids], documents=documents)
    state["records"][action] = entry
    if action == "buyerRequest": state["buyer_request"] = {**form, "summary": form["capability"], **entry}
    elif action == "sellerProfile": state["seller_profile"].update({"confirmed_by": user.username, "confirmed_at": entry["at"]})
    elif action in {"sellerL1Approval", "identityRequested", "ndaRecorded", "sellerL2Approval", "legalL3Approval", "crossBorderApproval", "noEscrowConfirmed", "sellerFileApproval"}:
        state["approvals"].append({"action": action, **entry})
        if action == "ndaRecorded": state["nda"] = {**form, **entry}
    elif action == "indicativeLoiSubmitted": state["indicative_loi"] = {**form, **entry, "non_binding": True}
    elif action == "vdrOpened": state["vdr_opening"] = entry
    elif action == "techDdSigned": state["tech_dd"].update({"signed_off_at": entry["at"], "signed_off_by": user.username, "sign_off_note": body.note})
    elif action == "loiSubmitted": state["definitive_offer"] = {**form, **entry, "status": "SUBMITTED"}
    elif action == "legalClosingChecklist": state["legal_closing_checklist"] = entry
    elif action == "spaSigned": state["signing"] = {**entry, "status": "SIGNED"}
    elif action == "dealClosed": state["closing"] = {**entry, "status": "CLOSED", "closed_at": entry["at"]}
    elif action == "postDealHandoff": state["handoff"] = {**form, **entry, "status": "HANDED_OFF"}


@router.post("/{deal_id}/actions/{action}", response_model=DealResponse, operation_id="complete_deal_action")
def complete_action(deal_id: UUID, action: DealAction, body: DealActionInput, session: DB, user: User):
    row = find_deal(session, deal_id, user, lock=True); state = normalize(row.state)
    check_party(session, state, user, ACTION_ROLES[action])
    if state["steps"][action]: return response(session, row, user)
    missing = [ACTION_LABELS[key] for key in REQUIRES.get(action, []) if not state["steps"].get(key)]
    if missing: raise HTTPException(409, f"Chưa đủ điều kiện: {'; '.join(missing)}.")
    if action in NOTE_REQUIRED and len(body.note.strip()) < 3: raise HTTPException(422, NOTE_REQUIRED[action])
    field, form_message = FORM_ACTIONS.get(action, (None, ""))
    stray = [name for name in FORM_FIELDS - {field} if getattr(body, name) is not None]
    if stray: raise HTTPException(422, f"Form {', '.join(stray)} không thuộc bước này.")
    form = getattr(body, field).model_dump(mode="json") if field and getattr(body, field) is not None else None
    if field and form is None: raise HTTPException(422, form_message)
    blocker = action_blocker(state, action)
    if blocker: raise HTTPException(409, blocker)
    cited = list(body.document_ids)
    if field == "nda" and body.nda.document_id: cited.append(body.nda.document_id)
    documents = version_snapshot(session, seller_documents(session, state, cited))
    apply_action(state, action, body, user, documents, form); state["steps"][action] = True
    return save(session, row, state, user)


# --- Closing evidence: only the files cited when signing/closing, for Finance/Legal/Admin --------

def evidence_items(state):
    return [{**item, "action": action, "action_label": ACTION_LABELS[action]}
            for action in EVIDENCE_ACTIONS for item in (state["records"].get(action) or {}).get("documents", [])]


def evidence_deal(session, deal_id, user):
    if user.role not in EVIDENCE_ROLES: raise HTTPException(403, "Chứng từ closing dành cho Finance, Legal và Admin.")
    return find_deal(session, deal_id, user)


@router.get("/{deal_id}/closing-evidence", response_model=list[ClosingEvidence], operation_id="list_closing_evidence")
def list_closing_evidence(deal_id: UUID, session: DB, user: User):
    items = evidence_items(normalize(evidence_deal(session, deal_id, user).state))
    return [ClosingEvidence(**{key: item[key] for key in ClosingEvidence.model_fields}) for item in items]


@router.get("/{deal_id}/closing-evidence/{document_id}/content", response_class=FileResponse, operation_id="get_closing_evidence_content")
def get_closing_evidence_content(deal_id: UUID, document_id: UUID, request: Request, session: DB, user: User, download: bool = False):
    state = normalize(evidence_deal(session, deal_id, user).state)
    item = next((value for value in evidence_items(state) if value["document_id"] == str(document_id)), None)
    if item is None: raise HTTPException(404, "Tài liệu này không phải chứng từ closing của deal.")
    version = session.get(DocumentVersion, UUID(item["version_id"]))
    if version is None: raise HTTPException(404, "Phiên bản được dẫn chứng không còn tồn tại.")
    return version_file(request, session, version, inline=not download)


@router.post("/{deal_id}/reset", response_model=DealResponse, operation_id="reset_deal")
def reset_deal(deal_id: UUID, session: DB, user: User):
    if user.role != "VAULT_ADMIN": raise HTTPException(403, "Chỉ VAULT Admin được reset thương vụ.")
    row = find_deal(session, deal_id, user, lock=True); state = normalize(row.state)
    return save(session, row, initial_state(seller_company_id(state), state["buyer_username"]), user)


def sample_state(state):
    """Illustrative data for demos. Every value is marked as sample, never as evidence."""
    sample = initial_state(seller_company_id(state), state["buyer_username"])
    sample["is_sample"] = True
    today = date.today()
    at = lambda days: (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()  # noqa: E731
    for index, action in enumerate(ACTIONS):
        sample["steps"][action] = True
        sample["records"][action] = {"by": ACTION_ROLES[action].lower(), "at": at(60 - index * 2), "note": "Dữ liệu minh họa", "document_ids": []}
    note = lambda text: {"by": "sample", "at": at(30), "note": f"Dữ liệu minh họa · {text}", "document_ids": []}  # noqa: E731
    day = lambda offset: (today + timedelta(days=offset)).isoformat()  # noqa: E731
    sample["buyer_request"] = {"capability": "Dữ liệu minh họa · Phần mềm quản lý kho B2B", "summary": "Dữ liệu minh họa · Phần mềm quản lý kho B2B", "goal": "Mở rộng sang nhà máy Nhật trong 24 tháng", "budget_min_vnd": "70000000000", "budget_max_vnd": "150000000000", "timeline": "LOI trong 90 ngày", **note("nhu cầu mua")}
    sample["nda"] = {"reference": "MH-NDA-01", "parties": ["Buyer minh họa", "Seller minh họa"], "signed_on": day(-50), "expires_on": day(320), "document_id": None, **note("NDA")}
    sample["approvals"] = [{"action": action, **note(ACTION_LABELS[action])} for action in ("sellerL1Approval", "identityRequested", "ndaRecorded", "sellerL2Approval", "legalL3Approval", "crossBorderApproval", "noEscrowConfirmed", "sellerFileApproval")]
    offer = lambda ref, low, high, valid: {"reference": ref, "price_low_vnd": low, "price_high_vnd": high, "valuation_basis": "EV", "exclusivity_days": 60, "valid_until": day(valid), "conditions": "Dữ liệu minh họa"}  # noqa: E731
    sample["indicative_loi"] = {**offer("MH-LOI-01", "90000000000", "120000000000", 30), **note("LOI sơ bộ"), "non_binding": True}
    sample["vdr_opening"] = note("mở phòng dữ liệu")
    finding = lambda title, severity, status: {"id": str(uuid4()), "title": title, "severity": severity, "description": "Dữ liệu minh họa", "remediation": "Dữ liệu minh họa", "impact_vnd": None, "status": status, "created_by": "tech", "created_at": at(20), "history": []}  # noqa: E731
    sample["tech_dd"] = {"findings": [finding("Khả năng mở rộng kiến trúc", "HIGH", "ACCEPTED_RISK"), finding("Thiếu bằng chứng giấy phép mã nguồn mở", "MEDIUM", "RESOLVED")], "signed_off_at": at(15), "signed_off_by": "tech", "sign_off_note": "Dữ liệu minh họa"}
    sample["definitive_offer"] = {**offer("MH-OFFER-01", "105000000000", None, 45), **note("đề nghị chính thức"), "status": "SUBMITTED"}
    sample["legal_closing_checklist"] = note("điều kiện đóng")
    sample["signing"] = {**note("hợp đồng đã ký"), "status": "SIGNED"}
    sample["closing"] = {**note("đóng giao dịch"), "status": "CLOSED", "closed_at": at(5)}
    sample["handoff"] = {"recipient": "Đội tích hợp minh họa", "handed_on": day(-2), "items": ["Mã nguồn", "Tài khoản hạ tầng", "Danh sách khách hàng"], **note("bàn giao"), "status": "HANDED_OFF"}
    fee = lambda kind, amount, due, invoiced, paid: {"id": str(uuid4()), "type": kind, "amount_vnd": amount, "due_on": (today + timedelta(days=due)).isoformat(), "note": "Dữ liệu minh họa", "invoice": {"number": f"MH-{kind}", "issued_on": (today - timedelta(days=30)).isoformat(), "by": "finance"} if invoiced else None, "payments": [{"amount_vnd": paid, "paid_on": (today - timedelta(days=3)).isoformat(), "reference": "Minh họa", "by": "finance"}] if paid else [], "created_by": "finance", "created_at": at(40)}  # noqa: E731
    sample["fees"] = [fee("PREP_PACKAGE", "150000000", -20, True, "150000000"), fee("TECH_DD", "90000000", -2, True, "40000000"), fee("SUCCESS_FEE", "2100000000", 25, True, None)]
    sample["opportunities"] = [{"type": "BUILD_TO_BUY", "status": "OPPORTUNITY", "note": "Dữ liệu minh họa · Cơ hội, chưa phải doanh thu", "at": at(2)}]
    sample["workflow"] = {"status": "CLOSED", "current_step": 20, "stop_reason": None, "opened_data": ["Teaser L1", "Hồ sơ L2", "Tài liệu hạn chế L3", "Finding Tech DD"], "unmet_conditions": [], "history": [{"step": number, "label": label, "owner": owner, "by": "sample", "outcome": "CONTINUE", "note": "Dữ liệu minh họa", "opened_data": [], "completed_at": at(60 - number * 2)} for number, label, owner in WORKFLOW_STAGES]}
    return sample


@router.post("/{deal_id}/complete-sample", response_model=DealResponse, operation_id="complete_sample_deal")
def complete_sample(deal_id: UUID, session: DB, user: User):
    if user.role != "VAULT_ADMIN": raise HTTPException(403, "Chỉ VAULT Admin được nạp dữ liệu minh họa.")
    row = find_deal(session, deal_id, user, lock=True)
    return save(session, row, sample_state(normalize(row.state)), user)
