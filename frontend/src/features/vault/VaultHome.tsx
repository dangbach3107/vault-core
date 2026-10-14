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
      title: 'Buyer Thesis & Requests',
      description: 'Quản lý nhu cầu mua và các deal đang quan tâm.',
      href: '#/deals',
    },
    {
      title: 'Yêu cầu disclosure',
      description: 'Gửi và theo dõi request L1/L2/L3/Closing theo mục đích.',
      href: '#/disclosures',
    },
  ],
  SELLER: [
    {
      title: 'Hồ sơ Seller',
      description: 'Pháp nhân, ownership, readiness và Trust Profile.',
      href: '#/companies',
    },
    {
      title: 'Phê duyệt disclosure',
      description: 'Duyệt buyer, scope, thời hạn và thu hồi quyền.',
      href: '#/disclosures',
    },
    {
      title: 'Tài liệu & Data Room',
      description: 'Quản lý tài liệu và phiên bản theo thương vụ.',
      href: '#/rooms',
    },
  ],
  VAULT_ADMIN: [
    {
      title: 'Lead & Deal',
      description: 'Tạo, chọn và điều phối hồ sơ thương vụ.',
      href: '#/deals',
    },
    {
      title: 'Disclosure approvals',
      description: 'Theo dõi request, approval, expiry và revoke.',
      href: '#/disclosures',
    },
    {
      title: 'Doanh nghiệp & Trust Profile',
      description: 'Quản lý hồ sơ seller/buyer đã xác minh.',
      href: '#/companies',
    },
    {
      title: 'Phòng dữ liệu',
      description: 'Tạo phòng, upload, version và xóa tài liệu.',
      href: '#/rooms',
    },
  ],
  LEGAL: [
    {
      title: 'Legal & Eligibility',
      description: 'Kiểm tra pháp lý, NDA, authority và Gate 0.',
      href: '#/deals',
    },
    {
      title: 'Disclosure Approval',
      description: 'Duyệt L1/L2/L3/Closing và cross-border scope.',
      href: '#/disclosures',
    },
    {
      title: 'Closing Room',
      description: 'Theo dõi tài liệu closing hạn chế.',
      href: '#/rooms',
    },
  ],
  TECH_DD: [
    {
      title: 'Tech DD',
      description: 'Findings, remediation, impact và sign-off.',
      href: '#/deals',
    },
    {
      title: 'DD Data Room',
      description: 'Tài liệu kỹ thuật được cấp theo scope.',
      href: '#/rooms',
    },
  ],
  FINANCE: [
    {
      title: 'Fee Management',
      description: 'Prep fee, success fee, Tech DD và Build-to-Buy.',
      href: '#/deals',
    },
    {
      title: 'Closing Evidence',
      description: 'Theo dõi chứng từ được cấp quyền.',
      href: '#/rooms',
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
        <p className="eyebrow">VAULT operating system</p>
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
