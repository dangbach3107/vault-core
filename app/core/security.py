import hashlib
import secrets
from datetime import datetime, timedelta

def generate_secure_token(prefix: str = "vlt_") -> str:
    """Tạo token bảo mật ngẫu nhiên không thể đoán trước."""
    random_hex = secrets.token_hex(24)
    return f"{prefix}{random_hex}"

def hash_document_content(content: bytes) -> str:
    """Tạo mã băm SHA-256 xác thực tài liệu bất biến."""
    return hashlib.sha256(content).hexdigest()

def calculate_expiry(days: int = 14) -> datetime:
    return datetime.utcnow() + timedelta(days=days)
