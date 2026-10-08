import type { AuthUser } from '../../api/config'

const roleModules: Record<AuthUser['role'], { title: string; description: string; href: string }[]> = {
  BUYER: [
    { title: 'Buyer Thesis & Requests', description: 'Quản lý nhu cầu mua và các deal đang quan tâm.', href: '#/deals' },
    { title: 'Yêu cầu disclosure', description: 'Gửi và theo dõi request L1/L2/L3/Closing theo mục đích.', href: '#/disclosures' },
  ],
  SELLER: [
    { title: 'Hồ sơ Seller', description: 'Pháp nhân, ownership, readiness và Trust Profile.', href: '#/companies' },
    { title: 'Phê duyệt disclosure', description: 'Duyệt buyer, scope, thời hạn và thu hồi quyền.', href: '#/disclosures' },
    { title: 'Tài liệu & Data Room', description: 'Quản lý tài liệu và phiên bản theo thương vụ.', href: '#/rooms' },
  ],
  VAULT_ADMIN: [
    { title: 'Lead & Deal', description: 'Tạo, chọn và điều phối hồ sơ thương vụ.', href: '#/deals' },
    { title: 'Disclosure approvals', description: 'Theo dõi request, approval, expiry và revoke.', href: '#/disclosures' },
    { title: 'Doanh nghiệp & Trust Profile', description: 'Quản lý hồ sơ seller/buyer đã xác minh.', href: '#/companies' },
    { title: 'Phòng dữ liệu', description: 'Tạo phòng, upload, version và xóa tài liệu.', href: '#/rooms' },
  ],
  LEGAL: [
    { title: 'Legal & Eligibility', description: 'Kiểm tra pháp lý, NDA, authority và Gate 0.', href: '#/deals' },
    { title: 'Disclosure Approval', description: 'Duyệt L1/L2/L3/Closing và cross-border scope.', href: '#/disclosures' },
    { title: 'Closing Room', description: 'Theo dõi tài liệu closing hạn chế.', href: '#/rooms' },
  ],
  TECH_DD: [
    { title: 'Tech DD', description: 'Findings, remediation, impact và sign-off.', href: '#/deals' },
    { title: 'DD Data Room', description: 'Tài liệu kỹ thuật được cấp theo scope.', href: '#/rooms' },
  ],
  FINANCE: [
    { title: 'Fee Management', description: 'Prep fee, success fee, Tech DD và Build-to-Buy.', href: '#/deals' },
    { title: 'Closing Evidence', description: 'Theo dõi chứng từ được cấp quyền.', href: '#/rooms' },
  ],
}

export default function VaultHome({ user }: { user: AuthUser }) {
  return <section className="vault-home">
    <div className="hero-panel"><p className="eyebrow">VAULT operating system</p><h1>Không gian làm việc của {user.display_name}</h1><p className="hero-sub">Các chức năng độc lập theo đúng trách nhiệm của role. Màn A–Z chỉ còn là demo tham khảo.</p></div>
    <div className="module-grid">{roleModules[user.role].map((module) => <a className="panel module-card" href={module.href} key={module.title}><span className="module-arrow">→</span><h2>{module.title}</h2><p>{module.description}</p></a>)}</div>
  </section>
}
