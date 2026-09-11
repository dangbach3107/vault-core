from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import ConfigDict, Field

from backend.app.schemas.company import StrictModel


class Folder(StrEnum):
    LEGAL = "LEGAL_CORPORATE"
    FINANCIAL = "FINANCIAL_TAX"
    COMMERCIAL = "COMMERCIAL_OPERATIONS"
    TECHNOLOGY = "TECHNOLOGY_IP"
    HR = "HUMAN_RESOURCES"
    QA = "QA_TRACKER"


FOLDER_LABELS = {
    Folder.LEGAL: "01 · Pháp lý & doanh nghiệp",
    Folder.FINANCIAL: "02 · Tài chính & thuế",
    Folder.COMMERCIAL: "03 · Kinh doanh & vận hành",
    Folder.TECHNOLOGY: "04 · Công nghệ & sở hữu trí tuệ",
    Folder.HR: "05 · Nhân sự",
    Folder.QA: "06 · Theo dõi Q&A",
}


class RoomInput(StrictModel):
    company_id: UUID
    title: str = Field(min_length=1, max_length=200)


class RoomResponse(StrictModel):
    id: UUID
    company_id: UUID
    company_name: str
    title: str
    created_at: datetime


class FolderResponse(StrictModel):
    id: Folder
    label: str
    document_count: int


class VersionResponse(StrictModel):
    model_config = ConfigDict(from_attributes=True)
    number: int
    filename: str
    media_type: str
    size_bytes: int
    sha256: str
    note: str
    uploaded_at: datetime


class DocumentResponse(StrictModel):
    id: UUID
    room_id: UUID
    title: str
    folder: Folder
    current_version: int
    latest: VersionResponse


class DocumentDetail(DocumentResponse):
    versions: list[VersionResponse]


class RoomDetail(RoomResponse):
    folders: list[FolderResponse]
    max_upload_bytes: int
    allowed_extensions: list[str]
    documents: list[DocumentResponse]
