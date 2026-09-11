"""Local immutable file store for the user-approved synthetic MVP, not a secure VDR."""
import hashlib
import io
from pathlib import Path
import re
from uuid import uuid4
import warnings
from zipfile import BadZipFile, ZipFile

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader

from backend.app.core.config import REPOSITORY_ROOT, Settings

MEDIA_TYPES = {
    ".pdf": "application/pdf", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".txt": "text/plain",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


def store_root(settings: Settings) -> Path:
    path = settings.upload_directory
    return (path if path.is_absolute() else REPOSITORY_ROOT / path).resolve()


def stored_path(settings: Settings, key: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{32}\.blob", key):
        raise HTTPException(503, "Thông tin file lưu trữ không hợp lệ.")
    root = store_root(settings)
    path = (root / key).resolve()
    if path.parent != root:
        raise HTTPException(503, "Đường dẫn file lưu trữ không hợp lệ.")
    return path


def validate_content(filename: str, data: bytes) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in MEDIA_TYPES:
        raise HTTPException(415, "Chỉ nhận PDF, PNG, JPG/JPEG, TXT, DOCX hoặc XLSX.")
    if not data:
        raise HTTPException(422, [{"loc": ["body", "file"], "type": "value_error", "msg": "File rỗng."}])
    try:
        if extension in {".png", ".jpg", ".jpeg"}:
            with warnings.catch_warnings():
                warnings.simplefilter("error", Image.DecompressionBombWarning)
                with Image.open(io.BytesIO(data)) as picture:
                    expected = "PNG" if extension == ".png" else "JPEG"
                    if picture.format != expected or picture.width * picture.height > 20_000_000:
                        raise ValueError("Invalid image format/size")
                    picture.verify()
                with Image.open(io.BytesIO(data)) as picture:
                    picture.load()
        elif extension == ".pdf":
            if not data.startswith(b"%PDF-"):
                raise ValueError("Not a PDF")
            reader = PdfReader(io.BytesIO(data), strict=True)
            if reader.is_encrypted or not 0 < len(reader.pages) <= 500:
                raise ValueError("Encrypted or too many pages")
            # Reject common active-content objects; not a malware scanner.
            for token in (b"/JavaScript", b"/JS", b"/Launch", b"/EmbeddedFile", b"/OpenAction", b"/XFA"):
                if token in data:
                    raise ValueError("Active content")
        elif extension == ".txt":
            text = data.decode("utf-8-sig")
            if any(ord(char) < 32 and char not in "\r\n\t" for char in text):
                raise ValueError("Binary text")
        else:
            with ZipFile(io.BytesIO(data)) as archive:
                entries = archive.infolist()
                names = {entry.filename for entry in entries}
                required = "word/document.xml" if extension == ".docx" else "xl/workbook.xml"
                if required not in names or "[Content_Types].xml" not in names:
                    raise ValueError("Not an Office document")
                if len(entries) > 2000 or sum(entry.file_size for entry in entries) > 50 * 1024 * 1024:
                    raise ValueError("Oversized archive")
                if any(entry.flag_bits & 1 or "vbaproject" in entry.filename.lower() or "../" in entry.filename or entry.filename.startswith(("/", "\\")) for entry in entries):
                    raise ValueError("Unsafe archive")
                if archive.testzip() is not None:
                    raise ValueError("Corrupt archive")
    except (ValueError, OSError, BadZipFile, UnidentifiedImageError, Image.DecompressionBombError, Image.DecompressionBombWarning, UnicodeError):
        raise HTTPException(415, "Nội dung file không hợp lệ hoặc không phù hợp đuôi file. PDF cần không có mật khẩu, tối đa 500 trang; ảnh tối đa 20 triệu điểm ảnh.") from None
    except Exception:
        # Parser errors must never reveal file paths or original document contents.
        raise HTTPException(415, "Không đọc được định dạng file. Hãy dùng một bản hợp lệ không có mật khẩu.") from None
    return MEDIA_TYPES[extension]


def persist_upload(settings: Settings, upload: UploadFile) -> dict:
    filename = (upload.filename or "").strip()
    if not filename or len(filename) > 255 or any(char in filename for char in ('/', '\\', ':', '\x00', '\r', '\n')) or any(ord(char) < 32 for char in filename):
        raise HTTPException(422, [{"loc": ["body", "file"], "type": "value_error", "msg": "Tên file không hợp lệ."}])
    data = upload.file.read(settings.max_upload_bytes + 1)
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(413, "File vượt giới hạn dung lượng của phòng dữ liệu.")
    media_type = validate_content(filename, data)
    key = uuid4().hex + ".blob"
    path = stored_path(settings, key)
    created = False
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as file:
            created = True
            file.write(data)
    except OSError:
        if created:
            path.unlink(missing_ok=True)
        raise HTTPException(503, "Không ghi được file. Kiểm tra thư mục lưu trữ hoặc dung lượng ổ đĩa.") from None
    return {"filename": filename, "media_type": media_type, "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "storage_key": key}
