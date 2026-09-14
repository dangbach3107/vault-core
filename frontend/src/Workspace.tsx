import { useEffect, useState } from 'react'
import App from './App'
import CompanyList from './features/profiles/CompanyList'
import CompanyForm, { EditCompany } from './features/profiles/CompanyForm'
import CompanyDetail from './features/profiles/CompanyDetail'
import RoomList from './features/rooms/RoomList'
import RoomPage from './features/rooms/RoomPage'
import DocumentPage from './features/rooms/DocumentPage'
import InvestorMvp from './features/investor-mvp/InvestorMvp'
import './workspace.css'

export default function Workspace() {
  const [hash, setHash] = useState(location.hash)
  useEffect(() => {
    const change = () => setHash(location.hash)
    addEventListener('hashchange', change)
    return () => removeEventListener('hashchange', change)
  }, [])
  const path = hash.slice(1).split('?')[0] || '/companies'
  const parts = path.split('/').filter(Boolean)
  const params = new URLSearchParams(hash.split('?')[1] || '')
  if (path === '/health') return <App />
  let screen = <CompanyList />
  if (path === '/investor-mvp') screen = <InvestorMvp />
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
        Không tìm thấy trang. <a href="#/companies">Về danh sách</a>
      </p>
    )
  return (
    <main className="shell workspace">
      <header className="topbar">
        <a className="brand" href="#/companies">
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
      </p>
      <div key={hash} className="workspace-content">
        {screen}
      </div>
      <footer>
        <span>VAULT Core · Trust Profile</span>
        <span>Thông tin xác minh theo từng dữ kiện</span>
      </footer>
    </main>
  )
}
