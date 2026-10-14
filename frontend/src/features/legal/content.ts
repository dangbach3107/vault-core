import { siteInfo } from './siteInfo'

export type LegalSection = { title: string; body: string[] }
export type LegalDoc = {
  title: string
  intro: string
  sections: LegalSection[]
}

const { product } = siteInfo

export const terms: LegalDoc = {
  title: 'Điều khoản sử dụng',
  intro: `Khi truy cập hoặc dùng ${product}, bạn đồng ý với các điều khoản dưới đây. Vui lòng đọc kỹ trước khi sử dụng.`,
  sections: [
    {
      title: '1. Dịch vụ',
      body: [
        `${product} là nền tảng quản lý hồ sơ doanh nghiệp, phòng dữ liệu và quy trình thương vụ M&A. Mỗi người dùng có một vai trò (Người mua, Người bán, Quản trị, Pháp lý, Thẩm định kỹ thuật, Tài chính) và chỉ thấy các chức năng thuộc vai trò đó.`,
      ],
    },
    {
      title: '2. Tài khoản và bảo mật đăng nhập',
      body: [
        'Bạn chịu trách nhiệm giữ bí mật thông tin đăng nhập và mọi hoạt động diễn ra dưới tài khoản của mình.',
        'Hãy báo ngay cho quản trị viên nếu nghi ngờ tài khoản bị sử dụng trái phép. Chúng tôi có thể tạm khóa đăng nhập khi phát hiện nhiều lần nhập sai liên tiếp.',
      ],
    },
    {
      title: '3. Nội dung và tài liệu bạn tải lên',
      body: [
        'Bạn bảo đảm có quyền hợp pháp đối với hồ sơ và tài liệu mình cung cấp, và việc chia sẻ chúng trên nền tảng không vi phạm nghĩa vụ bảo mật hay quyền của bên thứ ba.',
        'Hệ thống chỉ nhận các định dạng PDF, PNG, JPG, TXT, DOCX và XLSX, tối đa 10 MB mỗi tệp. Bạn không được tải lên mã độc, nội dung trái pháp luật hoặc tài liệu có mật khẩu.',
        'Mỗi lần cập nhật tài liệu tạo ra một phiên bản mới; các phiên bản cũ được giữ lại cho đến khi bạn xóa tài liệu.',
      ],
    },
    {
      title: '4. Quyền truy cập theo từng lớp',
      body: [
        'Thông tin doanh nghiệp được chia thành ba lớp công bố. Quyền xem lớp cao hơn chỉ được cấp theo yêu cầu, có người duyệt, mục đích và thời hạn, và có thể bị thu hồi bất cứ lúc nào.',
        'Bạn không được cố truy cập thông tin ngoài phạm vi đã được cấp, và không được chia sẻ lại thông tin đã nhận cho người không có quyền.',
      ],
    },
    {
      title: '5. Hành vi không được phép',
      body: [
        'Can thiệp, dò quét hoặc làm gián đoạn hệ thống; vượt qua cơ chế phân quyền; thu thập dữ liệu hàng loạt; hoặc dùng nền tảng cho mục đích trái pháp luật.',
      ],
    },
    {
      title: '6. Giới hạn trách nhiệm',
      body: [
        `${product} là công cụ hỗ trợ giao dịch, không thay thế tư vấn pháp lý, tài chính hay thẩm định độc lập. Thông tin do người dùng cung cấp là trách nhiệm của người cung cấp. Dịch vụ được cung cấp trên cơ sở nỗ lực hợp lý và có thể gián đoạn khi bảo trì.`,
      ],
    },
    {
      title: '7. Thay đổi điều khoản',
      body: [
        `Chúng tôi có thể cập nhật điều khoản này. Bản mới có hiệu lực khi được đăng tại trang này; việc tiếp tục sử dụng ${product} nghĩa là bạn chấp nhận bản đã cập nhật.`,
      ],
    },
  ],
}

export const privacy: LegalDoc = {
  title: 'Chính sách bảo mật',
  intro: `Chính sách này giải thích ${product} thu thập, sử dụng và bảo vệ thông tin như thế nào.`,
  sections: [
    {
      title: '1. Thông tin chúng tôi xử lý',
      body: [
        'Thông tin tài khoản: tên hiển thị, tên đăng nhập và vai trò.',
        'Thông tin doanh nghiệp và tài liệu do bạn nhập hoặc tải lên (hồ sơ, báo cáo, hợp đồng và các tệp tương tự).',
        'Thông tin kỹ thuật tối thiểu để vận hành và bảo vệ hệ thống, như địa chỉ IP dùng để giới hạn đăng nhập sai (chỉ giữ tạm trong bộ nhớ máy chủ, không lưu lâu dài).',
      ],
    },
    {
      title: '2. Mục đích sử dụng',
      body: [
        'Cung cấp các chức năng của nền tảng, áp dụng phân quyền, bảo vệ hệ thống khỏi truy cập trái phép và cải thiện độ ổn định.',
        'Chúng tôi không bán thông tin của bạn và không dùng tài liệu của bạn cho quảng cáo.',
      ],
    },
    {
      title: '3. Chia sẻ thông tin',
      body: [
        'Thông tin chỉ được hiển thị cho người dùng khác theo lớp công bố và quyền truy cập do chủ hồ sơ hoặc người có thẩm quyền duyệt.',
        'Để vận hành, chúng tôi dùng nhà cung cấp hạ tầng: dịch vụ lưu trữ ứng dụng (Render) và cơ sở dữ liệu (Neon). Họ xử lý dữ liệu thay mặt chúng tôi để vận hành dịch vụ.',
      ],
    },
    {
      title: '4. Lưu trữ và bảo vệ',
      body: [
        'Dữ liệu được truyền qua kết nối mã hóa HTTPS. Truy cập được phân quyền theo vai trò, và đăng nhập sai nhiều lần sẽ bị tạm khóa.',
        'Dữ liệu được giữ cho đến khi chủ sở hữu hoặc quản trị viên xóa. Khi một tài liệu hoặc phòng dữ liệu bị xóa, các phiên bản của nó bị xóa khỏi cơ sở dữ liệu.',
      ],
    },
    {
      title: '5. Phiên đăng nhập',
      body: [
        `${product} không dùng cookie theo dõi. Phiên đăng nhập được lưu trong bộ nhớ trình duyệt của bạn và hết hạn sau 8 giờ hoặc khi bạn đăng xuất.`,
      ],
    },
    {
      title: '6. Quyền của bạn',
      body: [
        'Bạn có thể yêu cầu xem, chỉnh sửa hoặc xóa thông tin của mình thông qua quản trị viên hoặc kênh liên hệ trên trang Liên hệ.',
      ],
    },
    {
      title: '7. Thay đổi chính sách',
      body: [
        'Chúng tôi sẽ đăng bản cập nhật tại trang này và ghi rõ ngày cập nhật.',
      ],
    },
  ],
}
