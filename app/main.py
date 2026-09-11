import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## VAULT Core Framework — 4 Module Kỹ Thuật Lõi (Proof Phase MVP)
    
    1. **Module 1: Trust Profile Engine** (Khử định danh, K-Anonymity, Range Binning, 3-tier profiles).
    2. **Module 2: Secure Virtual Data Room (VDR)** (Cây thư mục 6 cấp, Dynamic Watermarking, Audit Logging).
    3. **Module 3: NDA & Two-Person Approval Gate** (Ký số điện tử, quy tắc Bốn con mắt - Two-Person Rule).
    4. **Module 4: Tech DD & Remediation Cost Calculator** (Thẩm định công nghệ 6 trục, lượng hóa trừ lùi giá M&A).
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve Interactive Dashboard
@app.get("/", response_class=HTMLResponse, tags=["Interactive Web Demo"])
async def serve_dashboard():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
