import os

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "VAULT Core Engine")
    VERSION: str = os.getenv("VERSION", "0.1.0")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "vault_secret_key_demo_2026")
    DEFAULT_TOKEN_EXPIRY_DAYS: int = int(os.getenv("DEFAULT_TOKEN_EXPIRY_DAYS", "14"))

settings = Settings()
