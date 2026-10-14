import hashlib
import io
from uuid import UUID, uuid4
from zipfile import ZipFile

from PIL import Image
from pypdf import PdfWriter
import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from backend.app.db.models import DocumentVersion, DocumentBlob
from backend.app.services.files import stored_path


def png(color="red"):
    buffer = io.BytesIO()
    Image.new("RGB", (16, 16), color=color).save(buffer, format="PNG")
    return buffer.getvalue()


def new_room(client, title="Synthetic deal"):
    company = client.post("/api/v1/companies", json={"company_name": {"value": "Synthetic seller"}}).json()
    response = client.post("/api/v1/rooms", json={"company_id": company["id"], "title": title})
    assert response.status_code == 201, response.text
    return response.json()


def upload(client, room, content=None, name="evidence.png", folder="LEGAL_CORPORATE"):
    return client.post(f'/api/v1/rooms/{room["id"]}/documents', data={"title": "Evidence", "folder": folder, "note": "Synthetic v1"}, files={"file": (name, png() if content is None else content, "application/octet-stream")})


def blob_count(client):
    with client.app.state.session_factory() as session:
        return session.scalar(select(func.count()).select_from(DocumentBlob))


def test_room_six_folders_upload_versions_and_scoping(client):
    room = new_room(client)
    room_path = f'/api/v1/rooms/{room["id"]}'
    folders = client.get(room_path).json()["folders"]
    assert len(folders) == 6
    assert [row["document_count"] for row in folders] == [0] * 6
    assert client.get(f'/api/v1/rooms?company_id={room["company_id"]}').json()[0]["id"] == room["id"]
    assert client.post("/api/v1/rooms", json={"company_id": room["company_id"], "title": room["title"]}).status_code == 409
    document = upload(client, room).json()
    assert document["current_version"] == 1
    assert document["latest"]["sha256"] == hashlib.sha256(png()).hexdigest()
    assert "storage_key" not in str(document)
    path = f'{room_path}/documents/{document["id"]}'
    content1 = client.get(path + "/versions/1/content")
    assert content1.content == png()
    assert content1.headers["content-type"] == "image/png"
    assert content1.headers["x-content-type-options"] == "nosniff"
    assert content1.headers["content-disposition"].startswith("inline")
    version = client.post(path + "/versions", files={"file": ("evidence-2.png", png("blue"))}, data={"note": "Synthetic v2"})
    assert version.status_code == 201, version.text
    assert [row["number"] for row in version.json()["versions"]] == [2, 1]
    assert client.get(path + "/versions/1/content").content == png()
    assert client.get(path + "/versions/2/content").content == png("blue")
    assert client.get(path).json()["current_version"] == 2
    assert client.get(room_path).json()["folders"][0]["document_count"] == 1
    assert client.get(path + "/versions/2/content?download=true").headers["content-disposition"].startswith("attachment")
    other = new_room(client, "Other deal")
    wrong = f'/api/v1/rooms/{other["id"]}/documents/{document["id"]}'
    assert client.get(wrong).status_code == 404
    assert client.get(wrong + "/versions/1/content").status_code == 404
    assert client.post(wrong + "/versions", files={"file": ("other.png", png())}).status_code == 404
    assert client.get(path + "/versions/99/content").status_code == 404
    assert client.get(f"/api/v1/rooms/{uuid4()}").status_code == 404


@pytest.mark.parametrize("name,body,status", [
    ("wrong.png", b"<html>not an image</html>", 415),
    ("wrong.pdf", b"%PDF-not valid", 415),
    ("unsafe.html", b"<script>alert(1)</script>", 415),
    ("../escape.txt", b"Synthetic text", 422),
    ("empty.txt", b"", 422),
    ("large.txt", b"X" * 1025, 413),
    ("binary.txt", b"\x00abc", 415),
])
def test_rejected_upload_has_no_partial_record_or_blob(client, name, body, status):
    room = new_room(client)
    response = upload(client, room, body, name)
    assert response.status_code == status, response.text
    assert client.get(f'/api/v1/rooms/{room["id"]}').json()["documents"] == []
    assert blob_count(client) == 0


def test_invalid_folder_and_failed_version_preserve_old_file(client):
    room = new_room(client)
    assert upload(client, room, folder="UNAPPROVED").status_code == 422
    document = upload(client, room).json()
    path = f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}'
    assert client.post(path + "/versions", files={"file": ("broken.png", b"broken")}).status_code == 415
    assert client.get(path).json()["current_version"] == 1
    assert client.get(path + "/versions/1/content").content == png()


def test_commit_failure_stores_no_new_blob(client, monkeypatch):
    room = new_room(client)
    document = upload(client, room).json()
    old_count = blob_count(client)
    session_class = client.app.state.session_factory.class_
    with monkeypatch.context() as patch:
        def fail_commit(self):
            raise SQLAlchemyError("synthetic storage transaction failure")
        patch.setattr(session_class, "commit", fail_commit)
        response = client.post(f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}/versions', files={"file": ("new.png", png("blue"))})
        assert response.status_code == 503
    assert blob_count(client) == old_count
    assert client.get(f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}').json()["current_version"] == 1


def test_pdf_and_office_download_behavior(client):
    room = new_room(client)
    pdf = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    writer.write(pdf)
    document = upload(client, room, pdf.getvalue(), "synthetic.pdf").json()
    response = client.get(f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}/versions/1/content')
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content == pdf.getvalue()
    office = io.BytesIO()
    with ZipFile(office, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("word/document.xml", "<document>synthetic</document>")
    document = upload(client, room, office.getvalue(), "synthetic.docx").json()
    response = client.get(f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}/versions/1/content')
    assert response.status_code == 200
    assert response.headers["content-disposition"].startswith("attachment")


def test_modified_or_missing_blob_is_reported_without_losing_metadata(client):
    room = new_room(client)
    document = upload(client, room).json()
    content = f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}/versions/1/content'
    with client.app.state.session_factory() as session:
        version = session.scalar(select(DocumentVersion).where(DocumentVersion.document_id == UUID(document["id"])))
        key = version.storage_key
        original = session.get(DocumentBlob, key).content
        session.get(DocumentBlob, key).content = b"Modified outside application"
        session.commit()
        assert client.get(content).status_code == 503
        session.delete(session.get(DocumentBlob, key))
        session.commit()
    assert client.get(content).status_code == 503
    assert client.get(f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}').status_code == 200
    assert original == png()


def test_legacy_disk_file_is_still_served(client):
    room = new_room(client)
    document = upload(client, room).json()
    content = f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}/versions/1/content'
    with client.app.state.session_factory() as session:
        key = session.scalar(select(DocumentVersion.storage_key).where(DocumentVersion.document_id == UUID(document["id"])))
        session.delete(session.get(DocumentBlob, key))
        session.commit()
    root = client.app.state.settings.upload_directory
    root.mkdir(parents=True, exist_ok=True)
    (root / key).write_bytes(png())
    assert client.get(content).content == png()


def test_streamed_request_body_limit(client):
    response = client.post("/api/v1/companies", content=iter([b"X" * 34000, b"Y" * 34000]), headers={"Content-Type": "application/json"})
    assert response.status_code == 413, response.text


def test_delete_document_removes_all_versions_and_blobs(client):
    room = new_room(client)
    document = upload(client, room).json()
    path = f'/api/v1/rooms/{room["id"]}/documents/{document["id"]}'
    assert client.post(path + "/versions", files={"file": ("v2.png", png("blue"))}).status_code == 201
    assert blob_count(client) == 2
    assert client.delete(path).status_code == 204
    assert client.get(path).status_code == 404
    assert client.get(f'/api/v1/rooms/{room["id"]}').json()["documents"] == []
    assert blob_count(client) == 0


def test_delete_room_removes_documents_versions_and_blobs(client):
    room = new_room(client)
    upload(client, room)
    upload(client, room, name="second.png", folder="TECHNOLOGY_IP")
    assert blob_count(client) == 2
    assert client.delete(f'/api/v1/rooms/{room["id"]}').status_code == 204
    assert client.get(f'/api/v1/rooms/{room["id"]}').status_code == 404
    assert blob_count(client) == 0
