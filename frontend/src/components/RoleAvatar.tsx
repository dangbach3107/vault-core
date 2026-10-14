import { ROLE_META, type Role } from '../features/auth/roles'
import './role-avatar.css'

// 24px line icons, one per role, so roles are told apart by shape as well as colour.
const glyphs: Record<Role, string> = {
  BUYER:
    'M4 8h16v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1zM9 8V6a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M4 13.5h16',
  SELLER:
    'M3.5 9 5 4.5h14L20.5 9M3.5 9v10a1 1 0 0 0 1 1h15a1 1 0 0 0 1-1V9M3.5 9h17M9.5 20v-6h5v6',
  VAULT_ADMIN:
    'M12 3 4 6v6c0 4.4 3.4 8.3 8 9 4.6-.7 8-4.6 8-9V6zM8.8 12.2l2.2 2.2 4.2-4.4',
  LEGAL:
    'M12 4v16M7.5 20h9M5 8h14M5 8l-2.5 6a3 3 0 0 0 5 0zM19 8l-2.5 6a3 3 0 0 0 5 0z',
  TECH_DD: 'M8.5 8 4 12l4.5 4M15.5 8 20 12l-4.5 4M13.5 6l-3 12',
  FINANCE:
    'M12 4a8 8 0 1 0 0 16 8 8 0 0 0 0-16zM14.6 9.4c-.5-.7-1.4-1.1-2.6-1.1-1.5 0-2.5.8-2.5 1.9 0 2.6 5 1.4 5 4 0 1.1-1 1.9-2.5 1.9-1.2 0-2.1-.4-2.7-1.2M12 6.5v1.8M12 15.7v1.8',
}

export default function RoleAvatar({
  role,
  size = 36,
  className = '',
}: {
  role: Role
  size?: number
  className?: string
}) {
  return (
    <span
      className={`ra ra-${role} ${className}`.trim()}
      style={{ width: size, height: size }}
      role="img"
      aria-label={ROLE_META[role].label}
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.7"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <path d={glyphs[role]} />
      </svg>
    </span>
  )
}
