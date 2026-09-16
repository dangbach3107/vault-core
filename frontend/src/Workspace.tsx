import { useEffect, useState } from 'react'
import App from './App'
import CompanyList from './features/profiles/CompanyList'
import CompanyForm, { EditCompany } from './features/profiles/CompanyForm'
import CompanyDetail from './features/profiles/CompanyDetail'
import RoomList from './features/rooms/RoomList'
import RoomPage from './features/rooms/RoomPage'
import DocumentPage from './features/rooms/DocumentPage'
import InvestorMvp from './features/investor-mvp/InvestorMvp'
import {
  hasConfiguredBackend,
  getDemoPassword,
  setDemoPassword,
} from './api/config'
import './workspace.css'

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

function DemoPasswordControl() {
  const [value, setValue] = useState(getDemoPassword())
  if (!hasConfiguredBackend()) return null
  return (
    <details className="demo-access">
      <summary>Demo password</summary>
      <label>
        Nhập nếu backend demo đang bật shared password
        <input
          type="password"
          value={value}
          onChange={(event) => setValue(event.target.value)}
          placeholder="Để trống nếu backend không yêu cầu"
        />
      </label>
      <button
        type="button"
        className="secondary"
        onClick={() => setDemoPassword(value)}
      >
        Lưu password trên trình duyệt này
      </button>
    </details>
  )
}

export default function Workspace() {
  const [hash, setHash] = useState(location.hash)
  useEffect(() => {
    const change = () => setHash(location.hash)
    addEventListener('hashchange', change)
    return () => removeEventListener('hashchange', change)
  }, [])
  const hostedWithoutBackend = isHostedWithoutBackend()
  const path =
    hash.slice(1).split('?')[0] ||
    (hostedWithoutBackend ? '/investor-mvp' : '/companies')
  const parts = path.split('/').filter(Boolean)
  const params = new URLSearchParams(hash.split('?')[1] || '')
  if (path === '/health' && !hostedWithoutBackend) return <App />
  let screen = <CompanyList />
  if (hostedWithoutBackend && needsBackend(path))
    screen = <BackendRequiredNotice target={path} />
  else if (path === '/investor-mvp') screen = <InvestorMvp />
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
        <CompanyDetail id={parts[1]} saved={hash.endsWith('?saved=1')} />
      )
  else if (path !== '/companies')
    screen = (
      <p>
        Không tìm thấy trang. <a href="#/investor-mvp">Về Investor MVP</a>
      </p>
    )
  return (
    <main className="shell workspace">
      <header className="topbar">
        <a
          className="brand"
          href={hostedWithoutBackend ? '#/investor-mvp' : '#/companies'}
        >
          <span className="brand-mark">V</span>VAULT
        </a>
        <nav aria-label="Điều hướng chính">
          <a href="#/companies">Doanh nghiệp</a>
          <a href="#/rooms">Phòng dữ liệu</a>
          <a href="#/investor-mvp">Investor MVP</a>
          <a href="#/health">Kết nối API</a>
        </nav>
      </header>
      <p className="local-note">
        Bản thử nội bộ · Chỉ dùng dữ liệu giả lập · Chưa có đăng nhập hay chia
        sẻ cho buyer
        {hostedWithoutBackend
          ? ' · Vercel chưa cấu hình backend, hãy dùng Investor MVP để test flow A–Z'
          : hasConfiguredBackend()
            ? ' · Hosted full-stack demo: frontend gọi backend public đã cấu hình'
            : ''}
      </p>
      <DemoPasswordControl />
      <div key={hash || path} className="workspace-content">
        {screen}
      </div>
      <footer>
        <span>VAULT Core · Trust Profile</span>
        <span>Thông tin xác minh theo từng dữ kiện</span>
      </footer>
    </main>
  )
}
