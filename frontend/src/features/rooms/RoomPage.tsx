import { useState } from 'react'
import type { RoomDetail, DocumentDetail } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'
import UploadForm from './UploadForm'

export default function RoomPage({
  id,
  created,
}: {
  id: string
  created: boolean
}) {
  const result = useLoad<RoomDetail>(`/rooms/${id}`)
  const [folder, setFolder] = useState('')
  const [message, setMessage] = useState(
    created ? 'Đã tạo phòng dữ liệu với sáu nhóm thư mục.' : '',
  )
  const [uploading, setUploading] = useState(false)
  function onSaved(document: DocumentDetail) {
    setMessage(
      `Đã tải lên “${document.title}”, phiên bản ${document.current_version}.`,
    )
    setUploading(false)
    result.retry()
  }
  if (!result.data) return <LoadState {...result} />
  const room = result.data
  const documents = room.documents.filter(
    (document) => !folder || document.folder === folder,
  )
  return (
    <section>
      <a href="#/rooms">← Danh sách phòng dữ liệu</a>
      <div className="page-heading">
        <div>
          <p className="eyebrow">THƯƠNG VỤ · PHÒNG DỮ LIỆU NỘI BỘ</p>
          <h1>{room.title}</h1>
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
      <div className="room-layout">
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
            documents.map((document) => (
              <a
                className="record panel"
                href={`#/rooms/${id}/documents/${document.id}`}
                key={document.id}
              >
                <div>
                  <h2>{document.title}</h2>
                  <p>{document.latest.filename}</p>
                  <p>
                    Phiên bản {document.current_version} ·{' '}
                    {(document.latest.size_bytes / 1024).toFixed(1)} KB
                  </p>
                </div>
                <span>Xem & phiên bản →</span>
              </a>
            ))
          )}
        </div>
      </div>
    </section>
  )
}
