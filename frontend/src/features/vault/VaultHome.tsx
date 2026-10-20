import type { AuthUser } from '../../api/config'
import RoleAvatar from '../../components/RoleAvatar'
import { ROLE_META } from '../auth/roles'

const moduleIcons = [
  'M3 7h18M3 7v12a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V7M3 7l2-3h14l2 3M9 11h6',
  'M12 3 4 6v6c0 4.4 3.4 8.3 8 9 4.6-.7 8-4.6 8-9V6zM9 12l2 2 4-4',
  'M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16M15 9h4a1 1 0 0 1 1 1v11M8 8h3M8 12h3M8 16h3M2 21h20',
  'M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z',
]

const roleModules: Record<
  AuthUser['role'],
  { title: string; description: string; href: string }[]
> = {
  BUYER: [
    {
      title: 'Deal của tôi',
      description: 'Gửi nhu cầu mua, xem Teaser, LOI và tài liệu được duyệt.',
      href: '#/deals',
    },
    {
      title: 'Yêu cầu truy cập',
      description: 'Xin mở Lớp 2, Lớp 3 hoặc tài liệu closing theo mục đích.',
      href: '#/disclosures',
    },
  ],
  SELLER: [
    {
      title: 'Hồ sơ doanh nghiệp',
      description:
        'Pháp nhân, sở hữu, dữ kiện tự khai; gửi dữ kiện đi duyệt kèm bằng chứng.',
      href: '#/companies',
    },
    {
      title: 'Phê duyệt truy cập',
      description: 'Duyệt buyer, file, phiên bản, thời hạn và thu hồi quyền.',
      href: '#/disclosures',
    },
    {
      title: 'Deal của doanh nghiệp',
      description: 'Theo dõi tiến độ và phản hồi finding Tech DD.',
      href: '#/deals',
    },
    {
      title: 'Phòng dữ liệu',
      description: 'Quản lý tài liệu và phiên bản.',
      href: '#/rooms',
    },
  ],
  VAULT_ADMIN: [
    {
      title: 'Lead & deal',
      description: 'Tạo deal, gán buyer và seller, điều phối các bước.',
      href: '#/deals',
    },
    {
      title: 'Phê duyệt truy cập',
      description: 'Theo dõi yêu cầu, quyền, hết hạn và thu hồi.',
      href: '#/disclosures',
    },
    {
      title: 'Hồ sơ doanh nghiệp',
      description: 'Quản lý hồ sơ seller và gửi dữ kiện đi duyệt.',
      href: '#/companies',
    },
    {
      title: 'Duyệt dữ kiện',
      description:
        'Đối chiếu bằng chứng và gắn nhãn xác minh cho dữ kiện người khác gửi.',
      href: '#/reviews',
    },
    {
      title: 'Phòng dữ liệu',
      description: 'Tạo phòng, tải lên, quản lý phiên bản và xóa tài liệu.',
      href: '#/rooms',
    },
  ],
  LEGAL: [
    {
      title: 'Pháp lý theo deal',
      description: 'NDA, điều kiện tham gia, ký hợp đồng và điều kiện đóng.',
      href: '#/deals',
    },
    {
      title: 'Phê duyệt truy cập',
      description:
        'Duyệt Lớp 1/2/3, tài liệu closing và chuyển dữ liệu ra nước ngoài.',
      href: '#/disclosures',
    },
    {
      title: 'Duyệt dữ kiện',
      description:
        'Đối chiếu bằng chứng và gắn nhãn xác minh cho từng dữ kiện.',
      href: '#/reviews',
    },
    {
      title: 'Phòng dữ liệu',
      description: 'Xem tài liệu pháp lý và tài liệu closing.',
      href: '#/rooms',
    },
  ],
  TECH_DD: [
    {
      title: 'Thẩm định kỹ thuật',
      description: 'Ghi nhận finding, theo dõi xử lý, ký xác nhận kết thúc.',
      href: '#/deals',
    },
    {
      title: 'Phòng dữ liệu',
      description: 'Tài liệu kỹ thuật của seller.',
      href: '#/rooms',
    },
  ],
  FINANCE: [
    {
      title: 'Phí và thanh toán',
      description:
        'Lập phí, xuất hóa đơn, ghi nhận thanh toán, theo dõi quá hạn.',
      href: '#/deals',
    },
    {
      title: 'Trạng thái ký & đóng',
      description: 'Xem deal đã ký, đã đóng để lập phí thành công đúng lúc.',
      href: '#/deals',
    },
  ],
}

export default function VaultHome({ user }: { user: AuthUser }) {
  return (
    <section className="vault-home">
      <div className="hero-panel">
        <span className="hero-avatar">
          <RoleAvatar role={user.role} size={76} />
        </span>
        <p className="eyebrow">Không gian làm việc</p>
        <h2>Không gian làm việc của {user.display_name}</h2>
        <p className="hero-sub">
          Các chức năng được sắp xếp theo đúng trách nhiệm của vai trò “
          {ROLE_META[user.role].label}”.
        </p>
      </div>
      <div className="module-grid">
        {roleModules[user.role].map((module, index) => (
          <a
            className="panel module-card"
            href={module.href}
            key={module.title}
          >
            <span className="module-ico" aria-hidden="true">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d={moduleIcons[index % moduleIcons.length]} />
              </svg>
            </span>
            <span className="module-arrow">→</span>
            <h2>{module.title}</h2>
            <p>{module.description}</p>
          </a>
        ))}
      </div>
    </section>
  )
}
