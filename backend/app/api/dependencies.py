from collections.abc import Generator
import secrets
from threading import Lock
from urllib.parse import urlsplit

from fastapi import HTTPException, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.db.session import build_engine, build_session_factory

_engine_lock = Lock()


def origin_allowed(settings, origin: str) -> bool:
    parsed = urlsplit(origin)
    if parsed.hostname in {"127.0.0.1", "localhost", "testserver"}:
        return True
    return origin in settings.allowed_origin_values()


def database_session(request: Request) -> Generator[Session, None, None]:
    settings = request.app.state.settings
    if not settings.internal_preview_enabled:
        raise HTTPException(503, "Bản xem trước nội bộ chưa bật. Xem hướng dẫn thiết lập trong README.")

    # This synthetic preview may be exposed for an internal hosted demo only when
    # ALLOWED_HOSTS/ALLOWED_ORIGINS are explicitly configured. That still is not
    # buyer authentication or production access control.
    if request.url.hostname not in settings.allowed_hostnames():
        raise HTTPException(403, "Host chưa được phép dùng bản xem trước.")
    origin = (request.headers.get("origin") or "").rstrip("/")
    if origin and not origin_allowed(settings, origin):
        raise HTTPException(403, "Không chấp nhận yêu cầu từ trang bên ngoài.")
    if request.headers.get("sec-fetch-site") == "cross-site" and origin and not origin_allowed(settings, origin):
        raise HTTPException(403, "Không chấp nhận yêu cầu từ trang bên ngoài.")

    password = settings.demo_password.get_secret_value()
    if password and not secrets.compare_digest(request.headers.get("x-demo-password", ""), password):
        raise HTTPException(401, "Cần nhập demo password để dùng backend preview.")

    with _engine_lock:
        if request.app.state.session_factory is None:
            try:
                engine = build_engine(request.app.state.settings)
            except ValueError:
                raise HTTPException(503, "Chưa cấu hình PostgreSQL. Xem README.") from None
            request.app.state.engine = engine
            request.app.state.session_factory = build_session_factory(engine)
    try:
        with request.app.state.session_factory() as session:
            yield session
    except SQLAlchemyError:
        raise HTTPException(503, "Không thể lưu/đọc dữ liệu. Kiểm tra PostgreSQL và chạy migration rồi thử lại.") from None
