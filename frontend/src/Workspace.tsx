import { useEffect, useState } from 'react'
import App from './App'
import CompanyList from './features/profiles/CompanyList'
import CompanyForm, { EditCompany } from './features/profiles/CompanyForm'
import CompanyDetail from './features/profiles/CompanyDetail'
import RoomList from './features/rooms/RoomList'
import RoomPage from './features/rooms/RoomPage'
import DocumentPage from './features/rooms/DocumentPage'
<<<<<<< Updated upstream
import './workspace.css'

function pathOf(hash: string) {
  return hash.slice(1).split('?')[0] || '/companies'
}

function crumb(path: string) {
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
  if (path === '/companies/new') return 'Tạo hồ sơ'
  if (path.endsWith('/edit')) return 'Chỉnh sửa hồ sơ'
  if (path.startsWith('/companies/') && path !== '/companies')
    return 'Chi tiết doanh nghiệp'
  if (path.includes('/documents/')) return 'Tài liệu'
  if (path.startsWith('/rooms/') && path !== '/rooms') return 'Phòng dữ liệu'
  if (path === '/rooms') return 'Phòng dữ liệu'
  return 'Hồ sơ doanh nghiệp'
=======
import InvestorMvp from './features/investor-mvp/InvestorMvp'
import DealList from './features/deals/DealList'
import VaultHome from './features/vault/VaultHome'
import AccessWorkspace from './features/access/AccessWorkspace'
import {
  hasConfiguredBackend,
  getAuthSession,
  setAuthSession,
  type AuthSession,
} from './api/config'
import { request } from './api/workspace'
import './workspace.css'

type Role = NonNullable<AuthSession>['user']['role']

const navigation: { label: string; href: string; roles: Role[] }[] = [
  { label: 'Tổng quan', href: '#/vault', roles: ['BUYER', 'SELLER', 'VAULT_ADMIN', 'LEGAL', 'TECH_DD', 'FINANCE'] },
  { label: 'Deals', href: '#/deals', roles: ['BUYER', 'SELLER', 'VAULT_ADMIN', 'LEGAL', 'TECH_DD', 'FINANCE'] },
  { label: 'Disclosure approvals', href: '#/disclosures', roles: ['BUYER', 'SELLER', 'VAULT_ADMIN', 'LEGAL'] },
  { label: 'Doanh nghiệp', href: '#/companies', roles: ['SELLER', 'VAULT_ADMIN', 'LEGAL'] },
  { label: 'Phòng dữ liệu', href: '#/rooms', roles: ['SELLER', 'VAULT_ADMIN', 'LEGAL', 'TECH_DD'] },
  { label: 'Kết nối API', href: '#/health', roles: ['VAULT_ADMIN'] },
]

function routeAllowed(path: string, role?: Role) {
  if (!role || path === '/investor-mvp') return false
  if (path === '/vault') return true
  if (path === '/disclosures' || path === '/access') return ['BUYER', 'SELLER', 'VAULT_ADMIN', 'LEGAL'].includes(role)
  if (path === '/companies' || path.startsWith('/companies/')) return ['SELLER', 'VAULT_ADMIN', 'LEGAL'].includes(role)
  if (path === '/rooms' || path.startsWith('/rooms/')) return ['SELLER', 'VAULT_ADMIN', 'LEGAL', 'TECH_DD'].includes(role)
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
    path === '/access' || path === '/disclosures' ||
    path === '/health'
  )
}

function BackendRequiredNotice({ target }: { target: string }) {
  return (
    <section className="panel backend-required">
      <p className="eyebrow">Frontend-only demo</p>
      <h1>Màn này cần backend riêng</h1>
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
>>>>>>> Stashed changes
}

export default function Workspace() {
  const [session, setSession] = useState<AuthSession | null>(getAuthSession())
  const [hash, setHash] = useState(location.hash)
  useEffect(() => {
    const change = () => setHash(location.hash)
    addEventListener('hashchange', change)
    return () => removeEventListener('hashchange', change)
  }, [])
<<<<<<< Updated upstream
  const path = pathOf(hash)
  const parts = path.split('/').filter(Boolean)
  const params = new URLSearchParams(hash.split('?')[1] || '')
  if (path === '/health')
    return (
      <div className="health-shell">
        <App />
      </div>
    )
  let screen = <CompanyList />
  if (path === '/companies/new') screen = <CompanyForm />
=======
  const hostedWithoutBackend = isHostedWithoutBackend()
  const path =
    hash.slice(1).split('?')[0] ||
    (hostedWithoutBackend ? '/investor-mvp' : session ? '/vault' : '/companies')
  const parts = path.split('/').filter(Boolean)
  const params = new URLSearchParams(hash.split('?')[1] || '')
  if (path === '/health' && !hostedWithoutBackend && session?.user.role === 'VAULT_ADMIN') return <App />
  let screen = <CompanyList />
  if (hostedWithoutBackend && needsBackend(path))
    screen = <BackendRequiredNotice target={path} />
  else if (path === '/investor-mvp')
    screen = <InvestorMvp role={session?.user.role} />
  else if (path === '/vault' && session) screen = <VaultHome user={session.user} />
  else if (path === '/access' || path === '/disclosures') screen = <AccessWorkspace role={session?.user.role} initialDealId={params.get('deal') || undefined} />
  else if (path === '/deals') screen = <DealList role={session?.user.role} />
  else if (parts[0] === 'deals' && parts[1])
    screen = <AccessWorkspace role={session?.user.role} initialDealId={parts[1]} />
  else if (path === '/companies/new') screen = <CompanyForm />
>>>>>>> Stashed changes
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
  const companiesActive = path.startsWith('/companies') || path === '/'
  const roomsActive = path.startsWith('/rooms')
  return (
<<<<<<< Updated upstream
    <div className="app-frame">
      <aside className="sidebar">
        <a className="brand sidebar-brand" href="#/companies">
          <span className="brand-mark">V</span>VAULT
        </a>
        <nav className="sidebar-nav" aria-label="Điều hướng chính">
          <a
            href="#/companies"
            className={companiesActive ? 'active' : ''}
            aria-current={companiesActive ? 'page' : undefined}
          >
            <span className="nav-ico" aria-hidden="true">
              ⌂
            </span>
            Hồ sơ doanh nghiệp
          </a>
          <a
            href="#/rooms"
            className={roomsActive ? 'active' : ''}
            aria-current={roomsActive ? 'page' : undefined}
          >
            <span className="nav-ico" aria-hidden="true">
              ▣
            </span>
            Phòng dữ liệu
          </a>
        </nav>
        <div className="sidebar-foot">
          <div className="user-chip">
            <span className="avatar" aria-hidden="true">
              ĐN
            </span>
            <div className="user-meta">
              <strong>Điều hành viên</strong>
              <span>Bản thử nội bộ</span>
            </div>
          </div>
          <span className="demo-pill">Môi trường demo</span>
        </div>
      </aside>
      <div className="workspace-main">
        <p className="local-note">
          Bản thử nội bộ · Chỉ dùng dữ liệu giả lập · Chưa có đăng nhập hay chia
          sẻ cho buyer
        </p>
        <header className="context-bar">
          <div>
            <p className="crumb">
              {crumbs.map(([label, href], i) => (
                <span key={label}>
                  {i > 0 && ' / '}
                  {href ? <a href={href}>{label}</a> : label}
                </span>
              ))}
            </p>
            <h1>{titleOf(path)}</h1>
          </div>
        </header>
        <div key={hash} className="workspace-content">
          {screen}
        </div>
        <footer>
          <span>VAULT · Verified Access to Unlisted Listings & Transactions</span>
          <a href="#/health">Kết nối API</a>
        </footer>
=======
    <main className="shell workspace">
      <header className="topbar">
        <a className="brand" href="#/vault">
          <span className="brand-mark">V</span>VAULT
        </a>
        <nav aria-label="Điều hướng chính">
          {session && navigation.filter((item) => item.roles.includes(session.user.role)).map((item) => <a href={item.href} key={item.href}>{item.label}</a>)}
        </nav>
      </header>
      <p className="local-note">
        Bản thử nội bộ · Chỉ dùng dữ liệu giả lập
        {hostedWithoutBackend
          ? ' · Vercel chưa cấu hình backend, hãy dùng Investor MVP để test flow A–Z'
          : hasConfiguredBackend()
            ? ' · Hosted full-stack demo: frontend gọi backend public đã cấu hình'
            : ''}
      </p>
      {session && (
        <div className="session-bar">
          <span>
            Đăng nhập: <strong>{session.user.display_name}</strong> ·{' '}
            {session.user.username}
          </span>
          <button
            className="secondary"
            onClick={() => {
              setAuthSession(null)
              setSession(null)
            }}
          >
            Đăng xuất
          </button>
        </div>
      )}
      <div key={hash || path} className="workspace-content">
        {hostedWithoutBackend ? screen : session && routeAllowed(path, session.user.role) ? screen : session ? (
          <section className="panel forbidden"><p className="eyebrow">Không có quyền</p><h1>Role {session.user.display_name} không được mở chức năng này</h1><p>Hãy quay lại tổng quan để chọn đúng chức năng được cấp theo tài khoản đăng nhập.</p><a className="button-link" href="#/vault">Về tổng quan</a></section>
        ) : (
          <Login onLogin={setSession} />
        )}
>>>>>>> Stashed changes
      </div>
    </div>
  )
}
