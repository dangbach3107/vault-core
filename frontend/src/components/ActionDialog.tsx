import { useEffect, useRef, type FormEvent, type KeyboardEvent, type ReactNode } from 'react'

const FOCUSABLE = 'input, select, textarea, button, [href], [tabindex]:not([tabindex="-1"])'

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
  const panel = useRef<HTMLElement>(null)
  // Focus the first field on open and give focus back to the opener on close.
  useEffect(() => {
    const opener = document.activeElement as HTMLElement | null
    panel.current?.querySelector<HTMLElement>(FOCUSABLE)?.focus()
    return () => opener?.focus?.()
  }, [])
  const submit = (event: FormEvent) => {
    event.preventDefault()
    void onSubmit()
  }
  const keyDown = (event: KeyboardEvent) => {
    if (event.key === 'Escape' && !busy) {
      event.stopPropagation()
      onCancel()
      return
    }
    if (event.key !== 'Tab' || !panel.current) return
    const items = [...panel.current.querySelectorAll<HTMLElement>(FOCUSABLE)].filter(
      (item) => !item.hasAttribute('disabled'),
    )
    if (items.length === 0) return
    const first = items[0]
    const last = items[items.length - 1]
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault()
      last.focus()
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault()
      first.focus()
    }
  }
  return (
    <div className="dialog-backdrop" role="presentation" onKeyDown={keyDown} onMouseDown={(event) => event.target === event.currentTarget && !busy && onCancel()}>
      <section ref={panel} className="form-dialog" role="dialog" aria-modal="true" aria-labelledby="dialog-title">
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
