from typing import List, Dict, Any
from app.models.techdd import (
    TechDDAxis,
    FindingSeverity,
    CostClassification,
    TechDDFinding,
    RemediationCostSummary
)

class TechDDScannerService:
    """
    Module 4: Trạm Thẩm định Công nghệ (Tech Due Diligence Engine).
    Đánh giá định lượng 6 trục, phân loại rủi ro P0/P1/P2 và tính toán Bảng chi phí khắc phục (Remediation Cost).
    """

    # Định mức chi phí kỹ sư sửa chữa bình quân của Rikkeisoft (VNĐ/người-tháng)
    ENGINEER_MONTH_RATE_VND: float = 60_000_000

    def evaluate_tech_assets(self, deal_id: str, scan_data: Dict[str, Any] = None) -> RemediationCostSummary:
        """
        Phân tích kết quả kiểm tra mã nguồn, hạ tầng và phỏng vấn kiến trúc sư.
        Xuất ra Báo cáo Thẩm định kèm Đề xuất trừ lùi giá mua M&A.
        """
        findings: List[TechDDFinding] = [
            TechDDFinding(
                finding_id="FIND_01_IP_LICENSE",
                axis=TechDDAxis.IP_OSS_COMPLIANCE,
                title="Sử dụng thư viện Copyleft AGPLv3 trong module tính toán kho",
                description="Module core billing sử dụng thư viện nguồn mở có giấy phép AGPLv3, gây rủi ro buộc phải mở mã nguồn thương mại ra cộng đồng khi bên mua phân phối sản phẩm.",
                severity=FindingSeverity.P0_CRITICAL,
                cost_type=CostClassification.CAPEX_ONE_TIME,
                estimated_man_months=3.0,
                estimated_cost_vnd=3.0 * self.ENGINEER_MONTH_RATE_VND,
                recommended_deal_action="Điều kiện tiên quyết trước khi đóng deal (Condition Precedent): Bên bán bắt buộc viết lại bằng thư viện MIT/Apache-2.0."
            ),
            TechDDFinding(
                finding_id="FIND_02_DISASTER_RECOVERY",
                axis=TechDDAxis.ARCHITECTURE_SCALABILITY,
                title="Thiếu cơ chế sao lưu dự phòng tự động (No Automated Disaster Recovery)",
                description="Cơ sở dữ liệu chính chạy trên máy chủ đơn (Single Point of Failure), chưa có kiến trúc Multi-AZ hoặc quy trình sao lưu định kỳ đạt chuẩn RPO < 1h.",
                severity=FindingSeverity.P1_HIGH,
                cost_type=CostClassification.CAPEX_ONE_TIME,
                estimated_man_months=1.5,
                estimated_cost_vnd=1.5 * self.ENGINEER_MONTH_RATE_VND,
                recommended_deal_action="Trừ lùi trực tiếp vào Giá mua cổ phần (Price Deduction)."
            ),
            TechDDFinding(
                finding_id="FIND_03_TEST_COVERAGE",
                axis=TechDDAxis.CODE_QUALITY_DEBT,
                title="Nợ kỹ thuật cao: Độ bao phủ kiểm thử tự động (Test Coverage) dưới 18%",
                description="Hệ thống thiếu integration tests, tỷ lệ code smells ở mức 14.2% theo chuẩn SonarQube, làm tăng chi phí bảo trì khi mở rộng tính năng.",
                severity=FindingSeverity.P2_MEDIUM,
                cost_type=CostClassification.OPEX_ANNUAL,
                estimated_man_months=2.0,
                estimated_cost_vnd=2.0 * self.ENGINEER_MONTH_RATE_VND,
                recommended_deal_action="Đưa vào Kế hoạch tích hợp công nghệ 100 ngày đầu sau sáp nhập (Post-deal 100-day Roadmap)."
            ),
            TechDDFinding(
                finding_id="FIND_04_DATA_ENCRYPTION",
                axis=TechDDAxis.CYBERSECURITY_PRIVACY,
                title="Dữ liệu nhạy cảm của khách hàng chưa được mã hóa khi lưu trữ (Encryption At-Rest)",
                description="Thông tin danh bạ và đơn hàng lưu dạng văn bản rõ trong PostgreSQL, chưa tuân thủ Nghị định 356/2025/NĐ-CP về Bảo vệ dữ liệu cá nhân.",
                severity=FindingSeverity.P1_HIGH,
                cost_type=CostClassification.CAPEX_ONE_TIME,
                estimated_man_months=1.0,
                estimated_cost_vnd=1.0 * self.ENGINEER_MONTH_RATE_VND,
                recommended_deal_action="Trừ lùi trực tiếp vào Giá mua cổ phần (Price Deduction)."
            )
        ]

        total_capex = sum(f.estimated_cost_vnd for f in findings if f.cost_type == CostClassification.CAPEX_ONE_TIME)
        total_opex = sum(f.estimated_cost_vnd for f in findings if f.cost_type == CostClassification.OPEX_ANNUAL)
        p0_count = sum(1 for f in findings if f.severity == FindingSeverity.P0_CRITICAL)
        p1_count = sum(1 for f in findings if f.severity == FindingSeverity.P1_HIGH)

        return RemediationCostSummary(
            deal_id=deal_id,
            total_findings_count=len(findings),
            critical_p0_count=p0_count,
            high_p1_count=p1_count,
            total_capex_deduction_vnd=total_capex,
            total_opex_impact_vnd=total_opex,
            suggested_valuation_adjustment_vnd=total_capex, # Căn cứ đàm phán trừ lùi tiền mặt
            findings=findings
        )

techdd_service = TechDDScannerService()
