from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.vdr import (
    VDRDocument,
    WatermarkRequest,
    WatermarkOverlay,
    AuditLogEntry
)
from app.services.vdr_service import vdr_service

router = APIRouter(prefix="/vdr", tags=["Module 2: Virtual Data Room"])

@router.get("/documents/{deal_id}", response_model=List[VDRDocument])
def get_vdr_documents(deal_id: str):
    """Lấy danh mục cây tài liệu M&A 6 thư mục của deal."""
    return vdr_service.get_documents_for_deal(deal_id)

@router.post("/watermark", response_model=WatermarkOverlay)
def request_watermark_overlay(req: WatermarkRequest):
    """
    Tạo Dynamic Watermark theo thời gian thực (Email + IP + Timestamp)
    và ghi nhận sự kiện truy cập vào Audit Log bất biến.
    """
    return vdr_service.generate_dynamic_watermark(req)

@router.get("/audit-trail", response_model=List[AuditLogEntry])
def get_audit_trail(deal_id: Optional[str] = Query(None)):
    """Truy xuất nhật ký kiểm toán ai đã xem tài liệu nào, lúc nào."""
    return vdr_service.get_audit_trail(deal_id)
