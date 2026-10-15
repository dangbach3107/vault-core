import { useState, type FormEvent } from 'react'
import { setAuthSession, type AuthSession } from '../../api/config'
import { request } from '../../api/workspace'
import RoleAvatar from '../../components/RoleAvatar'
import './login.css'
import Logo from '../../components/Logo'
import { LegalLinks } from '../legal/LegalPage'

const accounts = [
  {
    id: 'buyer',
    name: 'Buyer',
    text: 'Tìm hồ sơ, xin quyền truy cập',
    role: 'BUYER',
  },
  {
    id: 'seller',
    name: 'Seller',
    text: 'Quản lý hồ sơ và tài liệu',
    role: 'SELLER',
  },
  {
    id: 'admin',
    name: 'VAULT Admin',
    text: 'Điều phối thương vụ',
    role: 'VAULT_ADMIN',
  },
  {
    id: 'legal',
    name: 'Legal',
    text: 'Duyệt NDA và quyền truy cập',
    role: 'LEGAL',
  },
  { id: 'tech', name: 'Tech DD', text: 'Thẩm định kỹ thuật', role: 'TECH_DD' },
  { id: 'finance', name: 'Finance', text: 'Phí và chứng từ', role: 'FINANCE' },
  {
    id: 'buyer2',
    name: 'Buyer 2',
    text: 'Buyer khác, deal riêng',
    role: 'BUYER',
  },
  {
    id: 'seller2',
    name: 'Seller 2',
    text: 'Seller khác, hồ sơ riêng',
    role: 'SELLER',
  },
] as const

const points = [
  'Hồ sơ doanh nghiệp tiết lộ theo 3 lớp',
  'Phòng dữ liệu có phiên bản và xem trước',
  'Quyền truy cập có thời hạn, thu hồi tức thì',
]

export default function Login({
  onLogin,
}: {
  onLogin: (session: AuthSession) => void
}) {
  const [username, setUsername] = useState<string>('buyer')
  // Convenience for local development only; hosted builds start empty.
  const [password, setPassword] = useState(
    import.meta.env.DEV ? 'vault-demo' : '',
  )
  const [show, setShow] = useState(false)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const submit = async (event: FormEvent) => {
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
      setError(reason instanceof Error ? reason.message : 'Đăng nhập thất bại.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="lg">
      <aside className="lg-side" aria-hidden="true">
        <span className="lg-blob lg-blob-a" />
        <span className="lg-blob lg-blob-b" />
        <span className="lg-blob lg-blob-c" />
        <a className="lg-brand" href="#/welcome">
          <Logo variant="white" height={42} />
        </a>
        <div className="lg-pitch">
          <h2>
            Phòng giao dịch M&amp;A
            <br />
            <em>an toàn từng lớp.</em>
          </h2>
          <ul>
            {points.map((point) => (
              <li key={point}>{point}</li>
            ))}
          </ul>
        </div>
        <div className="lg-float lg-float-a">
          <small>Trust Profile</small>
          <strong>VAULT-0142</strong>
          <span className="lg-chips">
            <b className="on">L1</b>
            <b className="on">L2</b>
            <b>L3</b>
          </span>
        </div>
        <div className="lg-float lg-float-b">
          <small>Quyền truy cập</small>
          <strong>Hết hạn sau 30 ngày</strong>
          <span className="lg-bar">
            <i />
          </span>
        </div>
      </aside>

      <section className="lg-main">
        <form className="lg-card" onSubmit={submit}>
          <a className="lg-back" href="#/welcome">
            ← Trang giới thiệu
          </a>
          <p className="lg-eyebrow">Đăng nhập</p>
          <h1>Chào mừng trở lại</h1>
          <p className="lg-sub">
            Chọn vai trò của bạn để vào đúng không gian làm việc.
          </p>

          <div className="lg-roles" role="radiogroup" aria-label="Vai trò">
            {accounts.map((account) => (
              <button
                key={account.id}
                type="button"
                role="radio"
                aria-checked={username === account.id}
                className="lg-role"
                onClick={() => setUsername(account.id)}
              >
                <RoleAvatar role={account.role} size={40} />
                <span className="lg-role-text">
                  <strong>{account.name}</strong>
                  <small>{account.text}</small>
                </span>
              </button>
            ))}
          </div>

          <label className="lg-field">
            <span>Mật khẩu</span>
            <span className="lg-input">
              <input
                type={show ? 'text' : 'password'}
                value={password}
                autoComplete="current-password"
                placeholder="Nhập mật khẩu"
                onChange={(event) => setPassword(event.target.value)}
              />
              <button
                type="button"
                onClick={() => setShow((value) => !value)}
                aria-label={show ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'}
              >
                {show ? 'Ẩn' : 'Hiện'}
              </button>
            </span>
          </label>

          {error && (
            <p className="lg-error" role="alert">
              {error}
            </p>
          )}

          <button className="lg-submit" disabled={busy || !password}>
            {busy ? <span className="lg-spin" aria-hidden="true" /> : null}
            {busy ? 'Đang đăng nhập…' : 'Đăng nhập'}
            {!busy && <span aria-hidden="true">→</span>}
          </button>
          <p className="lg-foot">
            VAULT · Verified Access to Unlisted Listings & Transactions
          </p>
          <LegalLinks className="lg-legal" />
        </form>
      </section>
    </main>
  )
}
