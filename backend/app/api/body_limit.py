from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse


class BodyLimitMiddleware:
    """Bound both declared and streamed request bodies before large uploads spool."""
    def __init__(self, app, max_bytes: int):
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope["headers"])
        try:
            declared = int(headers.get(b"content-length", b"0"))
        except ValueError:
            return await JSONResponse({"detail": "Content-Length không hợp lệ."}, 400)(scope, receive, send)
        if declared > self.max_bytes:
            return await JSONResponse({"detail": "Yêu cầu upload vượt giới hạn dung lượng."}, 413)(scope, receive, send)
        total = 0

        async def bounded_receive():
            nonlocal total
            message = await receive()
            if message["type"] == "http.request":
                total += len(message.get("body", b""))
                if total > self.max_bytes:
                    raise HTTPException(413, "Yêu cầu upload vượt giới hạn dung lượng.")
            return message

        await self.app(scope, bounded_receive, send)
