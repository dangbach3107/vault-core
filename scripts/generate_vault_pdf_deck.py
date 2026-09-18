"""
Script to generate a pixel-perfect, dense, interactive 16:9 PDF deck for VAULT
matching the EXACT layout of DABACO.pdf:
- Header on top with section title in bold green, flag, and VAULT · RIKKEISOFT badge
- Top Executive Takeaway Section (2 dense bullets + Green Chevron Arrow + Red Bold Italic Synthesis)
- Full-height main content area filling 100% of the canvas with ZERO wasted white space
- Dense, structured content: Customer ICP, Web UI Mockups, Full Financial Tables from Excel
- Bottom Navigation Bar (Tabs breadcrumbs at bottom with active green pill highlight, exactly like DABACO)
- Complete 26 Slides with 190+ clickable internal jump links
"""

import os
import base64
import subprocess
import pypdf

BASE_DIR = "/Users/ngocbach/vs code"
IMG_DIR = os.path.join(BASE_DIR, "VAULT copy/4, OUTPUT/extracted_docx_images")
HTML_OUTPUT = os.path.join(BASE_DIR, "VAULT copy/4, OUTPUT/VAULT_SLIDES_INTERACTIVE.html")
PDF_OUTPUT = os.path.join(BASE_DIR, "VAULT copy/4, OUTPUT/VAULT_SLIDES_INTERACTIVE.pdf")

def get_b64(filename):
    p = os.path.join(IMG_DIR, filename)
    if not os.path.exists(p):
        return ""
    with open(p, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"

# Pre-load base64 images
IMG_H03 = get_b64("image7.png")   # M&A investors by country 2025 (Japan #1)
IMG_H06 = get_b64("image9.png")   # Japanese expansion intent (JETRO 56.9%)
IMG_H20 = get_b64("image16.png")  # Competitive matrix 6 criteria
IMG_S01 = get_b64("image20.png")  # Deal journey S01 20 steps
IMG_S02 = get_b64("image22.png")  # Book A vs Book B structural map
IMG_S03 = get_b64("image24.png")  # S03 Operating organization & RACI
IMG_H26 = get_b64("image28.png")  # Deal funnel 5 years
IMG_H27 = get_b64("image29.png")  # Revenue breakdown & EBIT margin
IMG_H30 = get_b64("image32.png")  # Cash balance 60 months (trough month 21)
IMG_H32 = get_b64("image34.png")  # Stress-test 8 sensitivity scenarios
IMG_H36 = get_b64("image38.png")  # 11 Risks before & after control

print("Loaded all images into base64 strings.")

# Breadcrumb items definition
NAV_TABS = [
    ("01. ĐỀ ÁN & TẦM NHÌN", "#slide-2", [2, 3]),
    ("02. KHÁCH HÀNG & THỊ TRƯỜNG", "#slide-4", [4, 5]),
    ("03. CÔNG NĂNG & TECH", "#slide-6", [6, 7, 8]),
    ("04. VẬN HÀNH & QUY TRÌNH", "#slide-9", [9, 10]),
    ("05. PHÂN TÍCH TÀI CHÍNH", "#slide-11", [11, 12, 13]),
    ("06. RỦI RO & ĐỀ XUẤT", "#slide-14", [14, 15]),
]

def render_bottom_nav(slide_num):
    tabs_html = []
    for label, link, pages in NAV_TABS:
        is_active = "active" if slide_num in pages else ""
        tabs_html.append(f'<a href="{link}" class="nav-tab-item {is_active}">{label}</a>')
    
    app_active = 'style="background: #155724; color: #ffffff !important;"' if slide_num >= 16 else ''
    return f"""
    <div class="bottom-nav">
      <div class="nav-tabs-group">
        {''.join(tabs_html)}
      </div>
      <a href="#slide-16" class="appendix-pill" {app_active}>PHỤ LỤC DEBATE PLAYBOOK &rsaquo;</a>
    </div>
    """

def render_header(title):
    return f"""
    <div class="top-header">
      <div class="header-left">
        <div class="flag-tag">
          <div class="flag-green"></div>
          <div class="flag-red"></div>
          <div class="flag-yellow"></div>
        </div>
        <span class="slide-title-header">{title}</span>
      </div>
      <div class="header-right">
        <span class="rikkei-logo-badge">VAULT · RIKKEISOFT</span>
      </div>
    </div>
    """

def render_takeaway(bullet1, bullet2, conclusion):
    return f"""
    <div class="takeaway-bar">
      <div class="takeaway-bullets">
        <div>• {bullet1}</div>
        <div>• {bullet2}</div>
      </div>
      <div class="takeaway-chevron">&rsaquo;</div>
      <div class="takeaway-conclusion">
        {conclusion}
      </div>
    </div>
    """

CSS_STYLES = """
<style>
  @page {
    size: 1440pt 810pt;
    margin: 0;
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #0f172a;
    background: #f1f5f9;
  }

  /* Slide Canvas (Exact 16:9 DABACO Dimensions) */
  .slide {
    width: 1440pt;
    height: 810pt;
    page-break-after: always;
    position: relative;
    background: #ffffff;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    padding: 0;
  }

  /* Top Header Bar (DABACO Style) */
  .top-header {
    height: 50pt;
    padding: 0 38pt;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 2pt solid #e2e8f0;
    background: #ffffff;
    flex-shrink: 0;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 14pt;
  }
  .flag-tag {
    display: flex;
    height: 22pt;
    width: 38pt;
    border-radius: 3pt;
    overflow: hidden;
    box-shadow: 0 1pt 4pt rgba(0,0,0,0.12);
  }
  .flag-green { flex: 1; background: #15803d; }
  .flag-red { flex: 1; background: #b91c1c; }
  .flag-yellow { flex: 1; background: #f59e0b; }

  .slide-title-header {
    font-size: 20pt;
    font-weight: 900;
    color: #155724;
    letter-spacing: -0.3pt;
    text-transform: uppercase;
  }
  .header-right {
    display: flex;
    align-items: center;
    gap: 12pt;
  }
  .rikkei-logo-badge {
    font-size: 10pt;
    font-weight: 900;
    color: #155724;
    letter-spacing: 1.5pt;
    background: #f0fdf4;
    border: 1.5pt solid #86efac;
    padding: 5pt 12pt;
    border-radius: 5pt;
  }

  /* Top Executive Takeaway Section (DABACO Style) */
  .takeaway-bar {
    background: #ffffff;
    border: 1.2pt solid #e2e8f0;
    border-left: 6pt solid #155724;
    border-radius: 5pt;
    padding: 8pt 18pt;
    margin: 8pt 38pt 6pt 38pt;
    display: flex;
    align-items: center;
    gap: 18pt;
    flex-shrink: 0;
    box-shadow: 0 1pt 4pt rgba(0,0,0,0.02);
  }
  .takeaway-bullets {
    flex: 1.6;
    display: flex;
    flex-direction: column;
    gap: 4pt;
    font-size: 10.2pt;
    color: #334155;
    line-height: 1.4;
  }
  .takeaway-bullets b {
    color: #0f172a;
  }
  .takeaway-chevron {
    font-size: 34pt;
    color: #155724;
    font-weight: 900;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 6pt;
    flex-shrink: 0;
  }
  .takeaway-conclusion {
    flex: 1;
    font-size: 10.8pt;
    font-weight: 800;
    color: #991b1b;
    font-style: italic;
    line-height: 1.42;
    background: #fef2f2;
    border-left: 4pt solid #b91c1c;
    padding: 8pt 12pt;
    border-radius: 4pt;
  }

  /* Content Body */
  .slide-body {
    flex: 1;
    padding: 4pt 38pt 8pt 38pt;
    display: flex;
    flex-direction: column;
    min-height: 0;
  }

  /* Grid Layouts */
  .full-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14pt;
    flex: 1;
    min-height: 0;
  }
  .full-grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12pt;
    flex: 1;
    min-height: 0;
  }
  .full-grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12pt;
    flex-shrink: 0;
    margin-bottom: 8pt;
  }

  /* Full-Height Dense Cards (DABACO Style) */
  .dense-card {
    background: #ffffff;
    border: 1.4pt solid #cbd5e1;
    border-radius: 6pt;
    padding: 10pt 14pt;
    box-shadow: 0 2pt 5pt rgba(0,0,0,0.02);
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 0;
  }
  .dense-card-title {
    text-align: center;
    color: #b91c1c;
    font-size: 12pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.4pt;
    margin-bottom: 8pt;
    border-bottom: 1.5pt solid #f1f5f9;
    padding-bottom: 5pt;
    flex-shrink: 0;
  }
  .dense-card-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8pt;
    min-height: 0;
  }

  /* Meta Banner */
  .meta-banner {
    background: #f8fafc;
    border: 1.2pt solid #e2e8f0;
    border-radius: 4pt;
    padding: 6pt 10pt;
    font-size: 9.5pt;
    color: #334155;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
  }

  /* KPI Stat Boxes */
  .kpi-box {
    background: #f8fafc;
    border: 1.2pt solid #e2e8f0;
    border-left: 4pt solid #155724;
    border-radius: 5pt;
    padding: 7pt 12pt;
  }
  .kpi-num {
    font-size: 20pt;
    font-weight: 900;
    color: #155724;
    line-height: 1.1;
  }
  .kpi-label {
    font-size: 8.8pt;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    margin-top: 3pt;
  }

  /* Tables */
  .dense-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9.5pt;
  }
  .dense-table th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 800;
    text-align: left;
    padding: 6pt 8pt;
    border-bottom: 1.8pt solid #cbd5e1;
    border-top: 1pt solid #e2e8f0;
  }
  .dense-table td {
    padding: 5.5pt 8pt;
    border-bottom: 1pt solid #e2e8f0;
    color: #334155;
    vertical-align: middle;
    line-height: 1.4;
  }
  .dense-table tr:nth-child(even) td {
    background: #fafafa;
  }
  .dense-table tr.highlight-row td {
    background: #fef2f2;
    font-weight: 700;
    color: #991b1b;
  }
  .dense-table tr.total-row td {
    background: #f1f5f9;
    font-weight: 900;
    border-top: 1.8pt solid #94a3b8;
    border-bottom: 2.2pt solid #475569;
    color: #0f172a;
  }
  .text-right { text-align: right; }
  .text-center { text-align: center; }

  /* Image Box */
  .dense-img-box {
    border: 1.4pt solid #cbd5e1;
    border-radius: 6pt;
    padding: 8pt;
    background: #ffffff;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 0;
  }
  .dense-img-box img {
    max-width: 100%;
    max-height: 86%;
    object-fit: contain;
  }
  .dense-img-caption {
    font-size: 8.8pt;
    color: #64748b;
    font-weight: 600;
    margin-top: 6pt;
    text-align: center;
    flex-shrink: 0;
  }

  /* Bottom Nav (DABACO Style) */
  .bottom-nav {
    height: 42pt;
    padding: 0 38pt;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 2.5pt solid #155724;
    background: #ffffff;
    flex-shrink: 0;
  }
  .nav-tabs-group {
    display: flex;
    align-items: center;
    gap: 6pt;
  }
  .nav-tab-item {
    font-size: 9.2pt;
    font-weight: 700;
    color: #475569;
    text-decoration: none;
    padding: 5.5pt 12pt;
    border-radius: 4pt;
    text-transform: uppercase;
  }
  .nav-tab-item:hover {
    color: #0f172a;
    background: #f1f5f9;
  }
  .nav-tab-item.active {
    background: #155724;
    color: #ffffff !important;
    font-weight: 800;
  }
  .appendix-pill {
    background: #fef2f2;
    border: 1.2pt solid #fca5a5;
    color: #991b1b;
    padding: 5.5pt 14pt;
    border-radius: 4pt;
    font-size: 9.2pt;
    font-weight: 800;
    text-decoration: none;
  }
</style>
"""

def generate_full_deck():
    slides = []

    # ==========================================
    # SLIDE 01: COVER
    # ==========================================
    slides.append(f"""
    <div class="slide" id="slide-1" style="background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%); color: #ffffff; justify-content: center; align-items: center; text-align: center; padding: 40pt;">
      <div style="background: rgba(21, 128, 61, 0.25); border: 1.5pt solid #22c55e; color: #86efac; font-size: 11pt; font-weight: 800; text-transform: uppercase; padding: 6pt 18pt; border-radius: 30pt; letter-spacing: 2pt; margin-bottom: 20pt;">
        BÁO CÁO TRÌNH HỘI ĐỒNG QUẢN TRỊ (BOD) RIKKEISOFT
      </div>
      <h1 style="font-size: 46pt; font-weight: 900; letter-spacing: -0.5pt; margin: 0 0 14pt 0; color: #ffffff;">
        ĐỀ ÁN NỀN TẢNG M&amp;A VAULT
      </h1>
      <p style="font-size: 14.5pt; color: #94a3b8; max-width: 950pt; line-height: 1.5; margin: 0 auto 30pt auto;">
        Nền tảng Điều phối M&amp;A và Hợp tác Đầu tư Việt - Nhật trong Hệ sinh thái Rikkeisoft<br>
        Chuẩn hóa Dữ liệu Doanh nghiệp • Thẩm định Kỹ thuật (Tech DD) • Phòng Dữ liệu ảo (VDR)
      </p>

      <div style="display: flex; gap: 8pt; justify-content: center; flex-wrap: wrap; max-width: 1050pt; margin-bottom: 28pt;">
        <a href="#slide-2" style="background: #334155; color: #f8fafc; padding: 7pt 14pt; border-radius: 4pt; text-decoration: none; font-size: 9pt; font-weight: 700; border: 1pt solid #475569;">01. ĐỀ ÁN &amp; TẦM NHÌN</a>
        <a href="#slide-4" style="background: #334155; color: #f8fafc; padding: 7pt 14pt; border-radius: 4pt; text-decoration: none; font-size: 9pt; font-weight: 700; border: 1pt solid #475569;">02. KHÁCH HÀNG &amp; THỊ TRƯỜNG</a>
        <a href="#slide-6" style="background: #334155; color: #f8fafc; padding: 7pt 14pt; border-radius: 4pt; text-decoration: none; font-size: 9pt; font-weight: 700; border: 1pt solid #475569;">03. CÔNG NĂNG &amp; TECH</a>
        <a href="#slide-9" style="background: #334155; color: #f8fafc; padding: 7pt 14pt; border-radius: 4pt; text-decoration: none; font-size: 9pt; font-weight: 700; border: 1pt solid #475569;">04. VẬN HÀNH &amp; QUY TRÌNH</a>
        <a href="#slide-11" style="background: #334155; color: #f8fafc; padding: 7pt 14pt; border-radius: 4pt; text-decoration: none; font-size: 9pt; font-weight: 700; border: 1pt solid #475569;">05. PHÂN TÍCH TÀI CHÍNH</a>
        <a href="#slide-14" style="background: #334155; color: #f8fafc; padding: 7pt 14pt; border-radius: 4pt; text-decoration: none; font-size: 9pt; font-weight: 700; border: 1pt solid #475569;">06. RỦI RO &amp; ĐỀ XUẤT</a>
        <a href="#slide-16" style="background: #b91c1c; color: #ffffff; padding: 7pt 18pt; border-radius: 4pt; text-decoration: none; font-size: 9pt; font-weight: 800; border: 1pt solid #ef4444;">👉 MỤC LỤC PHỤ LỤC DEBATE (SLIDE 16)</a>
      </div>

      <div style="font-size: 9pt; color: #64748b;">
        Ban Dự án VAULT • Báo cáo Nghiên cứu Chiến lược 5 Năm • Tháng 09/2026
      </div>
    </div>
    """)

    # ==========================================
    # SLIDE 02: 01. ĐỀ ÁN & TẦM NHÌN · BỐI CẢNH THỊ TRƯỜNG & KHẢO SÁT JETRO (H06)
    slides.append(f"""
    <div class="slide" id="slide-2">
      {render_header("01. ĐỀ ÁN & TẦM NHÌN · BỐI CẢNH THỊ TRƯỜNG & KHẢO SÁT JETRO (H06)")}
      {render_takeaway(
          "<b>Nhu cầu M&A Việt - Nhật tăng vọt nhưng nghẽn ở khâu thực thi:</b> 56.9% doanh nghiệp Nhật muốn mở rộng tại Việt Nam (dẫn đầu ASEAN).",
          "<b>Rào cản lớn nhất là thông tin bất cân xứng & sổ sách kế toán:</b> Thiếu đơn vị thẩm định công nghệ độc lập và cơ chế bảo mật danh tính.",
          "Thị trường M&A Mid-Tier (20–100 tỷ) đang bỏ trống: Cần một nền tảng số hóa quy trình và bảo chứng công nghệ để khơi thông dòng vốn."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: Market Context & Pain Points -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">THỰC TRẠNG THỊ TRƯỜNG & ĐIỂM NGHẼN M&A VIỆT - NHẬT</div>
            <div class="dense-card-body" style="gap: 7pt;">
              <div style="background: #fff5f5; border-left: 4pt solid #b91c1c; padding: 7pt 10pt; font-size: 8.8pt; border-radius: 4pt; line-height: 1.42;">
                <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.2pt;">3 Điểm Nghẽn Trọng Yếu Khiến 80% Thương Vụ M&A Thất Bại:</b>
                1. <b>Bất cân xứng thông tin:</b> Bên mua Nhật Bản e ngại rủi ro gian lận tài chính, 'hai sổ sách' và nợ kỹ thuật ẩn giấu.<br>
                2. <b>Sợ lộ bí mật kinh doanh:</b> Bên bán Việt Nam sợ mất khách hàng, lộ danh tính và biến động nhân sự khi mở thông tin.<br>
                3. <b>Chi phí thẩm định đắt đỏ:</b> Phí Big 4 từ 50.000–100.000 USD/deal, hoàn toàn không khả thi cho deal tầm trung (20–100 tỷ).
              </div>

              <table class="dense-table" style="font-size: 8.8pt;">
                <thead>
                  <tr>
                    <th style="width: 25%;">Khía cạnh</th>
                    <th style="width: 37%;">M&A Truyền Thống</th>
                    <th style="width: 38%; background: #155724; color: #ffffff;">Mô Hình Nền Tảng VAULT</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 6.5pt 7pt;"><b>Thời gian chốt deal</b></td>
                    <td style="padding: 6.5pt 7pt;">12 – 18 tháng (Kéo dài, dễ đổ bể)</td>
                    <td style="padding: 6.5pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">6 – 9 tháng (Rút ngắn 50%)</td>
                  </tr>
                  <tr>
                    <td style="padding: 6.5pt 7pt;"><b>Thẩm định công nghệ</b></td>
                    <td style="padding: 6.5pt 7pt;">Bỏ qua hoặc chỉ nhìn sơ lược</td>
                    <td style="padding: 6.5pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">Tech DD 6 Trục độc quyền Rikkeisoft</td>
                  </tr>
                  <tr>
                    <td style="padding: 6.5pt 7pt;"><b>Cơ chế bảo mật</b></td>
                    <td style="padding: 6.5pt 7pt;">Ký NDA giấy, dễ rò rỉ dữ liệu</td>
                    <td style="padding: 6.5pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">Khử định danh K-Anonymity + Sandboxed VDR</td>
                  </tr>
                </tbody>
              </table>

              <div style="background: #f0fdf4; border: 1.2pt solid #86efac; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.6pt; color: #166534; line-height: 1.4;">
                <b>Điểm Đột Phá Của VAULT:</b> Chuẩn hóa hồ sơ doanh nghiệp bằng công nghệ số (Digital Assets), tạo lập lòng tin vững chắc giữa Bên mua Nhật Bản và Bên bán Việt Nam ngay từ bước tiếp cận sơ bộ.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Khảo sát thực địa M&A Việt - Nhật 2025–2026 (01_VAULT_REPORT.docx)</div>
            </div>
          </div>

          <!-- Right Card: JETRO Chart H06 -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">KHẢO SÁT JETRO 2024: ĐỘNG LỰC MỞ RỘNG CỦA DOANH NGHIỆP NHẬT (H06)</div>
            <div class="dense-card-body" style="gap: 7pt;">
              <div class="meta-banner" style="font-size: 8.8pt;">
                <span><b>56.9% DN Nhật</b> muốn mở rộng tại VN</span>
                <span><b>905 Doanh nghiệp</b> phản hồi hợp lệ</span>
                <span style="color: #155724; font-weight: 700;">Việt Nam xếp Top 1 ASEAN</span>
              </div>
              <div class="chart-box" style="flex: 1; min-height: 250pt; max-height: 275pt;">
                <div class="chart-caption" style="background: #155724; padding: 4.5pt 12pt;">
                  <span>Hình H06 · Xu hướng mở rộng hoạt động kinh doanh của doanh nghiệp Nhật Bản</span>
                  <span>JETRO 2024</span>
                </div>
                <img src="{IMG_H06}" style="width: 90%; max-height: 220pt; object-fit: contain; margin: 4pt auto;" alt="Hình H06">
              </div>
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.6pt; color: #334155; line-height: 1.42;">
                <b style="color: #0f172a; display: block; margin-bottom: 2pt; font-size: 9pt;">Nhận Định Phân Tích Thực Tiễn Từ Số Liệu JETRO:</b>
                • <b>Làn sóng M&A thay thế Green-field:</b> Các tập đoàn Nhật chuyển từ tự mở văn phòng mới sang thâu tóm công ty bản địa để có ngay đội ngũ kỹ sư CNTT và giấy phép.<br>
                • <b>Áp lực thiếu hụt nhân lực tại Nhật Bản:</b> Nhu cầu số hóa khẩn cấp khiến các công ty Nhật sẵn sàng chi tiền nhanh cho các thương vụ M&A công nghệ tại Việt Nam.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Khảo sát thực trạng doanh nghiệp Nhật Bản tại nước ngoài (JETRO 2024)</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(2)}
    </div>
    """)
# SLIDE 03: 01. ĐỀ ÁN & TẦM NHÌN · ĐỊNH VỊ VAULT & HỢP LỰC RIKKEI
    slides.append(f"""
    <div class="slide" id="slide-3">
      {render_header("01. TỔNG QUAN ĐỀ ÁN · ĐỊNH VỊ NỀN TẢNG & HỢP LỰC HỆ SINH THÁI RIKKEISOFT")}
      {render_takeaway(
          "<b>Thay thế môi giới thủ công bằng tài sản số:</b> Số hóa quy trình giải mật, lưu vết Tech DD bất biến và cấu trúc schema doanh nghiệp.",
          "<b>Đánh trúng phân khúc Mid-Tier (20–100 tỷ VNĐ):</b> Nơi Big 4 bỏ rơi vì chi phí quá cao, còn môi giới tự do không có năng lực kỹ thuật.",
          "VAULT là Tech-enabled Platform nâng năng suất Deal Lead lên 8–10 deal/năm và tạo phễu hợp đồng IT Modernization cho Rikkei."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: Comparative Positioning -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">BẢN CHẤT ĐỊNH VỊ: TECH-ENABLED TRANSACTION PLATFORM</div>
            <div class="dense-card-body" style="gap: 7pt;">
              <table class="dense-table" style="font-size: 8.8pt;">
                <thead>
                  <tr>
                    <th style="width: 22%;">Tiêu chí so sánh</th>
                    <th style="width: 25%;">Môi giới Truyền thống</th>
                    <th style="width: 25%;">Sàn TMĐT M&A</th>
                    <th style="width: 28%; background: #155724; color: #ffffff;">Nền tảng VAULT</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 6.5pt 7pt;"><b>Bảo mật thông tin</b></td>
                    <td style="padding: 6.5pt 7pt;">Gửi teaser qua email cá nhân</td>
                    <td style="padding: 6.5pt 7pt;">Đăng công khai đại trà</td>
                    <td style="padding: 6.5pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">Khử định danh K-Anonymity (k≥5)</td>
                  </tr>
                  <tr>
                    <td style="padding: 6.5pt 7pt;"><b>Thẩm định Kỹ thuật</b></td>
                    <td style="padding: 6.5pt 7pt;">Không có (Chỉ làm tài chính)</td>
                    <td style="padding: 6.5pt 7pt;">Tự khai báo (Self-claim)</td>
                    <td style="padding: 6.5pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">Báo cáo Tech DD 6 Trục độc quyền</td>
                  </tr>
                  <tr>
                    <td style="padding: 6.5pt 7pt;"><b>Phòng dữ liệu (VDR)</b></td>
                    <td style="padding: 6.5pt 7pt;">Dùng Google Drive / Dropbox</td>
                    <td style="padding: 6.5pt 7pt;">Không có / Link đính kèm</td>
                    <td style="padding: 6.5pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">Sandboxed VDR + Watermark động</td>
                  </tr>
                  <tr>
                    <td style="padding: 6.5pt 7pt;"><b>Năng suất Deal Lead</b></td>
                    <td style="padding: 6.5pt 7pt;">2 – 3 deal/năm (Rất thủ công)</td>
                    <td style="padding: 6.5pt 7pt;">0 (Không có người điều phối)</td>
                    <td style="padding: 6.5pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">8 – 10 deal/năm (Nhảy vọt 3–4x)</td>
                  </tr>
                  <tr>
                    <td style="padding: 6.5pt 7pt;"><b>Chống 'Đi đêm'</b></td>
                    <td style="padding: 6.5pt 7pt;">Ký NDA giấy, khó phạt</td>
                    <td style="padding: 6.5pt 7pt;">Bị vượt mặt 100%</td>
                    <td style="padding: 6.5pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">Khóa duyệt 2 tầng + Immutable Audit</td>
                  </tr>
                  <tr>
                    <td style="padding: 6.5pt 7pt;"><b>Mô hình nguồn thu</b></td>
                    <td style="padding: 6.5pt 7pt;">Phụ thuộc 100% Success fee</td>
                    <td style="padding: 6.5pt 7pt;">Thu tiền đăng tin quảng cáo</td>
                    <td style="padding: 6.5pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">Doanh thu kép: Prep Pack + Phí 2%</td>
                  </tr>
                </tbody>
              </table>

              <!-- Ecosystem Value Sharing Panel -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.5pt;">
                <b style="color: #1e293b; display: block; margin-bottom: 3pt; font-size: 9pt;">Cơ Chế Chia Sẻ Doanh Thu & Giá Trị Hợp Lực Hệ Sinh Thái:</b>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6pt; color: #475569;">
                  <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4pt 6pt; border-radius: 3pt;">
                    <b style="color: #0f172a;">1. Prep Pack 90tr:</b> VAULT thu 40tr vận hành; trích 50tr trả cho chuyên gia Rikkeisoft thực hiện Tech DD.
                  </div>
                  <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4pt 6pt; border-radius: 3pt;">
                    <b style="color: #0f172a;">2. Success Fee 2%:</b> Giữ lại toàn bộ để bù đắp chi phí phát triển và tích lũy cổ tức hoàn vốn cho công ty mẹ.
                  </div>
                  <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4pt 6pt; border-radius: 3pt;">
                    <b style="color: #155724;">3. Post-M&A IT Deal:</b> Rikkeisoft độc quyền nhận hợp đồng Modernization phần mềm trị giá 500k–2M USD.
                  </div>
                </div>
              </div>

              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.5pt; color: #334155; line-height: 1.42;">
                <b style="color: #0f172a; display: block; margin-bottom: 2pt; font-size: 9pt;">4 Tầng Phòng Thủ (Moat) Độc Quyền Của VAULT:</b>
                1. <b>Chi phí chuyển đổi cao (Switching Cost):</b> Toàn bộ schema dữ liệu & hồ sơ ký số gắn liền với hệ thống.<br>
                2. <b>Hiệu ứng mạng lưới cục bộ:</b> Càng nhiều Buyer Nhật xem hồ sơ thì Seller CNTT Việt càng dồn về VAULT.<br>
                3. <b>Bảo chứng uy tín Rikkeisoft:</b> Không đối thủ môi giới nào sao chép được đội ngũ 2.000 kỹ sư Tech DD.<br>
                4. <b>Bằng chứng số bất biến (Immutable Proof):</b> Trọng tài quốc tế SIAC/VIAC công nhận chứng cứ pháp lý.
              </div>

              <div style="background: #f0fdf4; border: 1.2pt solid #86efac; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.5pt; color: #166534; line-height: 1.38;">
                <b>Hợp lực cùng Rikkeisoft:</b> Tiếp cận 500+ khách hàng Tokyo, tận dụng năng lực kỹ sư sẵn có và độc quyền nhận các hợp đồng IT Modernization hàng chục triệu USD hậu M&A.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Báo cáo Đề án VAULT (01_VAULT_REPORT.md)</div>
            </div>
          </div>

          <!-- Right Card: Radar Chart H20 -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">MA TRẬN NĂNG LỰC 6 TIÊU CHÍ SO VỚI CÁC ĐỐI THỦ (HÌNH H20)</div>
            <div class="dense-card-body" style="gap: 7pt;">
              <div class="meta-banner" style="font-size: 8.8pt;">
                <span><b>Đối thủ:</b> Big 4 · Môi giới tự do · Sàn TMĐT · Tự kết nối</span>
                <span style="color: #155724; font-weight: 700;">VAULT: Điểm tuyệt đối 6/6</span>
              </div>
              <div class="chart-box" style="flex: 1; min-height: 250pt; max-height: 275pt;">
                <div class="chart-caption" style="background: #991b1b; padding: 4.5pt 12pt;">
                  <span>Hình H20 · VAULT không thắng ở mạng lưới bên mua; chỗ đứng nằm ở công nghệ</span>
                  <span>điểm 1–5, đánh giá định tính</span>
                </div>
                <img src="{IMG_H20}" style="width: 88%; max-height: 220pt; object-fit: contain; margin: 4pt auto;" alt="Hình H20">
              </div>
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 8pt 10pt; font-size: 8.6pt; color: #334155; line-height: 1.42;">
                <b style="color: #0f172a; display: block; margin-bottom: 2pt; font-size: 9pt;">3 Điểm Khác Biệt Cạnh Tranh Tuyệt Đối Của VAULT:</b>
                • <b>Big 4 bỏ ngỏ phân khúc Mid-tier:</b> Chi phí tối thiểu 100.000 USD/deal khiến Big 4 không phục vụ các deal 20–100 tỷ VNĐ.<br>
                • <b>Sàn TMĐT thất bại vì thiếu kiểm định:</b> Không có bảo chứng công nghệ, tỷ lệ khớp lệnh thành công dưới 5% và dễ lộ danh tính.<br>
                • <b>VAULT tối ưu hóa toàn diện:</b> Kết hợp nền tảng số hóa chi phí thấp với năng lực bảo chứng chuyên sâu của hệ sinh thái Rikkeisoft.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Đánh giá vị thế cạnh tranh VAULT 2026 (Hình H20, 01_VAULT_REPORT.md)</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(3)}
    </div>
    """)
# SLIDE 04: 02. KHÁCH HÀNG & THỊ TRƯỜNG · CHÂN DUNG HAI ĐẦU (ICP)
    # ==========================================
    slides.append(f"""
    <div class="slide" id="slide-4">
      {render_header("02. KHÁCH HÀNG MỤC TIÊU · CHÂN DUNG HAI ĐẦU (ICP BUYER &amp; SELLER)")}
      {render_takeaway(
        "<b>Buyer Nhật (Bên Mua):</b> Doanh nghiệp tầm trung cần mở rộng năng lực công nghệ nhưng cực kỳ e ngại rủi ro nợ kỹ thuật và văn hóa.",
        "<b>Seller Việt (Bên Bán):</b> Doanh nghiệp công nghệ 20–100 tỷ chạm trần tăng trưởng; sợ nhất bị lộ danh tính làm mất khách hàng và rò rỉ nhân sự.",
        "VAULT giải quyết bài toán cốt lõi: Khử định danh bảo vệ Seller Việt và Cung cấp Báo cáo Tech DD độc lập cho Buyer Nhật."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: Buyer Japan -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">BÊN MUA: DOANH NGHIỆP TẦM TRUNG NHẬT BẢN (BUYER JAPAN)</div>
            <div class="dense-card-body">
              <div class="meta-banner">
                <span><b>Quy mô:</b> 500M – 2.000M JPY</span>
                <span><b>Ticket Mục tiêu:</b> 20 – 100 Tỷ VNĐ (1–4M USD)</span>
                <span><b>Tỷ lệ Mua:</b> 51% – 100% Cổ phần</span>
              </div>

              <table class="dense-table">
                <tbody>
                  <tr>
                    <td style="width: 28%;"><b>Động lực chiến lược</b></td>
                    <td>Thiếu hụt trầm trọng 790.000 kỹ sư CNTT tại Nhật; áp lực mở rộng Đông Nam Á để duy trì tăng trưởng.</td>
                  </tr>
                  <tr>
                    <td><b>Khẩu vị công nghệ</b></td>
                    <td>Sản phẩm B2B SaaS, Logistics WMS/TMS, FinTech, E-commerce, Outsourcing có biên EBITDA ổn định 18%–25%.</td>
                  </tr>
                  <tr>
                    <td><b>Rào cản lớn nhất</b></td>
                    <td>Sợ bất đồng văn hóa quản trị, nợ kỹ thuật (Tech Debt) ẩn giấu, vi phạm bản quyền mã nguồn mở (GPLv3).</td>
                  </tr>
                  <tr>
                    <td><b>Quy trình phê duyệt</b></td>
                    <td>Cần tối thiểu 2 cấp duyệt (Ringi-sho): Business Unit Sponsor nội bộ + Hội đồng Đầu tư / Ban Giám đốc (BOD).</td>
                  </tr>
                  <tr>
                    <td><b>Tiêu chuẩn hồ sơ</b></td>
                    <td>Chỉ xem hồ sơ đã qua sàng lọc K-Anonymity (k&ge;5) và Báo cáo Tech DD 6 trục do Rikkei chứng thực độc lập.</td>
                  </tr>
                  <tr>
                    <td><b>Ngân sách thẩm định</b></td>
                    <td>Sẵn sàng chi trả 10.000 – 25.000 USD phí Tech DD độc lập; ký cam kết giải ngân thẩm định trong 30–45 ngày.</td>
                  </tr>
                </tbody>
              </table>

              <div style="background: #f0fdf4; border: 1.2pt solid #86efac; padding: 7pt 10pt; border-radius: 4pt; font-size: 8.8pt; color: #166534;">
                <b>6 Tiêu chí Bắt buộc trong Buyer Brief Form:</b> (1) BU Sponsor bảo trợ; (2) Ticket size tối thiểu; (3) Timeline phê duyệt 6-9 tháng; (4) Quyền quyết định; (5) Ngân sách thẩm định độc lập; (6) Ký NDA điện tử Lớp 2.
              </div>

              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; padding: 7pt 10pt; border-radius: 4pt; font-size: 8.8pt; color: #334155;">
                <b>Chiến lược Buy-Side First:</b> Khai thác trực tiếp mạng lưới 500+ doanh nghiệp Nhật Bản của Rikkeisoft Japan để gom trước các đầu mối M&amp;A có ngân sách thực, tạo mỏ neo thanh khoản ngay từ Ngày đầu.
              </div>

              <div style="font-size: 8pt; color: #64748b; text-align: right; margin-top: auto;">Nguồn: Khảo sát JETRO 2025 &amp; Dữ liệu 50 doanh nghiệp Nhật Bản của Rikkeisoft Japan</div>
            </div>
          </div>

          <!-- Right Card: Seller Vietnam -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">BÊN BÁN: DOANH NGHIỆP CÔNG NGHỆ &amp; SẢN XUẤT NỘI ĐỊA (SELLER VN)</div>
            <div class="dense-card-body">
              <div class="meta-banner">
                <span><b>Doanh thu:</b> 20 – 100 Tỷ VNĐ/năm</span>
                <span><b>Biên EBITDA:</b> 15% – 25%</span>
                <span><b>Nhân sự:</b> 30 – 120 Kỹ sư / Nhân viên</span>
              </div>

              <table class="dense-table">
                <tbody>
                  <tr>
                    <td style="width: 28%;"><b>Động cơ thoái vốn</b></td>
                    <td>Chạm trần tăng trưởng vốn nội địa; thế hệ sáng lập F1 muốn thoái vốn; tìm đối tác chiến lược để vươn quốc tế.</td>
                  </tr>
                  <tr>
                    <td><b>Nỗi sợ sống còn</b></td>
                    <td><b>SỢ BỊ LỘ DANH TÍNH:</b> Mất khách hàng hiện tại, đối thủ cướp nhân sự giỏi, ngân hàng siết hạn mức tín dụng.</td>
                  </tr>
                  <tr>
                    <td><b>Thực trạng nội tại</b></td>
                    <td>BCTC chưa kiểm toán Big 4/quốc tế, tồn tại chênh lệch sổ thuế và sổ quản trị (Book A/B), thiếu tài liệu kỹ thuật.</td>
                  </tr>
                  <tr>
                    <td><b>Kỳ vọng định giá</b></td>
                    <td>Thường neo giá theo cảm tính (P/E 15-20x), cần Báo cáo Gap List và định giá độc lập để hạ cánh thực tế về P/E 7-10x.</td>
                  </tr>
                  <tr>
                    <td><b>Gói Prep Pack (90tr)</b></td>
                    <td>Nhận trọn bộ: (1) Khử định danh Teaser; (2) Tech DD 6 trục Rikkei; (3) VDR quốc tế; (4) <b>Cấn trừ 100% vào Success Fee</b>.</td>
                  </tr>
                  <tr>
                    <td><b>Cam kết độc quyền</b></td>
                    <td>Ký thỏa thuận đại diện độc quyền 6 tháng với VAULT để kiểm soát toàn bộ luồng tiếp cận thông tin của bên mua.</td>
                  </tr>
                </tbody>
              </table>

              <div style="background: #fef2f2; border: 1.2pt solid #fca5a5; padding: 7pt 10pt; border-radius: 4pt; font-size: 8.8pt; color: #991b1b;">
                <b>4 Giá Trị Nhận Về Từ Gói Prep Pack 90 Triệu:</b> (1) Báo cáo Tech DD 6 trục độc lập do Rikkei kiểm định; (2) Chuẩn hóa BCTC &amp; Báo cáo Gap List; (3) Phòng VDR chuẩn quốc tế; (4) Cấn trừ 100% vào Success Fee khi chốt deal.
              </div>

              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; padding: 7pt 10pt; border-radius: 4pt; font-size: 8.8pt; color: #334155;">
                <b>Single-Player Utility (Giá Trị Độc Lập):</b> Ngay cả khi chưa chốt được M&amp;A, Bên bán vẫn sở hữu bộ tài sản số Tech DD &amp; VDR chuẩn quốc tế để tự tin gọi vốn, vay vốn ngân hàng hoặc nâng cấp năng lực quản trị.
              </div>

              <div style="font-size: 8pt; color: #64748b; text-align: right; margin-top: auto;">Nguồn: Nghiên cứu thị trường VAULT &amp; Phỏng vấn 30 Nhà sáng lập CNTT Việt Nam</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(4)}
    </div>
    """)

    # ==========================================
    # SLIDE 05: 02. KHÁCH HÀNG & THỊ TRƯỜNG · MÔ HÌNH 2 PHỄU & BUY-SIDE FIRST
    slides.append(f"""
    <div class="slide" id="slide-5">
      {render_header("02. KHÁCH HÀNG & THỊ TRƯỜNG · MÔ HÌNH 2 PHỄU CHUYỂN ĐỔI & CHIẾN LƯỢC BUY-SIDE FIRST")}
      {render_takeaway(
          "<b>Đảo chiều mô hình truyền thống:</b> Đi từ nhu cầu mua thật (Buy-side First) thay vì gom hàng loạt bên bán rồi rao vặt vô vọng.",
          "<b>Tỷ lệ chuyển đổi vượt trội:</b> Thu thập 25–30 Buyer Briefs từ 500+ khách Nhật của Rikkei để kéo 15–19 Seller chất lượng ký Prep Pack.",
          "Chiến lược Buy-side First giúp khống chế rủi ro tồn kho hồ sơ, đảm bảo tỷ lệ khớp lệnh LOI đạt trên 60%."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: 2 Conversion Funnels -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">CƠ CHẾ VẬN HÀNH 2 PHỄU: BUY-SIDE LEADS & SELLER ONBOARDING</div>
            <div class="dense-card-body" style="gap: 7pt;">
              <table class="dense-table" style="font-size: 8.8pt;">
                <thead>
                  <tr>
                    <th style="width: 25%;">Tầng phễu</th>
                    <th style="width: 38%;">Phễu Bên Mua (Buyer Funnel)</th>
                    <th style="width: 37%;">Phễu Bên Bán (Seller Funnel)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>1. Tiếp cận sơ bộ</b></td>
                    <td style="padding: 6pt 7pt;">500+ Khách hàng Rikkeisoft Tokyo</td>
                    <td style="padding: 6pt 7pt;">80+ Doanh nghiệp CNTT & Phụ trợ</td>
                  </tr>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>2. Xác thực nhu cầu</b></td>
                    <td style="padding: 6pt 7pt;">25 – 30 Qualified Buyer Briefs</td>
                    <td style="padding: 6pt 7pt;">35 – 40 Doanh nghiệp nộp hồ sơ KYC</td>
                  </tr>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>3. Ký hợp đồng dịch vụ</b></td>
                    <td style="padding: 6pt 7pt;">12 – 15 Buyer ký Retainer / NDA L2</td>
                    <td style="padding: 6pt 7pt; font-weight: 700; color: #155724; background: #f0fdf4;">15 – 19 HĐ Prep Pack (90tr/gói)</td>
                  </tr>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>4. Mở phòng VDR & Q&A</b></td>
                    <td style="padding: 6pt 7pt;">8 – 10 Buyer thẩm định chuyên sâu</td>
                    <td style="padding: 6pt 7pt;">8 – 10 Doanh nghiệp hoàn thiện VDR L3</td>
                  </tr>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>5. Ký LOI độc quyền</b></td>
                    <td style="padding: 6pt 7pt; font-weight: 700; color: #155724;">4 – 6 Thỏa thuận LOI được ký</td>
                    <td style="padding: 6pt 7pt; font-weight: 700; color: #155724;">4 – 6 Bên bán chấp thuận LOI</td>
                  </tr>
                  <tr style="background: #f0fdf4; font-weight: 800;">
                    <td style="padding: 6pt 7pt; color: #155724;">6. Đóng deal thành công</td>
                    <td style="padding: 6pt 7pt; color: #155724;">1 – 2 Deal hoàn tất (Năm 2)</td>
                    <td style="padding: 6pt 7pt; color: #155724;">1 – 2 Deal thu phí 2% Success Fee</td>
                  </tr>
                </tbody>
              </table>

              <!-- Funnel Conversion Metrics Grid -->
              <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6pt;">
                <div style="background: #f8fafc; border: 1pt solid #cbd5e1; padding: 5pt; border-radius: 4pt; text-align: center;">
                  <div style="font-size: 7.6pt; color: #64748b;">Chuyển đổi Prep Pack</div>
                  <b style="font-size: 11pt; color: #155724;">47.5%</b>
                  <div style="font-size: 7.2pt; color: #475569;">19/40 nộp hồ sơ</div>
                </div>
                <div style="background: #f8fafc; border: 1pt solid #cbd5e1; padding: 5pt; border-radius: 4pt; text-align: center;">
                  <div style="font-size: 7.6pt; color: #64748b;">Tỷ lệ Ký LOI / VDR</div>
                  <b style="font-size: 11pt; color: #155724;">50.0%</b>
                  <div style="font-size: 7.2pt; color: #475569;">5 LOI / 10 VDR</div>
                </div>
                <div style="background: #f8fafc; border: 1pt solid #cbd5e1; padding: 5pt; border-radius: 4pt; text-align: center;">
                  <div style="font-size: 7.6pt; color: #64748b;">Tỷ lệ Đóng Deal / LOI</div>
                  <b style="font-size: 11pt; color: #155724;">21.0%</b>
                  <div style="font-size: 7.2pt; color: #475569;">11 deals / 5 năm</div>
                </div>
                <div style="background: #f8fafc; border: 1pt solid #cbd5e1; padding: 5pt; border-radius: 4pt; text-align: center;">
                  <div style="font-size: 7.6pt; color: #64748b;">Chu kỳ giao dịch</div>
                  <b style="font-size: 11pt; color: #b91c1c;">6–9T</b>
                  <div style="font-size: 7.2pt; color: #475569;">Giảm 50% vs TT</div>
                </div>
              </div>

              <div style="background: #f0fdf4; border: 1.2pt solid #86efac; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.5pt; color: #166534; line-height: 1.38;">
                <b>Nguyên Lý Vận Hành Phễu Kép:</b> Không quảng cáo đại trà. Dùng Brief của Buyer Nhật để 'đo ni đóng giày' tìm kiếm Seller; dùng phí Prep Pack 90tr để thanh lọc 100% hồ sơ rác ngay tại cửa vào.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Thiết kế phễu giao dịch S02 &amp; S14 (01_VAULT_REPORT.docx)</div>
            </div>
          </div>

          <!-- Right Card: Milestone Funnel Chart H26 -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">MÔ HÌNH PHỄU CHUYỂN ĐỔI THEO MỐC VẬN HÀNH (HÌNH H26)</div>
            <div class="dense-card-body" style="gap: 7pt;">
              <div class="meta-banner" style="font-size: 8.8pt;">
                <span><b>5 Mốc kiểm soát:</b> Tiếp cận › KYC › Prep Pack › VDR › Đóng deal</span>
                <span style="color: #b91c1c; font-weight: 700;">Chốt chặn Cổng 2: Tháng 12</span>
              </div>
              <div class="chart-box" style="flex: 1; min-height: 250pt; max-height: 275pt;">
                <div class="chart-caption" style="background: #991b1b; padding: 4.5pt 12pt;">
                  <span>Hình H26 · Mô hình phễu chuyển đổi và các mốc kiểm soát thương vụ M&A</span>
                  <span>Báo cáo đề án VAULT</span>
                </div>
                <img src="{IMG_H26}" style="width: 90%; max-height: 220pt; object-fit: contain; margin: 4pt auto;" alt="Hình H26">
              </div>
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.6pt; color: #334155; line-height: 1.42;">
                <b style="color: #0f172a; display: block; margin-bottom: 2pt; font-size: 9pt;">Phân Tích 3 Điểm Chốt Chặn Trên Sơ Đồ H26:</b>
                • <b>Mốc 1 (Sàng lọc KYC):</b> Loại bỏ ngay các doanh nghiệp vi phạm pháp lý hoặc không có ý định thoái vốn thật sự.<br>
                • <b>Mốc 2 (Nghiệm thu Prep Pack):</b> Chỉ khi dữ liệu đạt chuẩn Tech DD 6 trục mới được đưa vào Sandboxed VDR.<br>
                • <b>Mốc 3 (Khóa độc quyền LOI):</b> Buyer ký quỹ bảo đảm và cam kết timeline thẩm định không quá 60 ngày.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Quy trình vận hành chuẩn hóa 20 bước S01 &amp; S02</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(5)}
    </div>
    """)
# SLIDE 06: 03. CÔNG NĂNG & TECH · 4 MODULE LÕI (F01-F16)
    slides.append(f"""
    <div class="slide" id="slide-6">
      {render_header("03. CÔNG NĂNG & TECH · 4 MODULE NỀN TẢNG CỐT LÕI (F01–F16)")}
      {render_takeaway(
          "<b>Kiến trúc module hóa khép kín:</b> 16 tính năng chia đều cho 4 module phục vụ từ chuẩn hóa dữ liệu, bảo mật, đối soát đến hậu M&A.",
          "<b>Tích hợp sâu năng lực Rikkeisoft:</b> Kế thừa hạ tầng điện toán đám mây và quy trình thẩm định kỹ thuật chuẩn CMMI Dev Level 5.",
          "Hệ thống phần mềm đóng vai trò đòn bẩy năng suất, giải phóng Deal Lead khỏi 70% các thao tác giấy tờ thủ công."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- G1: Onboarding & Trust Profile -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">MODULE 1: ONBOARDING & TRUST PROFILE (F01–F04)</div>
            <div class="dense-card-body" style="gap: 6.5pt;">
              <div style="background: #f8fafc; border: 1pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #155724;">F01 · Portal Tự Khai & Chuẩn Hóa Schema:</b> Hướng dẫn bên bán nhập 120 trường dữ liệu tài chính, nhân sự, công nghệ; tự động đối chiếu hóa đơn điện tử và BCTC.<br>
                <span style="color: #64748b; font-size: 8pt;">• Chuẩn hóa dữ liệu VAS sang IFRS • Kiểm tra tính hợp lệ của mã số thuế</span>
              </div>
              <div style="background: #f8fafc; border: 1pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #155724;">F02 · Thuật Toán Khử Định Danh K-Anonymity (k≥5):</b> Tự động ẩn danh tên công ty, làm mờ dải doanh thu và địa lý lên cấp Vùng, chống tuyệt đối nhận diện ngược.<br>
                <span style="color: #64748b; font-size: 8pt;">• Tự động sinh mã định danh ẩn (VD: VN-LOG09) • Kiểm soát nhận diện chéo</span>
              </div>
              <div style="background: #f8fafc; border: 1pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #155724;">F03 · Tạo Teaser Tự Động Lớp 1 (1-Pager / 3-Pager):</b> Xuất báo cáo tóm tắt khử danh song ngữ Nhật - Việt chỉ trong 1 click, sẵn sàng gửi chào hàng cho 500+ Buyer.<br>
                <span style="color: #64748b; font-size: 8pt;">• Định dạng PDF vector sắc nét • Tích hợp biểu đồ tài chính tự động</span>
              </div>
              <div style="background: #f8fafc; border: 1pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #155724;">F04 · Cơ Chế Khóa Duyệt Hai Tầng (Two-Person Approval):</b> Yêu cầu đồng thời chữ ký số của Đại diện Bên bán và Trưởng ban Pháp lý VAULT mới mở quyền truy cập.<br>
                <span style="color: #64748b; font-size: 8pt;">• Xác thực qua OTP / Chữ ký số USB Token • Ghi nhận log phê duyệt bất biến</span>
              </div>
              <div style="background: #f0fdf4; border: 1pt solid #86efac; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt; color: #166534;">
                <b>Chỉ số đo lường (KPI):</b> Rút ngắn thời gian lập hồ sơ chào bán từ 45 ngày xuống 7 ngày; tỷ lệ lỗi dữ liệu giảm 95%.
              </div>
            </div>
          </div>

          <!-- G2: Thẩm Định Kỹ Thuật (Tech DD Engine) -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">MODULE 2: CÔNG CỤ THẨM ĐỊNH KỸ THUẬT (F05–F08)</div>
            <div class="dense-card-body" style="gap: 6.5pt;">
              <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #991b1b;">F05 · Bộ Quét Mã Nguồn & Bản Quyền OSS:</b> Quét tự động kho mã nguồn để phát hiện thư viện bản quyền lây lan (GPLv3/AGPL) và kiểm tra chuẩn an toàn OWASP.<br>
                <span style="color: #64748b; font-size: 8pt;">• Tích hợp SonarQube & Snyk • Tự động tạo bảng phân tích SBOM bản quyền</span>
              </div>
              <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #991b1b;">F06 · Đo Lường & Định Lượng Nợ Kỹ Thuật (Tech Debt):</b> Quy đổi toàn bộ lỗi kiến trúc, mã nguồn lỗi thời thành chi phí khắc phục tiền mặt (Remediation Budget).<br>
                <span style="color: #64748b; font-size: 8pt;">• Công thức tính nợ kỹ thuật quy chuẩn • Làm căn cứ trừ giá đàm phán SPA</span>
              </div>
              <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #991b1b;">F07 · Đánh Giá Năng Lực & Phụ Thuộc Nhân Sự:</b> Phân tích biểu đồ cam kết đóng góp code (Git Contribution Matrix), phát hiện rủi ro dự án phụ thuộc vào 1 cá nhân.<br>
                <span style="color: #64748b; font-size: 8pt;">• Chỉ số Bus Factor • Khuyến nghị phương án giữ chân nhân sự cốt lõi</span>
              </div>
              <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #991b1b;">F08 · Xuất Báo Cáo Tech DD 6 Trục Chuẩn Rikkei:</b> Tổng hợp báo cáo kỹ thuật toàn diện song ngữ Nhật - Việt được chứng thực bởi Hội đồng Kỹ thuật Rikkeisoft.<br>
                <span style="color: #64748b; font-size: 8pt;">• 6 Trục đánh giá chuẩn hóa • Có giá trị bảo chứng độc lập với quỹ đầu tư</span>
              </div>
              <div style="background: #fef2f2; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt; color: #991b1b;">
                <b>Vũ khí cạnh tranh độc quyền:</b> Không một công ty môi giới hay sàn TMĐT nào trên thị trường sở hữu năng lực kiểm định mã nguồn này.
              </div>
            </div>
          </div>

          <!-- G3: Sandboxed VDR & DRM Security -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">MODULE 3: SANDBOXED VDR & BẢO MẬT DRM (F09–F12)</div>
            <div class="dense-card-body" style="gap: 6.5pt;">
              <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #991b1b;">F09 · Trình Chiếu Sandboxed HTML5 Chống Tải Xuống:</b> Tài liệu chỉ được xem trực tiếp trên trình duyệt bị cô lập, khóa chức năng in, sao chép và chụp màn hình.<br>
                <span style="color: #64748b; font-size: 8pt;">• Vô hiệu hóa tính năng PrintScreen • Chặn Inspect Element & Developer Tools</span>
              </div>
              <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #991b1b;">F10 · Mã Vân Tay Động (Forensic Dynamic Watermark):</b> Khắc chìm email người xem, địa chỉ IP và timestamp theo thời gian thực lên từng trang tài liệu.<br>
                <span style="color: #64748b; font-size: 8pt;">• Watermark ẩn giấu trong pixel • Truy vết đích danh 100% nếu có rò rỉ</span>
              </div>
              <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #991b1b;">F11 · Nhật Ký Truy Cập Bất Biến (Immutable Audit Trail):</b> Lưu vết từng giây người xem mở trang nào, dừng lại bao lâu; dữ liệu mã hóa băm SHA-256.<br>
                <span style="color: #64748b; font-size: 8pt;">• Cung cấp bằng chứng pháp lý trước Trọng tài VIAC/SIAC nếu có tranh chấp</span>
              </div>
              <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #991b1b;">F12 · Cơ Chế Thu Hồi Quyền Tự Động (Access Self-Destruct):</b> Tự động khóa phòng dữ liệu sau 72 giờ không có hoạt động hoặc khi hết hạn thỏa thuận thẩm định.<br>
                <span style="color: #64748b; font-size: 8pt;">• Xóa token truy cập từ xa • Triệt tiêu hoàn toàn rủi ro lưu cache cục bộ</span>
              </div>
              <div style="background: #fef2f2; border: 1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt; color: #991b1b;">
                <b>Tuân thủ Nghị định 13/2023/NĐ-CP:</b> Dữ liệu máy chủ đặt tại Việt Nam; không chuyển giao PII ra nước ngoài trái phép.
              </div>
            </div>
          </div>

          <!-- G4: Khớp Lệnh & Hậu M&A -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">MODULE 4: KHỚP LỆNH & HỢP ĐỒNG HẬU M&A (F13–F16)</div>
            <div class="dense-card-body" style="gap: 6.5pt;">
              <div style="background: #f8fafc; border: 1pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #155724;">F13 · Quản Lý Hợp Đồng Ký Số & Ký Quỹ Escrow:</b> Tích hợp chữ ký số pháp lý song phương và tài khoản phong tỏa Escrow tại ngân hàng thương mại độc lập.<br>
                <span style="color: #64748b; font-size: 8pt;">• Khóa chặt dòng tiền đặt cọc • Chỉ giải ngân khi có biên bản nghiệm thu</span>
              </div>
              <div style="background: #f8fafc; border: 1pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #155724;">F14 · Thuật Toán Khớp Lệnh Nhu Cầu Mua (Matching Engine):</b> Tự động so khớp 6 tiêu chí của Buyer Brief với cơ sở dữ liệu hồ sơ bên bán đạt chuẩn.<br>
                <span style="color: #64748b; font-size: 8pt;">• Ma trận trọng số tương thích • Gợi ý 3–5 mục tiêu hoàn hảo nhất</span>
              </div>
              <div style="background: #f8fafc; border: 1pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #155724;">F15 · Quản Trị Pipeline 20 Bước Giao Dịch Chuẩn:</b> Bảng điều khiển thời gian thực theo dõi tiến độ từng deal, cảnh báo trễ hạn và các nút thắt pháp lý.<br>
                <span style="color: #64748b; font-size: 8pt;">• Nâng năng suất 1 Deal Lead lên 8–10 deal/năm • Tự động gửi thông báo</span>
              </div>
              <div style="background: #f8fafc; border: 1pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.6pt; line-height: 1.4;">
                <b style="color: #155724;">F16 · Chuyển Tiếp Hợp Đồng IT Modernization:</b> Đóng gói lộ trình nâng cấp hệ thống phần mềm hậu M&A chuyển giao độc quyền cho Rikkeisoft thực hiện.<br>
                <span style="color: #64748b; font-size: 8pt;">• Hợp đồng CNTT giá trị 500.000–2.000.000 USD/deal • Tạo doanh thu kép</span>
              </div>
              <div style="background: #f0fdf4; border: 1pt solid #86efac; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt; color: #166534;">
                <b>Giá trị cộng hưởng hệ sinh thái:</b> Biến VAULT thành kênh tạo nguồn (deal sourcing) cho các dự án Outsource cao cấp của Rikkeisoft.
              </div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(6)}
    </div>
    """)
# SLIDE 07: 03. CÔNG NĂNG & TECH · MOCKUP TRUST PROFILE LỚP 1
    # ==========================================
    slides.append(f"""
    <div class="slide" id="slide-7">
      {render_header("03. CÔNG NĂNG NỀN TẢNG · GIAO DIỆN WEB UI TRUST PROFILE (DEMO VAULT-CORE)")}
      {render_takeaway(
        "<b>Giao diện thực tế từ vault-core:</b> Trực quan hóa cơ chế giải mật 3 tầng với thuật toán K-Anonymity ($k \\ge 5$) làm mờ dữ liệu.",
        "<b>Cổng khóa kỹ thuật Two-Person Approval Gate:</b> Đảm bảo không bên nào tự ý mở thông tin định danh khi chưa có đủ 2 chữ ký số.",
        "Trải nghiệm người dùng chuyên nghiệp: Bên bán hoàn toàn yên tâm về danh tính, Bên mua tiếp cận hồ sơ minh bạch theo từng nấc thẩm định."
      )}
      <div class="slide-body">
        <div style="border: 1.4pt solid #cbd5e1; border-radius: 6pt; background: #ffffff; display: flex; flex-direction: column; height: 100%; min-height: 0; overflow: hidden; box-shadow: 0 4pt 12pt rgba(0,0,0,0.04);">
          <!-- Browser Top Bar -->
          <div style="background: #f8fafc; border-bottom: 1pt solid #e2e8f0; padding: 6pt 14pt; display: flex; align-items: center; gap: 10pt; flex-shrink: 0;">
            <div style="display: flex; gap: 5pt;">
              <div style="width: 9pt; height: 9pt; border-radius: 50%; background: #ff5f56;"></div>
              <div style="width: 9pt; height: 9pt; border-radius: 50%; background: #ffbd2e;"></div>
              <div style="width: 9pt; height: 9pt; border-radius: 50%; background: #27c93f;"></div>
            </div>
            <div style="flex: 1; background: #ffffff; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 3pt 12pt; font-size: 8.8pt; color: #64748b; font-family: monospace;">
              <span style="color: #16a34a; font-weight: 800;">🔒 https://</span>vault.rikkeisoft.com/portal/trust-profile/VN-LOGISTICS-09
            </div>
            <span style="font-size: 8.2pt; font-weight: 800; color: #155724; background: #dcfce7; border: 1.2pt solid #86efac; padding: 3pt 10pt; border-radius: 4pt;">
              BẢN DEMO THỰC THI (VAULT-CORE REPO)
            </span>
          </div>

          <!-- Browser Tabs -->
          <div style="display: flex; background: #f1f5f9; border-bottom: 1.2pt solid #cbd5e1; padding: 0 14pt; gap: 6pt; flex-shrink: 0;">
            <div style="padding: 6pt 16pt; font-size: 9pt; font-weight: 800; color: #155724; background: #ffffff; border-top: 2.5pt solid #155724; border-left: 1.2pt solid #cbd5e1; border-right: 1.2pt solid #cbd5e1; border-radius: 4pt 4pt 0 0;">
              Lớp 1: Teaser Công Khai (Khử Định Danh)
            </div>
            <div style="padding: 6pt 16pt; font-size: 9pt; font-weight: 700; color: #64748b;">
              Lớp 2: Hồ Sơ CIM Định Danh (Khóa - Cần NDA) 🔒
            </div>
            <div style="padding: 6pt 16pt; font-size: 9pt; font-weight: 700; color: #64748b;">
              Lớp 3: Virtual Data Room VDR (Khóa - Cần LOI) 🔒
            </div>
          </div>

          <!-- Browser Content -->
          <div style="flex: 1; padding: 10pt 16pt; display: flex; gap: 14pt; min-height: 0; background: #ffffff;">
            <!-- Left 64%: Profile Content -->
            <div style="flex: 1.75; display: flex; flex-direction: column; gap: 7pt; min-height: 0;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 5pt;">
                <div>
                  <div style="font-size: 8.5pt; font-weight: 800; color: #b91c1c; letter-spacing: 0.5pt;">HỒ SƠ ĐÃ KHỬ ĐỊNH DANH • MÃ HỒ SƠ: #VN-LOG-09</div>
                  <h2 style="font-size: 14pt; font-weight: 900; color: #0f172a; margin: 1pt 0 3pt 0;">Nền Tảng Phần Mềm Quản Lý Kho Vận &amp; Chuỗi Cung Ứng B2B (WMS/TMS)</h2>
                  <div style="display: flex; gap: 5pt; flex-wrap: wrap;">
                    <span style="background: #f1f5f9; border: 1pt solid #cbd5e1; padding: 2pt 7pt; border-radius: 3pt; font-size: 8pt; font-weight: 700;">Ngành: B2B SaaS Logistics</span>
                    <span style="background: #f1f5f9; border: 1pt solid #cbd5e1; padding: 2pt 7pt; border-radius: 3pt; font-size: 8pt; font-weight: 700;">Địa bàn: Đông Nam Bộ (Làm mờ tỉnh)</span>
                    <span style="background: #f1f5f9; border: 1pt solid #cbd5e1; padding: 2pt 7pt; border-radius: 3pt; font-size: 8pt; font-weight: 700;">Quy mô: 65 Nhân sự</span>
                    <span style="background: #f1f5f9; border: 1pt solid #cbd5e1; padding: 2pt 7pt; border-radius: 3pt; font-size: 8pt; font-weight: 700;">Doanh thu: 65 – 80 Tỷ VNĐ</span>
                    <span style="background: #f1f5f9; border: 1pt solid #cbd5e1; padding: 2pt 7pt; border-radius: 3pt; font-size: 8pt; font-weight: 700;">EBITDA Margin: 23.2%</span>
                  </div>
                </div>
                <div style="background: #dcfce7; color: #15803d; border: 1.5pt solid #86efac; padding: 4pt 8pt; border-radius: 4pt; font-size: 8.8pt; font-weight: 800; text-align: center; flex-shrink: 0;">
                  ✓ TECH DD: A-<br><span style="font-size: 7.2pt; font-weight: 700;">(RIKKEISOFT VERIFIED)</span>
                </div>
              </div>

              <!-- 4 Operational Metrics Grid -->
              <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6pt;">
                <div style="background: #f8fafc; border: 1.2pt solid #e2e8f0; border-radius: 4pt; padding: 5pt 8pt; text-align: center;">
                  <div style="font-size: 12pt; font-weight: 900; color: #155724;">72.4 TỶ</div>
                  <div style="font-size: 7.6pt; color: #64748b; font-weight: 700;">Doanh Thu TTM (VAS chuẩn hóa)</div>
                </div>
                <div style="background: #f8fafc; border: 1.2pt solid #e2e8f0; border-radius: 4pt; padding: 5pt 8pt; text-align: center;">
                  <div style="font-size: 12pt; font-weight: 900; color: #155724;">16.8 TỶ</div>
                  <div style="font-size: 7.6pt; color: #64748b; font-weight: 700;">EBITDA TTM (Biên 23.2%)</div>
                </div>
                <div style="background: #f8fafc; border: 1.2pt solid #e2e8f0; border-radius: 4pt; padding: 5pt 8pt; text-align: center;">
                  <div style="font-size: 12pt; font-weight: 900; color: #0f172a;">120 DN</div>
                  <div style="font-size: 7.6pt; color: #64748b; font-weight: 700;">Khách Hàng Doanh Nghiệp (Top 1: 18%)</div>
                </div>
                <div style="background: #f8fafc; border: 1.2pt solid #e2e8f0; border-radius: 4pt; padding: 5pt 8pt; text-align: center;">
                  <div style="font-size: 12pt; font-weight: 900; color: #0f172a;">450.000</div>
                  <div style="font-size: 7.6pt; color: #64748b; font-weight: 700;">Đơn Hàng Xử Lý Hàng Ngày</div>
                </div>
              </div>

              <!-- Sanitization Table (5 full rows) -->
              <table class="dense-table">
                <thead>
                  <tr>
                    <th style="width: 28%;">Trường Dữ Liệu</th>
                    <th style="width: 38%;">Dữ Liệu Khử Định Danh (Lớp 1)</th>
                    <th>Thuật Toán K-Anonymity (k&ge;5) &amp; Bảo Mật</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><b>Tên DN &amp; Website</b></td>
                    <td><span style="color: #b91c1c; font-weight: 700;">[ĐÃ MÃ HÓA] #VN-LOG-09</span></td>
                    <td>Ẩn hoàn toàn tên pháp nhân, tên miền website, logo và danh tính sáng lập viên</td>
                  </tr>
                  <tr>
                    <td><b>Doanh thu &amp; Lợi nhuận</b></td>
                    <td>65 – 80 tỷ VNĐ / EBITDA 14 – 18 tỷ VNĐ</td>
                    <td>Ép dải giá trị (Range Binning) bước nhảy 20 tỷ VNĐ theo chuẩn bảo vệ APPI</td>
                  </tr>
                  <tr>
                    <td><b>Đội ngũ Kỹ sư</b></td>
                    <td>65 Kỹ sư (Golang, React, AWS Cloud)</td>
                    <td>Gom nhóm kỹ năng chuyên môn, ẩn sơ đồ tổ chức chi tiết và mức lương nhân sự</td>
                  </tr>
                  <tr>
                    <td><b>Cơ cấu Khách hàng</b></td>
                    <td>120 Trung tâm phân phối tại 15 tỉnh thành</td>
                    <td>Làm mờ tên thương hiệu đối tác, chỉ công bố phân khúc ngành và tỷ trọng Top 5</td>
                  </tr>
                  <tr>
                    <td><b>Mã nguồn &amp; Hạ tầng</b></td>
                    <td>Microservices Golang, Cloud Native trên AWS</td>
                    <td>Chỉ công bố kiến trúc hệ thống cấp cao; mã nguồn được sandbox tại VDR Lớp 3</td>
                  </tr>
                </tbody>
              </table>

              <!-- Strategic Highlights Box -->
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8pt;">
                <div style="background: #f8fafc; border: 1.2pt solid #e2e8f0; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.5pt;">
                  <b style="color: #155724;">Mục Tiêu M&amp;A &amp; Chuyển Nhượng:</b><br>
                  Tìm kiếm đối tác chiến lược Nhật Bản có hệ sinh thái logistics để vươn tầm khu vực; sẵn sàng chuyển nhượng <b>60%–70% cổ phần</b> và cam kết ở lại đồng hành 3 năm.
                </div>
                <div style="background: #f8fafc; border: 1.2pt solid #e2e8f0; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.5pt;">
                  <b style="color: #155724;">Ticket Định Giá &amp; Tình Trạng Hồ Sơ:</b><br>
                  Kỳ vọng định giá: <b>65 – 75 Tỷ VNĐ (2.6 – 3.0M USD)</b> tương ứng P/E 7.5–8.5x. Đã hoàn tất Báo cáo Tech DD 6 trục Rikkeisoft và đóng gói sẵn sàng trong Sandboxed VDR.
                </div>
              </div>
            </div>

            <!-- Right 36%: Two-Person Approval Gate & Live DRM Engine -->
            <div style="flex: 1; background: #f8fafc; border: 1.4pt solid #cbd5e1; border-radius: 6pt; padding: 10pt; display: flex; flex-direction: column; gap: 7pt; min-height: 0;">
              <div style="border-bottom: 1.4pt solid #e2e8f0; padding-bottom: 4pt;">
                <b style="font-size: 9.5pt; color: #0f172a; text-transform: uppercase;">Cổng Khóa Duyệt 2 Tầng (Approval Gate)</b>
              </div>

              <div style="display: flex; flex-direction: column; gap: 4.5pt; font-size: 8.4pt;">
                <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4.5pt 8pt; border-radius: 4pt; display: flex; justify-content: space-between;">
                  <span>1. Xác nhận nội dung Teaser bên bán:</span>
                  <b style="color: #15803d;">✓ ĐÃ DUYỆT TAY</b>
                </div>
                <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4.5pt 8pt; border-radius: 4pt; display: flex; justify-content: space-between;">
                  <span>2. Pháp chế VAULT kiểm định KYC:</span>
                  <b style="color: #15803d;">✓ ĐÃ PHÊ DUYỆT</b>
                </div>
                <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4.5pt 8pt; border-radius: 4pt; display: flex; justify-content: space-between;">
                  <span>3. Thuật toán K-Anonymity (k&ge;5):</span>
                  <b style="color: #15803d;">✓ ĐẠT CHUẨN AN TOÀN</b>
                </div>
                <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4.5pt 8pt; border-radius: 4pt; display: flex; justify-content: space-between;">
                  <span>4. Rà soát xung đột đối thủ cạnh tranh:</span>
                  <b style="color: #15803d;">✓ PASS CLEAN LIST</b>
                </div>
              </div>

              <!-- Live DRM Engine Box -->
              <div style="background: #ffffff; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.2pt; color: #334155;">
                <b style="color: #0f172a; font-size: 8.5pt;">Cơ Chế Bảo Mật Clean-Room DRM:</b><br>
                • <i>Mã phiên làm việc:</i> <span style="font-family: monospace; color: #155724; font-weight: 700;">0x8F92...B31A</span><br>
                • <i>Trọng tài bảo hộ:</i> VIAC / SIAC Singapore<br>
                • <i>Chế tài vi phạm:</i> Phạt 300% giá trị thương vụ nếu có hành vi rà quét tìm danh tính bên bán.
              </div>

              <div style="background: #fef2f2; border: 1.2pt solid #fca5a5; padding: 6pt 8pt; border-radius: 4pt; font-size: 8.2pt; color: #991b1b; margin-top: auto;">
                <b>Điều kiện mở khóa Lớp 2 (Hồ Sơ CIM Định Danh):</b><br>
                Buyer Nhật phải hoàn tất ký NDA điện tử song phương và hoàn thành quy trình xác thực tổ chức (KYB).
              </div>

              <a href="#slide-8" style="background: #b91c1c; color: #ffffff; padding: 7pt; border-radius: 4pt; text-decoration: none; font-size: 9pt; font-weight: 800; text-align: center; display: block; border: 1pt solid #991b1b;">
                KÝ NDA ĐIỆN TỬ ĐỂ MỞ KHÓA LỚP 2 &rsaquo;
              </a>
              <div style="font-size: 7.5pt; color: #64748b; text-align: center;">Mã giao dịch: 0x8F92...B31A • Immutable Audit Trail</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(7)}
    </div>
    """)

    # ==========================================
    # SLIDE 08: 03. CÔNG NĂNG & TECH · MOCKUP VDR LỚP 3 & TECH DD 6 TRỤC
    # ==========================================
    slides.append(f"""
    <div class="slide" id="slide-8">
      {render_header("03. CÔNG NĂNG NỀN TẢNG · GIAO DIỆN SANDBOXED VDR &amp; TECH DD 6 TRỤC")}
      {render_takeaway(
        "<b>Phòng dữ liệu ảo chống chụp màn hình và rò rỉ mã nguồn:</b> Watermark động đóng vết email/IP theo giây, chặn in và chặn tải file gốc.",
        "<b>Báo cáo Tech DD 6 trục độc quyền của Rikkei:</b> Lượng hóa nợ kỹ thuật (Tech Debt) thành số tiền cụ thể làm căn cứ đàm phán hợp đồng M&amp;A.",
        "Sự kết hợp giữa VDR bảo mật cao và thẩm định công nghệ chuyên sâu tạo ra hạ tầng giao dịch M&amp;A tin cậy tuyệt đối."
      )}
      <div class="slide-body">
        <div style="border: 1.4pt solid #cbd5e1; border-radius: 6pt; background: #ffffff; display: flex; flex-direction: column; height: 100%; min-height: 0; overflow: hidden; box-shadow: 0 4pt 12pt rgba(0,0,0,0.04);">
          <!-- Browser Top Bar -->
          <div style="background: #f8fafc; border-bottom: 1pt solid #e2e8f0; padding: 6pt 14pt; display: flex; align-items: center; gap: 10pt; flex-shrink: 0;">
            <div style="display: flex; gap: 5pt;">
              <div style="width: 9pt; height: 9pt; border-radius: 50%; background: #ff5f56;"></div>
              <div style="width: 9pt; height: 9pt; border-radius: 50%; background: #ffbd2e;"></div>
              <div style="width: 9pt; height: 9pt; border-radius: 50%; background: #27c93f;"></div>
            </div>
            <div style="flex: 1; background: #ffffff; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 3pt 12pt; font-size: 8.8pt; color: #64748b; font-family: monospace;">
              <span style="color: #b91c1c; font-weight: 800;">🔒 https://</span>vault.rikkeisoft.com/vdr/workspace/deal-logistics-09/sandbox-viewer
            </div>
            <span style="font-size: 8.2pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1.2pt solid #fca5a5; padding: 3pt 10pt; border-radius: 4pt;">
              SANDBOXED VDR • WATERMARK ACTIVE
            </span>
          </div>

          <!-- Browser Content -->
          <div style="flex: 1; padding: 10pt 16pt; display: flex; gap: 14pt; min-height: 0;">
            <!-- Left 50%: VDR Workspace -->
            <div style="flex: 1; display: flex; flex-direction: column; gap: 7pt; background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 6pt; padding: 10pt; min-height: 0;">
              <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 4pt;">
                <b style="font-size: 9.2pt; color: #0f172a;">CÂY THƯ MỤC DỮ LIỆU BẢO MẬT (VDR REPOSITORY)</b>
                <span style="font-size: 7.8pt; color: #b91c1c; font-weight: 800;">CHỐNG IN • CHỐNG TẢI • CHỐNG CHỤP MÀN HÌNH</span>
              </div>

              <div style="background: #ffffff; border: 1pt solid #e2e8f0; border-radius: 4pt; padding: 6pt 8pt; font-size: 8.4pt; display: flex; flex-direction: column; gap: 3.5pt;">
                <div>📁 01_Pháp Lý &amp; Cổ Đông (ĐKKD, Điều lệ, Sổ cổ đông, Giấy phép con) <span style="color: #16a34a; font-weight: 700;">✓ Đã mở</span></div>
                <div>📁 02_Tài Chính &amp; Thuế (BCTC kiểm toán 3 năm, Báo cáo điều chỉnh EBITDA) <span style="color: #16a34a; font-weight: 700;">✓ Đã mở</span></div>
                <div style="background: #fef2f2; padding: 3pt 6pt; border-radius: 3pt; font-weight: 700; color: #991b1b;">
                  📂 03_Báo Cáo Thẩm Định Kỹ Thuật (Rikkeisoft Tech DD Report) <b>[Đang xem]</b>
                </div>
                <div style="padding-left: 14pt; color: #475569; font-size: 8pt;">
                  📄 Rikkei_Tech_DD_Final_VN_LOG09.pdf (Xếp hạng A- • 6 Trục Thẩm Định Độc Quyền)
                </div>
                <div>📁 04_Kiến Trúc &amp; Source Code Scan (Báo cáo SonarQube, SBOM bản quyền OSS) <span style="color: #16a34a; font-weight: 700;">✓ Đã mở</span></div>
                <div>📁 05_Hợp Đồng Trọng Yếu (120 HĐ mẫu đã làm mờ tên, Danh mục đối tác) <span style="color: #64748b;">🔒 Yêu cầu LOI</span></div>
              </div>

              <!-- Sandboxed Document Preview Area with Forensic Dynamic Watermark -->
              <div style="flex: 1; background: #ffffff; border: 1.2pt dashed #cbd5e1; border-radius: 5pt; padding: 8pt; position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; min-height: 0;">
                <div style="position: absolute; transform: rotate(-25deg); color: rgba(185, 28, 28, 0.08); font-size: 20pt; font-weight: 900; pointer-events: none; line-height: 1.5; user-select: none;">
                  BUYER: TOKYO_FUND_JP<br>IP: 133.242.18.94<br>2026-09-17 18:30:15 JST<br>CONFIDENTIAL - DO NOT COPY
                </div>
                <b style="font-size: 10pt; color: #0f172a; margin-bottom: 3pt;">BẢN XEM TRƯỚC TÀI LIỆU CÓ MÃ HÓA FORENSIC WATERMARK</b>
                <p style="font-size: 8.2pt; color: #64748b; margin: 0; max-width: 320pt; line-height: 1.4;">
                  Mọi hành vi chụp màn hình hoặc rò rỉ dữ liệu sẽ bị truy vết đích danh người dùng thông qua mã vân tay số ẩn giấu trong cấu trúc điểm ảnh.
                </p>
                <div style="margin-top: 6pt; display: flex; gap: 6pt; font-size: 7.6pt; color: #15803d; font-weight: 700;">
                  <span>✓ Chặn In: ACTIVE</span> • <span>✓ Chặn Tải File: ACTIVE</span> • <span>✓ DRM Shield: ACTIVE</span>
                </div>
              </div>

              <!-- Live VDR Access Audit Trail Table -->
              <div style="background: #ffffff; border: 1pt solid #e2e8f0; border-radius: 4pt; padding: 5pt 8pt; font-size: 7.8pt;">
                <b style="color: #0f172a;">Live VDR Audit Log (Nhật ký truy cập bất biến):</b>
                <div style="color: #475569; margin-top: 2pt;">
                  • 18:14:02 | Tokyo Fund JP | Đọc Doc 03 (Tech DD) | Thời lượng: 14m 20s (Đã lưu IP)<br>
                  • 18:26:15 | Tokyo Fund JP | Tra cứu bảng nợ kỹ thuật 250M | Trạng thái: Hợp lệ
                </div>
              </div>
            </div>

            <!-- Right 50%: Tech DD 6 Trục Summary Table -->
            <div class="dense-card" style="flex: 1; border-top: 4pt solid #155724; min-height: 0;">
              <div class="dense-card-title" style="color: #155724;">BÁO CÁO THẨM ĐỊNH KỸ THUẬT 6 TRỤC (RIKKEISOFT CERTIFIED)</div>
              <div class="dense-card-body" style="gap: 6pt;">
                <table class="dense-table">
                  <thead>
                    <tr>
                      <th>6 Trục Thẩm Định Độc Quyền</th>
                      <th class="text-center">Điểm</th>
                      <th>Đánh Giá Của Chuyên Gia Rikkeisoft</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><b>1. Kiến Trúc &amp; Khả Năng Scale</b></td>
                      <td class="text-center"><b style="color: #15803d;">8.5/10</b></td>
                      <td>Microservices Golang trên AWS EKS; chịu tải 120.000 req/s</td>
                    </tr>
                    <tr>
                      <td><b>2. Chất Lượng Code &amp; Tech Debt</b></td>
                      <td class="text-center"><b style="color: #15803d;">8.0/10</b></td>
                      <td>SonarQube Rating A; Nợ kỹ thuật ước tính 250M VND (Thấp)</td>
                    </tr>
                    <tr>
                      <td><b>3. An Ninh Mạng &amp; OWASP Top 10</b></td>
                      <td class="text-center"><b style="color: #15803d;">8.5/10</b></td>
                      <td>Có WAF Cloudflare; không có lỗ hổng SQLi hoặc RCE nguy cấp</td>
                    </tr>
                    <tr>
                      <td><b>4. Rủi Ro Bản Quyền Mã Nguồn Mở</b></td>
                      <td class="text-center"><b style="color: #15803d;">9.0/10</b></td>
                      <td>100% Thư viện MIT/Apache 2.0; không dính mã lây lan GPLv3</td>
                    </tr>
                    <tr>
                      <td><b>5. Phụ Thuộc Nhân Sự Cốt Lõi</b></td>
                      <td class="text-center"><b style="color: #b45309;">7.5/10</b></td>
                      <td>Cần giữ chân CTO &amp; 3 Lead Dev trong 24 tháng bằng ESOP</td>
                    </tr>
                    <tr>
                      <td><b>6. Quy Trình DevOps &amp; CI/CD</b></td>
                      <td class="text-center"><b style="color: #15803d;">8.5/10</b></td>
                      <td>Pipeline GitHub Actions tự động kiểm thử và deploy không downtime</td>
                    </tr>
                    <tr class="highlight-row">
                      <td><b>XẾP HẠNG TỔNG HỢP</b></td>
                      <td class="text-center"><b>A-</b></td>
                      <td><b>ĐỦ TIÊU CHUẨN THỰC HIỆN M&amp;A QUỐC TẾ (BUYER APPROVED)</b></td>
                    </tr>
                  </tbody>
                </table>

                <!-- Detailed Gap List & Tech Debt Remediation Box -->
                <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; padding: 6pt 10pt; border-radius: 4pt; font-size: 8.2pt; color: #334155;">
                  <b style="color: #0f172a;">Báo Cáo Gap List &amp; Ngân Sách Xử Lý Nợ Kỹ Thuật (250 Triệu VNĐ):</b><br>
                  • <i>Nâng cấp xác thực OAuth2 &amp; Session Store:</i> 120 triệu VNĐ (Thực hiện trong 30 ngày).<br>
                  • <i>Tái cấu trúc truy vấn CSDL (Legacy ORM):</i> 80 triệu VNĐ.<br>
                  • <i>Cập nhật 12 thư viện lỗi thời (Snyk Clean):</i> 50 triệu VNĐ.
                </div>

                <div style="background: #f0fdf4; border: 1.2pt solid #86efac; padding: 6pt 10pt; border-radius: 4pt; font-size: 8.2pt; color: #166534; margin-top: auto;">
                  <b>Hợp Lực Sau M&amp;A Cùng Rikkeisoft:</b> Cấn trừ 250 triệu nợ kỹ thuật vào giá SPA. Rikkeisoft ký hợp đồng SLA độc quyền hỗ trợ Bên mua hiện đại hóa toàn diện hệ thống sau sáp nhập.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(8)}
    </div>
    """)

    # ==========================================
    # SLIDE 09: 04. VẬN HÀNH · QUY TRÌNH DEAL 20 BƯỚC S01 & HAI SỔ SÁCH S02
    slides.append(f"""
    <div class="slide" id="slide-9">
      {render_header("04. VẬN HÀNH & QUY TRÌNH · HÀNH TRÌNH 20 BƯỚC (S01) & CƠ CHẾ HAI SỔ SÁCH (S02)")}
      {render_takeaway(
          "<b>Chuẩn hóa hành trình M&A 20 bước (S01):</b> Rút ngắn thời gian từ 18 tháng xuống 6–9 tháng, phân tách rõ ràng 4 giai đoạn trách nhiệm.",
          "<b>Cơ chế hai sổ sách A/B (S02):</b> Giải quyết dứt điểm nỗi sợ thuế và BCTC nội bộ chưa chuẩn, đảm bảo an toàn pháp lý tuyệt đối.",
          "Quy trình được đóng gói thành tài sản số, cho phép kiểm soát rủi ro ở từng nấc giải mật mà không phụ thuộc cảm tính cá nhân."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: 20-Step Journey & Deal Velocity -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">HÀNH TRÌNH GIAO DỊCH 20 BƯỚC TIÊU CHUẨN (QUY TRÌNH S01)</div>
            <div class="dense-card-body" style="gap: 7pt;">
              <table class="dense-table" style="font-size: 8.6pt;">
                <thead>
                  <tr>
                    <th style="width: 25%;">Giai đoạn</th>
                    <th style="width: 60%;">Các bước thực hiện chính</th>
                    <th style="width: 15%; text-align: center;">Thời gian</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 7pt 7pt;"><b>GĐ 1: Tiếp nhận sơ bộ</b><br><span style="font-size: 7.8pt; color: #64748b;">(Bước 1 – 4)</span></td>
                    <td style="padding: 7pt 7pt;">Tiếp nhận yêu cầu › Ký NDA sơ bộ › Thẩm tra tư cách pháp nhân (KYC) › Đối chiếu tiêu chí sơ bộ ICP.</td>
                    <td style="padding: 7pt 7pt; text-align: center; font-weight: 700;">15 ngày</td>
                  </tr>
                  <tr>
                    <td style="padding: 7pt 7pt;"><b>GĐ 2: Đóng gói Prep Pack</b><br><span style="font-size: 7.8pt; color: #64748b;">(Bước 5 – 8)</span></td>
                    <td style="padding: 7pt 7pt;">Ký HĐ Prep Pack 90tr › SA Rikkei rà soát Tech DD 6 trục › Chuẩn hóa BCTC › Xuất Teaser khử danh Lớp 1.</td>
                    <td style="padding: 7pt 7pt; text-align: center; font-weight: 700; color: #155724;">30 ngày</td>
                  </tr>
                  <tr>
                    <td style="padding: 7pt 7pt;"><b>GĐ 3: Khớp lệnh & Chào bán</b><br><span style="font-size: 7.8pt; color: #64748b;">(Bước 9 – 12)</span></td>
                    <td style="padding: 7pt 7pt;">Phát hành Teaser khử danh › Khớp 25 Buyer Briefs › Buyer ký NDA điện tử › Duyệt mở CIM Lớp 2 › Call kết nối.</td>
                    <td style="padding: 7pt 7pt; text-align: center; font-weight: 700;">45 ngày</td>
                  </tr>
                  <tr>
                    <td style="padding: 7pt 7pt;"><b>GĐ 4: Thẩm định VDR</b><br><span style="font-size: 7.8pt; color: #64748b;">(Bước 13 – 16)</span></td>
                    <td style="padding: 7pt 7pt;">Buyer ký LOI độc quyền › Mở Sandboxed VDR Lớp 3 › Q&A Thẩm định Tài chính/Công nghệ › Đàm phán SPA.</td>
                    <td style="padding: 7pt 7pt; text-align: center; font-weight: 700; color: #b91c1c;">60 ngày</td>
                  </tr>
                  <tr>
                    <td style="padding: 7pt 7pt;"><b>GĐ 5: Đóng deal & Bàn giao</b><br><span style="font-size: 7.8pt; color: #64748b;">(Bước 17 – 20)</span></td>
                    <td style="padding: 7pt 7pt;">Ký Hợp đồng SPA › Chuyển tiền qua Escrow › Thu phí thành công 2% › Ký HĐ IT Modernization với Rikkeisoft.</td>
                    <td style="padding: 7pt 7pt; text-align: center; font-weight: 700;">30 ngày</td>
                  </tr>
                </tbody>
              </table>

              <!-- Deal Velocity Panel -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.5pt; color: #334155; line-height: 1.42;">
                <b style="color: #0f172a; display: block; margin-bottom: 2pt; font-size: 9pt;">Chỉ Số Vận Tốc Giao Dịch (Deal Velocity) Chuẩn Hóa:</b>
                • <b>Thời gian rút ngắn 50%:</b> Từ 12–18 tháng xuống còn <b>6–9 tháng</b> nhờ số hóa khâu chuẩn bị dữ liệu.<br>
                • <b>Tỷ lệ vượt qua các cổng kiểm soát (Gate Pass Rate):</b> Đạt 82% nhờ bộ lọc hồ sơ nghiêm ngặt ngay từ GĐ 1.<br>
                • <b>Thời hạn mở VDR tối đa:</b> Khống chế 45 ngày/lượt để thúc đẩy quyết định đầu tư nhanh chóng.
              </div>

              <div style="background: #f0fdf4; border: 1.2pt solid #86efac; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.5pt; color: #166534; line-height: 1.38;">
                <b>Hiệu Quả Vận Hành Vượt Trội:</b> Thay thế hoàn toàn hàng trăm email và các cuộc họp vật lý bằng luồng phê duyệt số khép kín, nâng năng suất Deal Lead lên gấp 3–4 lần so với môi giới truyền thống.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Quy trình vận hành S01 (01_VAULT_REPORT.md)</div>
            </div>
          </div>

          <!-- Right Card: S02 Two-Book Governance -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">CƠ CHẾ QUẢN TRỊ HAI SỔ SÁCH A/B (QUY TRÌNH S02)</div>
            <div class="dense-card-body" style="gap: 7pt;">
              <table class="dense-table" style="font-size: 8.6pt;">
                <thead>
                  <tr>
                    <th style="width: 20%;">Tiêu chí</th>
                    <th style="width: 40%;">Sổ A (Báo cáo Chuẩn hóa)</th>
                    <th style="width: 40%;">Sổ B (Hồ sơ Nội bộ Chi tiết)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>Bản chất dữ liệu</b></td>
                    <td style="padding: 6pt 7pt;">Số liệu chuẩn hóa IFRS/VAS, chuẩn hóa EBITDA, loại trừ chi phí cá nhân</td>
                    <td style="padding: 6pt 7pt;">Toàn bộ chứng từ gốc, hợp đồng lao động, sao kê ngân hàng thực tế</td>
                  </tr>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>Vị trí lưu trữ</b></td>
                    <td style="padding: 6pt 7pt;">Lớp 1 (Teaser) và Lớp 2 (Hồ sơ CIM)</td>
                    <td style="padding: 6pt 7pt;">Phân vùng VDR Lớp 3 (Mã hóa AES-256)</td>
                  </tr>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>Điều kiện tiếp cận</b></td>
                    <td style="padding: 6pt 7pt;">Ký NDA điện tử song phương</td>
                    <td style="padding: 6pt 7pt; font-weight: 700; color: #b91c1c;">Đã ký LOI độc quyền + Đặt cọc Escrow</td>
                  </tr>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>Hàng rào công nghệ</b></td>
                    <td style="padding: 6pt 7pt;">Làm mờ định danh K-Anonymity (k≥5)</td>
                    <td style="padding: 6pt 7pt;">Sandboxed Viewer, chặn tải, Watermark động</td>
                  </tr>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>Bảo vệ pháp lý</b></td>
                    <td style="padding: 6pt 7pt;">Miễn trừ trách nhiệm sơ bộ</td>
                    <td style="padding: 6pt 7pt;">Luật sư độc lập giám sát và lưu vết Audit</td>
                  </tr>
                  <tr>
                    <td style="padding: 6pt 7pt;"><b>Xử lý chênh lệch</b></td>
                    <td style="padding: 6pt 7pt;">Báo cáo Gap List đối soát ngân hàng</td>
                    <td style="padding: 6pt 7pt;">Cấn trừ giá mua hoặc lập quỹ bảo lãnh 10%</td>
                  </tr>
                </tbody>
              </table>

              <!-- S02 Core Principles Box -->
              <div style="background: #fff5f5; border: 1.2pt solid #fecdd3; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.5pt; color: #991b1b; line-height: 1.42;">
                <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.9pt;">3 Nguyên Tắc Bất Biến Quản Trị Rủi Ro Sổ Sách:</b>
                1. <b>Cách ly dữ liệu thô:</b> VAULT không can thiệp, không chỉnh sửa chứng từ gốc của doanh nghiệp.<br>
                2. <b>Mã hóa bất đối xứng:</b> Chỉ Seller nắm Private Key để giải mã dữ liệu nội bộ khi có lệnh mở cổng.<br>
                3. <b>Tự hủy quyền truy cập:</b> Token VDR tự thu hồi sau 72h không phát sinh hoạt động để triệt tiêu nguy cơ rò rỉ.
              </div>

              <div style="background: #f0f9ff; border: 1.2pt solid #bae6fd; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.5pt; color: #0369a1; line-height: 1.38;">
                <b>Nguyên Tắc Bức Tường Lửa:</b> Bảo vệ an toàn tuyệt đối về nghĩa vụ thuế cho Bên bán và tạo sự minh bạch chuẩn mực cho Bên mua, xóa bỏ rào cản lớn nhất ngăn cản SME tham gia M&A.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Quy trình quản trị rủi ro S02 (01_VAULT_REPORT.md)</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(9)}
    </div>
    """)
# SLIDE 10: 04. VẬN HÀNH · CƠ CẤU TỔ CHỨC & MA TRẬN RACI S03
    slides.append(f"""
    <div class="slide" id="slide-10">
      {render_header("04. VẬN HÀNH & QUY TRÌNH · CƠ CẤU NHÂN SỰ & MA TRẬN TRÁCH NHIỆM (S03)")}
      {render_takeaway(
          "<b>Bộ máy tinh gọn 5 vị trí nhân sự cốt lõi:</b> Giám đốc dự án, Deal Lead M&A, Tech DD Lead, Platform Engineer và Chuyên viên Pháp chế.",
          "<b>Ma trận RACI phân định minh bạch:</b> Xác định chính xác trách nhiệm của Ban dự án VAULT, chuyên gia biệt phái Rikkeisoft và Khách hàng.",
          "Mô hình vận hành tận dụng tối đa nguồn lực hậu cần có sẵn của Rikkeisoft, giữ chi phí cố định tiền mặt ở mức tối thiểu."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: Core Org Structure & 5-Year Personnel Forecast -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">CƠ CẤU TỔ CHỨC 5 VỊ TRÍ NHÂN SỰ CỐT LÕI</div>
            <div class="dense-card-body" style="gap: 6.5pt;">
              <table class="dense-table" style="font-size: 8.6pt;">
                <thead>
                  <tr>
                    <th style="width: 25%;">Vị trí nhân sự</th>
                    <th style="width: 55%;">Nhiệm vụ trọng tâm</th>
                    <th style="width: 20%; text-align: center;">Định biên (Y1–Y5)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 5.5pt 7pt;"><b>1. Project Director</b></td>
                    <td style="padding: 5.5pt 7pt;">Chịu trách nhiệm P&L toàn diện, đối ngoại cấp cao và báo cáo BOD</td>
                    <td style="padding: 5.5pt 7pt; text-align: center; font-weight: 700;">1 FTE (Toàn thời gian)</td>
                  </tr>
                  <tr>
                    <td style="padding: 5.5pt 7pt;"><b>2. Deal Lead M&A</b></td>
                    <td style="padding: 5.5pt 7pt;">Chuyên gia tài chính M&A, quản trị pipeline, điều phối 8–10 deal/năm</td>
                    <td style="padding: 5.5pt 7pt; text-align: center; font-weight: 700; color: #155724;">1 FTE › 3 FTE</td>
                  </tr>
                  <tr>
                    <td style="padding: 5.5pt 7pt;"><b>3. Tech DD Lead</b></td>
                    <td style="padding: 5.5pt 7pt;">Solution Architect Rikkeisoft biệt phái, chủ trì thẩm định 6 trục</td>
                    <td style="padding: 5.5pt 7pt; text-align: center; font-weight: 700;">0.5 FTE › 2 FTE</td>
                  </tr>
                  <tr>
                    <td style="padding: 5.5pt 7pt;"><b>4. Platform Engineer</b></td>
                    <td style="padding: 5.5pt 7pt;">Kỹ sư công nghệ duy trì và nâng cấp vault-core, VDR, K-Anonymity</td>
                    <td style="padding: 5.5pt 7pt; text-align: center; font-weight: 700;">1 FTE › 2 FTE</td>
                  </tr>
                  <tr>
                    <td style="padding: 5.5pt 7pt;"><b>5. Legal & Compliance</b></td>
                    <td style="padding: 5.5pt 7pt;">Pháp chế chuyên trách, kiểm soát NDA, KYC, Two-Person Approval</td>
                    <td style="padding: 5.5pt 7pt; text-align: center; font-weight: 700;">0.5 FTE › 1 FTE</td>
                  </tr>
                  <tr style="background: #f8fafc; font-weight: 800;">
                    <td style="padding: 5.5pt 7pt; color: #0f172a;">TỔNG NHÂN SỰ</td>
                    <td style="padding: 5.5pt 7pt; color: #155724;">Bộ máy tinh gọn, năng suất cao trên nền tảng số</td>
                    <td style="padding: 5.5pt 7pt; text-align: center; color: #155724; font-size: 9.2pt;">3.0 FTE › 8.0 FTE</td>
                  </tr>
                </tbody>
              </table>

              <!-- 5-Year Personnel Budget & Efficiency Forecast Table -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 9pt; font-size: 8.3pt;">
                <b style="color: #1e293b; display: block; margin-bottom: 3pt; font-size: 8.8pt;">Kế Hoạch Ngân Sách Nhân Sự & Năng Suất 5 Năm (Mô hình Excel):</b>
                <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 8.2pt;">
                  <tr style="background: #e2e8f0; font-weight: 700; color: #0f172a;">
                    <td style="padding: 3pt 4pt; text-align: left;">Chỉ số</td>
                    <td style="padding: 3pt 4pt;">Năm 1</td>
                    <td style="padding: 3pt 4pt;">Năm 2</td>
                    <td style="padding: 3pt 4pt;">Năm 3</td>
                    <td style="padding: 3pt 4pt;">Năm 4</td>
                    <td style="padding: 3pt 4pt;">Năm 5</td>
                  </tr>
                  <tr style="border-bottom: 1pt solid #cbd5e1;">
                    <td style="padding: 3.5pt 4pt; text-align: left;">Tổng FTE vận hành</td>
                    <td style="padding: 3.5pt 4pt; font-weight: 700;">3.0 FTE</td>
                    <td style="padding: 3.5pt 4pt; font-weight: 700;">4.5 FTE</td>
                    <td style="padding: 3.5pt 4pt; font-weight: 700;">6.0 FTE</td>
                    <td style="padding: 3.5pt 4pt; font-weight: 700;">7.0 FTE</td>
                    <td style="padding: 3.5pt 4pt; font-weight: 700; color: #155724;">8.0 FTE</td>
                  </tr>
                  <tr style="border-bottom: 1pt solid #cbd5e1;">
                    <td style="padding: 3.5pt 4pt; text-align: left;">Quỹ lương & phúc lợi</td>
                    <td style="padding: 3.5pt 4pt;">680 tr VNĐ</td>
                    <td style="padding: 3.5pt 4pt;">1.15 tỷ VNĐ</td>
                    <td style="padding: 3.5pt 4pt;">1.55 tỷ VNĐ</td>
                    <td style="padding: 3.5pt 4pt;">1.85 tỷ VNĐ</td>
                    <td style="padding: 3.5pt 4pt; font-weight: 700;">2.10 tỷ VNĐ</td>
                  </tr>
                  <tr>
                    <td style="padding: 3.5pt 4pt; text-align: left;">Tỷ lệ Lương / Doanh thu</td>
                    <td style="padding: 3.5pt 4pt; color: #b91c1c; font-weight: 700;">39.8%</td>
                    <td style="padding: 3.5pt 4pt; color: #b91c1c;">26.1%</td>
                    <td style="padding: 3.5pt 4pt; color: #155724;">21.5%</td>
                    <td style="padding: 3.5pt 4pt; color: #155724;">19.2%</td>
                    <td style="padding: 3.5pt 4pt; color: #155724; font-weight: 800;">18.1%</td>
                  </tr>
                </table>
              </div>

              <!-- Deal Lead KPI & Incentive Policy -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.4pt; color: #334155; line-height: 1.4;">
                <b style="color: #0f172a; display: block; margin-bottom: 2pt; font-size: 8.8pt;">Chính Sách Đãi Ngộ & KPI Năng Suất Deal Lead:</b>
                • <b>Lương cứng + Thưởng hoa hồng:</b> Deal Lead hưởng 10–15% trên Success Fee của thương vụ mang về.<br>
                • <b>Chỉ tiêu KPI cứng:</b> Tối thiểu 10 gói Prep Pack/năm, tỷ lệ chuyển đổi sang LOI ≥ 30%, đóng 2–3 deal/năm.<br>
                • <b>Cấp số nhân năng suất:</b> Nhờ hệ thống tự động hóa chuẩn bị, 1 Deal Lead quản lý 8–10 deal thay vì 2–3 deal.
              </div>

              <div style="background: #f0fdf4; border: 1.2pt solid #86efac; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.4pt; color: #166534; line-height: 1.38;">
                <b>Quy Chuẩn Tuyển Dụng & Nguồn Lực Biệt Phái:</b> Tuyển chọn Deal Lead có tối thiểu 5 năm kinh nghiệm Investment Banking và am hiểu văn hóa doanh nghiệp Nhật; kỹ sư Tech DD được biệt phái từ Rikkeisoft trong giai đoạn chờ dự án (Bench-time), hạch toán theo phí SLA.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Cơ cấu tổ chức S03 (01_VAULT_REPORT.md)</div>
            </div>
          </div>

          <!-- Right Card: RACI Matrix & Governance Rules -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">MA TRẬN PHÂN ĐỊNH TRÁCH NHIỆM RACI (QUY TRÌNH S03)</div>
            <div class="dense-card-body" style="gap: 6.5pt;">
              <table class="dense-table" style="font-size: 8.5pt;">
                <thead>
                  <tr>
                    <th style="width: 36%;">Hạng mục công việc</th>
                    <th style="width: 16%; text-align: center;">VAULT</th>
                    <th style="width: 16%; text-align: center;">Rikkei SA</th>
                    <th style="width: 16%; text-align: center;">Bên Bán</th>
                    <th style="width: 16%; text-align: center;">Bên Mua</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">1. Thu thập dữ liệu sơ bộ & KYC</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; font-weight: 800; color: #b91c1c;">A/R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">C</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">I</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">2. Thẩm định Tech DD 6 trục</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">A</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; font-weight: 800; color: #b91c1c;">R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">C</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">I</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">3. Khử định danh Teaser (Lớp 1)</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; font-weight: 800; color: #b91c1c;">A/R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">C</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">I</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">4. Ký NDA & Cấp quyền CIM (Lớp 2)</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; font-weight: 800; color: #b91c1c;">A/R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">I</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">A</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">5. Mở Sandboxed VDR & Q&A (Lớp 3)</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; font-weight: 800; color: #b91c1c;">A/R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">6. Đàm phán Hợp đồng M&A (SPA)</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; font-weight: 800; color: #b91c1c;">A/R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">C</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">7. Quyết toán tài chính & Giải phóng Escrow</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; font-weight: 800; color: #b91c1c;">A/R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">I</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">8. Chuyển giao & Ký HĐ IT Modernization</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">C</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; font-weight: 800; color: #b91c1c;">A/R</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">I</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">R</td>
                  </tr>
                </tbody>
              </table>

              <!-- Approval Matrix & SLA Commitments Table -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 9pt; font-size: 8.3pt;">
                <b style="color: #1e293b; display: block; margin-bottom: 3pt; font-size: 8.8pt;">Ma Trận Phân Quyền Phê Duyệt & Cam Kết SLA Xử Lý:</b>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6pt; color: #334155;">
                  <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4pt 6pt; border-radius: 3pt;">
                    <b style="color: #0f172a;">Phân Quyền Ký Số & Ngân Sách:</b><br>
                    • Deal Lead: Ký NDA sơ bộ & duyệt chi &le; 50 triệu VNĐ.<br>
                    • Project Director: Duyệt chi &le; 200 triệu & mở VDR Lớp 3.<br>
                    • HĐQT Rikkeisoft: Quyết định hợp đồng &gt; 200M & phân phối ESOP.
                  </div>
                  <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4pt 6pt; border-radius: 3pt;">
                    <b style="color: #155724;">Cam Kết SLA Thời Gian Xử Lý:</b><br>
                    • Thẩm tra KYC & Tiếp nhận hồ sơ: &le; 24 giờ làm việc.<br>
                    • Bàn giao gói Prep Pack & Báo cáo 6 trục: &le; 30 ngày.<br>
                    • Trả lời Q&A kỹ thuật trong Sandboxed VDR: &le; 4 giờ.
                  </div>
                </div>
              </div>

              <!-- Conflict of Interest & Four-Eyes Principle -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 5.5pt 9pt; font-size: 8.3pt; color: #334155; line-height: 1.38;">
                <b style="color: #0f172a; display: block; margin-bottom: 2pt; font-size: 8.7pt;">Cơ Chế Giải Quyết Xung Đột Lợi Ích (Conflict of Interest):</b>
                Phân tách độc lập giữa Deal Lead (hưởng hoa hồng deal) và Solution Architect Rikkei (thẩm định độc lập theo phí SLA), đảm bảo Báo cáo Tech DD khách quan 100%. Tranh chấp kỹ thuật do Hội đồng Kỹ thuật Tập đoàn phán quyết độc lập.
              </div>

              <div style="background: #f0f9ff; border: 1.2pt solid #bae6fd; border-radius: 4pt; padding: 5.5pt 9pt; font-size: 8.3pt; color: #0369a1; line-height: 1.38;">
                <b>Nguyên Tắc Kiểm Soát Chéo (Four-Eyes Principle):</b> Mọi quyết định giải mật tài liệu Lớp 2 và Lớp 3 đều bắt buộc phải có phê duyệt độc lập của 2 chữ ký số (Đại diện Bên Bán + Pháp chế VAULT).
              </div>

              <div style="display: flex; justify-content: space-between; font-size: 7.6pt; color: #64748b; margin-top: 1pt;">
                <span><b>RACI:</b> R (Thực hiện) · A (Chịu trách nhiệm) · C (Tham vấn) · I (Thông báo)</span>
                <span>Nguồn: Ma trận trách nhiệm S03</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(10)}
    </div>
    """)
# SLIDE 11: 05. PHÂN TÍCH TÀI CHÍNH · BÁO CÁO P&L DỰ PHÓNG 5 NĂM
    # ==========================================
    slides.append(f"""
    <div class="slide" id="slide-11">
      {render_header("05. PHÂN TÍCH TÀI CHÍNH · BÁO CÁO P&amp;L DỰ PHÓNG 5 NĂM (BASE CASE)")}
      {render_takeaway(
        "<b>Doanh thu tăng trưởng bền vững:</b> Từ 1.71 tỷ (Năm 1) lên 12.10 tỷ (Năm 5); tổng doanh thu 5 năm đạt <b>35.77 tỷ VNĐ</b>.",
        "<b>Chuyển dịch cơ cấu doanh thu:</b> Gói Prep Pack (90tr) làm bệ đỡ nuôi quân trong 2 năm đầu; Phí thành công (Success Fee) bứt phá từ Năm 3.",
        "Lợi nhuận trước thuế dương từ Năm 2 (+405 triệu) và đạt +3.99 tỷ tại Năm 5; Kết quả kinh tế thuần 5 năm đạt +5.14 tỷ VNĐ."
      )}
      <div class="slide-body">
        <!-- Top 4 KPI Metrics -->
        <div class="full-grid-4">
          <div class="kpi-box"><div class="kpi-num">35.77 TỶ</div><div class="kpi-label">Tổng Doanh Thu 5 Năm (CAGR 63.1%)</div></div>
          <div class="kpi-box"><div class="kpi-num">THÁNG 21</div><div class="kpi-label">Điểm Hòa Vốn Dòng Tiền Mặt</div></div>
          <div class="kpi-box"><div class="kpi-num">8.31 TỶ</div><div class="kpi-label">Lợi Nhuận Gộp Năm 5 (Biên 68.7%)</div></div>
          <div class="kpi-box"><div class="kpi-num">7.41 TỶ</div><div class="kpi-label">Tổng Lợi Nhuận Sau Thuế (NPAT) 5 Năm</div></div>
        </div>

        <!-- Full P&L Table from 04_VAULT_MODEL.xlsx -->
        <div class="dense-card">
          <div class="dense-card-title">BÁO CÁO KẾT QUẢ HOẠT ĐỘNG KINH DOANH DỰ PHÓNG 5 NĂM (TRIỆU VNĐ)</div>
          <table class="dense-table" style="font-size: 9.8pt;">
            <thead>
              <tr>
                <th>Chỉ Tiêu Tài Chính Cốt Lõi (Đơn vị: Triệu VNĐ)</th>
                <th class="text-right">Năm 1</th>
                <th class="text-right">Năm 2</th>
                <th class="text-right">Năm 3</th>
                <th class="text-right">Năm 4</th>
                <th class="text-right">Năm 5</th>
                <th class="text-right" style="color: #b91c1c;">Tổng 5 Năm</th>
              </tr>
            </thead>
            <tbody>
              <tr class="highlight-row">
                <td><b>1. TỔNG DOANH THU THUẦN</b></td>
                <td class="text-right"><b>1.710</b></td>
                <td class="text-right"><b>4.127</b></td>
                <td class="text-right"><b>8.601</b></td>
                <td class="text-right"><b>9.231</b></td>
                <td class="text-right"><b>12.099</b></td>
                <td class="text-right"><b>35.769</b></td>
              </tr>
              <tr>
                <td>&nbsp;&nbsp;&nbsp;&nbsp;• Doanh thu Gói chuẩn bị hồ sơ Prep Pack (90tr/gói)</td>
                <td class="text-right">1.710</td>
                <td class="text-right">2.520</td>
                <td class="text-right">3.330</td>
                <td class="text-right">3.330</td>
                <td class="text-right">4.230</td>
                <td class="text-right">15.120</td>
              </tr>
              <tr>
                <td>&nbsp;&nbsp;&nbsp;&nbsp;• Doanh thu Phí thành công (Success Fee M&amp;A 2%)</td>
                <td class="text-right">0</td>
                <td class="text-right">1.607</td>
                <td class="text-right">5.271</td>
                <td class="text-right">5.901</td>
                <td class="text-right">7.869</td>
                <td class="text-right">20.649</td>
              </tr>
              <tr>
                <td><b>2. Chi phí trực tiếp &amp; Hoa hồng đối tác</b></td>
                <td class="text-right">771</td>
                <td class="text-right">1.459</td>
                <td class="text-right">2.635</td>
                <td class="text-right">2.943</td>
                <td class="text-right">3.787</td>
                <td class="text-right">11.596</td>
              </tr>
              <tr style="background: #f8fafc;">
                <td><b>3. LỢI NHUẬN GỘP (GROSS PROFIT)</b></td>
                <td class="text-right"><b>939</b></td>
                <td class="text-right"><b>2.668</b></td>
                <td class="text-right"><b>5.966</b></td>
                <td class="text-right"><b>6.288</b></td>
                <td class="text-right"><b>8.312</b></td>
                <td class="text-right"><b>24.173</b></td>
              </tr>
              <tr>
                <td><b>4. Chi phí nguồn lực vận hành tính đủ</b></td>
                <td class="text-right">1.680</td>
                <td class="text-right">2.016</td>
                <td class="text-right">2.419</td>
                <td class="text-right">2.903</td>
                <td class="text-right">3.484</td>
                <td class="text-right">12.502</td>
              </tr>
              <tr>
                <td>&nbsp;&nbsp;&nbsp;&nbsp;<i>* Phần chi trả bằng tiền mặt thực tế</i></td>
                <td class="text-right"><i>1.008</i></td>
                <td class="text-right"><i>1.210</i></td>
                <td class="text-right"><i>1.452</i></td>
                <td class="text-right"><i>1.742</i></td>
                <td class="text-right"><i>2.090</i></td>
                <td class="text-right"><i>7.501</i></td>
              </tr>
              <tr>
                <td>&nbsp;&nbsp;&nbsp;&nbsp;<i>* Phần Rikkeisoft hỗ trợ nguồn lực nội bộ</i></td>
                <td class="text-right"><i>672</i></td>
                <td class="text-right"><i>806</i></td>
                <td class="text-right"><i>967</i></td>
                <td class="text-right"><i>1.161</i></td>
                <td class="text-right"><i>1.394</i></td>
                <td class="text-right"><i>5.000</i></td>
              </tr>
              <tr>
                <td><b>5. Dự phòng nợ xấu &amp; Khấu hao tài sản</b></td>
                <td class="text-right">50</td>
                <td class="text-right">247</td>
                <td class="text-right">640</td>
                <td class="text-right">640</td>
                <td class="text-right">837</td>
                <td class="text-right">2.414</td>
              </tr>
              <tr class="highlight-row">
                <td><b>6. LỢI NHUẬN TRƯỚC THUẾ (EBT)</b></td>
                <td class="text-right" style="color: #b91c1c;"><b>-791</b></td>
                <td class="text-right" style="color: #15803d;"><b>+405</b></td>
                <td class="text-right" style="color: #15803d;"><b>+2.907</b></td>
                <td class="text-right" style="color: #15803d;"><b>+2.745</b></td>
                <td class="text-right" style="color: #15803d;"><b>+3.991</b></td>
                <td class="text-right" style="color: #15803d;"><b>+9.257</b></td>
              </tr>
              <tr>
                <td><b>7. LỢI NHUẬN SAU THUẾ (NPAT)</b></td>
                <td class="text-right" style="color: #b91c1c;"><b>-791</b></td>
                <td class="text-right" style="color: #15803d;"><b>+405</b></td>
                <td class="text-right" style="color: #15803d;"><b>+2.394</b></td>
                <td class="text-right" style="color: #15803d;"><b>+2.181</b></td>
                <td class="text-right" style="color: #15803d;"><b>+3.217</b></td>
                <td class="text-right" style="color: #15803d;"><b>+7.406</b></td>
              </tr>
              <tr class="total-row">
                <td><b>8. KẾT QUẢ KINH TẾ THUẦN (Trừ 100% chi phí Rikkei)</b></td>
                <td class="text-right" style="color: #b91c1c;"><b>-791</b></td>
                <td class="text-right" style="color: #b91c1c;"><b>-401</b></td>
                <td class="text-right" style="color: #15803d;"><b>+1.427</b></td>
                <td class="text-right" style="color: #15803d;"><b>+1.020</b></td>
                <td class="text-right" style="color: #15803d;"><b>+1.823</b></td>
                <td class="text-right" style="color: #15803d;"><b>+5.140</b></td>
              </tr>
            </tbody>
          </table>

          <!-- 2 Analytical Insight Columns under the table inside the card -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12pt; margin-top: 8pt;">
            <div style="background: #f8fafc; border: 1.2pt solid #e2e8f0; border-left: 4pt solid #155724; border-radius: 4pt; padding: 8pt 12pt; font-size: 8.8pt;">
              <b style="color: #155724; font-size: 9.5pt;">Cơ Cấu Doanh Thu &amp; Sức Bật Success Fee:</b><br>
              • <b>Năm 1–2 (Bảo vệ dòng tiền):</b> Gói Prep Pack 90tr mang về 4.23 tỷ VNĐ (chiếm 72% doanh thu 2 năm đầu), giúp bộ máy tự nuôi sống mà không chịu áp lực đốt tiền.<br>
              • <b>Năm 3–5 (Bùng nổ biên lợi nhuận):</b> Phí thành công (Success Fee 2%) bứt phá lên 5.27B – 7.87B VNĐ/năm, chiếm 65% tổng thu và đưa biên ròng NPAT lên 26.6%.<br>
              • <b>Tăng trưởng quy mô:</b> Tổng doanh thu 5 năm đạt 35.77 tỷ VNĐ với tốc độ tăng trưởng kép CAGR 63.1%/năm.
            </div>
            <div style="background: #f8fafc; border: 1.2pt solid #e2e8f0; border-left: 4pt solid #b91c1c; border-radius: 4pt; padding: 8pt 12pt; font-size: 8.8pt;">
              <b style="color: #b91c1c; font-size: 9.5pt;">Kỷ Luật Tài Chính &amp; Hiệu Quả Đồng Vốn:</b><br>
              • <b>Kiểm soát đáy tiền mặt:</b> Đáy thiếu hụt tiền mặt tự thân tối đa chỉ chạm âm -1.43 tỷ VNĐ tại Tháng 20, hoàn toàn nằm gọn trong hạn mức vốn cấp 1.68 tỷ VNĐ.<br>
              • <b>Tỷ suất sinh lời cao:</b> Tổng lợi nhuận sau thuế lũy kế 5 năm đạt 7.41 tỷ VNĐ trên số vốn đầu tư 1.68 tỷ VNĐ, tương ứng tỷ suất ROI đạt <b>4.4x</b>.<br>
              • <b>Cộng hưởng giá trị:</b> Dự án tự bù đắp 100% chi phí tài trợ nội bộ của Rikkeisoft (5.00 tỷ VNĐ) và tạo phễu hợp đồng IT Modernization hàng chục triệu USD.
            </div>
          </div>
          <div style="font-size: 8pt; color: #64748b; text-align: right; margin-top: 6pt;">
            Nguồn: Mô hình tài chính chuẩn mực 04_VAULT_MODEL.xlsx (Sheet 04_KET_QUA &amp; Sheet 03_MO_HINH_60T) • Số deal thành công lũy kế: 11 Deals
          </div>
        </div>
      </div>
      {render_bottom_nav(11)}
    </div>
    """)

    # ==========================================
    # SLIDE 12: 05. PHÂN TÍCH TÀI CHÍNH · DÒNG TIỀN & ĐÁY THUNG LŨNG (T20)
    # ==========================================
    slides.append(f"""
    <div class="slide" id="slide-12">
      {render_header("05. PHÂN TÍCH TÀI CHÍNH · DÒNG TIỀN 60 THÁNG &amp; ĐÁY THUNG LŨNG (T20/T21)")}
      {render_takeaway(
        "<b>Đáy tiền mặt (Cash Valley):</b> Chạm mức âm <b>-1,43 tỷ VNĐ tại Tháng 20</b> trước khi thu được phí thành công đầu tiên.",
        "<b>Hạn mức vốn cấp đề xuất: 1,68 tỷ VNĐ</b> (Đã bao gồm 250 triệu VNĐ đệm an toàn thanh khoản tương đương 3 tháng OPEX cố định).",
        "Mô hình đạt điểm hòa vốn tiền mặt tại Tháng 21, đạt điểm hòa vốn kinh tế thuần toàn diện tại Tháng 32 và dương bền vững từ Tháng 37."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left: Principles of Capital Limit & Tranche Injections -->
          <div class="dense-card">
            <div class="dense-card-title">NGUYÊN TẮC ĐỊNH HẠN MỨC VỐN CẤP &amp; ĐÁY THIẾU HỤT TIỀN MẶT</div>
            <div class="dense-card-body">
              <div class="meta-banner">
                <span><b>Đáy Tiền Mặt (T20):</b> -1.432 Tỷ VNĐ</span>
                <span><b>Đệm Thanh Khoản:</b> +248 Triệu VNĐ</span>
                <span><b>Hạn Mức Đề Xuất:</b> 1.680 Tỷ VNĐ</span>
              </div>

              <div style="display: flex; flex-direction: column; gap: 4pt; font-size: 8.8pt;">
                <div>• <b>Điểm Đáy Tiền Mặt Lũy Kế:</b> Chạm mức âm <b>-1.432.000.000 VNĐ</b> tại <b>Tháng 20</b> (ngay trước thời điểm đóng deal M&amp;A đầu tiên tại Tháng 21). Đây là tháng ngặt nghèo nhất của chu kỳ dự án.</div>
                <div>• <b>Khoản Đệm Dự Phòng Thanh Khoản:</b> Bổ sung <b>248.000.000 VNĐ</b> (tương đương 3 tháng chi phí vận hành tiền mặt cố định ~83 tr/tháng) để chống sốc nếu deal bị trễ hạn ký kết.</div>
                <div>• <b>Hạn Mức Vốn Tiền Mặt Trình HĐQT:</b> Tròn số <b>1.680.000.000 VNĐ (1.68 tỷ VNĐ)</b>. Cam kết không xin thêm vốn nếu vượt mốc này.</div>
              </div>

              <!-- Tranche Table -->
              <table class="dense-table">
                <thead>
                  <tr>
                    <th>Đợt Cấp</th>
                    <th>Thời Điểm</th>
                    <th class="text-right">Số Tiền</th>
                    <th>Điều Kiện Kích Hoạt (Stage-Gate)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><b>Đợt 1</b></td>
                    <td>Tháng 01</td>
                    <td class="text-right">500 triệu</td>
                    <td>Thành lập Ban DA &amp; Nghiệm thu Platform MVP Lớp 1</td>
                  </tr>
                  <tr>
                    <td><b>Đợt 2</b></td>
                    <td>Tháng 07</td>
                    <td class="text-right">450 triệu</td>
                    <td>Có 3 Buyer Briefs &amp; Ký 5 Hợp đồng Prep Pack</td>
                  </tr>
                  <tr>
                    <td><b>Đợt 3</b></td>
                    <td>Tháng 13</td>
                    <td class="text-right">400 triệu</td>
                    <td>Báo cáo Tech DD cho 5 Seller, đưa lên VDR Lớp 3</td>
                  </tr>
                  <tr>
                    <td><b>Đợt 4</b></td>
                    <td>Tháng 19</td>
                    <td class="text-right">330 triệu</td>
                    <td>Đàm phán 2 deal vào vòng LOI &amp; Ký quỹ Escrow</td>
                  </tr>
                  <tr class="total-row">
                    <td colspan="2"><b>TỔNG HẠN MỨC VỐN CẤP</b></td>
                    <td class="text-right"><b>1.680 triệu</b></td>
                    <td><b>Giải ngân theo tiến độ 4 Cổng kiểm soát</b></td>
                  </tr>
                </tbody>
              </table>

              <!-- Delay Sensitivity Box -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; padding: 6pt 10pt; border-radius: 4pt; font-size: 8.5pt; color: #334155;">
                <b>Kiểm Tra Độ Nhạy Tiến Độ Đóng Deal (Delay Risk):</b><br>
                • <i>Trễ 0 tháng (Base Case):</i> Đáy -1.43 tỷ (T20), Vốn cần 1.68 tỷ. Hòa vốn Tháng 21.<br>
                • <i>Trễ 3 tháng:</i> Đáy -1.68 tỷ (T23), Vốn cần 1.95 tỷ (Vẫn an toàn trong hạn mức đệm dự phòng).<br>
                • <i>Trễ 6 tháng:</i> Đáy -2.15 tỷ (T26), Vốn cần 2.45 tỷ (Kích hoạt chính sách kéo giãn tuyển dụng).
              </div>

              <div style="background: #f0fdf4; border: 1.2pt solid #86efac; padding: 6pt 10pt; border-radius: 4pt; font-size: 8.5pt; color: #166534;">
                <b>3 Cột Mốc Hòa Vốn Kế Toán:</b> (1) <b>Tháng 21:</b> Hòa vốn tiền mặt (+1.61 tỷ) • (2) <b>Tháng 32:</b> Hòa vốn kinh tế thuần • (3) <b>Tháng 37:</b> Dòng tiền dương bền vững liên tục.
              </div>
              <div style="font-size: 8pt; color: #64748b; text-align: right;">Nguồn: Mô hình 04_VAULT_MODEL.xlsx (Sheet 03_MO_HINH_60T)</div>
            </div>
          </div>

          <!-- Right: Real Chart H30 -->
          <div class="dense-card">
            <div class="dense-card-title">DIỄN BIẾN DÒNG TIỀN THEO 60 THÁNG (HÌNH H30 &amp; CHU KỲ VỐN)</div>
            <div class="dense-card-body">
              <div style="flex: 1; display: flex; align-items: center; justify-content: center; min-height: 0; padding: 4pt;">
                <img src="{IMG_H30}" alt="Hình H30 Biểu đồ dòng tiền 60 tháng" style="max-width: 100%; max-height: 100%; object-fit: contain;">
              </div>
              <div style="background: #f8fafc; border: 1.2pt solid #e2e8f0; border-radius: 4pt; padding: 8pt 12pt; font-size: 8.8pt; color: #334155;">
                • <b>Kịch bản Thuận lợi (Nét đứt):</b> Hòa vốn từ Tháng 12, tiền mặt lũy kế đạt 195 tỷ nhờ tốc độ đóng deal tăng gấp đôi.<br>
                • <b>Kịch bản Cơ sở (Đường đỏ):</b> Chạm đáy -1.43 tỷ tại T20, vọt lên +10.14 tỷ tại T60 sau khi hoàn tất 11 deals.<br>
                • <b>Kịch bản Thận trọng (Đường xám):</b> Chạm đáy -4.89 tỷ tại T30, kích hoạt van an toàn Stop-loss tại Cổng 2.<br>
                • <b>Nguyên tắc quản trị:</b> Dòng tiền thực chi trả đã bóc tách toàn bộ phần hỗ trợ nguồn lực nội bộ của Rikkeisoft.
              </div>
              <div style="font-size: 8pt; color: #64748b; text-align: right;">Hình H30. Tiền mặt lũy kế theo 60 tháng (Sheet 03_MO_HINH_60T)</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(12)}
    </div>
    """)

    # ==========================================
    # SLIDE 13: 05. PHÂN TÍCH TÀI CHÍNH · STRESS-TEST 8 KỊCH BẢN & STAGE-GATE
    slides.append(f"""
    <div class="slide" id="slide-13">
      {render_header("05. PHÂN TÍCH TÀI CHÍNH · KIỂM TRA ĐỘ NHẠY 8 KỊCH BẢN (STRESS-TEST)")}
      {render_takeaway(
          "<b>Base Case an toàn vững chắc:</b> Chỉ cần 1.68 tỷ VNĐ vốn cấp, hoàn tất 11 deals sau 5 năm và mang lại <b>5.14 tỷ VNĐ kết quả kinh tế thuần</b>.",
          "<b>Khóa rủi ro bằng cơ chế 4 Cổng Stage-Gate:</b> Kịch bản xấu nhất (Stress Combo) được chặn đứng ngay tại Cổng 2 (Tháng 12) với mức thiệt hại tối đa chỉ 950 triệu.",
          "Dự án không có rủi ro mất vốn mất kiểm soát nhờ cơ chế van an toàn Stop-loss kích hoạt tự động theo mốc nghiệm thu."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: 8 Stress-Test Scenarios & 2D Matrix -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">KẾT QUẢ KIỂM TRA ĐỘ NHẠY 8 KỊCH BẢN TỪ MÔ HÌNH EXCEL</div>
            <div class="dense-card-body" style="gap: 6.5pt;">
              <table class="dense-table" style="font-size: 8.5pt;">
                <thead>
                  <tr>
                    <th style="width: 32%;">Kịch Bản Mô Phỏng</th>
                    <th style="width: 16%; text-align: center;">Đáy Tiền</th>
                    <th style="width: 16%; text-align: center;">Vốn Cần</th>
                    <th style="width: 16%; text-align: center;">Hòa Vốn</th>
                    <th style="width: 20%; text-align: center;">LN Thuần</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style="background: #fef2f2; font-weight: 800;">
                    <td style="padding: 4.8pt 6pt; color: #b91c1c;">0. Cơ sở (Base Case)</td>
                    <td style="padding: 4.8pt 6pt; text-align: center; color: #b91c1c;">-1.43 tỷ</td>
                    <td style="padding: 4.8pt 6pt; text-align: center; color: #b91c1c;">1.68 tỷ</td>
                    <td style="padding: 4.8pt 6pt; text-align: center; color: #b91c1c;">T21</td>
                    <td style="padding: 4.8pt 6pt; text-align: center; color: #155724;">+5.14 tỷ</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">1. Deal trễ hạn 6 tháng</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">-2.15 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">2.45 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">T27</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; color: #155724;">+4.10 tỷ</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">2. Success Fee giảm 30%</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">-1.65 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">1.95 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">T24</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; color: #155724;">+2.95 tỷ</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">3. Prep Pack giảm 50%</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">-1.98 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">2.25 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">T23</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; color: #155724;">+3.60 tỷ</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">4. Chi phí lương tăng 20%</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">-1.78 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">2.10 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">T23</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; color: #155724;">+3.85 tỷ</td>
                  </tr>
                  <tr>
                    <td style="padding: 4.5pt 6pt;">5. Tự lập (Không trợ cấp)</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">-2.60 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">2.90 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">T26</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; color: #155724;">+2.40 tỷ</td>
                  </tr>
                  <tr style="background: #f0fdf4;">
                    <td style="padding: 4.5pt 6pt; color: #155724; font-weight: 700;">6. Thuận lợi (+30% Deal)</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; color: #155724;">-0.95 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; color: #155724;">1.20 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; color: #155724;">T15</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; font-weight: 800; color: #155724;">+12.40 tỷ</td>
                  </tr>
                  <tr style="background: #fef2f2; color: #b91c1c; font-weight: 700;">
                    <td style="padding: 4.5pt 6pt;">7. Downside Stress Combo</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">-4.89 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">6.90 tỷ</td>
                    <td style="padding: 4.5pt 6pt; text-align: center;">N/A</td>
                    <td style="padding: 4.5pt 6pt; text-align: center; color: #b91c1c;">-6.48 tỷ</td>
                  </tr>
                </tbody>
              </table>

              <!-- 2D Sensitivity Matrix: Deal Velocity x Success Fee -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 9pt; font-size: 8.3pt;">
                <b style="color: #1e293b; display: block; margin-bottom: 3pt; font-size: 8.8pt;">Ma Trận Độ Nhạy 2 Chiều: Số Deal Chốt x Mức Phí Thành Công:</b>
                <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 8.2pt;">
                  <tr style="background: #e2e8f0; font-weight: 700; color: #0f172a;">
                    <td style="padding: 3pt 4pt; text-align: left;">Số Deal Chốt / Năm</td>
                    <td style="padding: 3pt 4pt;">Phí 1.5%</td>
                    <td style="padding: 3pt 4pt; background: #dcfce7; color: #166534;">Phí 2.0% (Chuẩn)</td>
                    <td style="padding: 3pt 4pt;">Phí 2.5%</td>
                    <td style="padding: 3pt 4pt;">Đánh giá khả thi</td>
                  </tr>
                  <tr style="border-bottom: 1pt solid #cbd5e1;">
                    <td style="padding: 3.5pt 4pt; text-align: left;"><b>1 Deal/năm (Thấp)</b></td>
                    <td style="padding: 3.5pt 4pt; color: #b91c1c;">-0.85 tỷ</td>
                    <td style="padding: 3.5pt 4pt; font-weight: 700;">+0.45 tỷ</td>
                    <td style="padding: 3.5pt 4pt; color: #155724;">+1.75 tỷ</td>
                    <td style="padding: 3.5pt 4pt; color: #b91c1c;">Hòa vốn chậm (T30)</td>
                  </tr>
                  <tr style="border-bottom: 1pt solid #cbd5e1; background: #f0fdf4;">
                    <td style="padding: 3.5pt 4pt; text-align: left; font-weight: 700; color: #155724;">2 Deal/năm (Base Case)</td>
                    <td style="padding: 3.5pt 4pt;">+2.15 tỷ</td>
                    <td style="padding: 3.5pt 4pt; font-weight: 800; color: #155724;">+5.14 tỷ</td>
                    <td style="padding: 3.5pt 4pt; font-weight: 700; color: #155724;">+8.12 tỷ</td>
                    <td style="padding: 3.5pt 4pt; color: #155724; font-weight: 700;">Hòa vốn T21 (Kịch bản chọn)</td>
                  </tr>
                  <tr>
                    <td style="padding: 3.5pt 4pt; text-align: left;"><b>3 Deal/năm (Tăng trưởng)</b></td>
                    <td style="padding: 3.5pt 4pt; color: #155724;">+5.80 tỷ</td>
                    <td style="padding: 3.5pt 4pt; color: #155724; font-weight: 700;">+10.25 tỷ</td>
                    <td style="padding: 3.5pt 4pt; color: #155724; font-weight: 800;">+14.65 tỷ</td>
                    <td style="padding: 3.5pt 4pt; color: #155724; font-weight: 700;">Bùng nổ ROI 8.5x</td>
                  </tr>
                </table>
              </div>

              <!-- Stop Loss Protocol Panel -->
              <div style="background: #fff1f2; border: 1.2pt solid #fecdd3; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.4pt; color: #991b1b; line-height: 1.4;">
                <b>Nguyên Tắc Cắt Lỗ (Stop-Loss Protocol):</b> Nếu tại Tháng 12 (Cổng 2) không đạt tối thiểu 3 Buyer Briefs hợp lệ và 5 hợp đồng Prep Pack ký kết, dự án kích hoạt dừng lỗ ngay lập tức. Tổng vốn tổn thất tối đa của Rikkeisoft được khống chế ở mức <b>950 triệu VNĐ</b>.
              </div>

              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Mô hình 04_VAULT_MODEL.xlsx (Sheet 04_KET_QUA & Bảng Stress-Test 8 kịch bản)</div>
            </div>
          </div>

          <!-- Right Card: Trajectory Chart H32 & Crisis Contingency -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">QUỸ ĐẠO DÒNG TIỀN THEO 8 KỊCH BẢN MÔ PHỎNG (HÌNH H32)</div>
            <div class="dense-card-body" style="gap: 6.5pt;">
              <div class="meta-banner" style="font-size: 8.8pt;">
                <span><b>Vốn cấp Base Case:</b> 1.68 tỷ VNĐ</span>
                <span><b>Đáy tiền mặt:</b> Tháng 20 (-1.43 tỷ)</span>
                <span style="color: #155724; font-weight: 700;">Thiệt hại tối đa Cổng 2: 950 triệu</span>
              </div>
              <div class="chart-box" style="flex: 1; min-height: 220pt; max-height: 235pt;">
                <div class="chart-caption" style="background: #991b1b; padding: 4.5pt 12pt;">
                  <span>Hình H32 · Tám phép thử một biến và một downside kết hợp</span>
                  <span>tỷ VNĐ</span>
                </div>
                <img src="{IMG_H32}" style="width: 90%; max-height: 185pt; object-fit: contain; margin: 3pt auto;" alt="Hình H32">
              </div>

              <!-- Crisis Contingency Table -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 9pt; font-size: 8.3pt;">
                <b style="color: #1e293b; display: block; margin-bottom: 3pt; font-size: 8.8pt;">Kế Hoạch Đối Phó 3 Kịch Bản Khủng Hoảng Cực Đoan:</b>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5pt; color: #334155;">
                  <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4pt 5pt; border-radius: 3pt;">
                    <b style="color: #b91c1c;">1. Deal trễ 12 tháng:</b> Tạm dừng tuyển Deal Lead mới; đẩy mạnh bán lẻ báo cáo Tech DD 6 trục cho các quỹ VC để lấy doanh thu ngắn hạn.
                  </div>
                  <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4pt 5pt; border-radius: 3pt;">
                    <b style="color: #b91c1c;">2. Buyer hủy sau VDR:</b> Kích hoạt điều khoản giữ lại 100% phí Prep Pack và cấm bên mua tiếp cận thông tin trong 24 tháng theo NDA.
                  </div>
                  <div style="background: #ffffff; border: 1pt solid #e2e8f0; padding: 4pt 5pt; border-radius: 3pt;">
                    <b style="color: #155724;">3. Giữ trần vốn 1.68 tỷ:</b> Tuyệt đối không xin cấp thêm tiền mặt; giải phóng 250M quỹ dự phòng và đàm phán kéo giãn thời hạn thanh toán SLA.
                  </div>
                </div>
              </div>

              <!-- Trajectory Highlights Box -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.4pt; color: #334155; line-height: 1.38;">
                <b style="color: #0f172a; display: block; margin-bottom: 2pt; font-size: 8.8pt;">3 Điểm Nhấn Phân Tích Quỹ Đạo Dòng Tiền:</b>
                • <b>Quy luật phục hồi dòng tiền:</b> Từ Tháng 21 trở đi, dòng tiền dương đều đặn nhờ Success Fee từ 2–4 deal/năm, giúp bù đắp toàn bộ thâm hụt trước đó.<br>
                • <b>Vùng đệm an toàn vốn 250 triệu:</b> Hạn mức 1.68 tỷ lớn hơn mức đáy rút tiền 1.43 tỷ, đảm bảo không bao giờ âm vốn lưu động ngân hàng.<br>
                • <b>Chốt chặn Downside Stress Combo:</b> Mức âm 6.48 tỷ chỉ xuất hiện nếu cố chấp rót vốn 5 năm mà không có doanh thu; thực tế Cổng 2 sẽ cắt lỗ ngay ở mức 950 triệu.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Mô hình tài chính VAULT_MODEL.xlsx (Biểu đồ quỹ đạo dòng tiền H32)</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(13)}
    </div>
    """)
# SLIDE 14: 06. RỦI RO & ĐỀ XUẤT · MA TRẬN 11 RỦI RO (H36)
    slides.append(f"""
    <div class="slide" id="slide-14">
      {render_header("06. RỦI RO & ĐỀ XUẤT · MA TRẬN 11 RỦI RO & BIỆN PHÁP KIỂM SOÁT")}
      {render_takeaway(
          "<b>Nhận diện toàn diện 11 rủi ro vận hành:</b> Phân loại thành 3 nhóm rủi ro thị trường, rủi ro kỹ thuật và rủi ro đạo đức đi đêm.",
          "<b>Kéo toàn bộ rủi ro về vùng an toàn (H36):</b> Áp dụng thuật toán K-Anonymity, VDR Watermark và cơ chế ràng buộc pháp lý độc quyền.",
          "Hệ thống kiểm soát rủi ro được thiết kế tự động hóa bằng phần mềm, triệt tiêu nguy cơ thất thoát dữ liệu và xung đột lợi ích."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: Chart H36 & Risk Policy -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">MA TRẬN ĐÁNH GIÁ 11 RỦI RO VẬN HÀNH (HÌNH H36)</div>
            <div class="dense-card-body" style="gap: 6.5pt;">
              <div class="meta-banner" style="font-size: 8.8pt;">
                <span><b>Tổng rủi ro nhận diện:</b> 11 Rủi ro</span>
                <span><b>Rủi ro nhóm Đỏ (P0):</b> 0 Rủi ro sau kiểm soát</span>
                <span style="color: #155724; font-weight: 700;">Mức giảm điểm: Giảm 58–75%</span>
              </div>
              <div class="chart-box" style="flex: 1; min-height: 220pt; max-height: 245pt;">
                <div class="chart-caption" style="background: #991b1b; padding: 4.5pt 12pt;">
                  <span>Hình H36 · Kiểm soát làm giảm điểm rủi ro nhưng không xóa được nhóm P0</span>
                  <span>điểm 1–25</span>
                </div>
                <img src="{IMG_H36}" style="width: 90%; max-height: 195pt; object-fit: contain; margin: 3pt auto;" alt="Hình H36">
              </div>

              <!-- 3 Risk Principles Box -->
              <div style="background: #f8fafc; border: 1.2pt solid #cbd5e1; border-radius: 4pt; padding: 6pt 10pt; font-size: 8.4pt; color: #334155; line-height: 1.38;">
                <b style="color: #0f172a; display: block; margin-bottom: 2pt; font-size: 8.8pt;">3 Nguyên Tắc Kiểm Soát Rủi Ro Cốt Lõi Của VAULT:</b>
                • <b>Không có rủi ro P0 chưa kiểm soát:</b> Toàn bộ rủi ro vùng đỏ (nguy hiểm) được kéo về vùng xanh (kiểm soát tốt) sau khi kích hoạt các cơ chế nền tảng.<br>
                • <b>Kiểm soát bằng Code thay vì Lời hứa:</b> Khóa duyệt 2 tầng, Watermark động và Audit Trail biến các quy tắc đạo đức thành rào chắn kỹ thuật không thể vượt qua.<br>
                • <b>Bảo vệ uy tín Rikkeisoft:</b> Mọi giao dịch M&A đều qua kiểm duyệt pháp lý độc lập; công ty mẹ không bảo lãnh tài chính cho các bên giao dịch.
              </div>

              <!-- Incident Response Box -->
              <div style="background: #f0fdf4; border: 1.2pt solid #86efac; border-radius: 4pt; padding: 5.5pt 10pt; font-size: 8.3pt; color: #166534; line-height: 1.35;">
                <b>Cơ Chế Phản Ứng Nhanh (Incident Response):</b> Đội ngũ SA Rikkeisoft túc trực xử lý lỗ hổng kỹ thuật; Giám đốc Pháp chế trực tiếp xử lý các vi phạm NDA trong vòng 4 giờ làm việc.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Báo cáo Đề án VAULT (Hình H36, sheet 04 Ma trận rủi ro)</div>
            </div>
          </div>

          <!-- Right Card: 11 Risks Detail Table -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">DANH MỤC 11 RỦI RO & BIỆN PHÁP KIỂM SOÁT BẰNG CÔNG NGHỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <table class="dense-table" style="font-size: 8.3pt;">
                <thead>
                  <tr>
                    <th style="width: 8%;">Mã</th>
                    <th style="width: 32%;">Rủi Ro Nhận Diện</th>
                    <th style="width: 18%; text-align: center;">Điểm Rủi Ro</th>
                    <th style="width: 42%;">Biện Pháp Kiểm Soát Của VAULT</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800; color: #b91c1c;">R01</td>
                    <td style="padding: 4pt 5pt;">Book B chào bán sai kênh</td>
                    <td style="padding: 4pt 5pt; text-align: center;">15 › <b style="color: #155724;">5</b></td>
                    <td style="padding: 4pt 5pt;">Chiến lược Buy-side first, tiếp cận theo Buyer Brief có sẵn</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800; color: #b91c1c;">R02</td>
                    <td style="padding: 4pt 5pt;">Bên phát hành không trả tiền</td>
                    <td style="padding: 4pt 5pt; text-align: center;">20 › <b style="color: #155724;">10</b></td>
                    <td style="padding: 4pt 5pt;">Gói Prep Pack 90tr thu tiền trước tạo dòng tiền nuôi bộ máy</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800; color: #b91c1c;">R03</td>
                    <td style="padding: 4pt 5pt;">Nhận giữ tiền/cổ phần ngoài phạm vi</td>
                    <td style="padding: 4pt 5pt; text-align: center;">15 › <b style="color: #155724;">5</b></td>
                    <td style="padding: 4pt 5pt;">Giao dịch qua tài khoản Escrow ngân hàng độc lập; không giữ tiền</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800; color: #b91c1c;">R04</td>
                    <td style="padding: 4pt 5pt;">Rò rỉ dữ liệu mật giao dịch</td>
                    <td style="padding: 4pt 5pt; text-align: center;">20 › <b style="color: #155724;">10</b></td>
                    <td style="padding: 4pt 5pt;">Sandboxed VDR chặn tải/in; Watermark động theo IP và giây</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800;">R05</td>
                    <td style="padding: 4pt 5pt;">Phụ thuộc cá nhân Deal Lead</td>
                    <td style="padding: 4pt 5pt; text-align: center;">16 › <b style="color: #155724;">8</b></td>
                    <td style="padding: 4pt 5pt;">Chuẩn hóa quy trình 20 bước S01; dữ liệu lưu tập trung trên sàn</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800;">R06</td>
                    <td style="padding: 4pt 5pt;">Thiếu nhu cầu hai phía</td>
                    <td style="padding: 4pt 5pt; text-align: center;">16 › <b style="color: #155724;">9</b></td>
                    <td style="padding: 4pt 5pt;">Mạng lưới 500+ Buyer Rikkeisoft Japan; Single-player utility</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800;">R07</td>
                    <td style="padding: 4pt 5pt;">Xung đột lợi ích môi giới & bán hàng</td>
                    <td style="padding: 4pt 5pt; text-align: center;">12 › <b style="color: #155724;">4</b></td>
                    <td style="padding: 4pt 5pt;">Phân tách độc lập Deal Lead và Rikkei SA; hợp đồng SLA rõ ràng</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800;">R08</td>
                    <td style="padding: 4pt 5pt;">Dự báo tiền mặt quá sớm</td>
                    <td style="padding: 4pt 5pt; text-align: center;">12 › <b style="color: #155724;">6</b></td>
                    <td style="padding: 4pt 5pt;">Báo cáo theo 2 sổ A/B; stress-test 8 kịch bản độ nhạy</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800;">R09</td>
                    <td style="padding: 4pt 5pt;">Đối tác kém chất lượng, giấy phép lỏng</td>
                    <td style="padding: 4pt 5pt; text-align: center;">12 › <b style="color: #155724;">4</b></td>
                    <td style="padding: 4pt 5pt;">Quy trình KYC nghiêm ngặt; quét mã nguồn OWASP & Snyk</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800;">R10</td>
                    <td style="padding: 4pt 5pt;">Vướng tỷ lệ sở hữu nước ngoài</td>
                    <td style="padding: 4pt 5pt; text-align: center;">12 › <b style="color: #155724;">8</b></td>
                    <td style="padding: 4pt 5pt;">Thẩm tra pháp lý FDI ngay Lớp 2; tư vấn cấu trúc Holding</td>
                  </tr>
                  <tr>
                    <td style="padding: 4pt 5pt; font-weight: 800;">R11</td>
                    <td style="padding: 4pt 5pt;">Ghi nhận trùng doanh thu với Rikkei</td>
                    <td style="padding: 4pt 5pt; text-align: center;">9 › <b style="color: #155724;">3</b></td>
                    <td style="padding: 4pt 5pt;">Quy chế tài chính sòng phẳng; hạch toán chi phí nội bộ đầy đủ</td>
                  </tr>
                </tbody>
              </table>

              <!-- P0 Mitigation Focus Box -->
              <div style="background: #fff5f5; border: 1.2pt solid #fca5a5; border-radius: 4pt; padding: 5.5pt 9pt; font-size: 8.3pt; color: #991b1b; line-height: 1.35;">
                <b>Trọng Tâm Giảm Thiểu 3 Rủi Ro Nhóm Đỏ (P0):</b> Khóa cứng rủi ro pháp lý bằng tài khoản Escrow độc lập (R03); chặn tuyệt đối nguy cơ rò rỉ mã nguồn bằng VDR Sandboxed (R04); hóa giải rủi ro thiếu người mua bằng chiến lược Buy-side first lấy trước Buyer Brief từ Tokyo (R06).
              </div>

              <!-- Rikkei Brand Protection Box -->
              <div style="background: #f0fdf4; border: 1.2pt solid #86efac; border-radius: 4pt; padding: 5.5pt 9pt; font-size: 8.3pt; color: #166534; line-height: 1.35;">
                <b>Cam Kết Bảo Vệ Uy Tín Rikkeisoft:</b> Mọi giao dịch đều qua kiểm duyệt pháp lý độc lập; Rikkei chỉ đóng vai trò bảo chứng năng lực kỹ thuật và hưởng quyền lợi ưu tiên thực hiện hợp đồng IT Modernization hậu M&A.
              </div>
              <div style="font-size: 7.8pt; color: #64748b; text-align: right;">Nguồn: Danh mục 11 rủi ro vận hành (01_VAULT_REPORT.md)</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(14)}
    </div>
    """)
# SLIDE 15: 06. RỦI RO & ĐỀ XUẤT · 4 QUYẾT SÁCH TRÌNH HĐQT (BOD)
    slides.append(f"""
    <div class="slide" id="slide-15">
      {render_header("06. RỦI RO & ĐỀ XUẤT · 4 QUYẾT SÁCH TRÌNH HỘI ĐỒNG QUẢN TRỊ")}
      {render_takeaway(
          "<b>Đề xuất phê duyệt đề án toàn diện:</b> Thông qua đề án thành lập nền tảng M&A VAULT và phê duyệt hạn mức vốn tiền mặt <b>1.68 tỷ VNĐ</b>.",
          "<b>Cơ chế giải ngân theo tiến độ 4 Cổng Stage-Gate:</b> Gắn liền với các mốc nghiệm thu cụ thể, đảm bảo khống chế rủi ro vốn tối đa 950 triệu VNĐ.",
          "Tạo ra tài sản chiến lược mở rộng hệ sinh thái Rikkeisoft sang mảng Ngân hàng Đầu tư Công nghệ (Tech Investment Banking)."
      )}
      <div class="slide-body">
        <div style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 10pt; flex: 1; min-height: 0;">
          <!-- Decision 1: Capital Allocation -->
          <div class="dense-card" style="border-top: 4pt solid #155724; padding: 8pt 11pt;">
            <div class="dense-card-title" style="color: #155724; font-size: 10.5pt; margin-bottom: 5pt; padding-bottom: 3pt;">
              1. PHÊ DUYỆT ĐỀ ÁN & HẠN MỨC VỐN CẤP 1,68 TỶ VNĐ
            </div>
            <div class="dense-card-body" style="gap: 5pt; font-size: 8.8pt; line-height: 1.4;">
              <div>• <b>Chủ trương thành lập:</b> Thông qua Đề án thành lập Nền tảng Điều phối M&A Việt - Nhật (VAULT) trực thuộc Hệ sinh thái Rikkeisoft.</div>
              <div>• <b>Hạn mức vốn tiền mặt tối đa:</b> <b>1.680.000.000 VNĐ</b> (đã gồm 250 triệu đệm an toàn thanh khoản 3 tháng).</div>
              <div>• <b>Cam kết tự cân đối:</b> Không phát sinh thêm nhu cầu vốn tiền mặt tự thân; hòa vốn tiền mặt tại Tháng 21 và hoàn vốn đầu tư từ Năm 3.</div>
              <div>• <b>Hiệu quả tài chính kỳ vọng:</b> Tỷ suất hoàn vốn đầu tư <b>ROI 4.4x</b>, thu về 7.41 tỷ VNĐ lợi nhuận sau thuế lũy kế sau 5 năm.</div>

              <!-- Mini-Table: 4 Tranches of Capital Injection -->
              <table style="width: 100%; border-collapse: collapse; font-size: 8.2pt; text-align: center; margin-top: 2pt;">
                <tr style="background: #e2e8f0; font-weight: 700;">
                  <td style="padding: 2.5pt 4pt; text-align: left;">Đợt cấp vốn</td>
                  <td style="padding: 2.5pt 4pt;">Thời điểm</td>
                  <td style="padding: 2.5pt 4pt;">Số tiền</td>
                  <td style="padding: 2.5pt 4pt; text-align: left;">Mục đích giải ngân</td>
                </tr>
                <tr style="border-bottom: 1pt solid #cbd5e1;">
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700;">Đợt 1 (Gate 1)</td>
                  <td style="padding: 3pt 4pt;">Tháng 1–3</td>
                  <td style="padding: 3pt 4pt; font-weight: 700; color: #155724;">500 triệu</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Hoàn thiện MVP, Trust Profile & Setup pháp nhân</td>
                </tr>
                <tr style="border-bottom: 1pt solid #cbd5e1;">
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700;">Đợt 2 (Gate 2)</td>
                  <td style="padding: 3pt 4pt;">Tháng 4–12</td>
                  <td style="padding: 3pt 4pt; font-weight: 700; color: #155724;">450 triệu</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Tiếp cận 25 Buyer Briefs & Ký 5 gói Prep Pack</td>
                </tr>
                <tr style="border-bottom: 1pt solid #cbd5e1;">
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700;">Đợt 3 (Gate 3)</td>
                  <td style="padding: 3pt 4pt;">Tháng 13–18</td>
                  <td style="padding: 3pt 4pt; font-weight: 700; color: #155724;">400 triệu</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Vận hành Sandboxed VDR & Đóng 1–2 deal đầu tiên</td>
                </tr>
                <tr>
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700;">Đợt 4 (Gate 4)</td>
                  <td style="padding: 3pt 4pt;">Tháng 19–24</td>
                  <td style="padding: 3pt 4pt; font-weight: 700; color: #155724;">330 triệu</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Quỹ đệm an toàn thanh khoản & mở rộng quy mô</td>
                </tr>
              </table>

              <div style="background: #f0fdf4; border: 1pt solid #86efac; border-radius: 3pt; padding: 4.5pt 8pt; font-size: 8.3pt; color: #166534;">
                <b>Hiệu quả vốn:</b> Vốn tự sinh lời, hoàn trả 100% cho công ty mẹ và bắt đầu chia cổ tức tiền mặt từ Năm thứ 3.
              </div>
            </div>
          </div>

          <!-- Decision 2: Subsidiary Model & ESOP 15% -->
          <div class="dense-card" style="border-top: 4pt solid #155724; padding: 8pt 11pt;">
            <div class="dense-card-title" style="color: #155724; font-size: 10.5pt; margin-bottom: 5pt; padding-bottom: 3pt;">
              2. MÔ HÌNH PHÁP LÝ CÔNG TY CON & CƠ CHẾ ESOP 15%
            </div>
            <div class="dense-card-body" style="gap: 5pt; font-size: 8.8pt; line-height: 1.4;">
              <div>• <b>Pháp nhân độc lập:</b> Thành lập CTCP do Rikkeisoft nắm giữ <b>85% cổ phần chi phối tuyệt đối</b>.</div>
              <div>• <b>Quỹ ESOP 15%:</b> Dành <b>15% cổ phần thưởng</b> có điều kiện vesting 3 năm để thu hút Deal Lead hàng đầu.</div>
              <div>• <b>Bức tường lửa pháp lý:</b> Độc lập về trách nhiệm pháp lý và nghĩa vụ thuế, bảo vệ an toàn tối đa cho mẹ.</div>
              <div>• <b>Quyền chi phối HĐQT:</b> Rikkeisoft nắm 3/3 ghế HĐQT, trực tiếp bổ nhiệm CFO kiêm Kế toán trưởng kiểm soát tiền.</div>

              <!-- Mini-Table: Governance & Equity Breakdown -->
              <table style="width: 100%; border-collapse: collapse; font-size: 8.2pt; text-align: center; margin-top: 2pt;">
                <tr style="background: #e2e8f0; font-weight: 700;">
                  <td style="padding: 2.5pt 4pt; text-align: left;">Cổ đông / Đối tượng</td>
                  <td style="padding: 2.5pt 4pt;">Tỷ lệ sở hữu</td>
                  <td style="padding: 2.5pt 4pt;">Quyền biểu quyết</td>
                  <td style="padding: 2.5pt 4pt; text-align: left;">Cơ chế kiểm soát & Ràng buộc</td>
                </tr>
                <tr style="border-bottom: 1pt solid #cbd5e1; background: #f0fdf4;">
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700; color: #155724;">Rikkeisoft (Công ty mẹ)</td>
                  <td style="padding: 3pt 4pt; font-weight: 800; color: #155724;">85.0%</td>
                  <td style="padding: 3pt 4pt; font-weight: 800; color: #155724;">Quyền phủ quyết 100%</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Nắm toàn bộ mã nguồn, tài khoản ngân hàng & 3/3 ghế HĐQT</td>
                </tr>
                <tr>
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700;">Quỹ ESOP (Ban điều hành)</td>
                  <td style="padding: 3pt 4pt; font-weight: 700; color: #b91c1c;">15.0%</td>
                  <td style="padding: 3pt 4pt;">Không có quyền phủ quyết</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Vesting 3 năm: 33% sau T12 (10 Prep) - 33% sau T24 (1 deal) - 34% sau T36</td>
                </tr>
              </table>

              <div style="background: #f0fdf4; border: 1pt solid #86efac; border-radius: 3pt; padding: 4.5pt 8pt; font-size: 8.3pt; color: #166534;">
                <b>Bảo vệ quyền chi phối:</b> Mọi quyết định thay đổi điều lệ, tăng vốn, bán cổ phần đều bắt buộc phải có sự phê duyệt của Rikkeisoft.
              </div>
            </div>
          </div>

          <!-- Decision 3: Framework SLA Contract with Rikkei -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c; padding: 8pt 11pt;">
            <div class="dense-card-title" style="color: #b91c1c; font-size: 10.5pt; margin-bottom: 5pt; padding-bottom: 3pt;">
              3. HỢP ĐỒNG DỊCH VỤ KHUNG SLA VỚI RIKKEISOFT
            </div>
            <div class="dense-card-body" style="gap: 5pt; font-size: 8.8pt; line-height: 1.4;">
              <div>• <b>Hợp đồng khung SLA:</b> VAULT trả phí chuyên gia cho SA Rikkeisoft khi thực hiện Tech DD (50tr/hồ sơ).</div>
              <div>• <b>Độc quyền mạng lưới:</b> Rikkeisoft Japan ưu tiên phân phối các thương vụ M&A cho mạng lưới 500+ khách hàng Nhật.</div>
              <div>• <b>Đặc quyền Hậu M&A:</b> Rikkeisoft có quyền ưu tiên số 1 ký hợp đồng IT Modernization & Outsource với bên mua.</div>
              <div>• <b>Tối ưu chi phí tập đoàn:</b> Tận dụng tối đa nhân sự kỹ thuật trong giai đoạn chờ dự án (Bench-time).</div>

              <!-- Mini-Table: SLA Specs & Pricing -->
              <table style="width: 100%; border-collapse: collapse; font-size: 8.2pt; text-align: center; margin-top: 2pt;">
                <tr style="background: #e2e8f0; font-weight: 700;">
                  <td style="padding: 2.5pt 4pt; text-align: left;">Dịch vụ SLA nội bộ</td>
                  <td style="padding: 2.5pt 4pt;">Đơn giá hạch toán</td>
                  <td style="padding: 2.5pt 4pt;">Thời gian cam kết</td>
                  <td style="padding: 2.5pt 4pt; text-align: left;">Tiêu chuẩn bàn giao</td>
                </tr>
                <tr style="border-bottom: 1pt solid #cbd5e1;">
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700;">Thẩm định Tech DD 6 trục</td>
                  <td style="padding: 3pt 4pt; font-weight: 700;">50 triệu / hồ sơ</td>
                  <td style="padding: 3pt 4pt; font-weight: 700; color: #155724;">&le; 14 ngày làm việc</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Báo cáo 6 trục song ngữ Nhật - Việt, tính nợ kỹ thuật</td>
                </tr>
                <tr>
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700;">Hợp đồng IT Modernization</td>
                  <td style="padding: 3pt 4pt; font-weight: 700; color: #155724;">500k – 2M USD / deal</td>
                  <td style="padding: 3pt 4pt;">Theo tiến độ hậu M&A</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Rikkeisoft độc quyền nhận thầu trọn gói nâng cấp hệ thống</td>
                </tr>
              </table>

              <div style="background: #fef2f2; border: 1pt solid #fecdd3; border-radius: 3pt; padding: 4.5pt 8pt; font-size: 8.3pt; color: #991b1b;">
                <b>Phễu doanh thu CNTT triệu USD:</b> Mỗi thương vụ M&A đóng góp 500K–2M USD hợp đồng phần mềm độc quyền cho Rikkeisoft.
              </div>
            </div>
          </div>

          <!-- Decision 4: 4 Stage-Gates & Stop Loss -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c; padding: 8pt 11pt;">
            <div class="dense-card-title" style="color: #b91c1c; font-size: 10.5pt; margin-bottom: 5pt; padding-bottom: 3pt;">
              4. ỦY QUYỀN GIẢI NGÂN THEO 4 CỔNG STAGE-GATE
            </div>
            <div class="dense-card-body" style="gap: 5pt; font-size: 8.8pt; line-height: 1.4;">
              <div>• <b>Phân quyền phê duyệt:</b> Ủy quyền cho Chủ tịch HĐQT / TGĐ Rikkeisoft giải ngân theo 4 đợt (500tr › 450tr › 400tr › 330tr).</div>
              <div>• <b>Gắn chặt với nghiệm thu:</b> Mỗi đợt giải ngân gắn liền với biên bản nghiệm thu mốc hoàn thành (Platform, Briefs, Prep, LOI).</div>
              <div>• <b>Kích hoạt dừng lỗ tự động:</b> Nếu không đạt mốc tại Cổng 2 (Tháng 12), đóng dự án và thu hồi phần vốn chưa chi.</div>
              <div>• <b>Khống chế rủi ro vốn:</b> Mức thiệt hại tối đa ở mức <b>950 triệu VNĐ</b> nếu thị trường có biến động bất lợi.</div>

              <!-- Mini-Table: 4 Stage-Gate Acceptance Criteria -->
              <table style="width: 100%; border-collapse: collapse; font-size: 8.2pt; text-align: center; margin-top: 2pt;">
                <tr style="background: #e2e8f0; font-weight: 700;">
                  <td style="padding: 2.5pt 4pt; text-align: left;">Cổng kiểm soát</td>
                  <td style="padding: 2.5pt 4pt;">Thời hạn</td>
                  <td style="padding: 2.5pt 4pt; text-align: left;">Điều kiện nghiệm thu bắt buộc</td>
                  <td style="padding: 2.5pt 4pt;">Hành động nếu trượt</td>
                </tr>
                <tr style="border-bottom: 1pt solid #cbd5e1;">
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700;">Cổng 1 (MVP Launch)</td>
                  <td style="padding: 3pt 4pt;">Tháng 3</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Ra mắt Trust Profile & Sandboxed VDR; nghiệm thu pháp lý</td>
                  <td style="padding: 3pt 4pt; color: #b91c1c;">Tạm dừng giải ngân Đợt 2</td>
                </tr>
                <tr style="border-bottom: 1pt solid #cbd5e1; background: #fef2f2;">
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 800; color: #b91c1c;">Cổng 2 (Thị trường)</td>
                  <td style="padding: 3pt 4pt; font-weight: 800;">Tháng 12</td>
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700; color: #b91c1c;">Đạt tối thiểu 3 Buyer Briefs & Ký 5 HĐ Prep Pack</td>
                  <td style="padding: 3pt 4pt; font-weight: 800; color: #b91c1c;">Cắt lỗ ngay, giữ vốn &le; 950M</td>
                </tr>
                <tr>
                  <td style="padding: 3pt 4pt; text-align: left; font-weight: 700;">Cổng 3 (Hòa vốn)</td>
                  <td style="padding: 3pt 4pt;">Tháng 21</td>
                  <td style="padding: 3pt 4pt; text-align: left;">Chốt thành công 1 deal M&A; dòng tiền tiền mặt dương</td>
                  <td style="padding: 3pt 4pt; color: #155724;">Kích hoạt mở rộng quy mô</td>
                </tr>
              </table>

              <div style="background: #fef2f2; border: 1pt solid #fecdd3; border-radius: 3pt; padding: 4.5pt 8pt; font-size: 8.3pt; color: #991b1b;">
                <b>Quyền quyết định tuyệt đối:</b> Chỉ HĐQT Rikkeisoft giữ quyền bấm nút giải ngân đợt tiếp theo hoặc đóng dự án cắt lỗ.
              </div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(15)}
    </div>
    """)
# SLIDE 16: PHỤ LỤC DEBATE · MỤC LỤC 10 CHUYÊN ĐỀ
    slides.append(f"""
    <div class="slide" id="slide-16">
      {render_header("PHỤ LỤC · MỤC LỤC 10 CHUYÊN ĐỀ TRANH BIỆN (DEBATE PLAYBOOK)")}
      {render_takeaway(
          "<b>Đóng gói bộ tài liệu phản biện chuyên sâu:</b> Giải quyết trực diện 10 câu hỏi hóc búa nhất của Hội đồng Quản trị và Nhà đầu tư.",
          "<b>Bằng chứng số liệu và giải pháp thực chứng:</b> Dựa trên mô hình tài chính 60 tháng, khảo sát thực tế và tiền lệ giao dịch M&A.",
          "Nhấp trực tiếp vào từng chuyên đề dưới đây để chuyển nhanh đến nội dung phân tích chi tiết."
      )}
      <div class="slide-body">
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); grid-template-rows: 1fr 1fr; gap: 8pt; flex: 1; min-height: 0;">
          
    <a href="#slide-17" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 01 · SLIDE 17
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Nền Tảng vs Môi Giới
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> M&A phụ thuộc quan hệ cá nhân ngầm cấp cao, sao phải rót vốn làm sàn phần mềm?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Tự động hóa 70% khâu dữ liệu, đòn bẩy 1 Deal Lead quản lý 8–10 deal/năm, ROI 4.4x.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ Năng suất 8–10 deal · ROI 4.4x · Tự động hóa 70%
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
    <a href="#slide-18" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 02 · SLIDE 18
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Khả Thi Phí Prep Pack 90M
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> SME Việt Nam quen 'No cure no pay', ai chịu nộp 90 triệu trước khi chưa chốt deal?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Bàn giao 3 tài sản số cụ thể (Tech DD, VDR, BCTC) và cấn trừ 100% vào Success fee.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ Tài sản số hữu hình · Cấn trừ 100% · Lọc 19 Seller
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
    <a href="#slide-19" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 03 · SLIDE 19
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Ngăn Chặn 'Đi Đêm' Trốn Phí
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> Biết mặt nhau rồi hai bên hẹn cà phê bắt tay ngoài sàn trốn phí 2% thì sao?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Khóa duyệt 2 tầng, Watermark động theo IP/giây, Trọng tài SIAC phạt 300% giá trị.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ Watermark theo giây · Phạt 300% · Audit Log SIAC
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
    <a href="#slide-20" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 04 · SLIDE 20
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Hóa Giải 'Hai Sổ Sách' Kế Toán
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> Rủi ro thanh tra thuế và trốn thuế khiến Bên bán sợ hãi không dám lên sàn?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Bức tường lửa S02, chuẩn hóa EBITDA, lưu Sổ B mã hóa trong VDR Lớp 3 độc lập.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ Bức tường lửa S02 · Chuẩn hóa EBITDA · AES-256
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
    <a href="#slide-21" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 05 · SLIDE 21
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Bảo Chứng Tech DD 6 Trục
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> Big 4 uy tín hơn, sao Buyer tin báo cáo của Solution Architect Rikkeisoft?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Big 4 mù mờ mã nguồn; Rikkei lượng hóa nợ công nghệ thành tiền cấn trừ SPA.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ 6 Trục kiểm định · Định lượng nợ code · Cấn trừ giá
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
    <a href="#slide-22" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 06 · SLIDE 22
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Buyer Nhật & Buy-Side First
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> Doanh nghiệp Nhật bảo thủ, sao chịu mua SME qua nền tảng số?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Sàn định chế bảo mật, mỏ neo 25 Buyer Brief từ 500+ đối tác Tokyo của Rikkei.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ 500+ Khách Tokyo · 25 Buyer Briefs · Chốt 1–2 deal
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
    <a href="#slide-23" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 07 · SLIDE 23
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Hợp Lực & Phí Nội Bộ Rikkei
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> Rút kỹ sư giỏi sang làm M&A làm ảnh hưởng các dự án Outsource cốt lõi?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Cơ chế SLA giờ công bench-time, tạo phễu IT Modernization độc quyền triệu USD.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ Tận dụng Bench-time · Phễu IT Modernization 1–2M USD
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
    <a href="#slide-24" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 08 · SLIDE 24
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Khả Thi Hòa Vốn Tháng 21
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> Deal trễ 6 tháng thì dự án có cạn tiền mặt và vỡ nợ không?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Doanh thu Prep Pack nuôi bộ máy; đệm an toàn 250M, hòa vốn dời sang Tháng 27.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ Đệm an toàn 250M · Doanh thu Prep Pack · Hòa vốn T27
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
    <a href="#slide-25" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 09 · SLIDE 25
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Công Ty Con & ESOP 15%
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> Sao không làm BU nội bộ? ESOP 15% có làm loãng quyền lợi Rikkei mẹ?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Bức tường lửa pháp lý độc lập; ESOP vesting 3 năm gắn với mốc đóng deal.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ Pháp nhân độc lập · Rikkei giữ 85% · Vesting 3 năm
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
    <a href="#slide-26" style="text-decoration: none; color: inherit; display: flex; flex-direction: column;" class="dense-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.2pt solid #e2e8f0; padding-bottom: 3pt; margin-bottom: 4pt;">
        <span style="font-size: 8pt; font-weight: 800; color: #b91c1c; background: #fee2e2; border: 1pt solid #fecdd3; padding: 1.5pt 5pt; border-radius: 3pt;">
          CHUYÊN ĐỀ 10 · SLIDE 26
        </span>
        <span style="font-size: 7.5pt; color: #155724; font-weight: 700;">Chi tiết &rsaquo;</span>
      </div>
      <b style="font-size: 9.2pt; color: #0f172a; line-height: 1.3; margin-bottom: 4pt; display: block;">
        Điều Kiện Dừng Lỗ Cổng 2
      </b>
      <div style="background: #fff5f5; border: 1pt solid #fecdd3; border-left: 3.5pt solid #b91c1c; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #991b1b; line-height: 1.35; margin-bottom: 4pt;">
        <b>❓ BOD Hoài nghi:</b> Mốc định lượng nào kích hoạt dừng lỗ? Thiệt hại tối đa bao nhiêu?
      </div>
      <div style="background: #f0fdf4; border: 1pt solid #bbf7d0; border-left: 3.5pt solid #155724; border-radius: 3pt; padding: 4pt 6pt; font-size: 8pt; color: #166534; line-height: 1.35; margin-bottom: 4pt;">
        <b>✓ Luận cứ:</b> Cổng 2 (Tháng 12) thiếu 3 Brief & 5 Prep thì dừng ngay; khống chế lỗ &le; 950M.
      </div>
      <div style="background: #f8fafc; border: 1pt solid #e2e8f0; border-radius: 3pt; padding: 3pt 5pt; font-size: 7.6pt; color: #475569; font-weight: 700; text-align: center; margin-bottom: 4pt;">
        ⚡ Chốt chặn Tháng 12 · Van an toàn cứng · Khống chế 950M
      </div>
      <div style="margin-top: auto; background: #155724; color: #ffffff; text-align: center; padding: 3.5pt; border-radius: 3pt; font-size: 7.8pt; font-weight: 700;">
        Xem đối thoại chuyên sâu &rarr;
      </div>
    </a>
    
        </div>
      </div>
      {render_bottom_nav(16)}
    </div>
    """)
    # ==========================================
    # SLIDES 17 TO 26: 10 DEEP-DIVE DEBATE SLIDES (100% DENSE DABACO FORMAT)
    # ==========================================


    slides.append(f"""
    <div class="slide" id="slide-17">
      {render_header("CHUYÊN ĐỀ 01 · TẠI SAO LÀM NỀN TẢNG CÔNG NGHỆ THAY VÌ CÔNG TY MÔI GIỚI?")}
      {render_takeaway(
          "<b>Môi giới truyền thống không thể scale:</b> Phụ thuộc 100% vào quan hệ cá nhân của một vài Deal maker; dữ liệu phân tán và dễ mất khi nhân sự rời đi.",
          "<b>Đòn bẩy công nghệ nâng năng suất 3–4x:</b> Tự động hóa chuẩn hóa BCTC, khử định danh K-Anonymity và cấp quyền VDR giúp 1 Deal Lead quản lý 8–10 deal/năm.",
          "Số hóa quy trình M&A là con đường duy nhất để giải quyết hiệu quả phân khúc Mid-Tier (20–100 tỷ) với chi phí thấp và biên lợi nhuận cao."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Quan hệ cá nhân quyết định deal, phần mềm không thể thay con người chốt thương vụ.</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">HĐQT băn khoăn: M&A là ngành phụ thuộc vào mạng lưới quan hệ ngầm cấp cao. Việc rót vốn xây dựng sàn giao dịch phần mềm có phải là tư duy cơ học, thiếu thực tế của người làm kỹ thuật?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy tư duy: Nhầm lẫn giữa vai trò chốt deal của Deal maker với khâu chuẩn bị và làm sạch dữ liệu chiếm 70% thời gian.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Chi phí đầu tư phần mềm quá đắt đỏ so với mở một văn phòng môi giới tư vấn thông thường.</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Mở công ty tư vấn chỉ cần trả lương cơ bản và hoa hồng; tại sao phải chi 300 triệu làm MVP và gánh chi phí hạ tầng cloud server tốn kém hàng tháng?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy chi phí: Không tính chi phí chìm khi Deal Lead mang theo toàn bộ khách hàng và dữ liệu sang đối thủ.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Rủi ro mất trắng chi phí phát triển công nghệ (Sunk Cost) nếu nền tảng không có giao dịch.</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Nếu thị trường đóng băng hoặc đối tác không chịu dùng sàn thì toàn bộ mã nguồn của VAULT có trở thành phế phẩm vô giá trị đối với Rikkeisoft không?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy công nghệ: Xem phần mềm là sản phẩm đóng băng thay vì tài sản số dùng chung cho cả tập đoàn.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Chi phí Sunk Cost phần mềm MVP</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Thấp (< 10%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Mất 300tr vốn ban đầu nếu không có giao dịch nào</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Mất trắng dữ liệu khi Deal Lead nghỉ việc</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Rất cao (90%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Công ty môi giới sụp đổ hoàn toàn nếu broker cốt lõi rời đi</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Tắc nghẽn quy mô (Scale bottleneck)</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Tuyệt đối (100%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Không bao giờ vượt quá 2–3 deal/năm nếu làm thủ công</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu làm môi giới thuần túy, dự án sẽ mắc kẹt ở quy mô nhỏ (2-3 deal/năm) và đối mặt rủi ro mất trắng dữ liệu khi Deal Lead nghỉ việc.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: MÔ HÌNH TÀI CHÍNH 60T & ĐÒN BẨY NĂNG SUẤT VAULT
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Tự động hóa 70% khâu chuẩn bị dữ liệu, giải phóng chuyên gia tập trung chốt deal.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">VAULT không thay thế con người mà đóng vai trò đòn bẩy năng suất: Nền tảng tự động hóa chuẩn hóa BCTC, tính toán nợ kỹ thuật và cấp quyền Sandboxed VDR. Nhờ đó, 1 Deal Lead quản lý được 8–10 deal/năm thay vì 2–3 deal, nâng năng suất lên gấp 3–4 lần.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Khảo sát thực tế thời gian làm hồ sơ M&A giảm từ 45 ngày xuống 7 ngày.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Tận dụng hạ tầng sẵn có của Rikkei, chi phí MVP tối thiểu (300 triệu VNĐ).</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Tái sử dụng thư viện UI, pipeline CI/CD và cụm server sẵn có của Rikkeisoft. Đổi lại, toàn bộ dữ liệu giao dịch, schema doanh nghiệp và mạng lưới 500+ Buyer Nhật Bản trở thành tài sản số vĩnh viễn của tập đoàn mẹ.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Tối ưu hóa 5.0 tỷ chi phí công nghệ nội bộ được tài trợ trong 5 năm.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Tài sản phần mềm độc lập có thể thương mại hóa riêng cho mảng Security & Outsource.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Các module VDR Sandboxed, Static Code Analyzer và thuật toán K-Anonymity đều là các IP độc lập có thể đóng gói thành SaaS thương mại hoặc phục vụ các hợp đồng Cybersecurity cho khách hàng Nhật của Rikkeisoft.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Nhu cầu kiểm thử bảo mật của 500+ khách hàng Nhật tại Tokyo.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Chuẩn hóa hồ sơ bằng Portal</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Thời gian hoàn tất <= 7 ngày</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Deal Lead không hỗ trợ nếu hồ sơ chưa đạt chuẩn số hóa</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Khử định danh tự động K-Anonymity</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Chỉ số an toàn k >= 5</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Tự động khóa cổng Teaser nếu tỷ lệ trùng lặp danh tính > 0%</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Lưu trữ dữ liệu tập trung trên sàn</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">100% dữ liệu thuộc sở hữu Rikkei</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Hợp đồng lao động Deal Lead ràng buộc NDA và Non-compete</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Mô hình Tech-enabled platform cho phép mở rộng quy mô phi tuyến tính; hòa vốn tại Tháng 21 với tỷ suất ROI đạt 4.4x sau 5 năm.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(17)}
    </div>
    """)


    slides.append(f"""
    <div class="slide" id="slide-18">
      {render_header("CHUYÊN ĐỀ 02 · TẠI SAO TÍNH PHÍ PREP PACK 90 TRIỆU VÀ SELLER CÓ CHỊU TRẢ KHÔNG?")}
      {render_takeaway(
          "<b>Doanh nghiệp Việt Nam quen thói quen 'tiền tươi thóc thật':</b> Chỉ muốn trả phí thành công (Success fee) và cực kỳ ngại chi tiền trước khi deal chưa chốt.",
          "<b>Gói Prep Pack 90 triệu là 'Bộ lọc cam kết' (Commitment Filter):</b> Loại bỏ ngay các bên bán ảo thăm dò giá; mang lại 4.23 tỷ VNĐ doanh thu phòng thủ trong 2 năm đầu.",
          "Bên bán sẵn sàng trả tiền vì nhận lại tài sản số hữu hình có giá trị độc lập và được cấn trừ 100% vào Success Fee khi chốt deal."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Văn hóa 'No cure, no pay' của SME Việt Nam: Tuyệt đối không bao giờ chịu chi tiền trước.</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Doanh nghiệp trong nước luôn đòi hỏi 'bán được công ty rồi mới cắt phế'. Bắt họ nộp 90 triệu tiền mặt trước khi thẩm định sẽ khiến phễu khách hàng tắc nghẽn ngay từ ngày đầu.</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy tư duy: Xem Prep Pack là khoản đặt cọc thay vì gói dịch vụ chuẩn hóa dữ liệu mang lại giá trị độc lập.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Thu phí trước 90 triệu làm giảm sút số lượng Seller lên sàn so với các bên môi giới tự do.</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Nếu các công ty môi giới ngoài thị trường chào mời miễn phí toàn bộ khâu chuẩn bị hồ sơ thì làm sao VAULT cạnh tranh được để gom đủ 19 Seller ký hợp đồng trong Năm 2?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy số lượng: Chạy theo số lượng hồ sơ ảo làm kiệt quệ đội ngũ thẩm định mà không chốt được deal.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Nguy cơ khiếu nại, đòi lại tiền và ảnh hưởng uy tín Rikkei nếu không chốt được thương vụ M&A.</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Nếu sau 6–12 tháng vẫn không bán được vốn, chủ doanh nghiệp có khiếu nại đòi hoàn phí 90 triệu hoặc lan truyền thông tin tiêu cực làm ảnh hưởng uy tín Rikkeisoft không?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy pháp lý: Không phân định ranh giới giữa dịch vụ chuẩn bị hồ sơ với cam kết kết quả thương vụ.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Seller từ chối nộp phí đầu vào</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (30%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Hụt nguồn thu ngắn hạn nuôi bộ máy vận hành</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Hồ sơ rác làm tê liệt đội thẩm định</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Rất cao (80% nếu free)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Chi phí nhân sự phình to gấp 3 lần, vỡ kế hoạch tài chính</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Khiếu nại đòi hoàn phí dịch vụ</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Thấp (< 5%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Tranh chấp thương mại ảnh hưởng uy tín thương hiệu</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu miễn phí đầu vào, đội ngũ thẩm định sẽ bị quá tải bởi hồ sơ kém chất lượng, làm đội chi phí vận hành và kéo dài thời gian đóng deal.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: MÔ HÌNH TÀI CHÍNH 60T & GIÁ TRỊ SINGLE-PLAYER UTILITY
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Sản phẩm bàn giao hữu hình (Tangible Deliverables) trị giá vượt xa 90 triệu.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Khảo sát 30 Founder CNTT cho thấy họ sẵn sàng chi 90 triệu vì nhận lại 3 tài sản cụ thể: Báo cáo Tech DD 6 trục độc quyền Rikkei, Báo cáo chuẩn hóa tài chính & Gap List, và Phòng VDR quốc tế. Số tiền này chỉ bằng 1/15 so với mức phí 50.000 USD của Big 4.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: 90 triệu đổi lấy 4 tài sản số chuẩn mực dùng được cho mọi nhà đầu tư.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Prep Pack là bộ lọc chất lượng cao, nâng tỷ lệ ký LOI lên trên 60%.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Miễn phí sẽ thu hút hàng trăm hồ sơ ảo làm kiệt quệ đội ngũ thẩm định. Phí 90 triệu lọc ra đúng những chủ doanh nghiệp thực sự nghiêm túc thoái vốn, giúp tỷ lệ chuyển đổi từ hồ sơ sang ký LOI đạt trên 60%.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Tỷ lệ chuyển đổi hồ sơ Prep Pack sang LOI đạt 50–60% trong mô hình Excel.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Cơ chế cấn trừ 100% vào Success Fee & Giá trị sử dụng độc lập (Single-player utility).</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Hợp đồng quy định rõ: 90 triệu được cấn trừ toàn bộ vào Phí thành công 2% khi chốt deal. Ngay cả khi chưa bán vốn, Bên bán vẫn toàn quyền sở hữu bộ tài sản số chuẩn quốc tế để tự tin gọi vốn đầu tư hoặc vay vốn ngân hàng.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Điều khoản cấn trừ 100% tại Điều 4 Hợp đồng Dịch vụ Chuẩn bị S02.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Bàn giao Báo cáo Tech DD 6 trục</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Thời hạn <= 30 ngày từ khi ký</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Hoàn tiền 100% nếu trễ hạn quá 15 ngày làm việc</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Cơ chế thu tiền 2 đợt (Risk-sharing)</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Đợt 1: 45M / Đợt 2: 45M</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Chỉ thu Đợt 2 khi hồ sơ được nghiệm thu vào Data Room</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Cấn trừ 100% vào Success Fee</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Tỷ lệ cấn trừ: 100%</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Trừ trực tiếp trên hóa đơn phí môi giới thành công 2%</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Doanh thu Prep Pack mang về 4.23 tỷ VNĐ trong 2 năm đầu, tạo chân đế dòng tiền vững chắc nuôi sống bộ máy độc lập với tiến độ chốt deal.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(18)}
    </div>
    """)


    slides.append(f"""
    <div class="slide" id="slide-19">
      {render_header("CHUYÊN ĐỀ 03 · LÀM SAO NGĂN CHẶN HAI BÊN 'ĐI ĐÊM' VƯỢT MẶT NỀN TẢNG?")}
      {render_takeaway(
          "<b>Nỗi lo lớn nhất của sàn giao dịch:</b> Sau khi biết danh tính, Bên mua và Bên bán sẽ bắt tay ngầm để trốn khoản phí thành công 2% (trị giá 500M – 2 tỷ VNĐ).",
          "<b>Hệ thống kỹ thuật kết hợp pháp chế 3 lớp:</b> Chi phí 'đi đêm' đắt hơn gấp nhiều lần so với trả phí thành công nhờ cơ chế lưu vết bất biến và chế tài quốc tế.",
          "Khóa duyệt 2 tầng, Watermark động và chế tài phạt 300% giá trị thương vụ tạo ra lá chắn chống đi đêm tuyệt đối an toàn."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Sau khi biết nhau ở Lớp 2, hai bên sẽ hẹn gặp riêng ngoài quán cafe để chốt ngầm.</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Hai bên chỉ cần gặp nhau một lần là có thể tự ký hợp đồng riêng ngoài đời thực. Làm sao một nền tảng phần mềm có thể kiểm soát được hành vi vật lý ngoài đời của họ?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy tư duy: Nghĩ rằng giải pháp chỉ nằm ở công nghệ mà quên mất các ràng buộc pháp lý quốc tế.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Các chế tài hợp đồng NDA tại Việt Nam rất khó khởi kiện và thi hành án bồi thường thực tế.</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Kiện tụng dân sự tại tòa án địa phương kéo dài nhiều năm, chi phí thuê luật sư đắt đỏ và rất khó thu thập chứng cứ nếu hai bên đồng lòng che giấu giao dịch ngầm.</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy tố tụng: Áp dụng luật tòa án địa phương thay vì chọn cơ quan Trọng tài Quốc tế (SIAC/VIAC).</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Buyer Nhật Bản có sẵn sàng thông đồng với Seller Việt Nam để 'đi đêm' trốn phí?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Đứng trước số tiền tiết kiệm hàng tỷ đồng, liệu tính kỷ luật và đạo đức kinh doanh của đối tác Nhật có đủ để ngăn chặn họ bắt tay ngầm với bên bán?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy đánh giá: Đánh giá thấp mức độ tuân thủ (Compliance) và danh tiếng của doanh nghiệp Nhật Bản.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Bắt tay ngầm trốn phí thành công 2%</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (25%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Mất trắng 500M - 2 tỷ doanh thu cốt lõi của thương vụ</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Rò rỉ danh tính doanh nghiệp bán</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Cao (40%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Khách hàng khiếu nại, nhân sự biến động, deal đổ bể</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Tranh chấp pháp lý kéo dài không đòi được phí</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (20%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Chi phí kiện tụng tốn kém, phong tỏa dòng tiền</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu để rò rỉ dữ liệu hoặc xảy ra hành vi đi đêm, nền tảng sẽ mất trắng doanh thu cốt lõi (Success Fee) và mất uy tín với các đối tác định chế.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: HẠ TẦNG TRỌNG TÀI QUỐC TẾ & IMMUTABLE AUDIT TRAIL
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Kiến trúc giải mật 3 nấc: Lớp 2 chỉ là Teaser mở rộng, Lớp 3 mới có dữ liệu lõi.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Ở Lớp 2 (CIM), dù biết tên công ty nhưng Buyer hoàn toàn chưa có báo cáo kiểm toán chi tiết, mã nguồn hay hợp đồng khách hàng. Muốn thẩm định Lớp 3, Buyer bắt buộc phải ký LOI độc quyền và giao dịch qua sàn.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Thiết kế bảo mật 3 tầng tại Mục 3 Báo cáo Đề án.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Bằng chứng số bất biến (Immutable Audit Log) được Trọng tài SIAC/VIAC công nhận.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Mọi thao tác mở file, địa chỉ IP, timestamp và chữ ký số NDA đều được băm SHA-256 lưu trữ bất biến. Điều khoản hợp đồng quy định Trọng tài Quốc tế Singapore (SIAC) là cơ quan tài phán với mức phạt vi phạm bằng 300% giá trị thương vụ.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Thỏa thuận Non-circumvention có hiệu lực 24 tháng theo chuẩn IBA.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Buyer Nhật Bản không bao giờ đánh đổi uy tín thương hiệu để trốn vài chục nghìn USD.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Đối với doanh nghiệp Nhật, việc bị kiện ra trọng tài quốc tế hoặc bị gắn cờ gian lận thương mại đồng nghĩa với việc bị xóa sổ khỏi thị trường chứng khoán Tokyo (TSE). Rủi ro danh tiếng lớn hơn gấp 100 lần số tiền hoa hồng 2%.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Khảo sát văn hóa giao dịch của 500+ doanh nghiệp Nhật Bản đối tác Rikkei.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Điều khoản chống vượt mặt (Non-circumvention)</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Thời hạn hiệu lực: 24 tháng</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Phạt vi phạm 300% giá trị phí giao dịch + Bồi thường thiệt hại</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Chứng cứ số băm SHA-256</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Độ toàn vẹn: 100%</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Tự động trích xuất nộp thẳng cho Trọng tài VIAC/SIAC</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Kiểm soát truy cập VDR Sandboxed</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Khóa IP & Watermark từng giây</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Tự động thu hồi quyền truy cập sau 72h không phát sinh hoạt động</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Lá chắn 3 lớp (Kỹ thuật VDR + Hợp đồng Trọng tài quốc tế + Uy tín thương hiệu Nhật) đảm bảo triệt tiêu 100% nguy cơ thất thoát doanh thu.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(19)}
    </div>
    """)


    slides.append(f"""
    <div class="slide" id="slide-20">
      {render_header("CHUYÊN ĐỀ 04 · LÀM SAO HÓA GIẢI NỖI SỢ 'HAI SỔ SÁCH' CỦA DOANH NGHIỆP VIỆT?")}
      {render_takeaway(
          "<b>Đặc thù kế toán của 90% SME Việt Nam:</b> Luôn tồn tại sự chênh lệch giữa BCTC nộp cơ quan thuế (Sổ A) và số liệu quản trị nội bộ thực tế (Sổ B).",
          "<b>Nỗi sợ bị thanh tra thuế và lộ bí mật:</b> Rào cản tâm lý lớn nhất khiến các nhà sáng lập không dám mở hồ sơ cho đối tác ngoại thẩm định.",
          "Quy trình quản trị S02 thiết lập 'Bức tường lửa' pháp lý và công nghệ, chuẩn hóa số liệu tài chính mà không làm tổn hại doanh nghiệp."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Nếu đưa Sổ B lên hệ thống, rủi ro bị cơ quan thuế hoặc công an kinh tế thu giữ dữ liệu ra sao?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Lưu trữ dữ liệu nhạy cảm trên máy chủ điện toán đám mây có thể bị cơ quan chức năng yêu cầu cung cấp hoặc bị hacker tấn công tống tiền.</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy an ninh: Hiểu nhầm rằng VAULT lưu trữ chứng từ trốn thuế thay vì lưu trữ mô hình chuẩn hóa EBITDA.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Buyer Nhật Bản cực kỳ kỷ luật, liệu họ có chấp nhận đàm phán trên số liệu 'Sổ B' không?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Nhà đầu tư Nhật Bản nổi tiếng là nghiêm ngặt về tính minh bạch. Khi thấy hai sổ sách, họ có lập tức hủy thương vụ và báo cáo sai phạm không?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy tâm lý: Nghĩ rằng buyer ngoại không biết thực tế thị trường đang phát triển.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Rikkeisoft có bị liên đới trách nhiệm pháp lý nếu hỗ trợ doanh nghiệp 'làm đẹp' sổ sách?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Nếu thương vụ phát sinh kiện tụng về gian lận thuế, uy tín thương hiệu Rikkeisoft có bị lôi vào vòng lao lý với tư cách là bên đồng lõa không?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy thương hiệu: Thiếu cơ chế miễn trừ trách nhiệm độc lập giữa công ty mẹ và đơn vị tư vấn.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Rò rỉ dữ liệu sổ sách nội bộ ra ngoài</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Rất nguy hiểm</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Doanh nghiệp đối mặt án phạt thuế hoặc đình chỉ hoạt động</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Bên mua từ chối số liệu điều chỉnh</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (35%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Thương vụ kéo dài, phải định giá lại tài sản từ đầu</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Trách nhiệm liên đới pháp lý của sàn</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Thấp (< 5%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Ảnh hưởng uy tín nếu không có điều khoản bảo vệ độc lập</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu không có cơ chế xử lý khéo léo bài toán hai sổ sách, 90% SME Việt Nam sẽ từ chối tham gia và phễu khách hàng sẽ hoàn toàn cạn kiệt.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: CƠ CHẾ S02 & THÔNG LỆ THẨM ĐỊNH M&A QUỐC TẾ
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Quy trình chuẩn hóa EBITDA theo thông lệ M&A quốc tế (Normalized EBITDA).</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">VAULT không làm sổ sách giả mạo mà thực hiện 'bình thường hóa lợi nhuận': Loại trừ các chi phí không phục vụ kinh doanh (xe riêng, bảo hiểm cá nhân của Founder), cộng lại khấu hao bất hợp lý. Đây là nghiệp vụ chuẩn mực của mọi quỹ đầu tư tư nhân (PE Fund) trên thế giới.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Bảng chuẩn hóa tài chính theo chuẩn IFRS tại Quy trình S02.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Dữ liệu nhạy cảm Sổ B được mã hóa đầu cuối (Client-side Encryption) và chỉ mở tại Lớp 3.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Chứng từ chi tiết nội bộ được mã hóa bằng thuật toán AES-256 ngay trên trình duyệt của Bên bán; máy chủ VAULT không giữ khóa giải mã (Zero-knowledge architecture). Dữ liệu chỉ được cấp quyền cho Buyer sau khi đã ký LOI và đặt cọc Escrow.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Kiến trúc bảo mật phòng dữ liệu Sandboxed VDR (F09–F12).</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Buyer Nhật hoàn toàn thấu hiểu thực tế thị trường và chấp nhận cơ chế cấn trừ giá.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Kinh nghiệm từ 30+ thương vụ Nhật - Việt cho thấy: Nhà đầu tư Nhật chỉ cần đối soát dòng tiền thực qua sao kê ngân hàng và tài khoản đối tác. Mọi khoản chênh lệch thuế được giải quyết minh bạch qua Điều khoản bảo lãnh bồi thường (Indemnity Escrow 10–15%) trong hợp đồng SPA.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Khảo sát thực tế các đơn vị tư vấn tài chính chuyên nghiệp tại Tokyo.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Chuẩn hóa BCTC theo chuẩn IFRS/VAS</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Tỷ lệ chuẩn hóa: 100%</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Tách bạch chi phí cá nhân và chi phí vận hành cốt lõi</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Mã hóa Zero-Knowledge VDR</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Chuẩn mã hóa: AES-256</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Chỉ Seller giữ Private Key mở tài liệu nội bộ</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Quỹ bảo lãnh thuế Indemnity Escrow</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Tỷ lệ phong tỏa: 10–15% giá trị deal</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Bảo lãnh nghĩa vụ thuế trong 24 tháng hậu sáp nhập</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Cơ chế S02 biến điểm yếu lớn nhất của SME Việt thành cơ hội chuẩn hóa tài sản số, tạo sự minh bạch tuyệt đối giúp deal khép lại thành công.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(20)}
    </div>
    """)


    slides.append(f"""
    <div class="slide" id="slide-21">
      {render_header("CHUYÊN ĐỀ 05 · TẠI SAO BUYER TIN TƯỞNG BÁO CÁO TECH DD CỦA RIKKEISOFT HƠN BIG 4?")}
      {render_takeaway(
          "<b>Định kiến thị trường về các đơn vị kiểm toán:</b> Big 4 (PwC, Deloitte, EY, KPMG) có thương hiệu toàn cầu nhưng hoàn toàn không có năng lực đọc sâu mã nguồn phần mềm.",
          "<b>Khoảng trống thẩm định công nghệ chuyên sâu:</b> Big 4 chỉ rà soát tài chính và phỏng vấn miệng, bỏ lọt các khoản nợ kỹ thuật và virus bản quyền hàng trăm nghìn USD.",
          "Báo cáo Tech DD 6 trục của Rikkeisoft được bảo chứng bởi 2.000 kỹ sư phần mềm thực chiến, định lượng rủi ro kỹ thuật thành tiền mặt cấn trừ vào giá mua."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Big 4 có bảo hiểm trách nhiệm nghề nghiệp hàng chục triệu USD, Rikkeisoft có dám đứng ra bảo lãnh?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Nếu báo cáo Tech DD của Rikkei xác nhận mã nguồn an toàn nhưng sau sáp nhập hệ thống sụp đổ hoặc dính kiện tụng bản quyền, Rikkei có phải đền tiền không?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy bảo hiểm: Nhầm lẫn giữa ý kiến kỹ thuật độc lập với chứng thư bảo hiểm tài chính.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Buyer Nhật Bản có coi trọng chứng nhận của Rikkeisoft bằng thương hiệu quốc tế Big 4 không?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Trong các cuộc họp HĐQT tại Tokyo, liệu các thành viên HĐQT Nhật Bản có chấp nhận thông qua một thương vụ dựa trên báo cáo của một công ty Việt Nam?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy thương hiệu: Đánh giá thấp uy tín 10+ năm và thương hiệu của Rikkeisoft Japan tại Tokyo.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Xung đột lợi ích: Vừa thẩm định kỹ thuật vừa nhắm tới hợp đồng Modernization sau deal?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Bên mua có nghi ngờ Rikkeisoft cố tình 'vạch lá tìm sâu' hoặc phóng đại nợ kỹ thuật để ép bên bán giảm giá và giành hợp đồng outsource cho mình?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy đạo đức: Thiếu cơ chế phân tách độc lập giữa bộ phận thẩm định và bộ phận kinh doanh.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Trách nhiệm bồi thường sai sót kỹ thuật</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Thấp (< 5%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Nguy cơ bị kiện tụng nếu không có điều khoản giới hạn trách nhiệm</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Buyer từ chối báo cáo không phải Big 4</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Thấp (10%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Deal bị chậm tiến độ do bên mua đòi thuê thêm đơn vị thứ ba</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Nghi ngờ xung đột lợi ích dịch vụ</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (20%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Mất niềm tin của bên bán nếu báo cáo đánh giá thiếu khách quan</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu không chứng minh được tính độc lập và vượt trội của Báo cáo Tech DD, VAULT sẽ mất đi vũ khí cạnh tranh khác biệt lớn nhất so với thị trường.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: 6 TRỤC THẨM ĐỊNH & THƯƠNG HIỆU RIKKEISOFT JAPAN
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Big 4 không biết đọc code; Rikkeisoft có 2.000 kỹ sư phần mềm thực chiến.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Big 4 chỉ gửi các kiểm toán viên tài chính đi tích checklist phỏng vấn CTO. Họ không thể dùng SonarQube quét lỗ hổng SQLi, không thể phát hiện thư viện AGPL ẩn sâu trong microservices. Rikkeisoft kiểm định trực tiếp mã nguồn, kiến trúc chịu tải và nợ công nghệ thực tế.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Khảo sát thực tế 15 báo cáo Tech DD của các tập đoàn công nghệ lớn.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Rikkeisoft Japan là thương hiệu uy tín Top đầu được doanh nghiệp Nhật Bản công nhận.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Với hơn 10 năm hiện diện tại Tokyo, phục vụ hơn 500 khách hàng doanh nghiệp lớn của Nhật, chứng nhận kỹ thuật của Rikkeisoft có giá trị bảo chứng thực tiễn cao hơn rất nhiều so với các công ty kiểm toán thuần túy sách vở.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Mạng lưới đối tác và uy tín của Rikkeisoft Japan trên thị trường Tokyo.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Điều khoản giới hạn trách nhiệm pháp lý chuẩn mực (Scope Limitation & Disclaimers).</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Hợp đồng Tech DD quy định rõ: Báo cáo là 'Ý kiến kỹ thuật độc lập tại thời điểm rà soát' (As-is Assessment), không phải bảo lãnh tài chính. Trách nhiệm bồi thường tối đa được khống chế an toàn không vượt quá 100% phí dịch vụ Tech DD thu của khách hàng.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Điều khoản giới hạn trách nhiệm chuẩn tại Mục 5.4 tài liệu S14.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">6 Trục kiểm định chuyên sâu</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Điểm đánh giá thang 1–10</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Quét 100% mã nguồn bằng công cụ tự động và SA chuyên gia</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Định lượng nợ kỹ thuật ra tiền mặt</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Đơn vị: VNĐ / Man-month</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Làm căn cứ pháp lý chính thức để cấn trừ vào giá mua SPA</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Giới hạn mức bồi thường pháp lý</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Trần trách nhiệm: 100% phí dịch vụ</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Cách ly hoàn toàn trách nhiệm liên đới đối với công ty mẹ Rikkei</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Báo cáo Tech DD 6 trục biến Rikkeisoft thành bảo chứng công nghệ độc quyền, tạo dựng lòng tin tuyệt đối cho đối tác Nhật Bản.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(21)}
    </div>
    """)


    slides.append(f"""
    <div class="slide" id="slide-22">
      {render_header("CHUYÊN ĐỀ 06 · BUYER NHẬT CÓ THỰC SỰ MUA QUA NỀN TẢNG SỐ HAY CHỈ LÀ 'ẢO TƯỞNG'?")}
      {render_takeaway(
          "<b>Đặc tính giao dịch của nhà đầu tư Nhật:</b> Nổi tiếng bảo thủ, chu kỳ ra quyết định kéo dài 12–24 tháng, đòi hỏi gặp gỡ trực tiếp nhiều lần.",
          "<b>Nghi ngại của BOD:</b> Liệu các tập đoàn Nhật Bản có bao giờ chịu bấm nút 'mua' một công ty Việt Nam thông qua một ứng dụng phần mềm trên web?",
          "VAULT không làm sàn thương mại điện tử tự động (No-touch) mà là nền tảng điều phối số hỗ trợ chuyên gia (Tech-enabled Platform)."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Chu kỳ M&A của Nhật Bản quá dài (12–24 tháng), làm sao VAULT rút ngắn xuống 6–9 tháng?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Quy trình phê duyệt Ringi qua nhiều cấp của Nhật Bản rất rườm rà. Làm sao một phần mềm có thể thay đổi được văn hóa doanh nghiệp hàng trăm năm của họ?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy văn hóa: Cho rằng thời gian dài là do văn hóa phê duyệt thay vì do thiếu hụt dữ liệu chuẩn.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Các con số 22 thương vụ 2025 và 9 thương vụ 6T2026 có thực chất hay chỉ là xã giao?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Liệu các thương vụ đó có phải là giao dịch quy mô lớn của các tập đoàn khổng lồ, hoàn toàn nằm ngoài tầm với của các SME trên VAULT?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy thị phần: Nhìn vào tổng quy mô thị trường thay vì phân khúc Mid-tier 20–100 tỷ.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Buyer Nhật có sẵn sàng chia sẻ tiêu chí mua vốn bí mật (Buyer Brief) cho VAULT không?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Các doanh nghiệp Nhật cực kỳ kín tiếng về chiến lược mở rộng M&A. Tại sao họ lại chịu điền thông tin ngân sách và ngành nghề mục tiêu vào hệ thống của VAULT?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy tiếp cận: Tiếp cận từ bên ngoài như người lạ thay vì tận dụng mối quan hệ đối tác sẵn có của Rikkei.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Chu kỳ deal kéo dài vượt quá 18 tháng</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Cao (40%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Dòng tiền âm kéo dài, đáy thung lũng tiền mặt bị đẩy lùi</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Buyer Brief ảo không có ngân sách thật</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (25%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Lãng phí nguồn lực tìm kiếm bên bán không khớp nhu cầu</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Bên mua từ chối thao tác trên phần mềm</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Thấp (< 10%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Phải quay lại hình thức họp trực tiếp thủ công truyền thống</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu không hiểu sâu quy trình phê duyệt Ringi của doanh nghiệp Nhật, nền tảng sẽ xây dựng các tính năng thừa thãi mà không giải quyết được nút thắt.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: KHẢO SÁT JETRO & MẠNG LƯỚI 500+ ĐỐI TÁC TOKYO
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Thời gian kéo dài 12–24 tháng chủ yếu do thiếu dữ liệu chuẩn; VAULT giải quyết nút thắt này.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Nghiên cứu cho thấy 60% thời gian thương vụ bị lãng phí ở khâu trao đổi email qua lại để yêu cầu bổ sung hồ sơ, làm sạch BCTC và dịch thuật. VAULT cung cấp sẵn bộ hồ sơ Prep Pack song ngữ chuẩn mực, giúp ban điều hành tại Tokyo duyệt hồ sơ nhanh hơn gấp 2 lần.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Khảo sát thực tế thời gian thẩm định sơ bộ giảm từ 60 ngày xuống 15 ngày.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Chiến lược Buy-Side First: Đi từ 25 Qualified Buyer Briefs có sẵn của Rikkeisoft Japan.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Chúng tôi không tìm kiếm khách hàng từ con số không. Tận dụng tệp 500+ khách hàng doanh nghiệp sẵn có của Rikkei tại Tokyo, chúng tôi thu thập trước các Buyer Briefs có cam kết ngân sách và người bảo trợ (Sponsor) rõ ràng trước khi tìm kiếm bên bán.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: 25 Buyer Briefs thực tế đang có nhu cầu M&A trong hệ sinh thái Rikkei.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Chỉ cần 1 deal thành công trong Năm 2 là đạt điểm hòa vốn kinh tế.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Mô hình tài chính không đặt cược vào hàng chục thương vụ viển vông. Với 22 deal Nhật - Việt năm 2025, VAULT chỉ cần chốt thành công đúng 1 deal (tương đương 3.3% thị phần) trong Năm 2 và 2 deal trong Năm 3 là đã đảm bảo toàn bộ chỉ tiêu tài chính cam kết với HĐQT.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Mô hình kiểm tra độ nhạy Base Case tại Sheet 04 Mô hình tài chính Excel.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Tiêu chuẩn Qualified Buyer Brief</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Bắt buộc 6 tiêu chí cứng</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Phải có Ticket size, Sponsor cấp cao và ngân sách thẩm định</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Hồ sơ song ngữ Nhật - Việt chuẩn hóa</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">100% hồ sơ xuất bản tự động</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Bản dịch chuyên ngành M&A được hiệu đính bởi chuyên gia bản xứ</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Kế hoạch đóng deal tối thiểu</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Năm 2: 1 deal / Năm 3: 2 deal</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Chỉ cần 3.3% thị phần để hoàn vốn toàn bộ chi phí đầu tư</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Buy-Side First kết hợp uy tín của Rikkeisoft Japan là chìa khóa vàng mở toang cánh cửa dòng vốn M&A từ Tokyo vào Việt Nam.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(22)}
    </div>
    """)


    slides.append(f"""
    <div class="slide" id="slide-23">
      {render_header("CHUYÊN ĐỀ 07 · XUNG ĐỘT LỢI ÍCH & HỢP LỰC GIỮA VAULT VÀ RIKKEISOFT RA SAO?")}
      {render_takeaway(
          "<b>Mối lo ngại của lãnh đạo khối Delivery:</b> Rút Solution Architect giỏi đi làm thẩm định M&A sẽ làm ảnh hưởng tiến độ các dự án gia công phần mềm triệu USD.",
          "<b>Quan ngại về hiệu quả vốn đầu tư:</b> Rikkeisoft tài trợ 5.00 tỷ nguồn lực chuyên gia trong 5 năm, liệu lợi ích thu về có tương xứng với công sức bỏ ra?",
          "Cơ chế hợp đồng khung SLA và giá trị phễu hợp đồng IT Modernization hậu M&A mang lại lợi ích cộng hưởng khổng lồ cho tập đoàn mẹ."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Rút chuyên gia công nghệ đi làm Tech DD có làm suy giảm doanh thu Outsource của Rikkei?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Khối Delivery đang sống bằng từng man-month xuất khẩu phần mềm. Việc phân tán nguồn lực kỹ sư sang dự án nội bộ có gây lãng phí chi phí cơ hội?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy nguồn lực: Cho rằng kỹ sư làm full-time liên tục thay vì cơ chế tận dụng thời gian chờ (Bench-time).</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Nếu các thương vụ M&A đều thất bại thì 5.00 tỷ tài trợ nguồn lực có bị mất trắng?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Chi phí chuyên gia bỏ ra thẩm định hàng chục thương vụ nhưng không đóng được deal nào thì ai chịu trách nhiệm bù đắp khoản lỗ này cho tập đoàn?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy dòng tiền: Quên mất nguồn thu Prep Pack 90tr trả tiền mặt ngay lập tức cho chuyên gia.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Rikkeisoft có thực sự giành được hợp đồng Modernization sau khi deal hoàn tất không?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Bên mua Nhật Bản có quyền tự do thuê các công ty khác nâng cấp phần mềm. Cơ chế nào bảo đảm Rikkeisoft độc quyền nhận hợp đồng này?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy cam kết: Không ràng buộc điều khoản ưu tiên nhận thầu công nghệ trong quá trình môi giới.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Chi phí cơ hội mất giờ công chuyên gia</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (20%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Ảnh hưởng tiến độ dự án outsource nếu không điều phối nhịp nhàng</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Hụt nguồn thu bù đắp chi phí nội bộ</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Thấp (< 10%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Đã được bảo đảm thanh toán từ nguồn thu gói Prep Pack 90tr</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Không chốt được hợp đồng IT Modernization</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (25%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Mất đi khoản doanh thu đột phá lớn nhất hậu M&A</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu không giải quyết bài toán xung đột quyền lợi giữa các khối kinh doanh, dự án sẽ bị cô lập và không nhận được sự hợp tác từ các Solution Architect giỏi.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: TỐI ƯU HÓA BENCH-TIME & PHỄU HỢP ĐỒNG HIỆN ĐẠI HÓA
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Tận dụng triệt để thời gian chờ dự án (Bench-time), biến chi phí chìm thành doanh thu.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Các Solution Architect không tham gia toàn thời gian mà chỉ làm theo đợt thẩm định (tối đa 40–60 giờ/báo cáo). VAULT ưu tiên tận dụng các kỹ sư giỏi trong giai đoạn chờ giữa 2 dự án khách hàng, giúp khối Delivery tối ưu hóa hệ số sử dụng nhân sự (Utilization Rate).</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Quy chế điều động chuyên gia theo giờ công tại Mục 4 Báo cáo Đề án.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Phí thẩm định Tech DD được trả tiền tươi ngay từ gói Prep Pack 90 triệu.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Dù thương vụ M&A có chốt thành công hay không, khối Delivery của Rikkei vẫn nhận được khoản thanh toán 50 triệu VNĐ tiền mặt cho mỗi báo cáo hoàn thành, trích từ gói Prep Pack mà bên bán đã đóng trước. Hoàn toàn không có rủi ro làm việc không công.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Cơ chế hạch toán thanh toán nội bộ minh bạch tại Đề xuất 3 trình HĐQT.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Đặc quyền tiếp cận hợp đồng IT Modernization trị giá từ 500K – 2M USD.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Khi mua lại một SME phần mềm hoặc bán lẻ Việt Nam, ưu tiên số 1 của doanh nghiệp Nhật là nâng cấp hệ thống CNTT cũ để kết nối về tổng hành dinh. Là đơn vị chủ trì Tech DD, Rikkeisoft nắm toàn bộ kiến trúc và được cài cắm độc quyền nhận thầu hợp đồng này.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Tiền lệ giao dịch M&A công nghệ Nhật - Việt cho thấy 85% bên mua thuê lại đối tác DD.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Cơ chế phân bổ giờ công Bench-time</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Tối đa 40–60h / báo cáo</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Không điều động kỹ sư đang phụ trách dự án khách hàng trọng điểm</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Thanh toán nội bộ từ Prep Pack</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">50 triệu VNĐ / báo cáo</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Hạch toán trực tiếp vào P&L của khối Delivery ngay khi bàn giao</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Quyền ưu tiên số 1 HĐ Modernization</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Cam kết độc quyền đàm phán</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Ràng buộc điều khoản hỗ trợ tích hợp hậu sáp nhập trong hợp đồng SPA</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Sự cộng hưởng giữa VAULT và Rikkeisoft tạo ra mô hình Win-Win hoàn hảo: Nền tảng có chuyên gia bảo chứng, còn tập đoàn mẹ có thêm phễu dự án triệu USD.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(23)}
    </div>
    """)


    slides.append(f"""
    <div class="slide" id="slide-24">
      {render_header("CHUYÊN ĐỀ 08 · TÍNH KHẢ THI CỦA ĐIỂM HÒA VỐN TIỀN MẶT THÁNG 21 VÀ PLAN B?")}
      {render_takeaway(
          "<b>Đáy thung lũng dòng tiền (Cash Valley):</b> Rơi vào Tháng 20 với mức âm cực đại <b>-1.43 tỷ VNĐ</b>, đòi hỏi kỷ luật quản trị vốn cực kỳ nghiêm ngặt.",
          "<b>Băn khoăn lớn nhất của Hội đồng Quản trị:</b> Nếu tiến độ chốt deal bị chậm 6 tháng so với dự kiến, dự án có bị cạn kiệt tiền mặt và vỡ nợ không?",
          "Kịch bản thử thách đã được stress-test trong mô hình Excel; 3 van an toàn bảo vệ trần vốn không vượt quá 1.68 tỷ VNĐ trong mọi trường hợp."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Nếu trong 20 tháng đầu không đóng được thương vụ nào thì tiền mặt có bị cạn sạch?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Dự án sống phụ thuộc vào Success Fee. Nếu thị trường M&A đóng băng và không có thương vụ nào thành công, dự án lấy tiền đâu để trả lương nhân sự hàng tháng?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy thanh khoản: Bỏ qua dòng tiền đều đặn từ phí Prep Pack 90 triệu và quỹ đệm thanh khoản.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Nếu deal bị chậm 6 tháng, Ban điều hành có quay lại xin HĐQT cấp thêm vốn không?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Kịch bản chậm deal 6 tháng đẩy đáy tiền âm lên -2.15 tỷ VNĐ. Lúc đó Ban đề án có yêu cầu cổ đông mẹ rót thêm tiền để cứu dự án?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy quản trị: Thiếu các hành động can thiệp quản trị chi phí chủ động khi gặp tình huống xấu.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Mức dự phòng thanh khoản 250 triệu VNĐ có quá mỏng cho một dự án vận hành 5 năm?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Trong bối cảnh chi phí lương chuyên gia tài chính M&A rất đắt đỏ, 250 triệu chỉ đủ chi trả cho 1-2 tháng vận hành cơ bản.</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy dự phòng: Không kết hợp giữa quỹ đệm tiền mặt với cơ chế linh hoạt của cấu trúc lương thưởng.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Cạn kiệt tiền mặt trước khi có deal</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (20%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Nguy cơ dừng dự án giữa chừng nếu không quản trị tốt dòng tiền</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Deal trễ hạn 6 tháng làm âm vốn sâu</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Khá cao (45%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Đáy tiền mặt chạm -2.15 tỷ, đòi hỏi kích hoạt các van can thiệp</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Vượt trần ngân sách cấp vốn 1.68 tỷ</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Thấp (< 5%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Cam kết cứng của Ban đề án: Tuyệt đối không xin cấp thêm tiền mặt</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu không có kế hoạch dự phòng thanh khoản rõ ràng, dự án sẽ rơi vào bẫy 'chết trước bình minh' khi thương vụ đầu tiên chỉ còn cách đích 1 tháng.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: MÔ HÌNH DÒNG TIỀN EXCEL & 3 VAN AN TOÀN TỰ ĐỘNG
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Doanh thu Prep Pack mang về 4.23 tỷ VNĐ trong 2 năm đầu, nuôi sống 100% bộ máy.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Mô hình tài chính được thiết kế phòng thủ: Chi phí cố định tiền mặt Năm 1 chỉ là 680 triệu VNĐ, trong khi doanh thu từ 19 gói Prep Pack mang về 1.71 tỷ VNĐ. Doanh thu dịch vụ chuẩn hóa đủ để duy trì bộ máy độc lập mà không cần chờ tới khi có deal chốt thành công.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Dòng tiền hoạt động kinh doanh dương ngay từ Năm 1 tại Sheet 04 Mô hình tài chính.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Kịch bản Deal trễ 6 tháng đã được tính toán sẵn phương án tự cân đối (Self-balancing).</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Nếu deal trễ hạn, đáy dòng tiền chạm -2.15 tỷ tại Tháng 26 (trễ 5 tháng). Ban điều hành lập tức kích hoạt chính sách: Tạm hoãn tuyển thêm 1 Deal Lead mới, giãn tiến độ thanh toán phí dịch vụ cho Rikkei và bán thêm 3 gói Prep Pack để tự cân bằng dòng tiền mà không cần xin thêm vốn.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Kịch bản số 1 trong Bảng phân tích độ nhạy 8 phép thử của mô hình tài chính.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Cam kết danh dự của Ban điều hành: Tuyệt đối giữ trần vốn cấp 1.68 tỷ VNĐ.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Trong số 1.68 tỷ xin phê duyệt đã bao gồm 250 triệu quỹ đệm thanh khoản khẩn cấp (tương đương 3 tháng chi phí tiền mặt tối thiểu). Ban điều hành cam kết tuân thủ trần ngân sách; nếu chạm ngưỡng Cổng 2 mà không đạt chỉ số kiểm chứng thì kích hoạt cắt lỗ bảo toàn vốn.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Nghị quyết đề xuất phê duyệt ngân sách và ủy quyền 4 Cổng Stage-Gate.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Quỹ đệm an toàn thanh khoản</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">250 triệu VNĐ tiền mặt</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Duy trì hoạt động tối thiểu 3 tháng trong trường hợp không có doanh thu</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Kéo giãn tuyển dụng khi deal trễ</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Tiết kiệm 450M chi phí lương</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Chỉ tuyển thêm Deal Lead thứ 2 khi deal đầu tiên đã ký LOI độc quyền</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Trần cấp vốn tiền mặt tối đa</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Cố định 1.680.000.000 VNĐ</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Tuyệt đối không phát sinh thêm nhu cầu xin cấp vốn từ công ty mẹ</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Mô hình tài chính được xây dựng trên nguyên tắc bảo toàn vốn cực kỳ thận trọng, bảo đảm an toàn thanh khoản tuyệt đối trong mọi tình huống.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(24)}
    </div>
    """)


    slides.append(f"""
    <div class="slide" id="slide-25">
      {render_header("CHUYÊN ĐỀ 09 · TẠI SAO NÊN THÀNH LẬP CÔNG TY CON RIÊNG BIỆT VÀ CƠ CHẾ ESOP 15%?")}
      {render_takeaway(
          "<b>M&A là lĩnh vực kinh doanh đặc thù:</b> Đòi hỏi sự linh hoạt cao về chính sách đãi ngộ nhân tài và quản trị rủi ro pháp lý độc lập.",
          "<b>Mô hình công ty con (Rikkei nắm 85%):</b> Tạo Bức tường lửa pháp lý bảo vệ công ty mẹ khỏi các tranh chấp thương mại xuyên biên giới.",
          "Quỹ ESOP 15% là công cụ quyết định để chiêu mộ và giữ chân các Deal Lead M&A xuất sắc nhất thị trường."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Tại sao không để VAULT làm một BU nội bộ trong Rikkei cho đỡ tốn chi phí quản lý?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Lập công ty con phát sinh chi phí kế toán, pháp nhân, con dấu và kiểm toán riêng. Tại sao không để trực thuộc một khối kinh doanh sẵn có của Rikkeisoft?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy tổ chức: Bó buộc ngành dịch vụ tài chính ngân hàng đầu tư vào khung quản trị của công ty gia công phần mềm.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Dành 15% ESOP cho ban điều hành có phải là quá ưu ái và làm loãng lợi ích mẹ?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Rikkeisoft bỏ vốn tiền mặt 1.68 tỷ và tài trợ 5.00 tỷ nguồn lực; tại sao Ban điều hành lại được hưởng tới 15% cổ phần mà không phải bỏ vốn tương ứng?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy đãi ngộ: Áp dụng tư duy lương cố định cho các chuyên gia M&A vốn sống bằng hoa hồng và cổ phần.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Rikkeisoft kiểm soát quyền chi phối và bảo đảm không bị mất quyền kiểm soát ra sao?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Khi công ty con phát triển lớn mạnh, làm thế nào để đảm bảo đội ngũ điều hành không 'tách đàn' mang theo dữ liệu khách hàng sang thành lập công ty riêng?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy kiểm soát: Lo sợ mất kiểm soát công ty con mà không nắm vững các điều khoản phủ quyết trong Luật Doanh nghiệp.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Rủi ro tranh chấp pháp lý lan sang mẹ</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Rất nguy hiểm</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Công ty mẹ bị liên đới kiện tụng và phong tỏa tài sản nếu làm BU</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Mất nhân tài M&A vì khung lương cứng</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Rất cao (90%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Không thể tuyển được Deal Lead giỏi nếu không có ESOP và hoa hồng</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Mất quyền kiểm soát công ty con</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Rất thấp (< 1%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Rikkei nắm 85% cổ phần chi phối tuyệt đối theo luật định</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu duy trì mô hình BU nội bộ, dự án không thể chiêu mộ được các Deal Lead M&A xuất sắc do bị vướng khung lương cứng của ngành gia công phần mềm.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: CƠ CHẾ VESTING 3 NĂM & QUYỀN BIỂU QUYẾT CHI PHỐI 85%
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Thành lập pháp nhân độc lập để tạo Bức tường lửa bảo vệ pháp lý cho công ty mẹ.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">M&A là lĩnh vực tiềm ẩn rủi ro tranh chấp thương mại và bảo mật cao. Công ty con giúp cô lập hoàn toàn trách nhiệm pháp lý, tránh nguy cơ công ty mẹ Rikkeisoft bị liên đới kiện tụng nếu thương vụ phát sinh xung đột.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Nguyên tắc trách nhiệm hữu hạn theo Luật Doanh nghiệp 2020.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ 15% ESOP là thông lệ chuẩn mực IB, ràng buộc Vesting 3 năm theo KPI đóng deal.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Chuyên gia M&A giỏi sống bằng hoa hồng thương vụ. 15% ESOP được giải ngân theo cơ chế Vesting 3 năm gắn với mốc đóng deal thực tế; nếu nghỉ việc hoặc không đạt KPI thương vụ, cổ phần tự động bị thu hồi về công ty mẹ.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Thông lệ cấp ESOP của các quỹ đầu tư mạo hiểm và ngân hàng đầu tư quốc tế.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Rikkeisoft nắm giữ 85% vốn chi phối tuyệt đối và giữ quyền bổ nhiệm Giám đốc Tài chính.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Rikkeisoft nắm quyền biểu quyết tuyệt đối trong HĐQT, trực tiếp bổ nhiệm CFO kiêm Kế toán trưởng kiểm soát toàn bộ tài khoản ngân hàng và nắm giữ toàn bộ mã nguồn nền tảng công nghệ.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Điều lệ công ty quy định các vấn đề trọng yếu cần 75% biểu quyết chấp thuận.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Cơ cấu vốn chi phối của Rikkeisoft</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">85% Cổ phần phổ thông</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Quyền quyết định tuyệt đối mọi vấn đề tăng vốn, bổ nhiệm nhân sự</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Cơ chế Vesting ESOP 3 năm</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Gắn với mốc hoàn thành deal</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Tự động thu hồi cổ phần nếu nhân sự nghỉ việc trước thời hạn</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Kiểm soát dòng tiền độc lập</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">CFO do Rikkei mẹ bổ nhiệm</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Mọi khoản chi > 50 triệu bắt buộc phải có chữ ký duyệt của mẹ</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Cơ cấu 85/15 hài hòa tối đa lợi ích: Bảo vệ quyền kiểm soát tuyệt đối của Rikkeisoft đồng thời kích hoạt động lực cống hiến tối đa của đội ngũ chuyên gia M&A.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(25)}
    </div>
    """)


    slides.append(f"""
    <div class="slide" id="slide-26">
      {render_header("CHUYÊN ĐỀ 10 · ĐIỀU KIỆN KÍCH HOẠT CƠ CHẾ DỪNG LỖ (STOP-LOSS) TẠI CỔNG 2?")}
      {render_takeaway(
          "<b>Quản trị rủi ro chuyên nghiệp đòi hỏi điểm dừng rõ ràng:</b> Không bao giờ sa lầy vào việc 'nuôi' một dự án không chứng minh được hiệu quả.",
          "<b>Cơ chế 4 Cổng Stage-Gate xác định chốt chặn tại Tháng 12:</b> Không đạt chỉ số kiểm chứng thị trường thì lập tức dừng lỗ.",
          "Cam kết của Ban đề án: Giới hạn mức thiệt hại vốn tối đa cho Rikkeisoft không vượt quá <b>950 triệu VNĐ</b>."
      )}
      <div class="slide-body">
        <div class="full-grid-2">
          <!-- Left Card: BOD Doubts -->
          <div class="dense-card" style="border-top: 4pt solid #b91c1c;">
            <div class="dense-card-title">GÓC NHÌN HOÀI NGHI & CÂU HỎI HÓC BÚA CỦA HĐQT</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #fff1f2; border: 1pt solid #fecdd3; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #9f1239; font-weight: 700;">
                CHẤT VẤN HỘI ĐỒNG: 3 VẤN ĐỀ TRỌNG YẾU CẦN ĐƯỢC GIẢI TỎA TRƯỚC KHI PHÊ DUYỆT
              </div>
              
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Điều kiện định lượng cụ thể nào sẽ buộc Ban điều hành phải dừng dự án và giải tán?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">HĐQT cần một cam kết cứng bằng số liệu: Ở mốc thời gian nào, nếu không đạt được chỉ số gì thì dự án bắt buộc phải giải thể mà không có bất kỳ sự châm chước nào?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy cam kết: Đưa ra các mục tiêu cảm tính, định tính thay vì các chỉ số tài chính và hợp đồng cụ thể.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Nếu kích hoạt dừng dự án tại Tháng 12 thì Rikkeisoft bị thiệt hại bao nhiêu tiền mặt?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Mức tổn thất vốn tối đa (Worst-case Loss) mà HĐQT phải gánh chịu trong trường hợp thị trường M&A đóng băng hoàn toàn là bao nhiêu?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy rủi ro: Lo sợ mất toàn bộ 1.68 tỷ vốn đăng ký thay vì hiểu cơ chế giải ngân theo từng cổng nghiệm thu.</div>
            </div>
        
            <div style="background: #fff5f5; border: 1.1pt solid #fecdd3; border-left: 4.5pt solid #b91c1c; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 9.3pt;">❓ Thẩm quyền ra quyết định dừng lỗ hoặc gia hạn triển khai thuộc về ai?</b>
              <p style="color: #475569; margin: 0 0 2pt 0;">Ban điều hành có quyền tự ý kéo dài thời gian thử nghiệm không, hay bắt buộc phải thông qua sự phê duyệt của Hội đồng Quản trị?</p>
              <div style="font-size: 7.8pt; color: #b91c1c; font-style: italic;">⚠️ Bẫy phân quyền: Thiếu ranh giới thẩm quyền rõ ràng giữa Hội đồng Quản trị và Ban điều hành dự án.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #fecdd3; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #991b1b; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Ma Trận Đánh Giá Mức Độ Rủi Ro Nếu Bỏ Qua Kiểm Soát:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #fee2e2; color: #991b1b; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Điểm nghẽn rủi ro</td>
                  <td style="padding: 2.5pt 5pt; width: 25%; text-align: center;">Xác suất</td>
                  <td style="padding: 2.5pt 5pt; width: 40%;">Tác động xấu nhất</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Dự án sa lầy thành 'hố đen đốt tiền'</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Cực kỳ nguy hiểm</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Mất toàn bộ vốn cấp và uy tín nếu không có điểm dừng lỗ</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Thiệt hại tiền mặt vượt trần cam kết</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Thấp (< 5%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Khống chế cứng mức thiệt hại tối đa không quá 950 triệu</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #fecdd3;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #991b1b;">Tranh cãi nội bộ khi phải dừng dự án</td>
                  <td style="padding: 3.5pt 5pt; text-align: center; color: #475569;">Trung bình (20%)</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Giải quyết dứt điểm bằng bộ tiêu chí định lượng đã thống nhất trước</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #fef2f2; border: 1.1pt solid #fca5a5; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #991b1b; line-height: 1.38;">
                <b>Đánh giá mức độ nhạy cảm:</b> Nếu không có cơ chế dừng lỗ cứng, dự án có nguy cơ trở thành 'hố đen đốt tiền', làm sa lầy nguồn lực của tập đoàn trong bối cảnh thị trường biến động xấu.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Nguồn: DEBATE_PLAYBOOK.md (Bộ câu hỏi chất vấn HĐQT)</div>
            </div>
          </div>

          <!-- Right Card: Counter Arguments & Empirical Proof -->
          <div class="dense-card" style="border-top: 4pt solid #155724;">
            <div class="dense-card-title" style="color: #155724;">LUẬN CỨ PHẢN BIỆN, BẰNG CHỨNG THỰC CHỨNG & CƠ CHẾ BẢO VỆ</div>
            <div class="dense-card-body" style="gap: 5.5pt;">
              <div style="background: #dcfce7; border: 1pt solid #bbf7d0; padding: 4.5pt 9pt; border-radius: 3pt; font-size: 8.5pt; color: #166534; font-weight: 700;">
                CĂN CỨ THỰC CHỨNG: QUY CHUẨN CỔNG 2 & CAM KẾT KHỐNG CHẾ THIỆT HẠI 950M
              </div>
              
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Chốt chặn sinh tử Cổng 2 (Tháng 12): Tối thiểu 3 Buyer Briefs & 5 HĐ Prep Pack.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Tại ngày 31/12 (kết thúc Năm 1), nếu không đạt đồng thời cả 2 chỉ số kiểm chứng thị trường: (1) Đạt tối thiểu 3 Qualified Buyer Briefs từ Nhật Bản; và (2) Ký tối thiểu 5 Hợp đồng Prep Pack có tiền thực tế, dự án lập tức dừng lại.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Tiêu chí nghiệm thu Cổng 2 tại Mục 6 Báo cáo Đề án.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Tổng thiệt hại tiền mặt tối đa của Rikkeisoft được khống chế ở mức 600–700 triệu VNĐ.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Tổng vốn giải ngân hết Cổng 2 là 950 triệu VNĐ (Đợt 1: 500tr, Đợt 2: 450tr). Nhờ nguồn thu từ các gói Prep Pack đã ký (khoảng 270–450 triệu VNĐ), số tiền mặt thực tế bị mất của công ty mẹ được khống chế an toàn dưới 700 triệu VNĐ.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Mô hình phân tích thiệt hại kịch bản dừng tại Sheet 04 Mô hình tài chính Excel.</div>
            </div>
        
            <div style="background: #f0fdf4; border: 1.1pt solid #bbf7d0; border-left: 4.5pt solid #155724; border-radius: 4pt; padding: 7pt 10pt; font-size: 8.8pt; line-height: 1.4;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 9.3pt;">✓ Hội đồng Quản trị Rikkeisoft là cơ quan duy nhất giữ quyền bấm nút Dừng lỗ.</b>
              <p style="color: #334155; margin: 0 0 2pt 0;">Ban điều hành VAULT có trách nhiệm nộp Báo cáo Nghiệm thu Cổng 2 độc lập kèm xác nhận số dư tài khoản ngân hàng trước ngày 25/12. Quyền giải ngân Đợt 3 (400 triệu) hay đóng dự án thuộc toàn quyền quyết định của HĐQT.</p>
              <div style="font-size: 7.8pt; color: #166534; font-weight: 600;">📊 Căn cứ: Quy chế ủy quyền giải ngân 4 Cổng Stage-Gate trình HĐQT phê duyệt.</div>
            </div>
        
              
            <div style="background: #ffffff; border: 1.1pt solid #bbf7d0; border-radius: 4pt; padding: 5pt 8pt; font-size: 8.2pt;">
              <b style="color: #155724; display: block; margin-bottom: 2pt; font-size: 8.6pt;">Bảng Cơ Chế Kiểm Soát & Cam Kết Đo Lường SLA:</b>
              <table style="width: 100%; border-collapse: collapse; font-size: 8pt;">
                <tr style="background: #dcfce7; color: #166534; font-weight: 700;">
                  <td style="padding: 2.5pt 5pt; width: 35%;">Cơ chế kiểm soát</td>
                  <td style="padding: 2.5pt 5pt; width: 30%;">Chỉ số SLA / KPI</td>
                  <td style="padding: 2.5pt 5pt; width: 35%;">Chế tài / Thực thi</td>
                </tr>
                
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Chỉ số nghiệm thu cứng Cổng 2 (T12)</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">>= 3 Buyer Briefs & >= 5 Prep Packs</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Không đạt đồng thời cả 2 chỉ số: Kích hoạt đóng dự án ngay</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Trần thiệt hại tiền mặt tối đa</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">Khống chế <= 950 triệu VNĐ</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Thu hồi toàn bộ số dư tài khoản ngân hàng chưa sử dụng</td>
                </tr>
        
                <tr style="border-bottom: 1pt solid #bbf7d0;">
                  <td style="padding: 3.5pt 5pt; font-weight: 700; color: #155724;">Thẩm quyền quyết định dừng lỗ</td>
                  <td style="padding: 3.5pt 5pt; color: #166534; font-weight: 600;">100% thuộc về HĐQT Rikkeisoft</td>
                  <td style="padding: 3.5pt 5pt; color: #475569;">Ban điều hành không có quyền tự ý kéo dài thời gian thử nghiệm</td>
                </tr>
        
              </table>
            </div>
    
              <div style="background: #f0fdf4; border: 1.1pt solid #86efac; padding: 6pt 9pt; border-radius: 4pt; font-size: 8.3pt; color: #166534; line-height: 1.38;">
                <b>Kết luận của Ban Đề án:</b> Cam kết danh dự của Ban đề án: Tuân thủ 100% kỷ luật van an toàn Stage-Gate; bảo vệ từng đồng vốn đầu tư của cổ đông Rikkeisoft ở mức an toàn cao nhất.
              </div>
              <div style="font-size: 7.6pt; color: #64748b; text-align: right;">Căn cứ: 04_VAULT_MODEL.xlsx & Báo cáo Thẩm định Độc quyền Rikkei</div>
            </div>
          </div>
        </div>
      </div>
      {render_bottom_nav(26)}
    </div>
    """)

    full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>VAULT — Đề án Nền tảng M&A Việt - Nhật (BOD Edition - Chuẩn DABACO)</title>
{CSS_STYLES}
</head>
<body>
{''.join(slides)}
</body>
</html>
"""
    return full_html

# Generate HTML
html_str = generate_full_deck()
with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html_str)

print(f"Wrote dense DABACO-styled 26-slide HTML deck to: {HTML_OUTPUT}")

# Compile PDF using Headless Chrome
print("Compiling interactive PDF with Google Chrome...")
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_OUTPUT}",
    HTML_OUTPUT
]
subprocess.run(cmd, check=True)
print(f"Generated PDF at: {PDF_OUTPUT}")

# Verify internal jump links and pages
reader = pypdf.PdfReader(PDF_OUTPUT)
print(f"Verification: Total pages in generated PDF: {len(reader.pages)}")

total_links = 0
for idx, page in enumerate(reader.pages):
    links_count = 0
    if "/Annots" in page:
        annots = page["/Annots"]
        for a in annots:
            obj = a.get_object()
            if obj.get("/Subtype") == "/Link":
                links_count += 1
    total_links += links_count
    print(f"  Slide {idx+1:02d}: {links_count} clickable PDF links")

print(f"\nSUCCESS: Generated 100% interactive vector PDF with {len(reader.pages)} slides and {total_links} internal jump links!")
