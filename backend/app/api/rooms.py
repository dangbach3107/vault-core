import hashlib
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, Query, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.app.api.companies import ApiError, DB, find_company
from backend.app.db.models import Company, Document, DocumentVersion, Room
from backend.app.schemas.room import (
    DocumentDetail, DocumentResponse, Folder, FolderResponse, FOLDER_LABELS,
    RoomDetail, RoomInput, RoomResponse, VersionResponse,
)
from backend.app.services.files import MEDIA_TYPES, persist_upload, stored_path
from backend.app.core.auth import require_roles
from backend.app.schemas.auth import UserResponse

router = APIRouter(prefix="/rooms", tags=["Internal local data rooms"], responses={code: {"model": ApiError} for code in (403, 404, 409, 413, 415, 503)})
RoomReader = Annotated[UserResponse, Depends(require_roles("SELLER", "VAULT_ADMIN", "LEGAL", "TECH_DD"))]
RoomEditor = Annotated[UserResponse, Depends(require_roles("SELLER", "VAULT_ADMIN"))]


def find_room(session, room_id: UUID) -> Room:
    room = session.get(Room, room_id)
    if room is None:
        raise HTTPException(404, "Không tìm thấy phòng dữ liệu.")
    return room


def find_document(session, room_id: UUID, document_id: UUID, lock=False) -> Document:
    query = select(Document).where(Document.id == document_id, Document.room_id == room_id)
    row = session.scalar(query.with_for_update() if lock else query)
    if row is None:
        raise HTTPException(404, "Không tìm thấy tài liệu trong phòng này.")
    return row


def room_response(room, company_name):
    return RoomResponse(id=room.id, company_id=room.company_id, company_name=company_name, title=room.title, created_at=room.created_at)


def document_response(document, latest):
    return DocumentResponse(id=document.id, room_id=document.room_id, title=document.title, folder=document.folder, current_version=document.current_version, latest=VersionResponse.model_validate(latest))


def document_detail(session, document):
    versions = list(session.scalars(select(DocumentVersion).where(DocumentVersion.document_id == document.id).order_by(DocumentVersion.number.desc())))
    return DocumentDetail(**document_response(document, versions[0]).model_dump(), versions=[VersionResponse.model_validate(row) for row in versions])


def delete_blob_files(settings, storage_keys: list[str]) -> None:
    """Remove only blobs resolved by the application's storage-key allowlist."""
    for storage_key in storage_keys:
        try:
            stored_path(settings, storage_key).unlink(missing_ok=True)
        except OSError:
            # Metadata has already been removed transactionally. A leftover opaque
            # blob is safer than reporting a failed request that users may retry.
            continue


@router.get("", response_model=list[RoomResponse], operation_id="list_rooms")
def list_rooms(session: DB, user: RoomReader, company_id: UUID | None = None, offset: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100)):
    query = select(Room, Company.name).join(Company, Room.company_id == Company.id).order_by(Room.created_at.desc(), Room.id)
    if company_id:
        query = query.where(Room.company_id == company_id)
    return [room_response(room, name) for room, name in session.execute(query.offset(offset).limit(limit))]


@router.post("", response_model=RoomResponse, status_code=201, operation_id="create_room")
def create_room(body: RoomInput, session: DB, user: RoomEditor):
    company = find_company(session, body.company_id)
    row = Room(company_id=company.id, title=body.title)
    session.add(row)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Doanh nghiệp đã có phòng dữ liệu mang tên này.") from None
    return room_response(row, company.name)


@router.get("/{room_id}", response_model=RoomDetail, operation_id="get_room")
def get_room(room_id: UUID, request: Request, session: DB, user: RoomReader):
    room = find_room(session, room_id)
    rows = session.execute(select(Document, DocumentVersion).join(DocumentVersion, (DocumentVersion.document_id == Document.id) & (DocumentVersion.number == Document.current_version)).where(Document.room_id == room_id).order_by(Document.title, Document.id))
    documents = [document_response(document, version) for document, version in rows]
    folders = [FolderResponse(id=folder, label=label, document_count=sum(doc.folder == folder for doc in documents)) for folder, label in FOLDER_LABELS.items()]
    return RoomDetail(**room_response(room, find_company(session, room.company_id).name).model_dump(), folders=folders, documents=documents, max_upload_bytes=request.app.state.settings.max_upload_bytes, allowed_extensions=list(MEDIA_TYPES))


@router.delete("/{room_id}", status_code=204, operation_id="delete_room")
def delete_room(room_id: UUID, request: Request, session: DB, user: RoomEditor):
    room = find_room(session, room_id)
    document_ids = list(session.scalars(select(Document.id).where(Document.room_id == room.id)))
    storage_keys = list(session.scalars(select(DocumentVersion.storage_key).where(DocumentVersion.document_id.in_(document_ids)))) if document_ids else []
    if document_ids:
        session.query(DocumentVersion).filter(DocumentVersion.document_id.in_(document_ids)).delete(synchronize_session=False)
        session.query(Document).filter(Document.id.in_(document_ids)).delete(synchronize_session=False)
    session.delete(room)
    try:
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(503, "Chưa xóa được phòng dữ liệu. Kiểm tra database rồi thử lại.") from None
    delete_blob_files(request.app.state.settings, storage_keys)


def save_file_version(request, session, document, upload, note):
    settings = request.app.state.settings
    metadata = persist_upload(settings, upload)
    version = DocumentVersion(document_id=document.id, number=document.current_version, note=note.strip(), **metadata)
    session.add(version)
    try:
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        # Remove only the uniquely-created new blob; earlier versions are untouched.
        stored_path(settings, metadata["storage_key"]).unlink(missing_ok=True)
        raise HTTPException(503, "Chưa lưu được phiên bản. Kiểm tra database rồi thử lại.") from None
    return document_detail(session, document)


@router.post("/{room_id}/documents", response_model=DocumentDetail, status_code=201, operation_id="upload_document")
def upload_document(room_id: UUID, request: Request, session: DB, user: RoomEditor, file: Annotated[UploadFile, File()], folder: Annotated[Folder, Form()], title: Annotated[str, Form(min_length=1, max_length=200)], note: Annotated[str, Form(max_length=1000)] = ""):
    find_room(session, room_id)
    if not title.strip():
        raise HTTPException(422, [{"loc": ["body", "title"], "type": "value_error", "msg": "Tên tài liệu không được trống."}])
    document = Document(room_id=room_id, folder=folder, title=title.strip(), current_version=1)
    session.add(document)
    session.flush()
    return save_file_version(request, session, document, file, note)


@router.get("/{room_id}/documents/{document_id}", response_model=DocumentDetail, operation_id="get_document")
def get_document(room_id: UUID, document_id: UUID, session: DB, user: RoomReader):
    return document_detail(session, find_document(session, room_id, document_id))


@router.delete("/{room_id}/documents/{document_id}", status_code=204, operation_id="delete_document")
def delete_document(room_id: UUID, document_id: UUID, request: Request, session: DB, user: RoomEditor):
    document = find_document(session, room_id, document_id, lock=True)
    storage_keys = list(session.scalars(select(DocumentVersion.storage_key).where(DocumentVersion.document_id == document.id)))
    session.query(DocumentVersion).filter(DocumentVersion.document_id == document.id).delete(synchronize_session=False)
    session.delete(document)
    try:
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise HTTPException(503, "Chưa xóa được tài liệu. Kiểm tra database rồi thử lại.") from None
    delete_blob_files(request.app.state.settings, storage_keys)


@router.post("/{room_id}/documents/{document_id}/versions", response_model=DocumentDetail, status_code=201, operation_id="upload_version")
def upload_version(room_id: UUID, document_id: UUID, request: Request, session: DB, user: RoomEditor, file: Annotated[UploadFile, File()], note: Annotated[str, Form(max_length=1000)] = ""):
    document = find_document(session, room_id, document_id, lock=True)
    document.current_version += 1
    return save_file_version(request, session, document, file, note)


@router.get("/{room_id}/documents/{document_id}/versions/{number}/content", response_class=FileResponse, responses={200: {"description": "Immutable version bytes; Office files are attachment-only.", "content": {media: {"schema": {"type": "string", "format": "binary"}} for media in set(MEDIA_TYPES.values())}}}, operation_id="get_document_content")
def get_content(room_id: UUID, document_id: UUID, number: Annotated[int, Path(ge=1)], request: Request, session: DB, user: RoomReader, download: bool = False):
    document = find_document(session, room_id, document_id)
    version = session.scalar(select(DocumentVersion).where(DocumentVersion.document_id == document.id, DocumentVersion.number == number))
    if version is None:
        raise HTTPException(404, "Không tìm thấy phiên bản.")
    path = stored_path(request.app.state.settings, version.storage_key)
    if not path.is_file():
        raise HTTPException(503, "File lưu trữ không còn khả dụng. Kiểm tra thư mục dữ liệu; metadata vẫn được giữ.")
    try:
        with path.open("rb") as file:
            actual_hash = hashlib.file_digest(file, "sha256").hexdigest()
        if path.stat().st_size != version.size_bytes or actual_hash != version.sha256:
            raise HTTPException(503, "File lưu trữ đã thay đổi ngoài ứng dụng. Không thể trả đúng phiên bản; cần khôi phục file gốc.")
    except OSError:
        raise HTTPException(503, "Không đọc được file lưu trữ. Kiểm tra thư mục dữ liệu.") from None
    inline = not download and version.media_type in {"application/pdf", "image/png", "image/jpeg", "text/plain"}
    return FileResponse(path, media_type=version.media_type, filename=version.filename, content_disposition_type="inline" if inline else "attachment", headers={
        "X-Content-Type-Options": "nosniff", "Cache-Control": "no-store",
        "Content-Security-Policy": "sandbox; default-src 'none'; frame-ancestors 'self'",
    })
