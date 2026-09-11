from fastapi import APIRouter, HTTPException
from app.models.profile import RawSellerInput, TrustProfileResponse
from app.services.profile_engine import profile_engine

router = APIRouter(prefix="/profile", tags=["Module 1: Trust Profile Engine"])

@router.post("/generate", response_model=TrustProfileResponse)
def generate_trust_profile(data: RawSellerInput):
    """
    Sinh Trust Profile 3 phân tầng từ dữ liệu thô bên bán.
    - Lớp 1: Blind Teaser (Ẩn danh, Range Binning, K-Anonymity)
    - Lớp 2: CIM (Định danh, gắn nhãn trạng thái kiểm toán)
    - Lớp 3: Danh mục phòng dữ liệu VDR
    """
    try:
        return profile_engine.process_raw_profile(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
