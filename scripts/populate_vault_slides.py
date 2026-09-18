"""
Script to complete DB_VAULT_KHUNG_SLIDE.pptx according to:
1. DABACO.pdf investment pitch framework (6 pillars, rich metrics, risk matrix, appendix structure)
2. DB_REPORT MO TA CHUC NANG (1).docx (VAULT functional specs, 20 steps, Trust Profile 3 layers, VDR, Tech DD)
3. 01_VAULT_REPORT.md (financial projections, breakeven, cap table, Rikkei synergies)
4. DEBATE_PLAYBOOK.md (6 strategic debate clusters as the interactive Appendix)
"""

import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Color Palette
COLOR_RED = RGBColor(0xB4, 0x23, 0x18)       # #B42318 Rikkei Crimson
COLOR_DARK = RGBColor(0x1A, 0x1A, 0x1A)      # #1A1A1A Body & Heading text
COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)     # #555555 Muted secondary text
COLOR_LIGHT_BG = RGBColor(0xF8, 0xF9, 0xFA)  # Light container
COLOR_BORDER = RGBColor(0xDE, 0xE2, 0xE6)    # Neutral border
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)     # White
COLOR_TINT = RGBColor(0xFD, 0xED, 0xEC)      # Soft red tint
COLOR_ZEBRA = RGBColor(0xFA, 0xFA, 0xFA)     # Off-white zebra row

FONT_NAME = "Arial"

def clear_and_set_text(shape, text, font_size=12, bold=False, color=COLOR_DARK, align=PP_ALIGN.LEFT):
    """Sets simple single-string text on a shape while preserving shape properties."""
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = FONT_NAME
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return p

def add_paragraph(tf, text, font_size=10, bold=False, color=COLOR_DARK, space_before=3, space_after=1, align=PP_ALIGN.LEFT):
    """Adds a paragraph to a text frame with specific formatting."""
    p = tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    run = p.add_run()
    run.text = text
    run.font.name = FONT_NAME
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return p

def add_key_value(tf, key, value, font_size=9.5, key_bold=True, key_color=COLOR_RED, val_color=COLOR_DARK, space_before=3, space_after=1):
    """Adds a paragraph with bold key prefix and regular value."""
    p = tf.add_paragraph()
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    
    r_key = p.add_run()
    r_key.text = key + " "
    r_key.font.name = FONT_NAME
    r_key.font.size = Pt(font_size)
    r_key.font.bold = key_bold
    r_key.font.color.rgb = key_color
    
    r_val = p.add_run()
    r_val.text = value
    r_val.font.name = FONT_NAME
    r_val.font.size = Pt(font_size)
    r_val.font.bold = False
    r_val.font.color.rgb = val_color
    return p

def format_cell(cell, text, font_size=9.5, bold=False, text_color=COLOR_DARK, bg_color=None, align=PP_ALIGN.LEFT):
    """Formats a table cell with padding, background color, and styled text."""
    cell.text = text
    if bg_color:
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color
    p = cell.text_frame.paragraphs[0]
    p.alignment = align
    if p.runs:
        run = p.runs[0]
        run.font.name = FONT_NAME
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = text_color

def populate_deck(src_path, dst_path):
    prs = pptx.Presentation(src_path)
    print(f"Loaded presentation with {len(prs.slides)} slides from {src_path}")

    # -------------------------------------------------------------
    # UPDATE FOOTER BUTTONS ON SLIDES 2 TO 8 (LINK_2 to LINK_7)
    # -------------------------------------------------------------
    footer_labels = [
        ("LINK_2", "01. THỊ TRƯỜNG"),
        ("LINK_3", "02. TỔNG QUAN"),
        ("LINK_4", "03. TÍNH NĂNG"),
        ("LINK_5", "04. VŨ KHÍ"),
        ("LINK_6", "05. VẬN HÀNH"),
        ("LINK_7", "06. KINH TẾ"),
    ]
    for slide_idx in range(1, 8):
        slide = prs.slides[slide_idx]
        for shape in slide.shapes:
            for l_name, l_text in footer_labels:
                if shape.name == l_name:
                    tf = shape.text_frame
                    tf.paragraphs[0].text = l_text
                    if tf.paragraphs[0].runs:
                        tf.paragraphs[0].runs[0].font.name = FONT_NAME
                        tf.paragraphs[0].runs[0].font.size = Pt(9.5)
                        tf.paragraphs[0].runs[0].font.bold = True
                        tf.paragraphs[0].runs[0].font.color.rgb = COLOR_DARK

    # -------------------------------------------------------------
    # SLIDE 1: COVER SLIDE
    # -------------------------------------------------------------
    slide1 = prs.slides[0]
    for s in slide1.shapes:
        if s.name == "text" and s.shape_id == 3:
            clear_and_set_text(s, "ĐỀ ÁN NỀN TẢNG M&A VAULT", font_size=36, bold=True, color=COLOR_WHITE)
        elif s.name == "text" and s.shape_id == 4:
            clear_and_set_text(s, "Nền tảng Điều phối M&A và Hợp tác Đầu tư Việt - Nhật trong Hệ sinh thái Rikkeisoft", font_size=15, bold=False, color=COLOR_WHITE)
        elif s.name == "text" and s.shape_id == 5:
            clear_and_set_text(s, "Ban Dự án VAULT · Báo cáo Trình Hội đồng Quản trị (BOD)", font_size=12, bold=True, color=COLOR_MUTED)
        elif s.name == "text" and s.shape_id == 6:
            clear_and_set_text(s, "Tháng 09/2026 · Bản Đề án Chiến lược & Khung Trình diễn", font_size=11, bold=False, color=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 2: MỤC 01: THỊ TRƯỜNG & NỖI ĐAU
    # -------------------------------------------------------------
    slide2 = prs.slides[1]
    for s in slide2.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "01. BỐI CẢNH THỊ TRƯỜNG & KHOẢNG TRỐNG M&A NHẬT - VIỆT", font_size=20, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 12:
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "THỰC TRẠNG DÒNG VỐN & 3 ĐIỂM NGHẼN CHÍ TỬ KHIẾN HƠN 80% THƯƠNG VỤ SƠ BỘ ĐỔ VỠ"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(12.5)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(8)

            add_key_value(tf, "1. Làn sóng M&A dịch chuyển mạnh mẽ:", 
                "Hơn 400 doanh nghiệp vừa và nhỏ (SME) Nhật Bản tích cực tìm kiếm mục tiêu M&A, góp vốn vào Việt Nam mỗi năm (mở rộng chuỗi cung ứng, CNTT, sản xuất tinh gọn). Tổng quy mô thị trường M&A duy trì 4 - 6 tỷ USD/năm, nhưng dòng vốn bị tắc nghẽn ở khâu tiếp cận đối tác tin cậy.",
                font_size=10.5, key_bold=True, key_color=COLOR_RED)

            add_key_value(tf, "2. Nỗi sợ lộ danh tính & Khách hàng đi đêm (Disintermediation):", 
                "Doanh nghiệp Việt Nam (Seller) rất e ngại rao bán công khai vì sợ mất khách hàng, rò rỉ nhân sự giỏi và mất uy tín kinh doanh. Đồng thời, các sàn môi giới trung gian truyền thống thiếu cơ chế bảo mật và ràng buộc pháp lý, khiến các bên dễ dàng tiếp cận thẳng ngoài sàn sau khi nắm thông tin.",
                font_size=10.5, key_bold=True, key_color=COLOR_RED, space_before=6)

            add_key_value(tf, "3. Khoảng trống Thẩm định Công nghệ (Tech DD Gap):", 
                "Các đơn vị tư vấn tài chính và luật truyền thống chỉ thẩm định sổ sách kế toán, hoàn toàn bất lực trong việc đánh giá nợ kỹ thuật, chất lượng mã nguồn, kiến trúc phần mềm và năng lực đội ngũ công nghệ thực tế của doanh nghiệp Việt Nam.",
                font_size=10.5, key_bold=True, key_color=COLOR_RED, space_before=6)

            add_key_value(tf, "➔ LỜI GIẢI ĐỘT PHÁ CỦA VAULT:", 
                "Xây dựng nền tảng điều phối khép kín: Giải mật theo 3 nấc thang pháp lý (Trust Profile), phòng dữ liệu số (VDR) bảo mật và dịch vụ thẩm định Tech DD độc quyền do Rikkeisoft trực tiếp bảo chứng uy tín.",
                font_size=11, key_bold=True, key_color=COLOR_DARK, val_color=COLOR_RED, space_before=10)

    # -------------------------------------------------------------
    # SLIDE 3: MỤC 02: TỔNG QUAN NỀN TẢNG VAULT & RIKKEI SYNERGY
    # -------------------------------------------------------------
    slide3 = prs.slides[2]
    for s in slide3.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "02. TỔNG QUAN NỀN TẢNG VAULT — ĐIỂM TỰA TIN CẬY CHO GIAO DỊCH", font_size=20, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 12:  # Left
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "BẢN CHẤT NỀN TẢNG VAULT"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(12)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(6)

            add_key_value(tf, "• Nền tảng điều phối SaaS khép kín:", 
                "Tổ chức thông tin, hồ sơ, tài liệu và tiến độ của các bên trên cùng một hồ sơ thương vụ số hóa tập trung; hỗ trợ toàn diện từ lúc nhận nhu cầu đến khi hoàn tất bàn giao.", font_size=10)
            add_key_value_paragraph_break = add_key_value(tf, "• Nguyên tắc trung lập & An toàn tuyệt đối:", 
                "VAULT không nắm giữ tiền giao dịch, không sở hữu cổ phần, không làm sai lệch số liệu. Mọi quyết định pháp lý và thanh toán diễn ra trực tiếp giữa Buyer và Seller.", font_size=10, space_before=6)
            add_key_value(tf, "• Chuẩn hóa hai đầu chuỗi giá trị:", 
                "Chuẩn hóa nhu cầu đầu tư (Buyer Request) kết hợp xây dựng hồ sơ tín nhiệm năng lực (Trust Profile) cho bên bán, tự động hóa ghép nối theo khẩu vị đầu tư.", font_size=10, space_before=6)
        elif s.name == "Placeholder" and s.shape_id == 14:  # Right
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "SỨC MẠNH CỘNG SINH CÙNG RIKKEISOFT"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(12)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(6)

            add_key_value(tf, "• Mạng lưới Buyer Nhật sẵn có:", 
                "Khai thác trực tiếp tệp hơn 500 khách hàng doanh nghiệp và đối tác chiến lược của Rikkei Japan, loại bỏ hoàn toàn chi phí đắt đỏ của việc tìm kiếm đối tác mua từ con số 0.", font_size=10)
            add_key_value(tf, "• Uy tín bảo chứng kỹ thuật độc quyền:", 
                "Tận dụng đội ngũ hơn 2.000 kỹ sư của Rikkei để cung cấp báo cáo thẩm định Tech DD độc quyền, tạo niềm tin tuyệt đối cho doanh nghiệp Nhật Bản vốn cực kỳ khắt khe.", font_size=10, space_before=6)
            add_key_value(tf, "• Cửa ngõ bán chéo hợp đồng DX:", 
                "Mọi thương vụ M&A thành công đều kéo theo nhu cầu tái cấu trúc hệ thống, tích hợp phần mềm và ủy thác CNTT, mang lại nguồn hợp đồng dịch vụ công nghệ lớn cho Rikkei.", font_size=10, space_before=6)

    # -------------------------------------------------------------
    # SLIDE 4: MỤC 03: TÍNH NĂNG CỐT LÕI - TRUST PROFILE 3 LỚP
    # -------------------------------------------------------------
    slide4 = prs.slides[3]
    for s in slide4.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "03. CƠ CHẾ GIẢI MẬT 3 LỚP (TRUST PROFILE) — LỘ ĐỦ ĐỂ ĐÁNH GIÁ, GIẤU ĐỦ ĐỂ AN TOÀN", font_size=18, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 12:  # Left: Main content
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "ĐẶC TẢ 3 TẦNG DỮ LIỆU BẢO MẬT"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(12)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(5)

            add_key_value(tf, "Lớp 1 · Teaser Ẩn danh (Công khai):", 
                "Hiển thị dải doanh thu, dải EBITDA, ngành nghề tổng quát, quy mô nhân sự, mô hình kinh doanh. Ẩn hoàn toàn tên công ty, MST và địa chỉ. Áp dụng K-Anonymity (k ≥ 5) chống truy vết ngược.", font_size=9.5)
            add_key_value(tf, "Lớp 2 · Hồ sơ Định danh (Sau NDA):", 
                "Hiển thị tên pháp nhân, MST, cơ cấu cổ đông, danh mục sản phẩm và BCTC tóm tắt đã chuẩn hóa. Điều kiện: Buyer ký NDA điện tử và được Seller trực tiếp bấm phê duyệt mở quyền.", font_size=9.5, space_before=5)
            add_key_value(tf, "Lớp 3 · Phòng Dữ liệu VDR (Sau LOI):", 
                "Mở BCTC kiểm toán chi tiết, hợp đồng kinh tế lớn, mã nguồn, kiến trúc hệ thống và Báo cáo Tech DD. Điều kiện: Buyer phát hành Ý định thư (LOI) và được Seller cấp quyền truy cập có thời hạn.", font_size=9.5, space_before=5)
        elif s.name == "Placeholder" and s.shape_id == 14:  # Right: Visual / Security Rules
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "CƠ CHẾ BẢO MẬT & PHÁP LÝ NGHỊ ĐỊNH 13"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(12)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(5)

            add_key_value(tf, "• Máy chủ đặt tại Việt Nam:", 
                "100% dữ liệu thương vụ được lưu trữ trên hạ tầng nội địa, tuân thủ nghiêm ngặt Nghị định 13/2023/NĐ-CP (PDPD) và Luật An ninh mạng.", font_size=9.5)
            add_key_value(tf, "• Cơ chế Opt-in Consent từng tầng:", 
                "Chủ thể dữ liệu (Seller & Cổ đông) phải ký văn bản chấp thuận trước mỗi lần hệ thống mở quyền truy cập cho bên mua.", font_size=9.5, space_before=5)
            add_key_value(tf, "• Watermarking động & Chống tải file:", 
                "Đóng dấu mờ danh tính người xem (Email, IP, Timestamp) theo thời gian thực trên từng trang; ngăn chặn chụp màn hình, chống tải về máy.", font_size=9.5, space_before=5)
            add_key_value(tf, "• Phân quyền độc lập & Audit Trail:", 
                "Kiểm tra phân quyền nghiêm ngặt tại máy chủ (Server-side RBAC) riêng cho từng thương vụ; ghi nhận nhật ký truy cập bất biến 24/7.", font_size=9.5, space_before=5)

    # -------------------------------------------------------------
    # SLIDE 5: MỤC 04: CÔNG CỤ TẠO SỰ KHÁC BIỆT
    # -------------------------------------------------------------
    slide5 = prs.slides[4]
    for s in slide5.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "04. BỘ CÔNG CỤ TẠO LỢI THẾ CẠNH TRANH ĐỘC QUYỀN CỦA VAULT", font_size=20, bold=True, color=COLOR_DARK)
        # Column 1
        elif s.name == "text" and s.shape_id == 11:
            clear_and_set_text(s, "01. AI BUYER MATCHING", font_size=12, bold=True, color=COLOR_RED, align=PP_ALIGN.CENTER)
        elif s.name == "Placeholder" and s.shape_id == 13:
            s.top = Inches(2.05)
            s.height = Inches(4.85)
            tf = s.text_frame
            tf.clear()
            add_key_value(tf, "• Thu thập nhu cầu Buyer:", "Agent thu thập và phân tích khẩu vị đầu tư của Buyer Nhật (ngành nghề, quy mô doanh thu, công nghệ mong muốn).", font_size=9.5)
            add_key_value(tf, "• Chấm điểm tương thích:", "Thuật toán Appetite Matching đối chiếu ma trận tiêu chí, tự động tính Fit Score giữa Buyer và Seller.", font_size=9.5, space_before=6)
            add_key_value(tf, "• Gợi ý tức thì:", "Đề xuất danh sách ứng viên phù hợp mà không để lộ danh tính của bất kỳ bên nào.", font_size=9.5, space_before=6)
        # Column 2
        elif s.name == "text" and s.shape_id == 14:
            clear_and_set_text(s, "02. PHÒNG DỮ LIỆU SỐ (VDR)", font_size=12, bold=True, color=COLOR_RED, align=PP_ALIGN.CENTER)
        elif s.name == "Placeholder" and s.shape_id == 16:
            s.top = Inches(2.05)
            s.height = Inches(4.85)
            tf = s.text_frame
            tf.clear()
            add_key_value(tf, "• Kho tài liệu chuẩn M&A:", "Cấu trúc thư mục theo tiêu chuẩn quốc tế (Pháp lý, Tài chính, Thuế, Nhân sự, Công nghệ, Khách hàng).", font_size=9.5)
            add_key_value(tf, "• Q&A Workflow kiểm duyệt:", "Buyer gửi câu hỏi gắn trực tiếp vào tài liệu; chuyên gia VAULT và Seller phản hồi tập trung.", font_size=9.5, space_before=6)
            add_key_value(tf, "• Chặn kênh đi đêm:", "Tự động ẩn thông tin liên lạc cá nhân khi chưa được phê duyệt, ngăn chặn giao dịch ngoài sàn.", font_size=9.5, space_before=6)
        # Column 3
        elif s.name == "text" and s.shape_id == 17:
            clear_and_set_text(s, "03. BÁO CÁO TECH DD RIKKEI", font_size=12, bold=True, color=COLOR_RED, align=PP_ALIGN.CENTER)
        elif s.name == "Placeholder" and s.shape_id == 19:
            s.top = Inches(2.05)
            s.height = Inches(4.85)
            tf = s.text_frame
            tf.clear()
            add_key_value(tf, "• Thẩm định 5 trụ cột:", "Đánh giá chất lượng mã nguồn & Nợ kỹ thuật, Kiến trúc hệ thống, An toàn bảo mật, Năng lực đội ngũ, Tính khả thi tích hợp.", font_size=9.5)
            add_key_value(tf, "• Vũ khí độc quyền:", "Do Rikkeisoft trực tiếp thực hiện và đóng dấu chứng thực — giải quyết nỗi lo lớn nhất của Buyer Nhật.", font_size=9.5, space_before=6)
            add_key_value(tf, "• Định lượng rủi ro:", "Quy đổi rủi ro kỹ thuật thành chi phí cần trích lập, giúp Buyer định giá chính xác thương vụ.", font_size=9.5, space_before=6)

    # -------------------------------------------------------------
    # SLIDE 6: MỤC 05: PHÂN RÃ HỆ THỐNG THEO 4 NHÓM NGHIỆP VỤ
    # -------------------------------------------------------------
    slide6 = prs.slides[5]
    for s in slide6.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "05. PHÂN RÃ HỆ THỐNG VAULT THEO 4 NHÓM NGHIỆP VỤ CỐT LÕI", font_size=20, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 12:  # Card 1
            s.top = Inches(1.40)
            s.height = Inches(2.50)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "NHÓM 1: QUẢN LÝ HỒ SƠ & NHU CẦU"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(3)
            add_paragraph(tf, "• Buyer Request: Thu thập tiêu chí, ngân sách, hình thức mua (Primary, Secondary, Mixed).", font_size=9)
            add_paragraph(tf, "• Seller Profile: Chuẩn hóa dữ liệu pháp lý, năng lực và danh mục sản phẩm doanh nghiệp.", font_size=9)
            add_paragraph(tf, "• Trust Profile: Xây dựng Teaser ẩn danh Lớp 1 và hồ sơ định danh Lớp 2.", font_size=9)
            add_paragraph(tf, "• AI Lead Discovery: Agent tìm kiếm Buyer theo ngành và đề xuất mức độ phù hợp.", font_size=9)
        elif s.name == "Placeholder" and s.shape_id == 14:  # Card 2
            s.top = Inches(1.40)
            s.height = Inches(2.50)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "NHÓM 2: BẢO MẬT & PHÒNG DỮ LIỆU VDR"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(3)
            add_paragraph(tf, "• Ký NDA điện tử: Ký số thỏa thuận bảo mật có ràng buộc pháp lý trước khi mở Lớp 2.", font_size=9)
            add_paragraph(tf, "• Luồng phê duyệt giải mật: Seller giữ quyền tối cao bấm phê duyệt cho từng Buyer.", font_size=9)
            add_paragraph(tf, "• Quản trị tài liệu VDR: Phân quyền theo thư mục, kiểm soát phiên bản, chống download.", font_size=9)
            add_paragraph(tf, "• Audit Trail: Giám sát toàn bộ lịch sử xem tài liệu và thao tác người dùng.", font_size=9)
        elif s.name == "Placeholder" and s.shape_id == 16:  # Card 3
            s.top = Inches(4.45)
            s.height = Inches(2.50)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "NHÓM 3: THẨM ĐỊNH & ĐỀ NGHỊ GIAO DỊCH"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(3)
            add_paragraph(tf, "• Phân hệ Tech DD Rikkei: Đánh giá nợ kỹ thuật, kiến trúc, an toàn mã nguồn phần mềm.", font_size=9)
            add_paragraph(tf, "• Q&A Workflow: Điều phối hỏi đáp trực tiếp trên từng mục tài liệu VDR có kiểm soát.", font_size=9)
            add_paragraph(tf, "• Đề nghị giao dịch: Buyer gửi Ý định thư (LOI) và đề nghị chính thức trên hệ thống.", font_size=9)
            add_paragraph(tf, "• Theo dõi tiến độ DD: Giám sát hoàn tất thẩm định tài chính, pháp lý và kỹ thuật.", font_size=9)
        elif s.name == "Placeholder" and s.shape_id == 18:  # Card 4
            s.top = Inches(4.45)
            s.height = Inches(2.50)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "NHÓM 4: CLOSING, PHÍ & BÀN GIAO POST-M&A"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(3)
            add_paragraph(tf, "• Checklist Closing: Theo dõi hoàn tất các điều kiện tiên quyết (CPs) trước ký kết.", font_size=9)
            add_paragraph(tf, "• Quản lý phí & Thanh toán: Theo dõi thu phí Prep Pack, Tech DD và phí thành công Success Fee.", font_size=9)
            add_paragraph(tf, "• Ghi nhận hoàn tất: Lưu trữ văn bản ký kết chính thức hợp đồng mua bán cổ phần (SPA).", font_size=9)
            add_paragraph(tf, "• Bàn giao dịch vụ IT: Bàn giao gói công việc nâng cấp hệ thống hậu M&A cho Rikkei.", font_size=9)

    # -------------------------------------------------------------
    # SLIDE 7: MỤC 05: QUY TRÌNH THƯƠNG VỤ 20 BƯỚC KHÉP KÍN
    # -------------------------------------------------------------
    slide7 = prs.slides[6]
    for s in slide7.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "05. QUY TRÌNH THƯƠNG VỤ 20 BƯỚC — CHẶT CHẼ, MINH BẠCH & TỰ ĐỘNG HÓA", font_size=19, bold=True, color=COLOR_DARK)
        # Step 01
        elif s.name == "text" and s.shape_id == 12:
            clear_and_set_text(s, "GIAI ĐOẠN 1: KHỞI TẠO & SÀNG LỌC", font_size=10, bold=True, color=COLOR_RED, align=PP_ALIGN.CENTER)
        elif s.name == "Placeholder" and s.shape_id == 14:
            s.top = Inches(3.35)
            s.height = Inches(2.50)
            tf = s.text_frame
            tf.clear()
            add_paragraph(tf, "• B1: Tiếp nhận Buyer Request", font_size=8.5)
            add_paragraph(tf, "• B2: Tiếp nhận Seller & chuẩn hóa", font_size=8.5)
            add_paragraph(tf, "• B3: Thu phí Prep Pack (90tr)", font_size=8.5)
            add_paragraph(tf, "• B4: Soạn Trust Profile & duyệt L1", font_size=8.5)
            add_paragraph(tf, "• B5: AI Matching đối chiếu tiêu chí", font_size=8.5)
        # Step 02
        elif s.name == "text" and s.shape_id == 17:
            clear_and_set_text(s, "GIAI ĐOẠN 2: TIẾP CẬN & GIẢI MẬT L2", font_size=10, bold=True, color=COLOR_RED, align=PP_ALIGN.CENTER)
        elif s.name == "Placeholder" and s.shape_id == 19:
            s.top = Inches(3.35)
            s.height = Inches(2.50)
            tf = s.text_frame
            tf.clear()
            add_paragraph(tf, "• B6: Buyer chọn Teaser & gửi yêu cầu", font_size=8.5)
            add_paragraph(tf, "• B7: Ký NDA điện tử ràng buộc", font_size=8.5)
            add_paragraph(tf, "• B8: Seller phê duyệt cấp quyền L2", font_size=8.5)
            add_paragraph(tf, "• B9: Mở hồ sơ định danh & BCTC tóm tắt", font_size=8.5)
            add_paragraph(tf, "• B10: Tổ chức gặp gỡ làm quen sơ bộ", font_size=8.5)
        # Step 03
        elif s.name == "text" and s.shape_id == 22:
            clear_and_set_text(s, "GIAI ĐOẠN 3: VDR & TECH DD CHUYÊN SÂU", font_size=10, bold=True, color=COLOR_RED, align=PP_ALIGN.CENTER)
        elif s.name == "Placeholder" and s.shape_id == 24:
            s.top = Inches(3.35)
            s.height = Inches(2.50)
            tf = s.text_frame
            tf.clear()
            add_paragraph(tf, "• B11: Buyer gửi Ý định thư (LOI)", font_size=8.5)
            add_paragraph(tf, "• B12: Seller duyệt mở phòng VDR L3", font_size=8.5)
            add_paragraph(tf, "• B13: Rikkei triển khai Tech DD độc quyền", font_size=8.5)
            add_paragraph(tf, "• B14: Vận hành Q&A xử lý vướng mắc", font_size=8.5)
            add_paragraph(tf, "• B15: Xuất Báo cáo Tech DD & điều chỉnh", font_size=8.5)
        # Step 04
        elif s.name == "text" and s.shape_id == 27:
            clear_and_set_text(s, "GIAI ĐOẠN 4: CLOSING & BÀN GIAO IT", font_size=10, bold=True, color=COLOR_RED, align=PP_ALIGN.CENTER)
        elif s.name == "Placeholder" and s.shape_id == 29:
            s.top = Inches(3.35)
            s.height = Inches(2.50)
            tf = s.text_frame
            tf.clear()
            add_paragraph(tf, "• B16: Đàm phán Hợp đồng mua bán (SPA)", font_size=8.5)
            add_paragraph(tf, "• B17: Rà soát Checklist điều kiện (CP)", font_size=8.5)
            add_paragraph(tf, "• B18: Ký kết chính thức & chuyển khoản", font_size=8.5)
            add_paragraph(tf, "• B19: Thu phí thành công (Success Fee)", font_size=8.5)
            add_paragraph(tf, "• B20: Nghiệm thu & bàn giao gói IT Rikkei", font_size=8.5)

    # -------------------------------------------------------------
    # SLIDE 8: MỤC 06: MÔ HÌNH KINH TẾ (TABLE) & RỦI RO
    # -------------------------------------------------------------
    slide8 = prs.slides[7]
    for s in slide8.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "06. MÔ HÌNH KINH TẾ, DÒNG TIỀN VÀ MA TRẬN PHÒNG NGỪA RỦI RO", font_size=19, bold=True, color=COLOR_DARK)
        elif s.has_table and s.shape_id == 23:
            tbl = s.table
            # Define 6 rows of table data
            table_data = [
                # Row 0: Header
                ("HẠNG MỤC THU / CHỈ SỐ", "QUY MÔ & ĐỊNH MỨC PHÍ", "THỜI ĐIỂM GHI NHẬN", "TÁC ĐỘNG CHIẾN LƯỢC CHO RIKKEI"),
                # Row 1
                ("1. Phí Prep Pack (Chuẩn bị hồ sơ)", "90 triệu VND / hồ sơ Seller", "Ngay khi nhận hồ sơ (Tháng 1–3)", "Dòng tiền sớm nuôi bộ máy; loại 80% hồ sơ không nghiêm túc"),
                # Row 2
                ("2. Phí Thẩm định Tech DD (Rikkei)", "120 – 250 triệu VND / thương vụ", "Giai đoạn VDR Lớp 3 (Sau LOI)", "Bảo chứng kỹ thuật độc quyền; giải tỏa nỗi sợ nợ công nghệ cho Buyer"),
                # Row 3
                ("3. Phí Thành công (Success Fee)", "2,0% – 3,5% giá trị giao dịch", "Khi ký kết SPA & Hoàn tất closing", "Nguồn thu đột phá; bình quân 1,5 – 3,0 tỷ VND / deal thành công"),
                # Row 4
                ("4. Doanh thu Bán chéo Hậu M&A", "100.000 – 500.000 USD / hợp đồng", "Giai đoạn hậu M&A (Post-closing)", "Ủy thác nâng cấp hệ thống, ERP, chuyển đổi số (DX) cho Rikkeisoft"),
                # Row 5: Highlight row
                ("HÒA VỐN & KẾ HOẠCH VỐN 5 NĂM", "Hòa vốn: Tháng 21 | Đáy: -2,2 tỷ", "Vốn hạt giống MVP: 2,0 tỷ VND", "Năm 1: 1,8 tỷ · Năm 2: 6,4 tỷ · Năm 3: 18,5 tỷ · Năm 5: 68,0 tỷ VND"),
            ]
            for r_idx, row_vals in enumerate(table_data):
                for c_idx, val in enumerate(row_vals):
                    cell = tbl.cell(r_idx, c_idx)
                    if r_idx == 0:
                        format_cell(cell, val, font_size=10, bold=True, text_color=COLOR_WHITE, bg_color=COLOR_RED, align=PP_ALIGN.CENTER)
                    elif r_idx == 5:
                        format_cell(cell, val, font_size=9, bold=True, text_color=COLOR_RED, bg_color=COLOR_TINT, align=PP_ALIGN.LEFT)
                    else:
                        bg = COLOR_ZEBRA if r_idx % 2 == 1 else COLOR_WHITE
                        format_cell(cell, val, font_size=9, bold=(c_idx == 0), text_color=COLOR_DARK, bg_color=bg, align=PP_ALIGN.LEFT)
        elif s.name == "text" and s.shape_id == 12:
            clear_and_set_text(s, "Nguồn: Mô hình tài chính VAULT Model 5 năm (Kịch bản cơ sở) · Điểm hòa vốn tháng 21 · Ban Dự án VAULT trình HĐQT Rikkeisoft 2026", font_size=9.5, bold=False, color=COLOR_MUTED)

    # -------------------------------------------------------------
    # SLIDE 9: KẾT LUẬN & ĐỀ NGHỊ ĐẦU TƯ
    # -------------------------------------------------------------
    slide9 = prs.slides[8]
    for s in slide9.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "VAULT — BIẾN NĂNG LỰC CÔNG NGHỆ VÀ UY TÍN NHẬT BẢN CỦA RIKKEISOFT THÀNH NỀN TẢNG M&A DẪN ĐẦU", font_size=20, bold=True, color=COLOR_RED, align=PP_ALIGN.CENTER)
        elif s.name == "text" and s.shape_id == 3:
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.alignment = PP_ALIGN.CENTER
            p0.text = "ĐỀ NGHỊ HỘI ĐỒNG QUẢN TRỊ (BOD) PHÊ DUYỆT:"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(13)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_DARK
            p0.space_after = Pt(6)

            add_paragraph(tf, "1. Phê duyệt chủ trương thành lập và triển khai Dự án Nền tảng VAULT trong Hệ sinh thái Rikkeisoft.", font_size=11, bold=True, align=PP_ALIGN.CENTER)
            add_paragraph(tf, "2. Cấp ngân sách hạt giống Giai đoạn 1 (MVP 6 tháng): 2,0 tỷ VND để hoàn thiện sản phẩm core và tiếp cận 20 deals đầu tiên.", font_size=11, bold=True, color=COLOR_RED, align=PP_ALIGN.CENTER)
            add_paragraph(tf, "3. Thiết lập cơ chế phối hợp chiến lược cùng Rikkei Japan khai thác tệp Buyer Nhật ngay từ Q4/2026.", font_size=11, bold=True, align=PP_ALIGN.CENTER)
            add_paragraph(tf, "Đầu mối Ban Dự án: vault@rikkeisoft.com · Hotline: (+84) 24 6258 3662", font_size=10, color=COLOR_MUTED, space_before=10, align=PP_ALIGN.CENTER)
        elif s.name == "LINK_10" and s.shape_id == 4:
            tf = s.text_frame
            tf.paragraphs[0].text = "PHỤ LỤC: CẨM NANG PHẢN BIỆN CHIẾN LƯỢC (DEBATE PLAYBOOK) ›"
            if tf.paragraphs[0].runs:
                tf.paragraphs[0].runs[0].font.name = FONT_NAME
                tf.paragraphs[0].runs[0].font.size = Pt(10.5)
                tf.paragraphs[0].runs[0].font.bold = True
                tf.paragraphs[0].runs[0].font.color.rgb = COLOR_RED

    # -------------------------------------------------------------
    # SLIDE 10: PHỤ LỤC MỤC LỤC DEBATE PLAYBOOK
    # -------------------------------------------------------------
    slide10 = prs.slides[9]
    debate_toc = [
        (8, "Thị trường, Khẩu vị Buyer Nhật & Phí Prep Pack"),
        (11, "Sức mạnh cộng sinh Rikkei & Trách nhiệm pháp lý Tech DD"),
        (14, "Ranh giới pháp lý, Nghị định 13 & Kiểm soát 'Sổ B'"),
        (17, "Kiến trúc kỹ thuật: Tự phát triển (Build) vs Mua ngoài (Buy)"),
        (20, "Dòng tiền, Vượt đáy thung lũng (Tháng 21) & Plan B"),
        (23, "Bản chất nền tảng, Hiệu ứng mạng & Bài toán Scale"),
    ]
    for s in slide10.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "PHỤ LỤC: CẨM NANG BẢO VỆ DỰ ÁN TRƯỚC HỘI ĐỒNG QUẢN TRỊ (DEBATE PLAYBOOK)", font_size=19, bold=True, color=COLOR_DARK)
        for shape_id, label in debate_toc:
            if s.shape_id == shape_id:
                tf = s.text_frame
                tf.paragraphs[0].text = label
                if tf.paragraphs[0].runs:
                    tf.paragraphs[0].runs[0].font.name = FONT_NAME
                    tf.paragraphs[0].runs[0].font.size = Pt(11)
                    tf.paragraphs[0].runs[0].font.bold = True
                    tf.paragraphs[0].runs[0].font.color.rgb = COLOR_DARK

    # -------------------------------------------------------------
    # SLIDE 11: PHỤ LỤC 01: THỊ TRƯỜNG & BUYER NHẬT
    # -------------------------------------------------------------
    slide11 = prs.slides[10]
    for s in slide11.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "PHỤ LỤC 01: THỊ TRƯỜNG, KHẨU VỊ BUYER NHẬT & TÍNH KHẢ THI PHÍ PREP PACK", font_size=19, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 8:
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "CÂU 1.1: BẪY 'ẢO TƯỞNG BUYER NHẬT' & CÂU 1.2: BẪY 'THU PHÍ TRẢ TRƯỚC (PREP PACK 90 TRIỆU)'"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11.5)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(4)

            add_key_value(tf, "❓ Câu hỏi 1.1 (Ảo tưởng Buyer Nhật):", 
                "Buyer Nhật cực kỳ bảo thủ, quy trình thẩm định 12-18 tháng qua các ngân hàng lớn. Tại sao họ chịu dùng một nền tảng mới?", font_size=10, key_bold=True)
            add_key_value(tf, "🛡️ Phản biện chuẩn:", 
                "VAULT không tìm Buyer qua quảng cáo mở; chúng ta khai thác trực tiếp tệp hơn 500 khách hàng doanh nghiệp của Rikkei Japan. Nền tảng giải quyết đúng 'tử huyệt' lớn nhất của Buyer Nhật: Sự thiếu minh bạch và rào cản thẩm định kỹ thuật tại Việt Nam. Báo cáo Tech DD của Rikkei chính là chìa khóa rút ngắn quy trình từ 12 tháng xuống còn 4-6 tháng.", font_size=9.5, key_bold=True, key_color=COLOR_DARK)

            add_key_value(tf, "❓ Câu hỏi 1.2 (Bẫy phí Prep Pack 90 triệu):", 
                "SME Việt Nam quen văn hóa 'thành công mới trả tiền', tại sao họ chịu trả 90 triệu trước khi chưa thấy kết quả?", font_size=10, key_bold=True, space_before=6)
            add_key_value(tf, "🛡️ Phản biện chuẩn:", 
                "(1) 90 triệu là chi phí nhận dịch vụ thực: Số hóa hồ sơ, chuẩn hóa tài chính theo chuẩn quốc tế và lập Trust Profile. Kể cả không bán qua VAULT, hồ sơ này Seller vẫn dùng được cho mọi nhà đầu tư. (2) Màng lọc nghiêm túc: Loại bỏ 80% chủ doanh nghiệp 'bán thử cho vui'. (3) Cơ chế bù trừ: 90 triệu sẽ được hoàn trừ 100% vào phí Success Fee khi giao dịch thành công.", font_size=9.5, key_bold=True, key_color=COLOR_DARK)

    # -------------------------------------------------------------
    # SLIDE 12: PHỤ LỤC 02: HỢP LỰC & TRÁCH NHIỆM PHÁP LÝ RIKKEI
    # -------------------------------------------------------------
    slide12 = prs.slides[11]
    for s in slide12.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "PHỤ LỤC 02: SỰ HỢP LỰC (SYNERGY) & TRÁCH NHIỆM PHÁP LÝ VỚI RIKKEISOFT", font_size=19, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 8:  # Left Card: Question 2.1
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "CÂU 2.1: BẪY 'CHI PHÍ CƠ HỘI NGUỒN LỰC'"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(4)

            add_key_value(tf, "❓ Vấn đề chất vấn:", 
                "Rikkei đang dồn lực làm Outsourcing và AI, tại sao phải phân tán tài nguyên kỹ sư và vốn sang một mảng M&A xa lạ?", font_size=9.5)
            add_key_value(tf, "🛡️ Khung phản biện:", 
                "• Mũi khoan tạo đầu ra giá trị cao: Biên lợi nhuận Outsourcing chỉ 15-20%, trong khi Success Fee M&A và Tech DD mang lại biên lợi nhuận trên 50%.\n• Bán chéo hợp đồng triệu đô: Mọi thương vụ M&A công nghệ đều mở ra hợp đồng nâng cấp hệ thống, ERP, DX cho Rikkei.\n• Nâng tầm định giá tập đoàn: Đưa Rikkei từ một công ty gia công thuần túy thành tập đoàn công nghệ làm chủ hệ sinh thái vốn khu vực.", font_size=9, key_color=COLOR_DARK, space_before=4)
        elif s.name == "Placeholder" and s.shape_id == 10:  # Right Card: Question 2.2
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "CÂU 2.2: BẪY 'TRÁCH NHIỆM PHÁP LÝ TECH DD'"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(4)

            add_key_value(tf, "❓ Vấn đề chất vấn:", 
                "Nếu sau M&A Buyer Nhật phát hiện phần mềm bị lỗi nghiêm trọng hoặc vi phạm bản quyền thì Rikkei có bị kiện đền bù?", font_size=9.5)
            add_key_value(tf, "🛡️ Khung phản biện:", 
                "• Tách biệt pháp nhân (Spinoff): Dự án hoạt động dưới pháp nhân độc lập, cách ly hoàn toàn rủi ro tài chính với công ty mẹ Rikkei.\n• Điều khoản miễn trừ độc lập: Hợp đồng quy định Báo cáo Tech DD là ý kiến chuyên môn độc lập tại thời điểm đánh giá dựa trên dữ liệu được cấp, không cấu thành cam kết bảo lãnh kết quả.\n• Giới hạn bồi thường & Bảo hiểm: Giới hạn trách nhiệm tối đa bằng giá trị phí thẩm định nhận được; mua bảo hiểm trách nhiệm nghề nghiệp chuyên nghiệp.", font_size=9, key_color=COLOR_DARK, space_before=4)

    # -------------------------------------------------------------
    # SLIDE 13: PHỤ LỤC 03: PHÁP LÝ NGHỊ ĐỊNH 13 & SỔ B
    # -------------------------------------------------------------
    slide13 = prs.slides[12]
    for s in slide13.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "PHỤ LỤC 03: RANH GIỚI PHÁP LÝ, NGHỊ ĐỊNH 13 & KIỂM SOÁT 'SỔ B'", font_size=19, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 8:  # Left: Question 3.1
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "CÂU 3.1: BẪY 'RỦI RO SỔ B & HUY ĐỘNG VỐN'"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(4)

            add_key_value(tf, "❓ Vấn đề chất vấn:", 
                "SME Việt Nam thường có 2 hệ thống sổ sách (Sổ A báo cáo thuế, Sổ B thực tế). VAULT xử lý thế nào mà không vi phạm pháp luật?", font_size=9.5)
            add_key_value(tf, "🛡️ Khung phản biện:", 
                "• Chỉ nhận Báo cáo tài chính chính thức: Nền tảng chỉ đưa lên hệ thống BCTC chính thức có xác nhận kiểm toán hoặc nộp cơ quan thuế (Sổ A).\n• Chuẩn hóa minh bạch theo chuẩn quốc tế: Mọi khoản điều chỉnh chi phí (Add-backs) phải có hóa đơn chứng từ hợp lệ theo thông lệ QoE (Quality of Earnings).\n• Không giữ tiền hay cổ phần: VAULT không cầm tiền cọc hay cổ phần, tuyệt đối không vi phạm quy định về trung gian tài chính hay ngân hàng.", font_size=9, key_color=COLOR_DARK, space_before=4)
        elif s.name == "Placeholder" and s.shape_id == 10:  # Right: Question 3.2
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "CÂU 3.2: BẪY 'NGHỊ ĐỊNH 13 & DỮ LIỆU XUYÊN BIÊN GIỚI'"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(4)

            add_key_value(tf, "❓ Vấn đề chất vấn:", 
                "Chia sẻ thông tin tài chính, cổ đông cho pháp nhân Nhật có vi phạm Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân?", font_size=9.5)
            add_key_value(tf, "🛡️ Khung phản biện:", 
                "• Máy chủ đặt 100% tại Việt Nam: Dữ liệu hồ sơ gốc lưu trữ trên hạ tầng trong nước đáp ứng tiêu chuẩn an toàn thông tin cấp độ 3.\n• Chấp thuận rõ ràng (Opt-in Consent): Seller và cổ đông ký văn bản chấp thuận trước khi giải mật từng tầng dữ liệu L1, L2, L3.\n• Lập hồ sơ Đánh giá tác động (DPIA): Hoàn thiện đầy đủ bộ hồ sơ đánh giá tác động xử lý và chuyển dữ liệu theo hướng dẫn của Bộ Công an.\n• Watermarking & Chống tải: Đóng dấu mờ định danh thời gian thực, ngăn ngừa triệt để rò rỉ dữ liệu cá nhân.", font_size=9, key_color=COLOR_DARK, space_before=4)

    # -------------------------------------------------------------
    # SLIDE 14: PHỤ LỤC 04: KIẾN TRÚC BUILD VS BUY & BẢO MẬT
    # -------------------------------------------------------------
    slide14 = prs.slides[13]
    for s in slide14.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "PHỤ LỤC 04: KIẾN TRÚC KỸ THUẬT: TỰ PHÁT TRIỂN (BUILD) VS MUA NGOÀI (BUY)", font_size=19, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 8:
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "CÂU 4.1: BẪY 'TẠI SAO PHẢI TỰ CODE' & CÂU 4.2: BẪY 'NHẬN DIỆN NGƯỢC TEASER LỚP 1'"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11.5)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(4)

            add_key_value(tf, "❓ Câu hỏi 4.1 (Tại sao phải tự code khi đã có Google Drive / VDR ngoại?):", 
                "Thị trường đã có các giải pháp VDR quốc tế (Datasite, Intralinks) hoặc dùng Google Drive. Tại sao phải tốn chi phí phát triển core riêng?", font_size=10, key_bold=True)
            add_key_value(tf, "🛡️ Phản biện chuẩn:", 
                "(1) Chi phí VDR ngoại quá đắt đỏ: Thuê VDR quốc tế tốn 2.000 - 5.000 USD/deal, quá sức chịu đựng đối với thương vụ SME Việt Nam. Google Drive thì hoàn toàn thiếu cơ chế Watermark động, luồng phê duyệt 3 cấp và Audit Trail. (2) Core VAULT là 'Hệ điều hành thương vụ': Điểm cốt lõi không phải lưu file, mà là luồng giải mật 3 tầng gắn với NDA điện tử và phân hệ thẩm định Tech DD độc quyền. Tự phát triển giúp Rikkei làm chủ công nghệ và tối ưu chi phí trọn đời.", font_size=9.5, key_bold=True, key_color=COLOR_DARK)

            add_key_value(tf, "❓ Câu hỏi 4.2 (Bẫy nhận diện ngược trên Teaser Lớp 1):", 
                "Dù ẩn tên, Buyer am hiểu ngành vẫn có thể đoán ra doanh nghiệp nếu dải doanh thu quá hẹp hoặc ngành nghề quá đặc thù?", font_size=10, key_bold=True, space_before=6)
            add_key_value(tf, "🛡️ Phản biện chuẩn:", 
                "(1) Thuật toán K-Anonymity (k ≥ 5): Bắt buộc trong cùng nhóm tiêu chí phải có ít nhất 5 doanh nghiệp tương đồng. Nếu là doanh nghiệp ngách độc quyền, hệ thống tự động gộp ngành lên cấp cao hơn. (2) Làm mờ số liệu theo dải: Doanh thu hiển thị theo dải bậc thang rộng (50-100 tỷ, 100-200 tỷ), nhân sự theo dải lớn (50-100 người). (3) Seller duyệt Teaser: Seller trực tiếp rà soát và xác nhận bản Teaser trước khi phát hành.", font_size=9.5, key_bold=True, key_color=COLOR_DARK)

    # -------------------------------------------------------------
    # SLIDE 15: PHỤ LỤC 05: QUẢN TRỊ DÒNG TIỀN, ĐÁY THÁNG 21 & PLAN B
    # -------------------------------------------------------------
    slide15 = prs.slides[14]
    for s in slide15.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "PHỤ LỤC 05: QUẢN TRỊ DÒNG TIỀN, VƯỢT ĐÁY THUNG LŨNG (THÁNG 21) & KỊCH BẢN PLAN B", font_size=18, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 8:  # Left: Question 5.1
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "CÂU 5.1: BẪY 'CẠN TIỀN TRƯỚC ĐÁY THUNG LŨNG'"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(4)

            add_key_value(tf, "❓ Vấn đề chất vấn:", 
                "Chu kỳ M&A kéo dài 9-12 tháng. Nếu năm đầu chưa đóng được thương vụ nào thì lấy gì để nuôi đội ngũ vận hành?", font_size=9.5)
            add_key_value(tf, "🛡️ Khung phản biện:", 
                "• Dòng tiền thu trước (Upfront Revenue): VAULT thu phí Prep Pack (90tr) và phí Tech DD (120-250tr) ngay từ các tháng đầu tiên, tạo 'bình oxy' chi trả chi phí vận hành (OPEX).\n• Đội ngũ tinh gọn linh hoạt: Giai đoạn đầu chỉ duy trì bộ khung cốt lõi 5-7 nhân sự; chi phí cố định được kiểm soát dưới 250 triệu VND/tháng.\n• Đáy thung lũng được bảo vệ: Đáy tiền mặt cực đại -2,2 tỷ VND tại tháng 21 đã được dự phòng đầy đủ trong gói vốn hạt giống 2,0 tỷ của HĐQT.", font_size=9, key_color=COLOR_DARK, space_before=4)
        elif s.name == "Placeholder" and s.shape_id == 10:  # Right: Plan B
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "KỊCH BẢN PHÒNG THỦ & PLAN B SINH TỒN"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(4)

            add_key_value(tf, "🛡️ Nếu thị trường đóng băng sau 12 tháng:", 
                "Kích hoạt cơ chế 'Ngủ đông có chọn lọc' (Selective Hibernation) để bảo toàn tuyệt đối dòng vốn cho tập đoàn Rikkei.", font_size=9.5)
            add_key_value(tf, "• Điều chuyển nhân sự kỹ thuật:", 
                "Chuyển dịch ngay 70% lập trình viên quay trở lại các dự án Outsourcing cốt lõi của Rikkei, chi phí kỹ thuật lập tức giảm về 0.", font_size=9, space_before=3)
            add_key_value(tf, "• Duy trì bộ khung tối thiểu:", 
                "Chỉ giữ lại 2 nhân sự chủ chốt (1 Business Lead, 1 Tech Lead) để tiếp tục vận hành các thương vụ đang trong giai đoạn thẩm định VDR.", font_size=9, space_before=3)
            add_key_value(tf, "• Bán dịch vụ Tech DD On-Demand:", 
                "Chuyển hướng bán gói dịch vụ thẩm định công nghệ độc lập cho các quỹ VC/PE tại Việt Nam, duy trì dòng tiền dương liên tục.", font_size=9, space_before=3)

    # -------------------------------------------------------------
    # SLIDE 16: PHỤ LỤC 06: BẢN CHẤT NỀN TẢNG & BÀI TOÁN SCALE
    # -------------------------------------------------------------
    slide16 = prs.slides[15]
    for s in slide16.shapes:
        if s.name == "text" and s.shape_id == 2:
            clear_and_set_text(s, "PHỤ LỤC 06: BẢN CHẤT NỀN TẢNG, HIỆU ỨNG MẠNG & LỜI GIẢI BÀI TOÁN SCALE", font_size=19, bold=True, color=COLOR_DARK)
        elif s.name == "Placeholder" and s.shape_id == 8:
            s.top = Inches(1.45)
            s.height = Inches(5.35)
            tf = s.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "GIẢI MÃ 4 BẪY NỀN TẢNG: TECH PLATFORM · CON GÀ QUẢ TRỨNG · KHÁCH ĐI ĐÊM · NGHỊCH LÝ SCALE"
            p0.font.name = FONT_NAME
            p0.font.size = Pt(11.5)
            p0.font.bold = True
            p0.font.color.rgb = COLOR_RED
            p0.space_after = Pt(4)

            add_key_value(tf, "1. Tech Platform vs M&A Broker:", 
                "Môi giới truyền thống phụ thuộc vào quan hệ cá nhân của broker. VAULT tự động hóa 80% quy trình: Lọc hồ sơ, matching khẩu vị, phân quyền bảo mật và VDR; con người chỉ tham gia 20% khâu đàm phán quan trọng.", font_size=9.5)
            add_key_value(tf, "2. Bẫy Con Gà và Quả Trứng (Chicken-and-Egg):", 
                "Chiến lược 'Anchor Demand': Gom trước 30-50 nhu cầu Buyer thực sự từ Rikkei Japan. Khi có sẵn danh sách Buyer Nhật cầm tiền, việc thuyết phục Seller Việt Nam tham gia nền tảng trở nên dễ dàng.", font_size=9.5, space_before=5)
            add_key_value(tf, "3. Khách hàng 'Đi đêm' (Disintermediation):", 
                "Ràng buộc điều khoản bảo vệ 24 tháng trong NDA điện tử + Sự phụ thuộc sống còn vào Báo cáo Tech DD độc quyền của Rikkei. Nếu giao dịch ngoài sàn, Buyer Nhật mất đi bảo chứng kỹ thuật và chịu rủi ro lừa đảo rất lớn.", font_size=9.5, space_before=5)
            add_key_value(tf, "4. Nghịch lý Scale (Scale Paradox):", 
                "Chuẩn hóa phương pháp luận Tech DD thành bộ khung bán tự động (Semi-automated framework) với thư viện quét mã nguồn và chấm điểm định lượng. Một kỹ sư Rikkei có thể thẩm định song song 3-4 hệ thống/tuần.", font_size=9.5, space_before=5)

    prs.save(dst_path)
    print(f"Successfully saved updated presentation to: {dst_path}")

if __name__ == "__main__":
    src = "/Users/ngocbach/vs code/VAULT copy/3, ARCHIVED/DB_VAULT_KHUNG_SLIDE_BACKUP.pptx"
    dst = "/Users/ngocbach/vs code/VAULT copy/3, ARCHIVED/DB_VAULT_KHUNG_SLIDE.pptx"
    populate_deck(src, dst)

    output_copy = "/Users/ngocbach/vs code/VAULT copy/4, OUTPUT/DB_VAULT_KHUNG_SLIDE_COMPLETED.pptx"
    populate_deck(src, output_copy)
