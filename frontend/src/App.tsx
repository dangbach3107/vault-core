import { useEffect, useState } from 'react'
import { getHealth, type HealthResponse } from './api/client'

type Connection =
  | { state: 'loading' }
  | { state: 'connected'; health: HealthResponse }
  | { state: 'error'; message: string }

export default function App() {
  const [attempt, setAttempt] = useState(0)
  const [connection, setConnection] = useState<Connection>({ state: 'loading' })

  useEffect(() => {
    const controller = new AbortController()
    getHealth(controller.signal)
      .then((health) => {
        if (!controller.signal.aborted)
          setConnection({ state: 'connected', health })
      })
      .catch(() => {
        if (!controller.signal.aborted) {
          setConnection({
            state: 'error',
            message:
              'Chưa kết nối được API. Hãy kiểm tra cửa sổ backend rồi thử lại.',
          })
        }
      })
    return () => controller.abort()
  }, [attempt])

  const retry = () => {
    setConnection({ state: 'loading' })
    setAttempt((value) => value + 1)
  }

  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="VAULT trang chủ">
          <span className="brand-mark" aria-hidden="true">
            V
          </span>{' '}
          VAULT
        </a>
        <span className="environment">Môi trường phát triển</span>
      </header>
      <section className="connection-card" aria-labelledby="page-title">
        <p className="eyebrow">BỘ KHUNG KỸ THUẬT · 01</p>
        <h1 id="page-title">Kiểm tra kết nối</h1>
        <p className="intro">
          Một bước nhỏ để bắt đầu: xác nhận giao diện có thể gọi đến API.
        </p>
        <div
          className={`status-panel ${connection.state}`}
          role="status"
          aria-live="polite"
        >
          <span className="status-dot" aria-hidden="true" />
          <div>
            <h2>
              {connection.state === 'loading'
                ? 'Đang kiểm tra…'
                : connection.state === 'connected'
                  ? 'Frontend đã kết nối backend'
                  : 'Không thể kết nối'}
            </h2>
            <p>
              {connection.state === 'connected'
                ? 'API đã trả lời thành công.'
                : connection.state === 'error'
                  ? connection.message
                  : 'Đang gửi yêu cầu đến API kiểm tra hoạt động.'}
            </p>
          </div>
        </div>
        {connection.state === 'connected' && (
          <dl className="details">
            <div>
              <dt>Dịch vụ</dt>
              <dd>{connection.health.service}</dd>
            </div>
            <div>
              <dt>Phiên bản</dt>
              <dd>{connection.health.version}</dd>
            </div>
            <div>
              <dt>Trạng thái API</dt>
              <dd>{connection.health.status}</dd>
            </div>
          </dl>
        )}
        <button onClick={retry} disabled={connection.state === 'loading'}>
          {connection.state === 'loading' ? 'Đang kiểm tra…' : 'Kiểm tra lại'}{' '}
          <span aria-hidden="true">↗</span>
        </button>
        <p className="scope-note">
          Kiểm tra này chỉ xác nhận API đang hoạt động. Chưa kiểm tra PostgreSQL
          hoặc dịch vụ bên ngoài.
        </p>
      </section>
      <footer>
        <span>VAULT Core</span>
        <a href="#/companies">Mở hồ sơ doanh nghiệp</a>
      </footer>
    </main>
  )
}
