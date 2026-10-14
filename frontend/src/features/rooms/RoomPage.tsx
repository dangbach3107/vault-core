import { useState } from 'react'
import type { RoomDetail, DocumentDetail } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'
import UploadForm from './UploadForm'
import { request } from '../../api/workspace'
import ActionDialog from '../../components/ActionDialog'

function extOf(name: string) {
  const i = name.lastIndexOf('.')
  return i >= 0 ? name.slice(i + 1).toUpperCase() : '—'
}

export default function RoomPage({
  id,
  created,
}: {
  id: string
  created: boolean
}) {
  const result = useLoad<RoomDetail>(`/rooms/${id}`)
  const [folder, setFolder] = useState('')
  const [selected, setSelected] = useState<string | null>(null)
  const [message, setMessage] = useState(
    created ? 'Đã tạo phòng dữ liệu với sáu nhóm thư mục.' : '',
  )
  const [uploading, setUploading] = useState(false)
  const [deleting, setDeleting] = useState('')
  const [error, setError] = useState('')
  const [pendingDelete, setPendingDelete] = useState<null | { kind: 'room' } | { kind: 'document'; document: RoomDetail['documents'][number] }>(null)
  function onSaved(document: DocumentDetail) {
    setMessage(
      `Đã tải lên “${document.title}”, phiên bản ${document.current_version}.`,
    )
    setUploading(false)
    setSelected(document.id)
    result.retry()
  }
  async function deleteDocument(document: RoomDetail['documents'][number]) {
    setDeleting(document.id)
    setError('')
    try {
      await request<void>(`/rooms/${id}/documents/${document.id}`, { method: 'DELETE' })
      setMessage(`Đã xóa tài liệu “${document.title}”.`)
      result.retry()
    } catch (reason) {
      setError((reason as Error).message)
    } finally {
      setDeleting('')
      setPendingDelete(null)
    }
  }
  async function deleteRoom() {
    setDeleting('room')
    setError('')
    try {
      await request<void>(`/rooms/${id}`, { method: 'DELETE' })
      location.hash = '/rooms'
    } catch (reason) {
      setError((reason as Error).message)
      setDeleting('')
    }
  }
  if (!result.data) return <LoadState {...result} />
  const room = result.data
  const documents = room.documents.filter(
    (document) => !folder || document.folder === folder,
  )
  const current = documents.find((row) => row.id === selected) || documents[0]
  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">THƯƠNG VỤ · PHÒNG DỮ LIỆU NỘI BỘ</p>
          <h2>{room.title}</h2>
          <a href={`#/companies/${room.company_id}`}>{room.company_name}</a>
        </div>
        <div className="actions">
          <button onClick={() => setUploading(!uploading)}>{uploading ? 'Đóng form upload' : 'Thêm tài liệu'}</button>
          <button className="danger-button" onClick={() => setPendingDelete({ kind: 'room' })} disabled={deleting === 'room'}>{deleting === 'room' ? 'Đang xóa…' : 'Xóa phòng'}</button>
        </div>
      </div>
      {message && (
        <p role="status" className="success-box">
          {message}
        </p>
      )}
      {error && <p role="alert" className="error-box">{error}</p>}
      {uploading && <UploadForm room={room} onSaved={onSaved} />}
      <div className="room-layout three">
        <aside className="folder-list" aria-label="Nhóm thư mục">
          <button
            className={!folder ? '' : 'secondary'}
            aria-pressed={!folder}
            onClick={() => setFolder('')}
          >
            Tất cả ({room.documents.length})
          </button>
          {room.folders.map((item) => (
            <button
              className={folder === item.id ? '' : 'secondary'}
              aria-pressed={folder === item.id}
              key={item.id}
              onClick={() => setFolder(item.id)}
            >
              {item.label} ({item.document_count})
            </button>
          ))}
        </aside>
        <div>
          <h2>
            {folder
              ? room.folders.find((item) => item.id === folder)?.label
              : 'Tất cả tài liệu'}
          </h2>
          {documents.length === 0 ? (
            <p className="empty panel">Chưa có tài liệu trong nhóm này.</p>
          ) : (
            <div className="table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Tên</th>
                    <th>Định dạng</th>
                    <th>Dung lượng</th>
                    <th>Phiên bản</th>
                    <th>Tải lên</th>
                    <th>Thao tác</th>
                  </tr>
                </thead>
                <tbody>
                  {documents.map((document) => (
                    <tr key={document.id}>
                      <td>
                        <a
                          href={`#/rooms/${id}/documents/${document.id}`}
                          onClick={() => setSelected(document.id)}
                        >
                          {document.title}
                        </a>
                      </td>
                      <td>{extOf(document.latest.filename)}</td>
                      <td>
                        {(document.latest.size_bytes / 1024).toFixed(1)} KB
                      </td>
                      <td>{document.current_version}</td>
                      <td>
                        {new Date(
                          document.latest.uploaded_at,
                        ).toLocaleString('vi-VN')}
                      </td>
                      <td>
                        <button className="danger-button" onClick={() => setPendingDelete({ kind: 'document', document })} disabled={deleting === document.id}>
                          {deleting === document.id ? 'Đang xóa…' : 'Xóa'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
        <aside className="panel">
          {current ? (
            <>
              <h2>{current.title}</h2>
              <p className="muted">{current.latest.filename}</p>
              <p>
                Phiên bản {current.current_version} ·{' '}
                {(current.latest.size_bytes / 1024).toFixed(1)} KB
              </p>
              <a
                className="button-link"
                href={`#/rooms/${id}/documents/${current.id}`}
              >
                Xem & phiên bản
              </a>
            </>
          ) : (
            <p className="muted">Chọn một tài liệu để xem tóm tắt.</p>
          )}
        </aside>
      </div>
      {pendingDelete && <ActionDialog
        title={pendingDelete.kind === 'room' ? `Xóa phòng “${room.title}”?` : `Xóa tài liệu “${pendingDelete.document.title}”?`}
        description={pendingDelete.kind === 'room' ? 'Toàn bộ tài liệu và mọi phiên bản trong phòng sẽ bị xóa vĩnh viễn.' : 'Tài liệu và toàn bộ lịch sử phiên bản sẽ bị xóa vĩnh viễn.'}
        confirmLabel={pendingDelete.kind === 'room' ? 'Xóa phòng dữ liệu' : 'Xóa tài liệu'}
        danger
        busy={Boolean(deleting)}
        onCancel={() => setPendingDelete(null)}
        onSubmit={() => pendingDelete.kind === 'room' ? deleteRoom() : deleteDocument(pendingDelete.document)}
      />}
    </section>
  )
}
