import { lazy, Suspense, useEffect, useState } from 'react'
import { getFile, type Version } from '../../api/workspace'

const PdfPreview = lazy(() => import('./PdfPreview'))

export default function FilePreview({
  path,
  version,
}: {
  path: string
  version: Version
}) {
  const [blob, setBlob] = useState<Blob | null>(null)
  const [blobUrl, setBlobUrl] = useState('')
  const [text, setText] = useState('')
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const supported = [
    'image/png',
    'image/jpeg',
    'application/pdf',
    'text/plain',
  ].includes(version.media_type)
  useEffect(() => {
    if (!supported) return
    const controller = new AbortController()
    let objectUrl = ''
    getFile(path, controller.signal)
      .then(async (data) => {
        const content =
          version.media_type === 'text/plain' ? await data.text() : ''
        if (!controller.signal.aborted) {
          objectUrl = URL.createObjectURL(data)
          setBlobUrl(objectUrl)
          setBlob(data)
          setText(content)
        }
      })
      .catch((reason: Error) => {
        if (!controller.signal.aborted) setError(reason.message)
      })
    return () => {
      controller.abort()
      if (objectUrl) URL.revokeObjectURL(objectUrl)
    }
  }, [path, version.media_type, supported, attempt])
  if (!supported)
    return (
      <div className="empty panel">
        Định dạng này chưa có bản xem trực tiếp. Dùng “Tải file phiên bản này”
        để mở bằng ứng dụng trên máy.
      </div>
    )
  if (error)
    return (
      <div role="alert" className="error-box">
        {error}
        <button
          onClick={() => {
            setError('')
            setBlob(null)
            setAttempt((value) => value + 1)
          }}
        >
          Thử lại xem trước
        </button>
      </div>
    )
  if (!blob) return <p role="status">Đang tải bản xem trước…</p>
  return (
    <div className="file-preview" aria-label={`Xem trước ${version.filename}`}>
      {version.media_type.startsWith('image/') ? (
        <img
          src={blobUrl}
          alt={`Xem trước ${version.filename}`}
          onError={() => setError('Không hiển thị được ảnh.')}
        />
      ) : version.media_type === 'text/plain' ? (
        <pre className="pdf-text">{text}</pre>
      ) : (
        <Suspense fallback={<p role="status">Đang mở trình xem PDF…</p>}>
          <PdfPreview blob={blob} />
        </Suspense>
      )}
    </div>
  )
}
