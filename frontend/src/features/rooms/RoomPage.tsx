import { useState } from 'react'
import type { RoomDetail, DocumentDetail } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'
import UploadForm from './UploadForm'

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
  function onSaved(document: DocumentDetail) {
    setMessage(
      `Đã tải lên “${document.title}”, phiên bản ${document.current_version}.`,
    )
    setUploading(false)
    setSelected(document.id)
    result.retry()
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
        <button onClick={() => setUploading(!uploading)}>
          {uploading ? 'Đóng form upload' : 'Thêm tài liệu'}
        </button>
      </div>
      {message && (
        <p role="status" className="success-box">
          {message}
        </p>
      )}
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
    </section>
  )
}
