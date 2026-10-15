import { FormEvent, useState } from 'react'
import { request } from '../../api/workspace'
import { formatVnd } from '../../lib/money'
import type { Role } from '../auth/roles'
import { formatDateTime, type Deal, type Finding } from './types'

const SEVERITY: Record<Finding['severity'], string> = {
  LOW: 'Thấp',
  MEDIUM: 'Trung bình',
  HIGH: 'Cao',
  CRITICAL: 'Nghiêm trọng',
}
const STATUS: Record<Finding['status'], string> = {
  OPEN: 'Đang mở',
  RESPONDED: 'Seller đã phản hồi',
  RESOLVED: 'Đã xử lý',
  ACCEPTED_RISK: 'Chấp nhận rủi ro',
}

/** Findings are handled one by one; the sign-off is a separate step in the deal. */
export default function TechDdPanel({
  deal,
  role,
  onChange,
}: {
  deal: Deal
  role: Role
  onChange: (deal: Deal) => void
}) {
  const techDd = deal.state.tech_dd
  const [form, setForm] = useState({
    title: '',
    severity: 'MEDIUM',
    description: '',
    remediation: '',
    impact_vnd: '',
  })
  const [notes, setNotes] = useState<Record<string, string>>({})
  const [message, setMessage] = useState('')
  if (!techDd) return null
  const locked = Boolean(techDd.signed_off_at)
  const canAdd = role === 'TECH_DD' && deal.state.steps.vdrOpened && !locked
  const canRespond = (role === 'SELLER' || role === 'VAULT_ADMIN') && !locked
  const canDecide = role === 'TECH_DD' && !locked

  const call = async (path: string, body: object, done: string) => {
    setMessage('')
    try {
      onChange(
        await request<Deal>(`/deals/${deal.id}/tech-dd/${path}`, {
          method: 'POST',
          body: JSON.stringify(body),
        }),
      )
      setMessage(done)
      return true
    } catch (error) {
      setMessage((error as Error).message)
      return false
    }
  }
  const add = async (event: FormEvent) => {
    event.preventDefault()
    const ok = await call(
      'findings',
      { ...form, impact_vnd: form.impact_vnd || null },
      'Đã ghi nhận finding.',
    )
    if (ok)
      setForm({
        title: '',
        severity: 'MEDIUM',
        description: '',
        remediation: '',
        impact_vnd: '',
      })
  }
  const update = async (finding: Finding, status: Finding['status']) => {
    const note = (notes[finding.id] || '').trim()
    if (note.length < 3) {
      setMessage('Nhập ghi chú (ít nhất 3 ký tự) trước khi cập nhật finding.')
      return
    }
    if (
      await call(
        `findings/${finding.id}/status`,
        { status, note },
        'Đã cập nhật finding.',
      )
    )
      setNotes((value) => ({ ...value, [finding.id]: '' }))
  }
  const open = techDd.findings.filter(
    (item) => item.status === 'OPEN' || item.status === 'RESPONDED',
  )

  return (
    <section className="panel tech-dd-panel" aria-labelledby="tech-dd-title">
      <div className="section-title">
        <div>
          <p className="eyebrow">Thẩm định kỹ thuật</p>
          <h2 id="tech-dd-title">Finding và xử lý</h2>
          <p className="muted">
            Tech DD ghi nhận finding; Seller phản hồi; chỉ Tech DD đóng hoặc
            chấp nhận rủi ro. Ký xác nhận kết thúc thẩm định là bước riêng và
            chỉ làm được khi không còn finding đang mở.
          </p>
        </div>
        <span className="status-pill">
          {locked
            ? `Đã ký ${formatDateTime(techDd.signed_off_at)}`
            : `${open.length} finding đang mở`}
        </span>
      </div>
      {!deal.state.steps.vdrOpened && (
        <p className="muted">
          Phòng dữ liệu chưa mở nên chưa bắt đầu thẩm định.
        </p>
      )}
      {canAdd && (
        <form className="finding-form" onSubmit={add}>
          <label>
            Tiêu đề
            <input
              value={form.title}
              onChange={(event) =>
                setForm({ ...form, title: event.target.value })
              }
              minLength={3}
              maxLength={200}
              required
            />
          </label>
          <label>
            Mức độ
            <select
              value={form.severity}
              onChange={(event) =>
                setForm({ ...form, severity: event.target.value })
              }
            >
              {Object.entries(SEVERITY).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Ảnh hưởng ước tính (VND, không bắt buộc)
            <input
              inputMode="numeric"
              pattern="\d+(\.\d{1,2})?"
              value={form.impact_vnd}
              onChange={(event) =>
                setForm({ ...form, impact_vnd: event.target.value })
              }
              placeholder="90000000"
            />
          </label>
          <label className="wide">
            Mô tả
            <textarea
              value={form.description}
              onChange={(event) =>
                setForm({ ...form, description: event.target.value })
              }
              maxLength={2000}
              rows={2}
            />
          </label>
          <label className="wide">
            Đề xuất khắc phục
            <textarea
              value={form.remediation}
              onChange={(event) =>
                setForm({ ...form, remediation: event.target.value })
              }
              maxLength={1000}
              rows={2}
            />
          </label>
          <button>Thêm finding</button>
        </form>
      )}
      {message && (
        <p className="notice" role="status">
          {message}
        </p>
      )}
      {techDd.findings.length === 0 ? (
        <p className="muted">Chưa có finding.</p>
      ) : (
        <div className="finding-list">
          {techDd.findings.map((finding) => (
            <article
              key={finding.id}
              className={`access-item finding ${finding.severity.toLowerCase()}`}
            >
              <strong>{finding.title}</strong>
              <small>
                Mức độ {SEVERITY[finding.severity]} · {STATUS[finding.status]}
                {finding.impact_vnd
                  ? ` · Ảnh hưởng ${formatVnd(finding.impact_vnd)}`
                  : ''}
              </small>
              {finding.description && <p>{finding.description}</p>}
              {finding.remediation && (
                <p className="muted">Khắc phục: {finding.remediation}</p>
              )}
              {finding.history.length > 0 && (
                <details>
                  <summary>Lịch sử ({finding.history.length})</summary>
                  <ul>
                    {finding.history.map((item, index) => (
                      <li key={index}>
                        {formatDateTime(item.at)} · {item.by} ·{' '}
                        {STATUS[item.status as Finding['status']] ||
                          item.status}{' '}
                        · {item.note}
                      </li>
                    ))}
                  </ul>
                </details>
              )}
              {(canRespond || canDecide) && (
                <div className="finding-update">
                  <input
                    aria-label={`Ghi chú cho ${finding.title}`}
                    value={notes[finding.id] || ''}
                    onChange={(event) =>
                      setNotes((value) => ({
                        ...value,
                        [finding.id]: event.target.value,
                      }))
                    }
                    maxLength={1000}
                    placeholder="Ghi chú"
                  />
                  {canRespond &&
                    finding.status !== 'RESOLVED' &&
                    finding.status !== 'ACCEPTED_RISK' && (
                      <button
                        type="button"
                        className="secondary"
                        onClick={() => update(finding, 'RESPONDED')}
                      >
                        Gửi phản hồi
                      </button>
                    )}
                  {canDecide && (
                    <>
                      <button
                        type="button"
                        onClick={() => update(finding, 'RESOLVED')}
                      >
                        Đã xử lý
                      </button>
                      <button
                        type="button"
                        className="secondary"
                        onClick={() => update(finding, 'ACCEPTED_RISK')}
                      >
                        Chấp nhận rủi ro
                      </button>
                      {finding.status !== 'OPEN' && (
                        <button
                          type="button"
                          className="secondary"
                          onClick={() => update(finding, 'OPEN')}
                        >
                          Mở lại
                        </button>
                      )}
                    </>
                  )}
                </div>
              )}
            </article>
          ))}
        </div>
      )}
    </section>
  )
}
