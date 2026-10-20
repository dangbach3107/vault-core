import copy
from datetime import date
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from backend.app.api.companies import ApiError, DB, CompanyReader, find_company_for_user
from backend.app.core.auth import require_roles
from backend.app.db.models import Company, Document, DocumentVersion, FactReview, Room, utcnow
from backend.app.schemas.auth import UserResponse
from backend.app.schemas.company import CompanyInput
from backend.app.schemas.review import ReviewDecisionInput, ReviewRequestInput, ReviewResponse
from backend.app.services.profiles import find_fact

router = APIRouter(tags=["Fact reviews"], responses={code: {"model": ApiError} for code in (403, 404, 409, 503)})
Requester = Annotated[UserResponse, Depends(require_roles("SELLER", "VAULT_ADMIN"))]
Reviewer = Annotated[UserResponse, Depends(require_roles("LEGAL", "VAULT_ADMIN"))]


def review_response(review: FactReview, company: Company) -> ReviewResponse:
    return ReviewResponse(
        id=review.id, company_id=review.company_id, company_alias=company.alias, company_name=company.name,
        field=review.field, value=review.value, source=review.source, source_date=review.source_date,
        document=review.document, note=review.note, status=review.status, verification=review.verification,
        requested_by=review.requested_by, requested_at=review.requested_at, decided_by=review.decided_by,
        decided_at=review.decided_at, reason=review.reason,
    )


def evidence_document(session, company: Company, document_id: UUID | None):
    """The cited file must be in this company's own data room; the version is fixed at request time."""
    if document_id is None:
        return None
    row = session.execute(
        select(Document, Room).join(Room, Room.id == Document.room_id)
        .where(Document.id == document_id, Room.company_id == company.id)
    ).first()
    if row is None:
        raise HTTPException(422, "File bằng chứng phải nằm trong phòng dữ liệu của doanh nghiệp này.")
    document, room = row
    version = session.scalar(select(DocumentVersion).where(DocumentVersion.document_id == document.id, DocumentVersion.number == document.current_version))
    return {"document_id": str(document.id), "room_id": str(room.id), "title": document.title, "version_number": version.number, "filename": version.filename}


@router.post("/companies/{company_id}/reviews", response_model=ReviewResponse, status_code=201, operation_id="request_fact_review")
def request_review(company_id: UUID, body: ReviewRequestInput, session: DB, user: Requester):
    company = find_company_for_user(session, company_id, user, lock=True)
    fact = find_fact(company.profile, body.field)
    if fact is None:
        raise HTTPException(422, "Không có dữ kiện này trong hồ sơ.")
    if fact.get("value") is None:
        raise HTTPException(409, "Dữ kiện chưa có giá trị; nhập giá trị trước khi gửi duyệt.")
    if fact.get("issue", "NONE") != "NONE":
        raise HTTPException(409, "Dữ kiện đang mâu thuẫn hoặc hết hạn; xử lý trước khi gửi duyệt.")
    if fact.get("verification", "SELF_DECLARED") != "SELF_DECLARED":
        raise HTTPException(409, "Dữ kiện đã được xác minh.")
    pending = session.scalar(select(FactReview.id).where(FactReview.company_id == company.id, FactReview.field == body.field, FactReview.status == "PENDING"))
    if pending is not None:
        raise HTTPException(409, "Dữ kiện này đang chờ duyệt.")
    review = FactReview(
        company_id=company.id, field=body.field, value=fact["value"], source=body.source, source_date=body.source_date,
        document=evidence_document(session, company, body.document_id), note=body.note, status="PENDING",
        requested_by=user.username, reason="",
    )
    session.add(review); session.commit()
    return review_response(review, company)


@router.get("/companies/{company_id}/reviews", response_model=list[ReviewResponse], operation_id="list_company_reviews")
def list_company_reviews(company_id: UUID, session: DB, user: CompanyReader):
    company = find_company_for_user(session, company_id, user)
    rows = session.scalars(select(FactReview).where(FactReview.company_id == company.id).order_by(FactReview.requested_at.desc()))
    return [review_response(row, company) for row in rows]


@router.get("/reviews", response_model=list[ReviewResponse], operation_id="list_reviews")
def list_reviews(session: DB, user: Reviewer, status: Literal["PENDING", "APPROVED", "REJECTED"] | None = "PENDING"):
    query = select(FactReview, Company).join(Company, Company.id == FactReview.company_id).order_by(FactReview.requested_at)
    if status:
        query = query.where(FactReview.status == status)
    return [review_response(review, company) for review, company in session.execute(query.limit(200))]


@router.post("/reviews/{review_id}/decision", response_model=ReviewResponse, operation_id="decide_fact_review")
def decide_review(review_id: UUID, body: ReviewDecisionInput, session: DB, user: Reviewer):
    review = session.scalar(select(FactReview).where(FactReview.id == review_id).with_for_update())
    if review is None:
        raise HTTPException(404, "Không tìm thấy yêu cầu duyệt.")
    if review.status != "PENDING":
        raise HTTPException(409, "Yêu cầu đã được xử lý.")
    if review.requested_by == user.username:
        raise HTTPException(409, "Người gửi duyệt không tự duyệt dữ kiện của mình.")
    company = session.scalar(select(Company).where(Company.id == review.company_id).with_for_update())
    if body.approved:
        if body.verification is None:
            raise HTTPException(422, "Chọn loại xác minh: đã đối chiếu chứng từ hoặc bên thứ ba xác nhận.")
        profile = copy.deepcopy(company.profile)
        fact = find_fact(profile, review.field)
        if fact is None or fact.get("value") != review.value or fact.get("verification", "SELF_DECLARED") != "SELF_DECLARED" or fact.get("issue", "NONE") != "NONE":
            raise HTTPException(409, "Dữ kiện đã thay đổi sau khi gửi duyệt; cần gửi duyệt lại.")
        fact.update({"verification": body.verification, "source": review.source, "source_date": review.source_date.isoformat(), "reviewed_by": user.username, "reviewed_on": date.today().isoformat()})
        company.profile = CompanyInput.model_validate(profile).model_dump(mode="json")
        company.revision += 1
        company.updated_at = utcnow()
    review.status = "APPROVED" if body.approved else "REJECTED"
    review.verification = body.verification if body.approved else None
    review.decided_by, review.decided_at, review.reason = user.username, utcnow(), body.reason
    session.commit()
    return review_response(review, company)
