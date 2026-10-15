import { FormEvent, useState } from 'react'
import { request } from '../../api/workspace'
import { ROLE_META, type Role } from '../auth/roles'
import { formatDateTime, type Catalog, type Deal } from './types'

type Props = {
  deal: Deal
  catalog: Catalog
  role: Role
  onChange: (deal: Deal) => void
}

/** Every gated step, who owns it, and the evidence recorded when it was done. */
export default function ActionPanel({ deal, catalog, role, onChange }: Props) {
  const [open, setOpen] = useState('')
  const [note, setNote] = useState('')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  const steps = deal.state.steps
  const labels = Object.fromEntries(
    catalog.actions.map((item) => [item.key, item.label]),
  )
  const available = (key: string) =>
    !steps[key] &&
    (catalog.actions.find((item) => item.key === key)?.requires || []).every(
      (need) => steps[need],
    )
  const mine = catalog.actions.filter(
    (item) => item.role === role && available(item.key),
  )
  const done = catalog.actions.filter((item) => steps[item.key]).length

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setBusy(true)
    setMessage('')
    try {
      const updated = await request<Deal>(`/deals/${deal.id}/actions/${open}`, {
        method: 'POST',
        body: JSON.stringify({ note: note.trim() }),
      })
      onChange(updated)
      setOpen('')
      setNote('')
      setMessage('Đã ghi nhận.')
    } catch (error) {
      setMessage((error as Error).message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <section
      className="panel deal-actions"
      aria-labelledby="deal-actions-title"
    >
      <div className="section-title">
        <div>
          <p className="eyebrow">Tiến độ</p>
          <h2 id="deal-actions-title">Các bước của thương vụ</h2>
        </div>
        <span className="status-pill">
          {done}/{catalog.actions.length} bước
        </span>
      </div>
      <div className="deal-mine">
        <h3>Việc của bạn</h3>
        {mine.length === 0 ? (
          <p className="muted">Chưa có bước nào chờ vai trò của bạn.</p>
        ) : (
          mine.map((item) => (
            <div key={item.key} className="deal-mine-item">
              <strong>{item.label}</strong>
              {open === item.key ? (
                <form onSubmit={submit} className="deal-note-form">
                  <label>
                    Ghi chú / bằng chứng (số văn bản, ngày, nội dung chính)
                    <textarea
                      value={note}
                      onChange={(event) => setNote(event.target.value)}
                      maxLength={1000}
                      rows={3}
                    />
                  </label>
                  <div className="actions">
                    <button disabled={busy}>
                      {busy ? 'Đang lưu…' : 'Xác nhận đã hoàn tất'}
                    </button>
                    <button
                      type="button"
                      className="secondary"
                      onClick={() => setOpen('')}
                    >
                      Hủy
                    </button>
                  </div>
                </form>
              ) : (
                <button
                  type="button"
                  onClick={() => {
                    setOpen(item.key)
                    setNote('')
                    setMessage('')
                  }}
                >
                  Thực hiện
                </button>
              )}
            </div>
          ))
        )}
        {message && (
          <p className="notice" role="status">
            {message}
          </p>
        )}
      </div>
      <ol className="deal-step-list">
        {catalog.actions.map((item) => {
          const record = deal.state.records?.[item.key]
          const state = steps[item.key]
            ? 'done'
            : available(item.key)
              ? 'ready'
              : 'blocked'
          return (
            <li key={item.key} className={`deal-step ${state}`}>
              <span className="deal-step-mark" aria-hidden="true" />
              <div>
                <strong>{item.label}</strong>
                <span className="muted">
                  {' '}
                  · {ROLE_META[item.role as Role]?.label || item.role}
                </span>
                {state === 'done' && record && (
                  <p className="muted">
                    {record.by} · {formatDateTime(record.at)}
                    {record.note ? ` · ${record.note}` : ''}
                  </p>
                )}
                {state === 'blocked' && (
                  <p className="muted">
                    Chờ:{' '}
                    {item.requires
                      .filter((need) => !steps[need])
                      .map((need) => labels[need])
                      .join('; ')}
                  </p>
                )}
              </div>
              <span className="sr-only">
                {state === 'done'
                  ? 'Đã xong'
                  : state === 'ready'
                    ? 'Sẵn sàng'
                    : 'Chưa đủ điều kiện'}
              </span>
            </li>
          )
        })}
      </ol>
    </section>
  )
}
