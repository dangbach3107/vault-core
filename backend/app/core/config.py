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
