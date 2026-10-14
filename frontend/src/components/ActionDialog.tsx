import type { FormEvent, ReactNode } from 'react'

export default function ActionDialog({
  title,
  description,
  confirmLabel,
  busy = false,
  danger = false,
  children,
  onCancel,
  onSubmit,
}: {
  title: string
  description: string
  confirmLabel: string
  busy?: boolean
  danger?: boolean
  children?: ReactNode
  onCancel: () => void
  onSubmit: () => void | Promise<void>
}) {
  const submit = (event: FormEvent) => {
    event.preventDefault()
    void onSubmit()
  }
  return (
    <div className="dialog-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && !busy && onCancel()}>
      <section className="form-dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
        <form onSubmit={submit}>
          <div className="dialog-heading">
            <p className="eyebrow">Xác nhận thao tác</p>
            <h2 id="dialog-title">{title}</h2>
            <p>{description}</p>
          </div>
          {children && <div className="dialog-fields">{children}</div>}
          <div className="dialog-actions">
            <button type="button" className="secondary" onClick={onCancel} disabled={busy}>Hủy</button>
            <button type="submit" className={danger ? 'danger-button' : ''} disabled={busy}>{busy ? 'Đang xử lý…' : confirmLabel}</button>
          </div>
        </form>
      </section>
    </div>
  )
}
