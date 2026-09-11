from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.api.dependencies import database_session
from backend.app.db.models import Company, utcnow
from backend.app.schemas.company import (
    AnonymousPreview, CompanyInput, CompanyResponse, CompanySummary, CompanyUpdate,
    IdentifiedPreview, RestrictedPreview,
)
from backend.app.services.profiles import changed_verified_facts, preview, response
from backend.app.schemas.company import StrictModel

class ApiError(StrictModel):
    detail: str


router = APIRouter(prefix="/companies", tags=["Internal company drafts"], responses={
    403: {"model": ApiError}, 404: {"model": ApiError},
    409: {"model": ApiError}, 503: {"model": ApiError},
})
DB = Annotated[Session, Depends(database_session)]


def find_company(session: Session, company_id: UUID, lock: bool = False) -> Company:
    query = select(Company).where(Company.id == company_id)
    company = session.scalar(query.with_for_update() if lock else query)
    if company is None:
        raise HTTPException(404, "Không tìm thấy doanh nghiệp.")
    return company


def save(session: Session):
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Mã số thuế đã tồn tại trong một hồ sơ khác.") from None


@router.get("", response_model=list[CompanySummary], operation_id="list_companies")
def list_companies(session: DB, q: str = Query(default="", max_length=200), offset: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    query = select(Company).order_by(Company.updated_at.desc(), Company.id).offset(offset).limit(limit)
    if q.strip():
        query = query.where(or_(Company.name.icontains(q.strip(), autoescape=True), Company.tax_id.icontains(q.strip(), autoescape=True)))
    return [CompanySummary(id=row.id, alias=row.alias, name=row.name, tax_id=row.tax_id, updated_at=row.updated_at) for row in session.scalars(query)]


@router.post("", response_model=CompanyResponse, status_code=201, operation_id="create_company")
def create_company(body: CompanyInput, session: DB):
    row = Company(alias=f"VAULT-{uuid4().hex[:12].upper()}", name=body.company_name.value, tax_id=body.tax_id.value, profile=body.model_dump(mode="json"))
    session.add(row)
    save(session)
    return response(row)


@router.get("/{company_id}", response_model=CompanyResponse, operation_id="get_company")
def get_company(company_id: UUID, session: DB):
    return response(find_company(session, company_id))


@router.put("/{company_id}", response_model=CompanyResponse, operation_id="update_company")
def update_company(company_id: UUID, body: CompanyUpdate, session: DB):
    row = find_company(session, company_id, lock=True)
    if row.revision != body.expected_revision:
        raise HTTPException(409, "Hồ sơ đã được sửa ở nơi khác. Tải lại trước khi sửa tiếp.")
    profile = body.profile.model_dump(mode="json")
    if changed_verified_facts(row.profile, profile):
        raise HTTPException(422, [{"loc": ["body", "profile"], "type": "value_error", "msg": "Dữ kiện vừa thay đổi phải lưu nhãn tự khai trước khi đối chiếu lại."}])
    row.profile, row.name, row.tax_id = profile, body.profile.company_name.value, body.profile.tax_id.value
    row.revision += 1
    row.updated_at = utcnow()
    save(session)
    return response(row)


@router.get("/{company_id}/preview/{layer}", response_model=AnonymousPreview | IdentifiedPreview | RestrictedPreview, operation_id="preview_company")
def preview_company(company_id: UUID, layer: Annotated[int, Path(ge=1, le=3)], session: DB):
    return preview(find_company(session, company_id), layer)
