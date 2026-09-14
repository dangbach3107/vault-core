import { useState } from 'react'
import {
  request,
  type DocumentDetail,
  type RoomDetail,
} from '../../api/workspace'

export default function UploadForm({
  room,
  document,
  onSaved,
}: {
  room: RoomDetail
  document?: DocumentDetail
  onSaved: (saved: DocumentDetail) => void
}) {
  const [title, setTitle] = useState('')
  const [folder, setFolder] = useState(room.folders[0].id)
  const [note, setNote] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [fileKey, setFileKey] = useState(0)
  const [over, setOver] = useState(false)
  async function upload(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    if (!file) {
      setError('Hãy chọn file cần tải lên.')
      return
    }
    if (file.size > room.max_upload_bytes) {
      setError('File vượt giới hạn dung lượng. Hãy chọn file nhỏ hơn.')
      return
    }
    const data = new FormData()
    data.append('file', file)
    data.append('note', note)
    if (!document) {
      data.append('title', title)
      data.append('folder', folder)
    }
    setBusy(true)
    try {
      const saved = await request<DocumentDetail>(
        `/rooms/${room.id}/documents${document ? `/${document.id}/versions` : ''}`,
        { method: 'POST', body: data },
      )
      setTitle('')
      setNote('')
      setFile(null)
      setFileKey((value) => value + 1)
      onSaved(saved)
    } catch (reason) {
      setError((reason as Error).message)
    } finally {
      setBusy(false)
    }
  }
  return (
    <form className="panel" onSubmit={upload}>
      <h2>{document ? 'Thêm phiên bản mới' : 'Tải tài liệu lên'}</h2>
      <p className="muted">
        {room.allowed_extensions.join(', ')} · Tối đa{' '}
        {Math.round(room.max_upload_bytes / 1024 / 1024)} MB/file. PDF và ảnh
        xem trực tiếp; DOCX/XLSX tải xuống để mở.
      </p>
      <fieldset className="upload-fields" disabled={busy}>
        {!document && (
          <>
            <label>
              Tên tài liệu
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                maxLength={200}
              />
            </label>
            <label>
              Nhóm thư mục
              <select
                value={folder}
                onChange={(e) => setFolder(e.target.value as typeof folder)}
              >
                {room.folders.map((item) => (
                  <option key={item.id} value={item.id}>
                    {item.label}
                  </option>
                ))}
              </select>
            </label>
          </>
        )}
        <div className="field">
          <label htmlFor="upload-file">
            {document ? 'File phiên bản mới' : 'Chọn file'}
          </label>
          <div
            className={over ? 'dropzone over' : 'dropzone'}
            onDragOver={(e) => {
              e.preventDefault()
              setOver(true)
            }}
            onDragLeave={() => setOver(false)}
            onDrop={(e) => {
              e.preventDefault()
              setOver(false)
              const dropped = e.dataTransfer.files[0]
              if (dropped) setFile(dropped)
            }}
          >
            <p>
              {file
                ? `${file.name} · ${(file.size / 1024).toFixed(1)} KB`
                : 'Kéo thả file vào đây hoặc chọn từ máy'}
            </p>
            <input
              id="upload-file"
              key={fileKey}
              type="file"
              accept={room.allowed_extensions.join(',')}
              required
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </div>
        </div>
        <label>
          Ghi chú phiên bản
          <input
            value={note}
            onChange={(e) => setNote(e.target.value)}
            maxLength={1000}
          />
        </label>
        <button type="submit">
          {busy ? 'Đang tải lên…' : document ? 'Lưu phiên bản mới' : 'Tải lên'}
        </button>
      </fieldset>
      {busy && <p role="status">Đang tải và lưu tài liệu…</p>}
      {error && (
        <p role="alert" className="error-box">
          {error}
        </p>
      )}
    </form>
  )
}
