"""
Script to add comprehensive, robust, dual-level hyperlinks (Shape click action + Text run a:hlinkClick)
across all 16 slides of DB_VAULT_KHUNG_SLIDE.pptx so that clicking any title, heading,
breadcrumb, or table of contents entry navigates directly to that slide.
"""

import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

FONT_NAME = "Arial"
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_RED = RGBColor(0xB4, 0x23, 0x18)
COLOR_DARK = RGBColor(0x1A, 0x1A, 0x1A)
COLOR_MUTED = RGBColor(0x55, 0x55, 0x55)
COLOR_TINT = RGBColor(0xFD, 0xED, 0xEC)

def link_shape_and_runs(slide, shape, target_slide, tooltip="Chuyển đến slide"):
    """
    Applies dual-level PowerPoint hyperlink:
    1. Shape-level click_action (for Slide Show presentation mode F5)
    2. Run-level a:hlinkClick on every paragraph run (for Edit mode Cmd+click, hover tooltip, and PDF export)
    """
    # 1. Set shape level click action
    shape.click_action.target_slide = target_slide
    
    # 2. Get slide relationship ID
    rel_id = slide.part.relate_to(
        target_slide.part,
        'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide'
    )
    
    import html
    safe_tooltip = html.escape(tooltip, quote=True)
    
    # 3. Ensure shape cNvPr has hlinkClick
    cNvPr = shape._element.nvSpPr.cNvPr
    existing_hlink = cNvPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}hlinkClick')
    if existing_hlink is not None:
        existing_hlink.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', rel_id)
        existing_hlink.set('action', 'ppaction://hlinksldjump')
        existing_hlink.set('tooltip', tooltip)
    else:
        hlink_xml = parse_xml(
            f'<a:hlinkClick {nsdecls("a")} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{rel_id}" action="ppaction://hlinksldjump" tooltip="{safe_tooltip}"/>'
        )
        cNvPr.append(hlink_xml)
        
    # 4. Attach hlinkClick to all text runs
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            for r in p.runs:
                rPr = r._r.get_or_add_rPr()
                for child in list(rPr):
                    if child.tag.endswith('hlinkClick'):
                        rPr.remove(child)
                run_hlink = parse_xml(
                    f'<a:hlinkClick {nsdecls("a")} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{rel_id}" action="ppaction://hlinksldjump" tooltip="{safe_tooltip}"/>'
                )
                rPr.append(run_hlink)

def apply_all_hyperlinks(pptx_path, out_path):
    prs = pptx.Presentation(pptx_path)
    slides = list(prs.slides)
    print(f"Loaded {len(slides)} slides.")

    # Slides mapping (1-indexed: Slide 1 -> slides[0], Slide 16 -> slides[15])
    s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16 = slides

    # =========================================================
    # 1. SLIDE 1 (COVER SLIDE)
    # =========================================================
    for s in s1.shapes:
        if s.name == "text" and s.shape_id == 3:  # Main title
            link_shape_and_runs(s1, s, s2, "Bắt đầu bài thuyết trình (01. Thị trường)")
        elif s.name == "LINK_10" or s.shape_id == 7:  # Logo VAULT
            link_shape_and_runs(s1, s, s2, "Chuyển đến Slide 02")

    # Add quick navigation bar under subtitle on Slide 1
    # Let's check if quick bar already exists or create it
    quick_bar = None
    for s in s1.shapes:
        if s.name == "Cover Quick Nav":
            quick_bar = s
            break
    if not quick_bar:
        quick_bar = s1.shapes.add_textbox(Inches(0.83), Inches(4.70), Inches(13.33), Inches(0.50))
        quick_bar.name = "Cover Quick Nav"
    
    tf = quick_bar.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT

    nav_items = [
        ("01. Thị trường", s2),
        ("  ·  ", None),
        ("02. Tổng quan", s3),
        ("  ·  ", None),
        ("03. Tính năng", s4),
        ("  ·  ", None),
        ("04. Vũ khí", s5),
        ("  ·  ", None),
        ("05. Vận hành", s6),
        ("  ·  ", None),
        ("06. Kinh tế", s8),
        ("  ·  ", None),
        ("Phụ lục Debate ›", s10),
    ]
    for label, target in nav_items:
        run = p.add_run()
        run.text = label
        run.font.name = FONT_NAME
        run.font.size = Pt(11)
        if target:
            run.font.bold = True
            run.font.color.rgb = COLOR_WHITE
            rel_id = s1.part.relate_to(
                target.part,
                'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide'
            )
            rPr = run._r.get_or_add_rPr()
            run_hlink = parse_xml(
                f'<a:hlinkClick {nsdecls("a")} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{rel_id}" action="ppaction://hlinksldjump" tooltip="Chuyển đến {label}"/>'
            )
            rPr.append(run_hlink)
        else:
            run.font.bold = False
            run.font.color.rgb = COLOR_TINT

    # =========================================================
    # 2. SLIDES 2 TO 8 (MAIN DECK NAVIGATION & TITLES)
    # =========================================================
    footer_targets = {
        "LINK_2": (s2, "01. Thị trường & Nỗi đau"),
        "LINK_3": (s3, "02. Tổng quan Nền tảng"),
        "LINK_4": (s4, "03. Tính năng & Trust Profile"),
        "LINK_5": (s5, "04. Vũ khí khác biệt & Tech DD"),
        "LINK_6": (s6, "05. Phân rã hệ thống"),
        "LINK_7": (s8, "06. Mô hình kinh tế & Rủi ro"), # FIXED: Point to Slide 8!
    }

    for slide_idx in range(1, 8):
        slide = slides[slide_idx]
        for s in slide.shapes:
            # Logo VAULT (top right)
            if s.name == "LINK_10":
                link_shape_and_runs(slide, s, s10, "Chuyển đến Mục lục Phụ lục (Slide 10)")
            # Footer navigation buttons
            if s.name in footer_targets:
                tgt_slide, tooltip = footer_targets[s.name]
                link_shape_and_runs(slide, s, tgt_slide, f"Chuyển đến {tooltip}")
            # Slide Titles on Slides 2-8: Click title to jump to Cover (Slide 1) or TOC
            if s.name == "text" and s.shape_id == 2:
                link_shape_and_runs(slide, s, s1, "Nhấn để quay về Trang bìa (Slide 01)")

    # Special inter-slide links between Slide 6 and Slide 7:
    # Slide 6: Add jump to Slide 7 (Quy trình 20 bước)
    s6_link_shape = None
    for s in s6.shapes:
        if s.name == "Link to Slide 7":
            s6_link_shape = s
            break
    if not s6_link_shape:
        s6_link_shape = s6.shapes.add_textbox(Inches(7.67), Inches(7.15), Inches(6.92), Inches(0.40))
        s6_link_shape.name = "Link to Slide 7"
    tf6 = s6_link_shape.text_frame
    tf6.clear()
    p6 = tf6.paragraphs[0]
    p6.alignment = PP_ALIGN.RIGHT
    r6 = p6.add_run()
    r6.text = "› Xem chi tiết Quy trình thương vụ 20 bước (Slide 07) ›"
    r6.font.name = FONT_NAME
    r6.font.size = Pt(10)
    r6.font.bold = True
    r6.font.color.rgb = COLOR_RED
    link_shape_and_runs(s6, s6_link_shape, s7, "Chuyển đến Quy trình thương vụ 20 bước (Slide 07)")

    # Slide 7: Add jump back to Slide 6 and forward to Slide 8
    s7_link_shape = None
    for s in s7.shapes:
        if s.name == "Link between 6 and 8":
            s7_link_shape = s
            break
    if not s7_link_shape:
        s7_link_shape = s7.shapes.add_textbox(Inches(0.42), Inches(7.15), Inches(14.17), Inches(0.40))
        s7_link_shape.name = "Link between 6 and 8"
    tf7 = s7_link_shape.text_frame
    tf7.clear()
    p7 = tf7.paragraphs[0]
    p7.alignment = PP_ALIGN.RIGHT
    
    r7_back = p7.add_run()
    r7_back.text = "‹ Quay lại Phân rã hệ thống (Slide 06)    |    "
    r7_back.font.name = FONT_NAME
    r7_back.font.size = Pt(10)
    r7_back.font.bold = True
    r7_back.font.color.rgb = COLOR_MUTED
    rel_back = s7.part.relate_to(s6.part, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
    r7_back._r.get_or_add_rPr().append(parse_xml(
        f'<a:hlinkClick {nsdecls("a")} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{rel_back}" action="ppaction://hlinksldjump" tooltip="Quay lại Slide 06"/>'
    ))

    r7_next = p7.add_run()
    r7_next.text = "Chuyển sang 06. Mô hình kinh tế (Slide 08) ›"
    r7_next.font.name = FONT_NAME
    r7_next.font.size = Pt(10)
    r7_next.font.bold = True
    r7_next.font.color.rgb = COLOR_RED
    rel_next = s7.part.relate_to(s8.part, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
    r7_next._r.get_or_add_rPr().append(parse_xml(
        f'<a:hlinkClick {nsdecls("a")} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:id="{rel_next}" action="ppaction://hlinksldjump" tooltip="Chuyển sang Slide 08"/>'
    ))

    # =========================================================
    # 3. SLIDE 9 (CLOSING / TRANSITION)
    # =========================================================
    for s in s9.shapes:
        if s.name == "LINK_10" and s.shape_id == 4:
            link_shape_and_runs(s9, s, s10, "Chuyển đến Mục lục Phụ lục (Slide 10)")
        elif s.name == "LINK_10" and s.shape_id == 5:
            link_shape_and_runs(s9, s, s2, "Quay lại Bắt đầu Phần chính (Slide 02)")
        elif s.name == "text" and s.shape_id == 2:  # Closing title
            link_shape_and_runs(s9, s, s10, "Chuyển đến Mục lục Phụ lục (Slide 10)")

    # =========================================================
    # 4. SLIDE 10 (MỤC LỤC PHỤ LỤC - DEBATE TOC)
    # =========================================================
    debate_targets = {
        "LINK_11": (s11, "Phụ lục 01: Thị trường & Khẩu vị Buyer Nhật"),
        "LINK_12": (s12, "Phụ lục 02: Hợp lực Rikkei & Trách nhiệm Tech DD"),
        "LINK_13": (s13, "Phụ lục 03: Ranh giới pháp lý & Sổ B"),
        "LINK_14": (s14, "Phụ lục 04: Kiến trúc kỹ thuật: Build vs Buy"),
        "LINK_15": (s15, "Phụ lục 05: Dòng tiền, Đáy thung lũng & Plan B"),
        "LINK_16": (s16, "Phụ lục 06: Bản chất nền tảng & Bài toán Scale"),
    }
    for s in s10.shapes:
        if s.name in debate_targets:
            tgt_slide, tooltip = debate_targets[s.name]
            link_shape_and_runs(s10, s, tgt_slide, f"Nhấn để chuyển đến {tooltip}")
        elif s.name == "LINK_2" and s.shape_id == 6:  # VỀ PHẦN CHÍNH
            link_shape_and_runs(s10, s, s2, "Quay lại Phần chính (Slide 02)")
        elif s.name == "LINK_10" and s.shape_id == 5:  # MỤC LỤC PHỤ LỤC
            link_shape_and_runs(s10, s, s10, "Mục lục Phụ lục (Slide 10)")
        elif s.name == "LINK_10" and s.shape_id == 3:  # VAULT logo
            link_shape_and_runs(s10, s, s2, "Quay lại Phần chính (Slide 02)")

    # =========================================================
    # 5. SLIDES 11 TO 16 (APPENDIX SLIDES)
    # =========================================================
    for idx, slide in enumerate([s11, s12, s13, s14, s15, s16]):
        for s in slide.shapes:
            # Title of Appendix slide: Click to return to TOC (Slide 10)
            if s.name == "text" and s.shape_id == 2:
                link_shape_and_runs(slide, s, s10, "Nhấn để quay lại Mục lục Phụ lục (Slide 10)")
            # MỤC LỤC PHỤ LỤC button
            elif s.name == "LINK_10" and s.shape_id == 5:
                link_shape_and_runs(slide, s, s10, "Quay lại Mục lục Phụ lục (Slide 10)")
            # VỀ PHẦN CHÍNH button
            elif s.name == "LINK_2" and s.shape_id == 6:
                link_shape_and_runs(slide, s, s2, "Quay lại Phần chính (Slide 02)")
            # VAULT logo
            elif s.name == "LINK_10" and s.shape_id == 3:
                link_shape_and_runs(slide, s, s2, "Quay lại Phần chính (Slide 02)")

    prs.save(out_path)
    print(f"Successfully applied and verified all hyperlinks to {out_path}!")

if __name__ == "__main__":
    target = "/Users/ngocbach/vs code/VAULT copy/3, ARCHIVED/DB_VAULT_KHUNG_SLIDE.pptx"
    apply_all_hyperlinks(target, target)

    output_copy = "/Users/ngocbach/vs code/VAULT copy/4, OUTPUT/DB_VAULT_KHUNG_SLIDE_COMPLETED.pptx"
    apply_all_hyperlinks(target, output_copy)
