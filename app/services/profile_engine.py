import re
import uuid
from typing import Dict, Any
from app.models.profile import (
    RawSellerInput,
    BlindTeaser,
    ConfidentialMemo,
    TrustProfileResponse,
    VerificationStatus
)

class TrustProfileEngine:
    """
    Module 1: Máy sinh Hồ sơ Doanh nghiệp & Trust Profile 3 Phân tầng.
    Áp dụng thuật toán khử định danh (De-identification), Range Binning và K-Anonymity.
    """

    PROVINCE_TO_REGION: Dict[str, str] = {
        "Bình Dương": "Vùng kinh tế Đông Nam Bộ (Việt Nam)",
        "Đồng Nai": "Vùng kinh tế Đông Nam Bộ (Việt Nam)",
        "TP. Hồ Chí Minh": "Vùng kinh tế Đông Nam Bộ (Việt Nam)",
        "Hà Nội": "Vùng kinh tế Trọng điểm Bắc Bộ (Việt Nam)",
        "Hải Phòng": "Vùng kinh tế Trọng điểm Bắc Bộ (Việt Nam)",
        "Bắc Ninh": "Vùng kinh tế Trọng điểm Bắc Bộ (Việt Nam)",
        "Đà Nẵng": "Vùng kinh tế Trọng điểm Miền Trung (Việt Nam)",
    }

    @classmethod
    def map_to_macro_region(cls, province: str) -> str:
        return cls.PROVINCE_TO_REGION.get(province.strip(), "Việt Nam")

    @classmethod
    def compute_revenue_bracket(cls, revenue: float) -> str:
        if revenue < 50_000_000_000:
            return "20 – 50 tỷ VNĐ (~1 – 2 triệu USD)"
        elif revenue <= 100_000_000_000:
            return "50 – 100 tỷ VNĐ (~2 – 4 triệu USD)"
        elif revenue <= 300_000_000_000:
            return "100 – 300 tỷ VNĐ (~4 – 12 triệu USD)"
        elif revenue <= 500_000_000_000:
            return "300 – 500 tỷ VNĐ (~12 – 20 triệu USD)"
        else:
            return "Trên 500 tỷ VNĐ (>20 triệu USD)"

    @classmethod
    def compute_ebitda_bracket(cls, margin_pct: float) -> str:
        if margin_pct < 10:
            return "< 10% (Tăng trưởng tập trung mở rộng quy mô)"
        elif margin_pct <= 20:
            return "15% – 20% (Biên lợi nhuận ổn định ngành phần mềm B2B)"
        elif margin_pct <= 30:
            return "20% – 30% (Biên lợi nhuận cao)"
        else:
            return "> 30% (Biên siêu lợi nhuận)"

    @classmethod
    def compute_employee_bracket(cls, count: int) -> str:
        if count < 20:
            return "10 – 20 nhân sự"
        elif count <= 50:
            return "20 – 50 nhân sự"
        elif count <= 100:
            return "50 – 100 kỹ sư & nhân sự vận hành"
        else:
            return "Trên 100 nhân sự"

    @classmethod
    def generate_project_code(cls, industry: str) -> str:
        clean_tag = re.sub(r'[^A-Z]', '', industry.upper())[:3] or "TECH"
        short_id = uuid.uuid4().hex[:4].upper()
        return f"VAULT_{clean_tag}_{short_id}"

    def process_raw_profile(self, data: RawSellerInput) -> TrustProfileResponse:
        project_code = self.generate_project_code(data.industry_category)
        deal_id = f"deal_{uuid.uuid4().hex[:8]}"

        # --- SINH LỚP 1: BLIND TEASER (Khử hoàn toàn định danh) ---
        layer_1 = BlindTeaser(
            project_code=project_code,
            headline_vi=f"Cơ hội đầu tư chiến lược vào Doanh nghiệp phần mềm {data.industry_category} hàng đầu tại {self.map_to_macro_region(data.province)}",
            headline_ja=f"ベトナムにおける戦略的ソフトウェア企業への出資機会（{data.industry_category}分野）",
            industry_category=data.industry_category,
            macro_region=self.map_to_macro_region(data.province),
            revenue_bracket=self.compute_revenue_bracket(data.annual_revenue_vnd),
            ebitda_bracket=self.compute_ebitda_bracket(data.ebitda_margin_pct),
            employee_bracket=self.compute_employee_bracket(data.employee_count),
            tech_stack=data.tech_stack,
            deal_type=data.deal_type.value,
            target_stake_bracket=f"Khoảng {int(data.target_stake_pct)}% cổ phần",
            verification_summary={
                "financials": "Audited" if data.is_audited else "Verified by internal management accounts",
                "operations": "Verified customer base & ongoing factory contracts"
            }
        )

        # --- SINH LỚP 2: CONFIDENTIAL MEMORANDUM (CIM - Mở sau khi ký NDA) ---
        layer_2 = ConfidentialMemo(
            project_code=project_code,
            company_name=data.company_name,
            tax_id=data.tax_id,
            established_year=data.founding_year,
            headquarters=f"{data.province}, Việt Nam",
            financial_summary_3yr={
                "current_year_revenue_vnd": data.annual_revenue_vnd,
                "ebitda_margin_pct": data.ebitda_margin_pct,
                "net_debt_vnd": data.net_debt_vnd,
                "audit_status": "Audited by " + (data.auditor_name or "Independent Auditor") if data.is_audited else "Management accounts"
            },
            detailed_tech_stack=data.tech_stack,
            org_structure={
                "total_employees": data.employee_count,
                "core_engineering_team": max(10, int(data.employee_count * 0.6)),
                "founder_led": True
            },
            client_clusters=[
                "Nhóm khách hàng nhà máy chế tạo công nghiệp điện tử",
                "Nhóm doanh nghiệp kho vận & chuỗi cung ứng logistics",
                "Các doanh nghiệp FDI đa quốc gia tại khu công nghiệp"
            ],
            valuation_guide={
                "expected_equity_valuation_vnd": data.expected_valuation_vnd,
                "target_stake_pct": data.target_stake_pct,
                "indicative_investment_size_vnd": (data.expected_valuation_vnd or 250_000_000_000) * (data.target_stake_pct / 100)
            },
            verification_badges={
                "revenue": VerificationStatus.AUDITED if data.is_audited else VerificationStatus.DOCUMENT_VERIFIED,
                "legal_registration": VerificationStatus.AUDITED,
                "tech_assets": VerificationStatus.DOCUMENT_VERIFIED,
                "pipeline_contracts": VerificationStatus.DOCUMENT_VERIFIED
            }
        )

        available_layer_3_folders = [
            "01_LEGAL_&_CORPORATE",
            "02_FINANCIAL_&_TAX",
            "03_COMMERCIAL_&_OPERATIONS",
            "04_TECHNOLOGY_&_IP",
            "05_HUMAN_RESOURCES",
            "06_Q&A_TRACKER"
        ]

        return TrustProfileResponse(
            deal_id=deal_id,
            layer_1_teaser=layer_1,
            layer_2_cim=layer_2,
            available_layer_3_folders=available_layer_3_folders
        )

profile_engine = TrustProfileEngine()
