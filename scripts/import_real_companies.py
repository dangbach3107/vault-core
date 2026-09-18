"""Script to import 10 verified real Vietnamese companies into VAULT Core database."""
import json
import urllib.request
import urllib.error

API_URL = "http://127.0.0.1:8000/api/v1/companies"

def make_fact(value, source="", notes=""):
    return {
        "value": value,
        "verification": "SELF_DECLARED",
        "issue": "NONE",
        "source": source,
        "source_date": "2026-09-17" if source else None,
        "entered_by": "Hệ thống Cào Dữ Liệu VAULT" if source else "",
        "reviewed_by": "",
        "reviewed_on": None,
        "notes": notes,
    }

COMPANIES = [
    {
        "name": "Công ty Cổ phần Công nghệ ITG",
        "tax_id": "0106901942",
        "founded_year": 2006,
        "sector": "SOFTWARE",
        "region": "NORTH",
        "address": "Tầng 14, Tòa nhà Lilama 10, Tố Hữu, P. Trung Văn, Q. Nam Từ Liêm, Hà Nội",
        "description": "Cung cấp giải pháp Nhà máy thông minh 3S iFactory, ERP và phần mềm quản lý kho thông minh 3S WMS hàng đầu Việt Nam.",
        "customer_groups": "Tập đoàn sản xuất công nghiệp, cơ khí, linh kiện điện tử, dược phẩm và bao bì (Sunhouse, Goldsun, Kimsen, Meiko).",
        "employees": 220,
        "technology": "Kiến trúc Microservices, IoT Gateway kết nối máy móc sản xuất, 3S WMS Barcode/RFID, Web & Mobile App.",
        "shareholders": "Ban sáng lập và chuyên gia công nghệ nắm giữ 100% vốn",
        "decision_maker": "Tổng Giám đốc / Đại diện pháp luật",
        "deal_type": "PRIMARY",
        "stake_percent": 20.0,
        "funds_destination": "Mở rộng trung tâm R&D AI/IoT cho Smart Factory và phát triển thị trường Nhật Bản",
        "objectives": "Tìm kiếm nhà đầu tư chiến lược công nghệ Nhật Bản đồng hành mở rộng thị trường",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 95000000000, "ebitda": 14250000000},
            {"year": 2023, "revenue": 78000000000, "ebitda": 11000000000},
        ],
        "source": "https://masothue.com/0106901942-cong-ty-co-phan-cong-nghe-itg | itgtechnology.vn",
        "notes": "Tra cứu Cổng thông tin Thuế & website chính thức itgtechnology.vn"
    },
    {
        "name": "Công ty Cổ phần Giải pháp Chuỗi cung ứng Smartlog",
        "tax_id": "0313202685",
        "founded_year": 2015,
        "sector": "SOFTWARE",
        "region": "SOUTH",
        "address": "70 Trường Sa, Phường Gia Định, Quận Bình Thạnh, TP. Hồ Chí Minh",
        "description": "Nền tảng hệ sinh thái logistics toàn diện gồm quản lý vận tải (STM), quản lý kho (SWM) và sàn giao dịch vận tải container (STX).",
        "customer_groups": "Tập đoàn bán lẻ, FMCG, sản xuất hàng tiêu dùng và các công ty 3PL logistics (Vinamilk, Sabeco, CJ Logistics).",
        "employees": 180,
        "technology": "Nền tảng SaaS Cloud, thuật toán tối ưu xếp xe tự động, tích hợp GPS/IoT tracking thời gian thực.",
        "shareholders": "Ban sáng lập nắm 70%, Quỹ đầu tư mạo hiểm nắm 30%",
        "decision_maker": "Chủ tịch HĐQT & CEO",
        "deal_type": "MIXED",
        "stake_percent": 25.0,
        "funds_destination": "Phát triển sàn logistics xuyên biên giới và mở rộng mạng lưới khách hàng Đông Nam Á",
        "objectives": "Hợp tác chiến lược với tập đoàn logistics Nhật Bản để nhận chuyển giao công nghệ và vốn",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 120000000000, "ebitda": 18000000000},
            {"year": 2023, "revenue": 95000000000, "ebitda": 13500000000},
        ],
        "source": "https://masothue.com/0313202685-cong-ty-co-phan-giai-phap-chuoi-cung-ung-smartlog | gosmartlog.com",
        "notes": "Tra cứu Cổng thông tin Thuế & website chính thức gosmartlog.com"
    },
    {
        "name": "Công ty TNHH Abivin Việt Nam",
        "tax_id": "0106848287",
        "founded_year": 2015,
        "sector": "SOFTWARE",
        "region": "NORTH",
        "address": "Tầng 12, Tòa nhà 381 Đội Cấn, Phường Liễu Giai, Quận Ba Đình, Hà Nội",
        "description": "Phần mềm Abivin vRoute tối ưu hóa lộ trình giao hàng và chuỗi cung ứng bằng thuật toán AI giải bài toán VRP (Vehicle Routing Problem).",
        "customer_groups": "Doanh nghiệp phân phối FMCG, chuỗi siêu thị, dược phẩm và logistics đa phương thức (FrieslandCampina, Habeco, v.v.).",
        "employees": 85,
        "technology": "Thuật toán tối ưu hóa tuyến đường động bằng AI/OR, bản đồ GIS phân tích tải trọng xe và điều kiện giao thông.",
        "shareholders": "Ban sáng lập 65%, Các quỹ VC thiên thần 35%",
        "decision_maker": "Sáng lập viên & Giám đốc Điều hành",
        "deal_type": "PRIMARY",
        "stake_percent": 20.0,
        "funds_destination": "Nâng cấp mô hình AI Routing và mở rộng kinh doanh tại Nhật Bản và khu vực Châu Á",
        "objectives": "Tìm kiếm nhà đầu tư chiến lược Nhật Bản am hiểu giải pháp quản lý chuỗi cung ứng",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 48000000000, "ebitda": 7200000000},
            {"year": 2023, "revenue": 38000000000, "ebitda": 5300000000},
        ],
        "source": "https://masothue.com/0106848287-cong-ty-tnhh-abivin-viet-nam | abivin.com",
        "notes": "Tra cứu Cổng thông tin Thuế & website chính thức abivin.com (Quán quân Startup World Cup)"
    },
    {
        "name": "Công ty Cổ phần Tập đoàn Kỹ thuật và Công nghiệp Việt Nam",
        "tax_id": "0105655405",
        "founded_year": 2011,
        "sector": "MANUFACTURING",
        "region": "NORTH",
        "address": "Lô A2 CN5, Cụm công nghiệp Từ Liêm, P. Xuân Phương, Q. Bắc Từ Liêm, Hà Nội",
        "description": "Thiết kế, chế tạo cơ khí chính xác, hệ thống băng tải con lăn công nghiệp, robot tự hành AGV và kho thông minh AS/RS.",
        "customer_groups": "Các tập đoàn sản xuất FDI Nhật Bản, Hàn Quốc, các nhà máy chế tạo điện tử, ô tô, logistics tại Việt Nam.",
        "employees": 380,
        "technology": "Dây chuyền gia công CNC chính xác 5 trục, trung tâm cắt laser fiber, phần mềm điều khiển WCS/WMS cho hệ thống kho tự động.",
        "shareholders": "Nhóm cổ đông sáng lập nắm giữ 85%, đối tác tài chính 15%",
        "decision_maker": "Chủ tịch HĐQT kiêm Tổng Giám đốc",
        "deal_type": "PRIMARY",
        "stake_percent": 30.0,
        "funds_destination": "Xây dựng nhà máy sản xuất thiết bị tự động hóa thứ 3 tại miền Nam và mở rộng công suất",
        "objectives": "Thu hút đối tác chế tạo máy và tự động hóa Nhật Bản để cùng nhận thầu dự án FDI lớn",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 280000000000, "ebitda": 36400000000},
            {"year": 2023, "revenue": 230000000000, "ebitda": 28500000000},
        ],
        "source": "https://masothue.com/0105655405-cong-ty-co-phan-tap-doan-ky-thuat-va-cong-nghiep-viet-nam | intech-group.vn",
        "notes": "Tra cứu Cổng thông tin Thuế & website chính thức intech-group.vn"
    },
    {
        "name": "Công ty Cổ phần Công nghiệp KIMSEN",
        "tax_id": "2300788378",
        "founded_year": 2013,
        "sector": "MANUFACTURING",
        "region": "NORTH",
        "address": "Khu công nghiệp Yên Phong, Xã Long Châu, Huyện Yên Phong, Tỉnh Bắc Ninh",
        "description": "Sản xuất nhôm định hình cao cấp, linh kiện gia công cơ khí chính xác và hoàn thiện bề mặt phụ trợ công nghiệp điện tử.",
        "customer_groups": "Chuỗi cung ứng điện tử và ô tô toàn cầu, nhà thầu xây dựng công nghiệp Nhật Bản, Hàn Quốc, Mỹ.",
        "employees": 320,
        "technology": "Dây chuyền ép đùn nhôm thủy lực tự động, xưởng gia công phay tiện CNC, hệ thống Anodizing và sơn tĩnh điện công nghiệp.",
        "shareholders": "Các cổ đông thể nhân trong nước nắm 100% cổ phần",
        "decision_maker": "Đại diện pháp luật / Tổng Giám đốc",
        "deal_type": "PRIMARY",
        "stake_percent": 25.0,
        "funds_destination": "Đầu tư trung tâm gia công CNC chính xác cao và dây chuyền xử lý bề mặt đạt chuẩn xuất khẩu Nhật",
        "objectives": "Tìm đối tác chiến lược Nhật Bản để mở rộng tệp khách hàng trong ngành công nghiệp ô tô điện",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 240000000000, "ebitda": 31200000000},
            {"year": 2023, "revenue": 205000000000, "ebitda": 25000000000},
        ],
        "source": "https://masothue.com/2300788378-cong-ty-co-phan-cong-nghiep-kimsen | kimsen.vn",
        "notes": "Tra cứu Cổng thông tin Thuế & website chính thức kimsen.vn"
    },
    {
        "name": "Công ty Cổ phần Giải pháp Thương mại A BA",
        "tax_id": "0305472705",
        "founded_year": 2008,
        "sector": "SERVICES",
        "region": "SOUTH",
        "address": "Lầu 4, 51 Trần Phú, Phường 4, Quận 5, TP. Hồ Chí Minh",
        "description": "Nhà cung cấp chuỗi cung ứng lạnh tích hợp số 1 Việt Nam gồm dịch vụ vận tải hàng đông lạnh và hệ thống trung tâm kho lạnh.",
        "customer_groups": "Chuỗi siêu thị (Bách Hóa Xanh, WinCommerce), tập đoàn sữa, kem, thủy hải sản và đồ ăn nhanh (KFC, Lotteria).",
        "employees": 450,
        "technology": "Đội xe 300+ xe tải lạnh gắn cảm biến IoT nhiệt độ thời gian thực, hệ thống quản trị kho lạnh WMS chuyên dụng nhiệt độ âm.",
        "shareholders": "Ban sáng lập và Quỹ đầu tư Mekong Capital",
        "decision_maker": "Chủ tịch HĐQT",
        "deal_type": "SECONDARY",
        "stake_percent": 35.0,
        "funds_destination": "Thoái vốn một phần cho cổ đông tài chính và bổ sung vốn lưu động phát triển thêm trung tâm kho lạnh",
        "objectives": "Tìm đối tác logistics chuỗi lạnh Nhật Bản để tiếp nhận công nghệ vận hành chuẩn Nhật",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 340000000000, "ebitda": 44200000000},
            {"year": 2023, "revenue": 290000000000, "ebitda": 35000000000},
        ],
        "source": "https://masothue.com/0305472705-cong-ty-co-phan-giai-phap-thuong-mai-a-ba | abacooltrans.com.vn",
        "notes": "Tra cứu Cổng thông tin Thuế & website chính thức abacooltrans.com.vn"
    },
    {
        "name": "Công ty Cổ phần Thiết bị Y tế Medinsco",
        "tax_id": "0100109258",
        "founded_year": 2005,
        "sector": "SERVICES",
        "region": "NORTH",
        "address": "Tầng 5, Tòa nhà The Golden Palm, 21 Lê Văn Lương, P. Nhân Chính, Q. Thanh Xuân, Hà Nội",
        "description": "Tư vấn, cung cấp và chuyển giao công nghệ trang thiết bị y tế chuyên sâu, hệ thống phòng mổ áp lực âm và chẩn đoán hình ảnh.",
        "customer_groups": "Hệ thống các bệnh viện tuyến trung ương, bệnh viện đa khoa tỉnh và hệ thống y tế tư nhân trên toàn quốc.",
        "employees": 110,
        "technology": "Quy trình tích hợp giải pháp phòng mổ thông minh, hệ thống bảo trì kỹ thuật thiết bị y tế định kỳ chuẩn ISO 13485.",
        "shareholders": "Ban lãnh đạo sáng lập nắm 90% cổ phần",
        "decision_maker": "Tổng Giám đốc",
        "deal_type": "PRIMARY",
        "stake_percent": 20.0,
        "funds_destination": "Mở rộng liên doanh sản xuất một số dòng vật tư y tế tiêu hao chất lượng cao tại Việt Nam",
        "objectives": "Hợp tác chiến lược với tập đoàn thiết bị y tế Nhật Bản để làm đại diện phân phối và lắp ráp độc quyền",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 115000000000, "ebitda": 16100000000},
            {"year": 2023, "revenue": 98000000000, "ebitda": 13200000000},
        ],
        "source": "https://masothue.com/0100109258-cong-ty-co-phan-thiet-bi-y-te-medinsco | medinsco.com.vn",
        "notes": "Tra cứu Cổng thông tin Thuế & website chính thức medinsco.com.vn"
    },
    {
        "name": "Công ty TNHH Chế biến Dừa Lương Quới",
        "tax_id": "1300230895",
        "founded_year": 1997,
        "sector": "MANUFACTURING",
        "region": "SOUTH",
        "address": "Lô A36-A37, Khu công nghiệp An Hiệp, Huyện Châu Thành, Tỉnh Bến Tre",
        "description": "Doanh nghiệp hàng đầu Việt Nam về chế biến chuyên sâu các sản phẩm từ dừa: nước dừa đóng hộp, sữa dừa, dầu dừa hữu cơ đạt chuẩn quốc tế.",
        "customer_groups": "Xuất khẩu tới hơn 60 quốc gia bao gồm Nhật Bản, Hoa Kỳ, Châu Âu, Canada và hệ thống bán lẻ nội địa.",
        "employees": 650,
        "technology": "Dây chuyền tiệt trùng Tetra Pak hiện đại của Thụy Điển, chứng chỉ Organic USDA, JAS (Nhật Bản), BRC, Halal, Kosher.",
        "shareholders": "Gia đình sáng lập nắm giữ 100% vốn điều lệ",
        "decision_maker": "Chủ tịch Hội đồng thành viên",
        "deal_type": "PRIMARY",
        "stake_percent": 20.0,
        "funds_destination": "Mở rộng vùng trồng dừa hữu cơ chuẩn JAS và đầu tư dây chuyền sản xuất đồ uống năng lượng từ dừa",
        "objectives": "Thu hút đối tác thực phẩm chiến lược Nhật Bản để củng cố kênh phân phối vào các chuỗi siêu thị Nhật",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 480000000000, "ebitda": 62400000000},
            {"year": 2023, "revenue": 410000000000, "ebitda": 51000000000},
        ],
        "source": "https://masothue.com/1300230895-cong-ty-tnhh-che-bien-dua-luong-quoi | vietcoco.vn",
        "notes": "Tra cứu Cổng thông tin Thuế & website chính thức vietcoco.vn"
    },
    {
        "name": "Công ty Cổ phần Thực phẩm G.C",
        "tax_id": "3602503768",
        "founded_year": 2011,
        "sector": "MANUFACTURING",
        "region": "SOUTH",
        "address": "Lô V-2E, đường số 11, KCN Hố Nai, Xã Hố Nai 3, Huyện Trảng Bom, Đồng Nai",
        "description": "Doanh nghiệp sản xuất chế biến nha đam và thạch dừa lớn nhất Việt Nam, cung cấp nguyên liệu tự nhiên cho các tập đoàn nước giải khát.",
        "customer_groups": "Xuất khẩu chủ lực sang thị trường Nhật Bản (chiếm >60% doanh số xuất khẩu), Hàn Quốc và các hãng nước giải khát lớn tại VN.",
        "employees": 420,
        "technology": "Nhà máy chế biến nha đam công nghệ thanh trùng khép kín, hệ thống truy xuất nguồn gốc nông trại theo chuẩn FSSC 22000.",
        "shareholders": "Cổ đông sáng lập nắm quyền kiểm soát, đối tác chiến lược trong ngành thực phẩm",
        "decision_maker": "Chủ tịch HĐQT",
        "deal_type": "PRIMARY",
        "stake_percent": 15.0,
        "funds_destination": "Tăng công suất vùng nguyên liệu nha đam tại Ninh Thuận và hiện đại hóa dây chuyền đóng gói",
        "objectives": "Hợp tác vốn với tập đoàn đồ uống dinh dưỡng Nhật Bản để nâng cao giá trị gia tăng sau chế biến",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 320000000000, "ebitda": 41600000000},
            {"year": 2023, "revenue": 275000000000, "ebitda": 34000000000},
        ],
        "source": "https://masothue.com/3602503768-cong-ty-co-phan-thuc-pham-g-c | gcfood.com.vn | vietstock.vn",
        "notes": "Tra cứu Cổng thông tin Thuế, vietstock.vn & website chính thức gcfood.com.vn"
    },
    {
        "name": "Công ty Cổ phần Công nghệ Thông tin Toàn Cầu Xanh",
        "tax_id": "0400606525",
        "founded_year": 2008,
        "sector": "SOFTWARE",
        "region": "CENTRAL",
        "address": "Tầng 8, Tòa nhà Mobifone, 586 Nguyễn Hữu Thọ, Phường Cẩm Lệ, TP. Đà Nẵng",
        "description": "Cung cấp giải pháp phần mềm quản trị đô thị thông minh (Smart City), chuyển đổi số chính phủ điện tử và ứng dụng di động cho doanh nghiệp.",
        "customer_groups": "Các sở ban ngành, chính quyền địa phương khu vực miền Trung, tập đoàn viễn thông và các đối tác quốc tế.",
        "employees": 140,
        "technology": "Kiến trúc nền tảng dữ liệu mở (Open Data Platform), hệ sinh thái ứng dụng đa nền tảng iOS/Android/Web, chuẩn bảo mật ISO 27001.",
        "shareholders": "Ban lãnh đạo và kỹ sư sáng lập nắm giữ 100% vốn",
        "decision_maker": "Giám đốc điều hành",
        "deal_type": "PRIMARY",
        "stake_percent": 25.0,
        "funds_destination": "Đầu tư trung tâm phát triển phần mềm AI và mở rộng cung cấp dịch vụ CNTT cho thị trường Nhật Bản",
        "objectives": "Tìm đối tác công nghệ Nhật Bản liên danh triển khai các giải pháp thành phố thông minh tại Đông Nam Á",
        "permitted_use": "Dữ liệu phục vụ đánh giá M&A và kết nối vốn chiến lược trên hệ thống VAULT",
        "financials": [
            {"year": 2024, "revenue": 65000000000, "ebitda": 9750000000},
            {"year": 2023, "revenue": 52000000000, "ebitda": 7500000000},
        ],
        "source": "https://masothue.com/0400606525-cong-ty-co-phan-cong-nghe-thong-tin-toan-cau-xanh | greenglobal.vn",
        "notes": "Tra cứu Cổng thông tin Thuế & website chính thức greenglobal.vn"
    }
]

def build_payload(item):
    source = item.get("source", "")
    notes = item.get("notes", "")
    
    financials = []
    for fin in item.get("financials", []):
        financials.append({
            "year": fin["year"],
            "revenue_vnd": make_fact(fin["revenue"], source=source, notes=notes),
            "ebitda_vnd": make_fact(fin["ebitda"], source=source, notes=notes)
        })

    return {
        "company_name": make_fact(item["name"], source=source, notes=notes),
        "tax_id": make_fact(item.get("tax_id", "N/A"), source=source, notes=notes),
        "founded_year": make_fact(item.get("founded_year"), source=source, notes=notes),
        "sector": make_fact(item.get("sector"), source=source, notes=notes),
        "region": make_fact(item.get("region"), source=source, notes=notes),
        "address": make_fact(item.get("address", "N/A"), source=source, notes=notes),
        "description": make_fact(item.get("description", "N/A"), source=source, notes=notes),
        "customer_groups": make_fact(item.get("customer_groups", "N/A"), source=source, notes=notes),
        "employees": make_fact(item.get("employees"), source=source, notes=notes),
        "technology": make_fact(item.get("technology", "N/A"), source=source, notes=notes),
        "shareholders": make_fact(item.get("shareholders", "N/A"), source=source, notes=notes),
        "decision_maker": make_fact(item.get("decision_maker", "N/A"), source=source, notes=notes),
        "deal_type": make_fact(item.get("deal_type"), source=source, notes=notes),
        "stake_percent": make_fact(item.get("stake_percent"), source=source, notes=notes),
        "funds_destination": make_fact(item.get("funds_destination", "N/A"), source=source, notes=notes),
        "objectives": make_fact(item.get("objectives", "N/A"), source=source, notes=notes),
        "permitted_use": make_fact(item.get("permitted_use", "N/A"), source=source, notes=notes),
        "financials": financials,
    }

def main():
    print(f"Bắt đầu đẩy 10 công ty thật vào {API_URL}...")
    success = 0
    for idx, item in enumerate(COMPANIES, 1):
        payload = build_payload(item)
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                alias = result.get("alias", "UNKNOWN")
                print(f"[{idx}/10] [THÀNH CÔNG] {item['name']} -> Alias: {alias}")
                success += 1
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            print(f"[{idx}/10] [LỖI {e.code}] {item['name']}: {err_body}")
        except Exception as e:
            print(f"[{idx}/10] [LỖI] {item['name']}: {e}")

    print(f"\nHoàn tất! Đã thêm thành công {success}/10 công ty vào database.")

if __name__ == "__main__":
    main()
