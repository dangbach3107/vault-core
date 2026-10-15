import { useEffect, useState } from 'react'
import { getFile, request, type Preview } from '../../api/workspace'
import { PreviewBody } from '../profiles/PreviewView'
import { formatDate, type Deal, type DealDocument } from './types'

const LAYERS = [
  { layer: 1, label: 'Lớp 1 · Teaser ẩn danh' },
  { layer: 2, label: 'Lớp 2 · Định danh' },
  { layer: 3, label: 'Lớp 3 · Tài liệu hạn chế theo quyền' },
]

/** What the deal's buyer may read: teaser, approved layers, approved file versions. */
export default function BuyerPanel({ deal }: { deal: Deal }) {
  const [layer, setLayer] = useState(1)
  const [preview, setPreview] = useState<Preview | null>(null)
  const [error, setError] = useState('')
  const [documents, setDocuments] = useState<DealDocument[]>([])
  const [fileMessage, setFileMessage] = useState('')

  useEffect(() => {
    const controller = new AbortController()
    const path =
      layer === 1
        ? `/deals/${deal.id}/teaser`
        : `/deals/${deal.id}/profile/${layer}`
    request<Preview>(path, { signal: controller.signal })
      .then((value) => {
        setPreview(value)
        setError('')
      })
      .catch((reason: Error) => {
        if (controller.signal.aborted) return
        setPreview(null)
        setError(reason.message)
      })
    return () => controller.abort()
  }, [deal.id, deal.revision, layer])

  useEffect(() => {
    request<DealDocument[]>(`/deals/${deal.id}/documents`)
      .then(setDocuments)
      .catch((reason: Error) => setFileMessage(reason.message))
  }, [deal.id, deal.revision])

  const open = async (item: DealDocument, download: boolean) => {
    setFileMessage('')
    try {
      const blob = await getFile(
        `/deals/${deal.id}/documents/${item.grant_id}/${item.document_id}/content${download ? '?download=true' : ''}`,
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
      setFileMessage((reason as Error).message)
    }
  }

  const viewable = (item: DealDocument) =>
    ['application/pdf', 'image/png', 'image/jpeg', 'text/plain'].includes(
      item.media_type,
    )

  return (
    <section className="panel buyer-panel" aria-labelledby="buyer-panel-title">
      <div className="section-title">
        <div>
          <p className="eyebrow">Thông tin được mở cho bạn</p>
          <h2 id="buyer-panel-title">Hồ sơ doanh nghiệp theo quyền</h2>
          <p className="muted">
            Mỗi lớp chỉ mở khi đã có căn cứ (Seller duyệt Teaser, NDA, LOI) và
            Seller/Legal cấp quyền còn hiệu lực.
          </p>
        </div>
      </div>
      <div className="tabs" aria-label="Chọn lớp thông tin">
        {LAYERS.map((item) => (
          <button
            key={item.layer}
            type="button"
            aria-pressed={layer === item.layer}
            className={layer === item.layer ? '' : 'secondary'}
            onClick={() => setLayer(item.layer)}
          >
            {item.label}
          </button>
        ))}
      </div>
      {error ? (
        <p className="notice" role="status">
          {error}
        </p>
      ) : preview ? (
        <PreviewBody data={preview} layer={layer} />
      ) : (
        <p className="muted">Đang tải…</p>
      )}
      <h3>Tài liệu được duyệt</h3>
      {fileMessage && (
        <p className="notice" role="status">
          {fileMessage}
        </p>
      )}
      {documents.length === 0 ? (
        <p className="muted">
          Chưa có tài liệu nào được duyệt cho bạn trong deal này.
        </p>
      ) : (
        <ul className="deal-doc-list">
          {documents.map((item) => (
            <li key={`${item.grant_id}-${item.document_id}`}>
              <div>
                <strong>{item.title}</strong>
                <span className="muted">
                  {' '}
                  · phiên bản {item.version_number} · hết hạn{' '}
                  {formatDate(item.expires_at)}
                </span>
                {item.latest_version > item.version_number && (
                  <p className="muted">
                    Seller đã tải phiên bản {item.latest_version}; bạn chỉ xem
                    được phiên bản đã duyệt. Gửi yêu cầu mới nếu cần bản mới.
                  </p>
                )}
              </div>
              <div className="actions">
                {viewable(item) && (
                  <button
                    type="button"
                    className="secondary"
                    onClick={() => open(item, false)}
                  >
                    Xem
                  </button>
                )}
                {item.can_download ? (
                  <button type="button" onClick={() => open(item, true)}>
                    Tải xuống
                  </button>
                ) : (
                  !viewable(item) && (
                    <span className="muted">
                      File Word/Excel cần quyền tải xuống
                    </span>
                  )
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
