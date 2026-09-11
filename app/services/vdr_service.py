import uuid
from datetime import datetime
from typing import List, Dict, Optional
from app.models.vdr import (
    VDRFolderType,
    DocumentAccessLevel,
    VDRDocument,
    WatermarkRequest,
    WatermarkOverlay,
    AuditLogEntry
)

class VDRService:
    """
    Module 2: Phòng dữ liệu ảo an toàn (Secure Virtual Data Room).
    Quản lý cây thư mục 6 cấp, phát sinh Watermark động theo danh tính và ghi Audit Log.
    """

    def __init__(self):
        # Bộ nhớ in-memory giả lập database tài liệu cho MVP
        self._documents: Dict[str, List[VDRDocument]] = {}
        self._audit_logs: List[AuditLogEntry] = []

    def initialize_deal_vdr(self, deal_id: str) -> List[VDRDocument]:
        """Khởi tạo cây thư mục tài liệu M&A chuẩn hóa cho một thương vụ."""
        docs = [
            VDRDocument(
                doc_id=f"doc_{uuid.uuid4().hex[:6]}",
                deal_id=deal_id,
                folder=VDRFolderType.LEGAL,
                filename="01_Enterprise_Registration_Certificate.pdf",
                title="Giấy chứng nhận Đăng ký Doanh nghiệp (Bản mới nhất)",
                access_level=DocumentAccessLevel.LAYER_2_NDA_REQUIRED,
                file_size_bytes=2_450_000,
                is_downloadable=False
            ),
            VDRDocument(
                doc_id=f"doc_{uuid.uuid4().hex[:6]}",
                deal_id=deal_id,
                folder=VDRFolderType.FINANCIAL,
                filename="02_Audited_Financial_Statement_3Years.pdf",
                title="Báo cáo Kiểm toán độc lập 3 năm (2023 - 2025)",
                access_level=DocumentAccessLevel.LAYER_3_DEEP_DD,
                file_size_bytes=8_900_000,
                is_downloadable=False
            ),
            VDRDocument(
                doc_id=f"doc_{uuid.uuid4().hex[:6]}",
                deal_id=deal_id,
                folder=VDRFolderType.OPERATIONS,
                filename="03_Key_Factory_Clients_Sample_Contracts.pdf",
                title="Hợp đồng khung tiêu biểu với các nhà máy sản xuất (Masked)",
                access_level=DocumentAccessLevel.LAYER_3_DEEP_DD,
                file_size_bytes=5_100_000,
                is_downloadable=False
            ),
            VDRDocument(
                doc_id=f"doc_{uuid.uuid4().hex[:6]}",
                deal_id=deal_id,
                folder=VDRFolderType.TECHNOLOGY,
                filename="04_System_Architecture_&_Security_Specs.pdf",
                title="Sơ đồ Kiến trúc Phần mềm WMS & Chính sách An toàn Thông tin",
                access_level=DocumentAccessLevel.LAYER_3_DEEP_DD,
                file_size_bytes=12_400_000,
                is_downloadable=False
            ),
            VDRDocument(
                doc_id=f"doc_{uuid.uuid4().hex[:6]}",
                deal_id=deal_id,
                folder=VDRFolderType.HR,
                filename="05_Key_Engineers_Retention_&_Org_Structure.pdf",
                title="Cơ cấu Tổ chức, Danh sách Kỹ sư cốt cán & Chính sách Cam kết",
                access_level=DocumentAccessLevel.LAYER_3_DEEP_DD,
                file_size_bytes=3_200_000,
                is_downloadable=False
            ),
            VDRDocument(
                doc_id=f"doc_{uuid.uuid4().hex[:6]}",
                deal_id=deal_id,
                folder=VDRFolderType.QA,
                filename="06_Technical_&_Financial_QA_Log.pdf",
                title="Nhật ký Giải đáp Thắc mắc Thẩm định (Q&A Tracker)",
                access_level=DocumentAccessLevel.LAYER_3_DEEP_DD,
                file_size_bytes=1_100_000,
                is_downloadable=False
            )
        ]
        self._documents[deal_id] = docs
        return docs

    def get_documents_for_deal(self, deal_id: str) -> List[VDRDocument]:
        if deal_id not in self._documents:
            return self.initialize_deal_vdr(deal_id)
        return self._documents[deal_id]

    def generate_dynamic_watermark(self, req: WatermarkRequest) -> WatermarkOverlay:
        """Tạo chuỗi watermark động định danh duy nhất theo viewer."""
        now_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        watermark_text = (
            f"VAULT STRICTLY CONFIDENTIAL\n"
            f"VIEWER: {req.viewer_email} | IP: {req.viewer_ip}\n"
            f"ORG: {req.viewer_organization} | TIME: {now_utc}\n"
            f"UNAUTHORIZED COPYING OR DISTRIBUTION IS PUNISHABLE BY LAW"
        )
        
        # Ghi log audit truy cập
        self.record_audit_event(
            deal_id=req.deal_id,
            doc_id=req.doc_id,
            viewer_email=req.viewer_email,
            viewer_ip=req.viewer_ip,
            action="VIEW_DOCUMENT_WITH_DYNAMIC_WATERMARK"
        )

        return WatermarkOverlay(
            watermark_text=watermark_text,
            opacity=0.22,
            rotation_degrees=-45,
            color="rgba(190, 20, 20, 0.28)",
            generated_at=now_utc
        )

    def record_audit_event(
        self, deal_id: str, doc_id: str, viewer_email: str, viewer_ip: str, action: str, page: int = 1
    ) -> AuditLogEntry:
        entry = AuditLogEntry(
            log_id=f"log_{uuid.uuid4().hex[:8]}",
            deal_id=deal_id,
            doc_id=doc_id,
            viewer_email=viewer_email,
            viewer_ip=viewer_ip,
            action=action,
            page_number=page,
            duration_seconds=30
        )
        self._audit_logs.append(entry)
        return entry

    def get_audit_trail(self, deal_id: Optional[str] = None) -> List[AuditLogEntry]:
        if deal_id:
            return [l for l in self._audit_logs if l.deal_id == deal_id]
        return self._audit_logs

vdr_service = VDRService()
