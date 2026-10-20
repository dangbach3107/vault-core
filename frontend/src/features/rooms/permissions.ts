import { getAuthSession } from '../../api/config'

/** Read-only roles (Legal, Tech DD) see rooms without upload/delete controls; the backend enforces the same. */
export function canEditRooms() {
  const role = getAuthSession()?.user.role
  return role === 'SELLER' || role === 'VAULT_ADMIN'
}

export function canOpenCompanies() {
  const role = getAuthSession()?.user.role
  return role === 'SELLER' || role === 'VAULT_ADMIN' || role === 'LEGAL'
}
