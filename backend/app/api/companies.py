from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.api.dependencies import database_session
from backend.app.db.models import Company, Room, utcnow
from backend.app.schemas.company import (
    AnonymousPreview, CompanyInput, CompanyResponse, CompanySummary, CompanyUpdate,
    DealType, IdentifiedPreview, Region, RestrictedPreview, Sector, StrictModel,
)
from backend.app.services.profiles import changed_verified_facts, extract_summary, preview, response, verified_fact_changed
from backend.app.core.auth import require_roles
from backend.app.schemas.auth import UserResponse

class ApiError(StrictModel):
    detail: str


router = APIRouter(prefix="/companies", tags=["Internal company drafts"], responses={
    403: {"model": ApiError}, 404: {"model": ApiError},
    409: {"model": ApiError}, 503: {"model": ApiError},
})
DB = Annotated[Session, Depends(database_session)]
CompanyReader = Annotated[UserResponse, Depends(require_roles("SELLER", "VAULT_ADMIN", "LEGAL"))]
CompanyEditor = Annotated[UserResponse, Depends(require_roles("SELLER", "VAULT_ADMIN"))]
# Verification is a reviewer's decision with evidence, recorded only through /reviews (api/reviews.py).
REVIEWER_ONLY = "Hồ sơ chỉ lưu dữ kiện tự khai. Nhãn xác minh được gắn khi người duyệt chấp thuận yêu cầu duyệt dữ kiện có bằng chứng."


def find_company(session: Session, company_id: UUID, lock: bool = False) -> Company:
    query = select(Company).where(Company.id == company_id)
    company = session.scalar(query.with_for_update() if lock else query)
    if company is None:
        raise HTTPException(404, "Không tìm thấy doanh nghiệp.")
    return company


def find_company_for_user(session: Session, company_id: UUID, user: UserResponse, lock: bool = False) -> Company:
    company = find_company(session, company_id, lock)
    if user.role == "SELLER" and company.owner_username != user.username:
        raise HTTPException(404, "Không tìm thấy doanh nghiệp.")
    return company


def save(session: Session):
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Mã số thuế đã tồn tại trong một hồ sơ khác.") from None


@router.get("", response_model=list[CompanySummary], operation_id="list_companies")
def list_companies(
    session: DB,
    user: CompanyReader,
    q: str = Query(default="", max_length=200),
    sector: Sector | None = Query(default=None),
    region: Region | None = Query(default=None),
    deal_type: DealType | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
):
    query = select(Company).order_by(Company.updated_at.desc(), Company.id)
    if user.role == "SELLER":
        query = query.where(Company.owner_username == user.username)
    if q.strip():
        term = q.strip()
        query = query.where(
            or_(
                Company.name.icontains(term, autoescape=True),
                Company.tax_id.icontains(term, autoescape=True),
                Company.alias.icontains(term, autoescape=True),
            )
        )
    if sector is not None:
        query = query.where(Company.profile[("sector", "value")].as_string() == sector.value)
    if region is not None:
        query = query.where(Company.profile[("region", "value")].as_string() == region.value)
    if deal_type is not None:
        query = query.where(Company.profile[("deal_type", "value")].as_string() == deal_type.value)

    query = query.offset(offset).limit(limit)
    return [extract_summary(row) for row in session.scalars(query)]


@router.post("", response_model=CompanyResponse, status_code=201, operation_id="create_company")
def create_company(body: CompanyInput, session: DB, user: CompanyEditor):
    if verified_fact_changed({}, body.model_dump(mode="json")):
        raise HTTPException(403, REVIEWER_ONLY)
    row = Company(alias=f"VAULT-{uuid4().hex[:12].upper()}", owner_username=user.username, name=body.company_name.value, tax_id=body.tax_id.value, profile=body.model_dump(mode="json"))
    session.add(row)
    save(session)
    return response(row)


@router.get("/{company_id}", response_model=CompanyResponse, operation_id="get_company")
def get_company(company_id: UUID, session: DB, user: CompanyReader):
    return response(find_company_for_user(session, company_id, user))


@router.put("/{company_id}", response_model=CompanyResponse, operation_id="update_company")
def update_company(company_id: UUID, body: CompanyUpdate, session: DB, user: CompanyEditor):
    row = find_company_for_user(session, company_id, user, lock=True)
    if row.revision != body.expected_revision:
        raise HTTPException(409, "Hồ sơ đã được sửa ở nơi khác. Tải lại trước khi sửa tiếp.")
    profile = body.profile.model_dump(mode="json")
    if changed_verified_facts(row.profile, profile):
        raise HTTPException(422, [{"loc": ["body", "profile"], "type": "value_error", "msg": "Dữ kiện vừa thay đổi phải lưu nhãn tự khai trước khi đối chiếu lại."}])
    if verified_fact_changed(CompanyInput.model_validate(row.profile).model_dump(mode="json"), profile):
        raise HTTPException(403, REVIEWER_ONLY)
    row.profile, row.name, row.tax_id = profile, body.profile.company_name.value, body.profile.tax_id.value
    row.revision += 1
    row.updated_at = utcnow()
    save(session)
    return response(row)


@router.delete("/{company_id}", status_code=204, operation_id="delete_company")
def delete_company(company_id: UUID, session: DB, user: CompanyEditor):
    row = find_company_for_user(session, company_id, user, lock=True)
    if session.scalar(select(Room.id).where(Room.company_id == company_id).limit(1)) is not None:
        raise HTTPException(
            409,
            "Hồ sơ đang có phòng dữ liệu. MVP không tự xoá tài liệu; hãy giữ hồ sơ để bảo toàn dữ liệu.",
        )
    session.delete(row)
    session.commit()


@router.get("/{company_id}/preview/{layer}", response_model=AnonymousPreview | IdentifiedPreview | RestrictedPreview, operation_id="preview_company")
def preview_company(company_id: UUID, layer: Annotated[int, Path(ge=1, le=3)], session: DB, user: CompanyReader):
    return preview(find_company_for_user(session, company_id, user), layer)
