import base64
import hashlib
import hmac
import json
import secrets
import time

from fastapi import Depends, HTTPException, Request

from backend.app.schemas.auth import Role, UserResponse

USERS: dict[str, tuple[Role, str]] = {
    "buyer": ("BUYER", "Buyer"),
    "seller": ("SELLER", "Seller"),
    "seller2": ("SELLER", "Seller khác"),
    "admin": ("VAULT_ADMIN", "VAULT Admin"),
    "legal": ("LEGAL", "Legal/Compliance"),
    "tech": ("TECH_DD", "Tech DD"),
    "finance": ("FINANCE", "Finance"),
}


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def authenticate(settings, username: str, password: str) -> UserResponse:
    record = USERS.get(username.strip().lower())
    expected = settings.demo_role_password.get_secret_value()
    if record is None or not secrets.compare_digest(password, expected):
        raise HTTPException(401, "Tên đăng nhập hoặc mật khẩu không đúng.")
    role, display_name = record
    return UserResponse(username=username.strip().lower(), role=role, display_name=display_name)


def issue_token(settings, user: UserResponse) -> str:
    payload = _encode(json.dumps({"sub": user.username, "role": user.role, "exp": int(time.time()) + 8 * 3600}, separators=(",", ":")).encode())
    signature = _encode(hmac.new(settings.demo_auth_secret.get_secret_value().encode(), payload.encode(), hashlib.sha256).digest())
    return f"{payload}.{signature}"


def current_user(request: Request) -> UserResponse:
    authorization = request.headers.get("authorization", "")
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Cần đăng nhập để sử dụng chức năng này.", headers={"WWW-Authenticate": "Bearer"})
    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload, signature = token.split(".", 1)
        expected = _encode(hmac.new(request.app.state.settings.demo_auth_secret.get_secret_value().encode(), payload.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(signature, expected):
            raise ValueError
        data = json.loads(_decode(payload))
        if int(data["exp"]) < int(time.time()):
            raise ValueError
        role, display_name = USERS[data["sub"]]
        if role != data["role"]:
            raise ValueError
        return UserResponse(username=data["sub"], role=role, display_name=display_name)
    except (ValueError, KeyError, json.JSONDecodeError):
        raise HTTPException(401, "Phiên đăng nhập không hợp lệ hoặc đã hết hạn.", headers={"WWW-Authenticate": "Bearer"}) from None


def require_roles(*allowed_roles: Role):
    def dependency(user: UserResponse = Depends(current_user)) -> UserResponse:
        if user.role not in allowed_roles:
            raise HTTPException(403, "Tài khoản hiện tại không có quyền thực hiện chức năng này.")
        return user
    return dependency
