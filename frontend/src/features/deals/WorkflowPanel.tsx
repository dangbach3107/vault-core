import { FormEvent, useState } from 'react'
import { request } from '../../api/workspace'
import { ROLE_META, type Role } from '../auth/roles'
import { formatDateTime, type Catalog, type Deal } from './types'

const STATUS: Record<string, string> = {
  ACTIVE: 'Đang chạy',
  STOPPED: 'Đã dừng',
  CLOSED: 'Đã đóng hồ sơ',
}

/** The 20-stage operating checklist; each stage records an owner decision. */
export default function WorkflowPanel({
  deal,
  catalog,
  role,
  onChange,
}: {
  deal: Deal
  catalog: Catalog
  role: Role
  onChange: (deal: Deal) => void
}) {
  const workflow = deal.state.workflow
  const [note, setNote] = useState('')
  const [outcome, setOutcome] = useState<'CONTINUE' | 'STOP'>('CONTINUE')
  const [message, setMessage] = useState('')
  const current = catalog.stages.find(
    (stage) => stage.number === workflow.current_step,
  )
  const history = new Map(
    (workflow.history || []).map((item) => [item.step, item]),
  )
  const canAct = workflow.status === 'ACTIVE' && current?.owner === role

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    setMessage('')
    try {
      onChange(
        await request<Deal>(
          `/deals/${deal.id}/workflow/${workflow.current_step}/complete`,
          {
            method: 'POST',
            body: JSON.stringify({ note: note.trim(), outcome }),
          },
        ),
      )
      setNote('')
      setOutcome('CONTINUE')
    } catch (error) {
      setMessage((error as Error).message)
    }
  }

  return (
    <section className="panel workflow-panel" aria-labelledby="workflow-title">
      <div className="section-title">
        <div>
          <p className="eyebrow">Quy trình vận hành</p>
          <h2 id="workflow-title">20 bước điều phối</h2>
        </div>
        <span className="status-pill">
          {STATUS[workflow.status]} · bước {workflow.current_step}/20
        </span>
      </div>
      {workflow.stop_reason && (
        <p className="notice">Lý do dừng: {workflow.stop_reason}</p>
      )}
      {canAct && current && (
        <form className="deal-note-form" onSubmit={submit}>
          <strong>
            Bước {current.number}: {current.label}
          </strong>
          <label>
            Kết quả và ghi chú
            <textarea
              value={note}
              onChange={(event) => setNote(event.target.value)}
              required
              maxLength={1000}
              rows={2}
            />
          </label>
          <label>
            Quyết định
            <select
              value={outcome}
              onChange={(event) =>
                setOutcome(event.target.value as 'CONTINUE' | 'STOP')
              }
            >
              <option value="CONTINUE">Đạt — chuyển bước tiếp theo</option>
              <option value="STOP">Không đạt — dừng thương vụ</option>
            </select>
          </label>
          <button className={outcome === 'STOP' ? 'danger-button' : ''}>
            Ghi nhận
          </button>
        </form>
      )}
      {message && (
        <p className="notice" role="status">
          {message}
        </p>
      )}
      <ol className="deal-step-list compact">
        {catalog.stages.map((stage) => {
          const done = history.get(stage.number)
          const state = done
            ? done.outcome === 'STOP'
              ? 'stopped'
              : 'done'
            : stage.number < workflow.current_step ||
                workflow.status === 'CLOSED'
              ? 'done' // roles without the history still see overall progress
              : stage.number === workflow.current_step &&
                  workflow.status === 'ACTIVE'
                ? 'ready'
                : 'blocked'
          return (
            <li key={stage.number} className={`deal-step ${state}`}>
              <span className="deal-step-mark" aria-hidden="true" />
              <div>
                <strong>
                  {stage.number}. {stage.label}
                </strong>
                <span className="muted">
                  {' '}
                  · {ROLE_META[stage.owner as Role]?.label || stage.owner}
                </span>
                {done && (
                  <p className="muted">
                    {done.by || done.owner} ·{' '}
                    {formatDateTime(done.completed_at)} · {done.note}
                  </p>
                )}
              </div>
            </li>
          )
        })}
      </ol>
    </section>
  )
}
