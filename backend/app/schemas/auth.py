from typing import Literal

from pydantic import Field

from backend.app.schemas.company import StrictModel

Role = Literal["BUYER", "SELLER", "VAULT_ADMIN", "LEGAL", "TECH_DD", "FINANCE"]


class LoginInput(StrictModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)


class UserResponse(StrictModel):
    username: str
    role: Role
    display_name: str


class LoginResponse(StrictModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
