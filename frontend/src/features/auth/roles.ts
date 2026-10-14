import type { AuthUser } from '../../api/config'

export type Role = AuthUser['role']

/** Display names for each role (Vietnamese label + the short English name used in the UI). */
export const ROLE_META: Record<Role, { label: string; short: string }> = {
  BUYER: { label: 'Người mua', short: 'Buyer' },
  SELLER: { label: 'Người bán', short: 'Seller' },
  VAULT_ADMIN: { label: 'Quản trị VAULT', short: 'Admin' },
  LEGAL: { label: 'Pháp lý', short: 'Legal' },
  TECH_DD: { label: 'Thẩm định kỹ thuật', short: 'Tech DD' },
  FINANCE: { label: 'Tài chính', short: 'Finance' },
}
