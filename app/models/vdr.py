from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class VDRFolderType(str, Enum):
    LEGAL = "01_LEGAL_&_CORPORATE"
    FINANCIAL = "02_FINANCIAL_&_TAX"
    OPERATIONS = "03_COMMERCIAL_&_OPERATIONS"
    TECHNOLOGY = "04_TECHNOLOGY_&_IP"
    HR = "05_HUMAN_RESOURCES"
    QA = "06_Q&A_TRACKER"

class DocumentAccessLevel(int, Enum):
    LAYER_1_PUBLIC = 1
    LAYER_2_NDA_REQUIRED = 2
    LAYER_3_DEEP_DD = 3

class VDRDocument(BaseModel):
    doc_id: str
    deal_id: str
    folder: VDRFolderType
    filename: str
    title: str
    access_level: DocumentAccessLevel
    file_size_bytes: int
    is_downloadable: bool = False
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class WatermarkRequest(BaseModel):
    deal_id: str
    doc_id: str
    viewer_email: str
    viewer_ip: str
    viewer_organization: Optional[str] = "Strategic Investor"

class WatermarkOverlay(BaseModel):
    watermark_text: str
    opacity: float = 0.25
    rotation_degrees: int = -45
    color: str = "rgba(180, 0, 0, 0.3)"
    generated_at: str

class AuditLogEntry(BaseModel):
    log_id: str
    deal_id: str
    doc_id: str
    viewer_email: str
    viewer_ip: str
    action: str  # VIEW_PAGE, DOWNLOAD_ATTEMPT_BLOCKED, ACCESS_GRANTED
    page_number: Optional[int] = 1
    duration_seconds: Optional[int] = 0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
