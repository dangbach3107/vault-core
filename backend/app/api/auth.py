from fastapi import APIRouter, Depends, HTTPException, Request

from backend.app.core.auth import authenticate, current_user, issue_token
from backend.app.schemas.auth import LoginInput, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Synthetic role login"])


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    return forwarded.split(",")[0].strip() or (request.client.host if request.client else "unknown")


@router.post("/login", response_model=LoginResponse, operation_id="login", responses={429: {"description": "Too many failed attempts."}})
def login(body: LoginInput, request: Request):
    limiter = request.app.state.login_limiter
    name, ip = body.username.strip().lower(), client_ip(request)
    limiter.check(name, ip)
    try:
        user = authenticate(request.app.state.settings, body.username, body.password)
    except HTTPException as error:
        if error.status_code == 401:
            limiter.failure(name, ip)
        raise
    limiter.success(name)
    return LoginResponse(access_token=issue_token(request.app.state.settings, user), user=user)


@router.get("/me", response_model=UserResponse, operation_id="current_session")
def me(user: UserResponse = Depends(current_user)):
    return user
