import { useEffect, useState } from 'react'
import App from './App'
import CompanyList from './features/profiles/CompanyList'
import CompanyForm, { EditCompany } from './features/profiles/CompanyForm'
import CompanyDetail from './features/profiles/CompanyDetail'
import RoomList from './features/rooms/RoomList'
import RoomPage from './features/rooms/RoomPage'
import DocumentPage from './features/rooms/DocumentPage'
import InvestorMvp from './features/investor-mvp/InvestorMvp'
import DealList from './features/deals/DealList'
import VaultHome from './features/vault/VaultHome'
import AccessWorkspace from './features/access/AccessWorkspace'
import Landing from './features/landing/Landing'
import {
  hasConfiguredBackend,
  getAuthSession,
  setAuthSession,
  type AuthSession,
} from './api/config'
import { request } from './api/workspace'

type Role = NonNullable<AuthSession>['user']['role']

// Outline icons (24px grid, stroke = currentColor).
const icons = {
  home: 'M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z',
  deals:
    'M3 7h18M3 7v12a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V7M3 7l2-3h14l2 3M9 11h6',
  approvals: 'M12 3 4 6v6c0 4.4 3.4 8.3 8 9 4.6-.7 8-4.6 8-9V6zM9 12l2 2 4-4',
  companies:
    'M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16M15 9h4a1 1 0 0 1 1 1v11M8 8h3M8 12h3M8 16h3M2 21h20',
  rooms:
    'M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z',
}

function Icon({ name }: { name: keyof typeof icons }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d={icons[name]} />
    </svg>
  )
}

function pathOf(hash: string) {
  return hash.slice(1).split('?')[0] || ''
}

// Sidebar entries. A session only sees sections its synthetic role may open.
const navigation: {
  label: string
  href: string
  icon: keyof typeof icons
  roles: Role[]
}[] = [
  {
    label: 'Tổng quan',
    href: '#/vault',
    icon: 'home',
    roles: ['BUYER', 'SELLER', 'VAULT_ADMIN', 'LEGAL', 'TECH_DD', 'FINANCE'],
  },
  {
    label: 'Deals',
    href: '#/deals',
    icon: 'deals',
    roles: ['BUYER', 'SELLER', 'VAULT_ADMIN', 'LEGAL', 'TECH_DD', 'FINANCE'],
  },
  {
    label: 'Disclosure approvals',
    href: '#/disclosures',
    icon: 'approvals',
    roles: ['BUYER', 'SELLER', 'VAULT_ADMIN', 'LEGAL'],
  },
  {
    label: 'Doanh nghiệp',
    href: '#/companies',
    icon: 'companies',
    roles: ['SELLER', 'VAULT_ADMIN', 'LEGAL'],
  },
  {
    label: 'Phòng dữ liệu',
    href: '#/rooms',
    icon: 'rooms',
    roles: ['SELLER', 'VAULT_ADMIN', 'LEGAL', 'TECH_DD'],
  },
]

function routeAllowed(path: string, role?: Role) {
  if (!role || path === '/investor-mvp') return false
  if (path === '/vault') return true
  if (path === '/disclosures' || path === '/access')
    return ['BUYER', 'SELLER', 'VAULT_ADMIN', 'LEGAL'].includes(role)
  if (path === '/companies' || path.startsWith('/companies/'))
    return ['SELLER', 'VAULT_ADMIN', 'LEGAL'].includes(role)
  if (path === '/rooms' || path.startsWith('/rooms/'))
    return ['SELLER', 'VAULT_ADMIN', 'LEGAL', 'TECH_DD'].includes(role)
  if (path === '/health') return role === 'VAULT_ADMIN'
  if (path === '/deals' || path.startsWith('/deals/')) return true
  return false
}

function isHostedWithoutBackend() {
  return location.hostname.endsWith('vercel.app') && !hasConfiguredBackend()
}

function needsBackend(path: string) {
  return (
    path === '/companies' ||
    path === '/companies/new' ||
    path.startsWith('/companies/') ||
    path === '/rooms' ||
    path.startsWith('/rooms/') ||
    path === '/deals' ||
    path.startsWith('/deals/') ||
    path === '/vault' ||
    path === '/access' ||
    path === '/disclosures' ||
    path === '/health'
  )
}

function navActive(path: string, href: string) {
  const target = href.slice(1)
  if (target === '/')
    return (
      path === '/' || path === '/companies' || path.startsWith('/companies/')
    )
  return path === target || path.startsWith(target + '/')
}

function crumb(path: string) {
  if (path === '/vault') return [['Tổng quan', '']]
  if (path === '/investor-mvp') return [['Investor MVP', '']]
  if (path === '/access' || path === '/disclosures')
    return [['Disclosure approvals', '']]
  if (path === '/deals') return [['Deals', '']]
  if (path.startsWith('/deals/'))
    return [
      ['Deals', '#/deals'],
      ['Chi tiết', ''],
    ]
  if (path === '/companies/new')
    return [
      ['Hồ sơ doanh nghiệp', '#/companies'],
      ['Tạo hồ sơ', ''],
    ]
  if (path.startsWith('/companies/') && path.endsWith('/edit'))
    return [
      ['Hồ sơ doanh nghiệp', '#/companies'],
      ['Chỉnh sửa', ''],
    ]
  if (path.startsWith('/companies/'))
    return [
      ['Hồ sơ doanh nghiệp', '#/companies'],
      ['Chi tiết', ''],
    ]
  if (path === '/rooms') return [['Phòng dữ liệu', '']]
  if (path.includes('/documents/'))
    return [
      ['Phòng dữ liệu', '#/rooms'],
      ['Tài liệu', ''],
    ]
  if (path.startsWith('/rooms/'))
    return [
      ['Phòng dữ liệu', '#/rooms'],
      ['Chi tiết phòng', ''],
    ]
  return [['Hồ sơ doanh nghiệp', '']]
}

function titleOf(path: string) {
  if (path === '/vault') return 'Tổng quan'
  if (path === '/investor-mvp') return 'Investor MVP'
  if (path === '/access' || path === '/disclosures')
    return 'Disclosure approvals'
  if (path === '/deals') return 'Deals'
  if (path.startsWith('/deals/')) return 'Chi tiết deal'
  if (path === '/companies/new') return 'Tạo hồ sơ'
  if (path.endsWith('/edit')) return 'Chỉnh sửa hồ sơ'
  if (path.startsWith('/companies/') && path !== '/companies')
    return 'Chi tiết doanh nghiệp'
  if (path.includes('/documents/')) return 'Tài liệu'
  if (path.startsWith('/rooms/') && path !== '/rooms') return 'Phòng dữ liệu'
  if (path === '/rooms') return 'Phòng dữ liệu'
  return 'Hồ sơ doanh nghiệp'
}

function BackendRequiredNotice({ target }: { target: string }) {
  return (
    <section className="panel backend-required">
      <p className="eyebrow">Frontend-only demo</p>
      <h2>Màn này cần backend riêng</h2>
      <p>
        Link Vercel hiện chỉ deploy frontend để demo luồng A–Z. Các màn{' '}
        <strong>Doanh nghiệp</strong>, <strong>Phòng dữ liệu</strong> và{' '}
        <strong>Kết nối API</strong> cần FastAPI/PostgreSQL chạy riêng nên không
        dùng trực tiếp trên Vercel-only deployment.
      </p>
      <p>
        Để demo cho đồng nghiệp hoặc nhà đầu tư, hãy dùng màn{' '}
        <strong>Investor MVP</strong>. Màn đó dùng dữ liệu giả lập và không cần
        backend.
      </p>
      <div className="actions">
        <a className="button-link" href="#/investor-mvp">
          Mở Investor MVP
        </a>
        <span className="muted">Route vừa mở: {target}</span>
      </div>
    </section>
  )
}

const demoAccounts = [
  ['buyer', 'Buyer'],
  ['seller', 'Seller'],
  ['admin', 'VAULT Admin'],
  ['legal', 'Legal'],
  ['tech', 'Tech DD'],
  ['finance', 'Finance'],
]

function Login({ onLogin }: { onLogin: (session: AuthSession) => void }) {
  const [username, setUsername] = useState('buyer')
  const [password, setPassword] = useState('vault-demo')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  return (
    <section className="panel login-panel">
      <p className="eyebrow">Synthetic MVP access</p>
      <h1>Đăng nhập VAULT theo vai trò</h1>
      <p className="notice">
        Tài khoản demo chỉ dùng dữ liệu giả lập; không phải SSO/MFA production.
      </p>
      <form
        onSubmit={async (event) => {
          event.preventDefault()
          setBusy(true)
          setError('')
          try {
            const session = await request<AuthSession>('/auth/login', {
              method: 'POST',
              body: JSON.stringify({ username, password }),
            })
            setAuthSession(session)
            onLogin(session)
            location.hash = '/vault'
          } catch (reason) {
            setError(
              reason instanceof Error ? reason.message : 'Đăng nhập thất bại.',
            )
          } finally {
            setBusy(false)
          }
        }}
      >
        <label>
          Vai trò
          <select
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          >
            {demoAccounts.map(([value, label]) => (
              <option key={value} value={value}>
                {label} ({value})
              </option>
            ))}
          </select>
        </label>
        <label>
          Mật khẩu demo
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        {error && (
          <p className="error-box" role="alert">
            {error}
          </p>
        )}
        <button disabled={busy}>
          {busy ? 'Đang đăng nhập…' : 'Đăng nhập'}
        </button>
      </form>
    </section>
  )
}

export default function Workspace() {
  const [session, setSession] = useState<AuthSession | null>(getAuthSession())
  const [hash, setHash] = useState(location.hash)
  useEffect(() => {
    const change = () => setHash(location.hash)
    addEventListener('hashchange', change)
    return () => removeEventListener('hashchange', change)
  }, [])
  const hostedWithoutBackend = isHostedWithoutBackend()
  const path =
    pathOf(hash) ||
    (hostedWithoutBackend ? '/investor-mvp' : session ? '/vault' : '/welcome')
  const parts = path.split('/').filter(Boolean)
  const params = new URLSearchParams(hash.split('?')[1] || '')
  if (path === '/health' && !hostedWithoutBackend)
    return (
      <div className="health-shell">
        <App />
      </div>
    )
  if (path === '/welcome') return <Landing signedIn={Boolean(session)} />
  let screen = <CompanyList />
  if (hostedWithoutBackend && needsBackend(path))
    screen = <BackendRequiredNotice target={path} />
  else if (path === '/investor-mvp')
    screen = <InvestorMvp role={session?.user.role} />
  else if (path === '/vault' && session)
    screen = <VaultHome user={session.user} />
  else if (path === '/access' || path === '/disclosures')
    screen = (
      <AccessWorkspace
        role={session?.user.role}
        initialDealId={params.get('deal') || undefined}
      />
    )
  else if (path === '/deals') screen = <DealList role={session?.user.role} />
  else if (parts[0] === 'deals' && parts[1])
    screen = (
      <AccessWorkspace role={session?.user.role} initialDealId={parts[1]} />
    )
  else if (path === '/companies/new') screen = <CompanyForm />
  else if (path === '/rooms')
    screen = <RoomList companyId={params.get('company') || undefined} />
  else if (parts[0] === 'rooms' && parts[1])
    screen =
      parts[2] === 'documents' && parts[3] ? (
        <DocumentPage roomId={parts[1]} documentId={parts[3]} />
      ) : (
        <RoomPage id={parts[1]} created={params.has('created')} />
      )
  else if (parts[0] === 'companies' && parts[1])
    screen =
      parts[2] === 'edit' ? (
        <EditCompany id={parts[1]} />
      ) : (
        <CompanyDetail id={parts[1]} saved={hash.includes('saved=1')} />
      )
  else if (path !== '/companies')
    screen = (
      <p className="not-found">
        Không tìm thấy trang. <a href="#/companies">Về danh sách</a>
      </p>
    )
  const crumbs = crumb(path)
  if (!session && !hostedWithoutBackend)
    return (
      <main className="auth-shell">
        <div className="auth-stack">
          <span className="brand">
            <span className="brand-mark" aria-hidden="true">
              V
            </span>
            VAULT
          </span>
          <Login onLogin={setSession} />
          <p className="auth-foot">
            VAULT · Verified Access to Unlisted Listings & Transactions
          </p>
        </div>
      </main>
    )
  return (
    <div className="app-frame">
      <aside className="sidebar">
        <a
          className="brand sidebar-brand"
          href={session ? '#/vault' : '#/companies'}
        >
          <span className="brand-mark" aria-hidden="true">
            V
          </span>
          VAULT
        </a>
        <nav className="sidebar-nav" aria-label="Điều hướng chính">
          {navigation
            .filter(
              (item) => !session || item.roles.includes(session.user.role),
            )
            .map((item) => {
              const active = navActive(path, item.href)
              return (
                <a
                  key={item.href}
                  href={item.href}
                  className={active ? 'active' : ''}
                  aria-current={active ? 'page' : undefined}
                >
                  <span className="nav-ico" aria-hidden="true">
                    <Icon name={item.icon} />
                  </span>
                  {item.label}
                </a>
              )
            })}
        </nav>
        <div className="sidebar-foot">
          <div className="user-chip">
            <span className="avatar" aria-hidden="true">
              {session
                ? session.user.display_name.slice(0, 2).toUpperCase()
                : 'ĐN'}
            </span>
            <div className="user-meta">
              <strong>
                {session ? session.user.display_name : 'Chưa đăng nhập'}
              </strong>
              <span>
                {session
                  ? `Đang đăng nhập · ${session.user.username}`
                  : 'Bản thử nội bộ'}
              </span>
            </div>
          </div>
          {session && (
            <button
              className="secondary"
              onClick={() => {
                setAuthSession(null)
                setSession(null)
              }}
            >
              Đăng xuất
            </button>
          )}
        </div>
      </aside>
      <div className="workspace-main form-skin">
        <div className="app-topbar">
          <nav className="crumb" aria-label="Breadcrumb">
            {crumbs.map(([label, href], i) => (
              <span key={label} className="crumb-item">
                {i > 0 && (
                  <span className="crumb-sep" aria-hidden="true">
                    /{' '}
                  </span>
                )}
                {href ? (
                  <a href={href}>{label}</a>
                ) : (
                  <span aria-current="page">{label}</span>
                )}
              </span>
            ))}
          </nav>
          <div className="env-note">
            {hostedWithoutBackend
              ? 'Vercel chưa cấu hình backend, hãy dùng Investor MVP để test flow A–Z'
              : hasConfiguredBackend()
                ? 'Hosted full-stack demo'
                : null}
            <span className="env-pill">Demo nội bộ · dữ liệu giả lập</span>
          </div>
        </div>
        <header className="context-bar">
          <h1>{titleOf(path)}</h1>
        </header>
        <div key={hash} className="workspace-content">
          {hostedWithoutBackend ? (
            screen
          ) : session && routeAllowed(path, session.user.role) ? (
            screen
          ) : session ? (
            <section className="panel forbidden">
              <p className="eyebrow">Không có quyền</p>
              <h2>{session.user.display_name} không được mở chức năng này</h2>
              <p>
                Hãy quay lại tổng quan để chọn đúng chức năng được cấp theo tài
                khoản đăng nhập.
              </p>
              <a className="button-link" href="#/vault">
                Về tổng quan
              </a>
            </section>
          ) : (
            <Login onLogin={setSession} />
          )}
        </div>
        <footer>
          <span>
            VAULT · Verified Access to Unlisted Listings & Transactions
          </span>
          <a href="#/health">Kết nối API</a>
        </footer>
      </div>
    </div>
  )
}
