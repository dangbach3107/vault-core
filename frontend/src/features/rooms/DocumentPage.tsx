import { useState } from 'react'
import {
  apiBase,
  type DocumentDetail,
  type RoomDetail,
} from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'
import UploadForm from './UploadForm'
import FilePreview from './FilePreview'

export default function DocumentPage({
  roomId,
  documentId,
}: {
  roomId: string
  documentId: string
}) {
  const documentResult = useLoad<DocumentDetail>(
    `/rooms/${roomId}/documents/${documentId}`,
  )
  const roomResult = useLoad<RoomDetail>(`/rooms/${roomId}`)
  const [number, setNumber] = useState<number | null>(null)
  const [editing, setEditing] = useState(false)
  const [message, setMessage] = useState('')
  if (!documentResult.data) return <LoadState {...documentResult} />
  if (!roomResult.data) return <LoadState {...roomResult} />
  const document = documentResult.data
  const version =
    document.versions.find((row) => row.number === number) || document.latest
  const url = `${apiBase}/rooms/${roomId}/documents/${documentId}/versions/${version.number}/content`
  function saved(updated: DocumentDetail) {
    setNumber(updated.current_version)
    setEditing(false)
    setMessage(
      `Đã lưu phiên bản ${updated.current_version}. Các phiên bản cũ vẫn được giữ lại.`,
    )
    documentResult.retry()
  }
  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">{roomResult.data.title}</p>
          <h1>{document.title}</h1>
          <p className="muted">
            Phiên bản mới nhất: {document.current_version}
          </p>
          <a href={`#/rooms/${roomId}`}>Về phòng dữ liệu</a>
        </div>
        <button onClick={() => setEditing(!editing)}>
          {editing ? 'Đóng form phiên bản' : 'Thêm phiên bản'}
        </button>
      </div>
      {message && (
        <p className="success-box" role="status">
          {message}
        </p>
      )}
      {editing && (
        <UploadForm
          room={roomResult.data}
          document={document}
          onSaved={saved}
        />
      )}
      <div className="room-layout">
        <aside className="panel version-list">
          <h2>Lịch sử phiên bản</h2>
          {document.versions.map((row) => (
            <button
              className={version.number === row.number ? '' : 'secondary'}
              aria-pressed={version.number === row.number}
              key={row.number}
              onClick={() => setNumber(row.number)}
            >
              <strong>Phiên bản {row.number}</strong>
              <span>{new Date(row.uploaded_at).toLocaleString('vi-VN')}</span>
              <span>{row.filename}</span>
              {row.note && <span>{row.note}</span>}
            </button>
          ))}
        </aside>
        <div>
          <div className="panel">
            <h2>Đang xem phiên bản {version.number}</h2>
            <p>
              {version.filename} · {(version.size_bytes / 1024).toFixed(1)} KB
            </p>
            <a href={`${url}?download=true`} download>
              Tải file phiên bản này
            </a>
            <details>
              <summary>Mã kiểm tra SHA-256</summary>
              <code className="file-hash">{version.sha256}</code>
            </details>
          </div>
          <FilePreview
            key={version.number}
            path={url.slice(apiBase.length)}
            version={version}
          />
        </div>
      </div>
    </section>
  )
}
