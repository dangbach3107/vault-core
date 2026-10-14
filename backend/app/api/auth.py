from fastapi import APIRouter, Depends, Request

from backend.app.core.auth import authenticate, current_user, issue_token
from backend.app.schemas.auth import LoginInput, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Synthetic role login"])


@router.post("/login", response_model=LoginResponse, operation_id="login")
def login(body: LoginInput, request: Request):
    user = authenticate(request.app.state.settings, body.username, body.password)
    return LoginResponse(access_token=issue_token(request.app.state.settings, user), user=user)


@router.get("/me", response_model=UserResponse, operation_id="current_session")
def me(user: UserResponse = Depends(current_user)):
    return user
