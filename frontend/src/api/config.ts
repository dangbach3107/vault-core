const configuredBase = import.meta.env.VITE_API_BASE_URL as string | undefined

export const apiBase = (configuredBase || '/api/v1').replace(/\/$/, '')

export function hasConfiguredBackend() {
  return Boolean(configuredBase && configuredBase.trim())
}

const demoPasswordKey = 'vault.demoPassword'
const authKey = 'vault.auth'

export type AuthUser = {
  username: string
  role: 'BUYER' | 'SELLER' | 'VAULT_ADMIN' | 'LEGAL' | 'TECH_DD' | 'FINANCE'
  display_name: string
}

export type AuthSession = { access_token: string; user: AuthUser }

export function getAuthSession(): AuthSession | null {
  try {
    const value = localStorage.getItem(authKey)
    return value ? (JSON.parse(value) as AuthSession) : null
  } catch {
    return null
  }
}

export function setAuthSession(value: AuthSession | null) {
  try {
    if (value) localStorage.setItem(authKey, JSON.stringify(value))
    else localStorage.removeItem(authKey)
  } catch {
    // Storage unavailable: the caller still keeps the session in React state.
  }
}

export function getDemoPassword() {
  try {
    return localStorage.getItem(demoPasswordKey) || ''
  } catch {
    return ''
  }
}

export function setDemoPassword(value: string) {
  try {
    if (value) localStorage.setItem(demoPasswordKey, value)
    else localStorage.removeItem(demoPasswordKey)
  } catch {
    // Ignore storage failures; requests will simply omit the demo header.
  }
}

export function demoHeaders(): Record<string, string> {
  const password = getDemoPassword()
  const token = getAuthSession()?.access_token
  return {
    ...(password ? { 'X-Demo-Password': password } : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}
