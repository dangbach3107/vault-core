import { useEffect, useState } from 'react'
import { getFile, request } from '../../api/workspace'
import type { components } from '../../api/generated/schema'
import type { Deal } from './types'

type Evidence = components['schemas']['ClosingEvidence']

const VIEWABLE = ['application/pdf', 'image/png', 'image/jpeg', 'text/plain']

/** Only the file versions cited when the checklist, signing or closing was recorded. */
export default function ClosingEvidence({ deal }: { deal: Deal }) {
  const [items, setItems] = useState<Evidence[]>([])
  const [message, setMessage] = useState('')

  useEffect(() => {
    request<Evidence[]>(`/deals/${deal.id}/closing-evidence`)
      .then(setItems)
      .catch((reason: Error) => setMessage(reason.message))
  }, [deal.id, deal.revision])

  const open = async (item: Evidence, download: boolean) => {
    setMessage('')
    try {
      const blob = await getFile(
        `/deals/${deal.id}/closing-evidence/${item.document_id}/content${download ? '?download=true' : ''}`,
        new AbortController().signal,
      )
      const url = URL.createObjectURL(blob)
      if (download) {
        const link = document.createElement('a')
        link.href = url
        link.download = item.filename
        link.click()
      } else {
        window.open(url, '_blank', 'noopener')
      }
      setTimeout(() => URL.revokeObjectURL(url), 60000)
    } catch (reason) {
      setMessage((reason as Error).message)
    }
  }

  return (
    <>
      <h3>Chứng từ ký và đóng</h3>
      {message && (
        <p className="notice" role="status">
          {message}
        </p>
      )}
      {items.length === 0 ? (
        <p className="muted">
          Chưa có chứng từ. Legal/Admin đính kèm file khi ghi nhận checklist
          điều kiện đóng, ký hợp đồng hoặc đóng giao dịch.
        </p>
      ) : (
        <ul className="deal-doc-list">
          {items.map((item) => (
            <li key={`${item.action}-${item.document_id}`}>
              <div>
                <strong>{item.title}</strong>
                <span className="muted">
                  {' '}
                  · phiên bản {item.version_number} · {item.action_label}
                </span>
              </div>
              <div className="actions">
                {VIEWABLE.includes(item.media_type) && (
                  <button
                    type="button"
                    className="secondary"
                    onClick={() => open(item, false)}
                  >
                    Xem
                  </button>
                )}
                <button type="button" onClick={() => open(item, true)}>
                  Tải xuống
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </>
  )
}
