import { useEffect, useState } from 'react'
import App from './App'
import CompanyList from './features/profiles/CompanyList'
import CompanyForm, { EditCompany } from './features/profiles/CompanyForm'
import CompanyDetail from './features/profiles/CompanyDetail'
import RoomList from './features/rooms/RoomList'
import RoomPage from './features/rooms/RoomPage'
import DocumentPage from './features/rooms/DocumentPage'
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
}

export default function Workspace() {
  const [hash, setHash] = useState(location.hash)
  useEffect(() => {
    const change = () => setHash(location.hash)
    addEventListener('hashchange', change)
    return () => removeEventListener('hashchange', change)
  }, [])
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
      </div>
    </div>
  )
}
