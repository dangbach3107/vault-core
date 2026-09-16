from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPOSITORY_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = "VAULT Core"
    version: str = "0.1.0"
    api_v1_str: str = Field(default="/api/v1", pattern=r"^/api(?:/[a-zA-Z0-9_-]+)+$")
    environment: str = "development"
    # Optional: liveness checks must not open a database connection.
    database_url: SecretStr = SecretStr("")
    internal_preview_enabled: bool = False
    upload_directory: Path = REPOSITORY_ROOT / ".data" / "uploads"
    max_upload_bytes: int = Field(default=10 * 1024 * 1024, ge=1024, le=50 * 1024 * 1024)

    # Deployment/demo controls. Keep empty for local-only behavior.
    # Comma-separated values; examples:
    # ALLOWED_HOSTS=vault-core-api.onrender.com
    # ALLOWED_ORIGINS=https://frontend-xi-eosin-36.vercel.app
    allowed_hosts: str = ""
    allowed_origins: str = ""
    # Railway injects this after a public domain is generated. Include it in
    # the backend host allowlist so ALLOWED_HOSTS is only needed for custom
    # domains or non-Railway hosts.
    railway_public_domain: str = ""
    # Optional shared demo password. This is only a light demo gate, not real auth/RBAC.
    demo_password: SecretStr = SecretStr("")

    def allowed_hostnames(self) -> set[str]:
        return {
            "127.0.0.1",
            "localhost",
            "testserver",
            *csv_values(self.allowed_hosts),
            *csv_values(self.railway_public_domain),
        }

    def allowed_origin_values(self) -> set[str]:
        return csv_values(self.allowed_origins)


def csv_values(value: str) -> set[str]:
    return {item.strip().rstrip("/") for item in value.split(",") if item.strip()}
