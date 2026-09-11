from collections.abc import Generator
from threading import Lock
from urllib.parse import urlsplit

from fastapi import HTTPException, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.db.session import build_engine, build_session_factory

_engine_lock = Lock()


def database_session(request: Request) -> Generator[Session, None, None]:
    if not request.app.state.settings.internal_preview_enabled:
        raise HTTPException(503, "Bản xem trước nội bộ chưa bật. Xem hướng dẫn thiết lập trong README.")
    # A loopback preview is not buyer authentication. Reject browser cross-site
    # requests and hostile Host values, including DNS-rebinding attempts.
    if request.url.hostname not in {"127.0.0.1", "localhost", "testserver"}:
        raise HTTPException(403, "Bản xem trước chỉ dùng trên máy cục bộ.")
    origin = request.headers.get("origin")
    if request.headers.get("sec-fetch-site") == "cross-site" or (origin and urlsplit(origin).hostname not in {"127.0.0.1", "localhost"}):
        raise HTTPException(403, "Không chấp nhận yêu cầu từ trang bên ngoài.")
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
