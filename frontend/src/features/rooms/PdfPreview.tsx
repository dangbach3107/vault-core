import { useEffect, useRef, useState } from 'react'
import {
  getDocument,
  GlobalWorkerOptions,
  type PDFDocumentProxy,
  type RenderTask,
} from 'pdfjs-dist'
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url'

GlobalWorkerOptions.workerSrc = workerUrl

function Page({ pdf, number }: { pdf: PDFDocumentProxy; number: number }) {
  const canvas = useRef<HTMLCanvasElement>(null)
  const [state, setState] = useState('loading')
  const [text, setText] = useState('')
  useEffect(() => {
    let stopped = false
    let render: RenderTask | undefined
    pdf
      .getPage(number)
      .then(async (page) => {
        if (stopped || !canvas.current) return
        const original = page.getViewport({ scale: 1 })
        const viewport = page.getViewport({
          scale: Math.min(
            1.5,
            1600 / Math.max(original.width, original.height),
          ),
        })
        canvas.current.width = Math.ceil(viewport.width)
        canvas.current.height = Math.ceil(viewport.height)
        render = page.render({ canvas: canvas.current, viewport })
        await render.promise
        const content = await page.getTextContent()
        if (!stopped) {
          setText(
            content.items
              .map((item) => ('str' in item ? item.str : ''))
              .join(' '),
          )
          setState('ready')
        }
      })
      .catch(() => {
        if (!stopped) setState('error')
      })
    return () => {
      stopped = true
      render?.cancel()
    }
  }, [pdf, number])
  return (
    <div>
      {state === 'loading' && <p role="status">Đang dựng trang PDF…</p>}
      {state === 'error' && (
        <p role="alert">
          Không dựng được trang PDF này. Bạn có thể tải file để mở trên máy.
        </p>
      )}
      <canvas
        ref={canvas}
        aria-label={`Trang PDF ${number}`}
        className="pdf-canvas"
      />
      {state === 'ready' && (
        <details>
          <summary>Văn bản trang {number}</summary>
          <p className="pdf-text">
            {text || 'Trang không có lớp văn bản; nội dung có thể là ảnh quét.'}
          </p>
        </details>
      )}
    </div>
  )
}

export default function PdfPreview({ blob }: { blob: Blob }) {
  const [pdf, setPdf] = useState<PDFDocumentProxy | null>(null)
  const [error, setError] = useState(false)
  const [number, setNumber] = useState(1)
  useEffect(() => {
    let stopped = false
    let task: ReturnType<typeof getDocument> | undefined
    blob
      .arrayBuffer()
      .then((data) => {
        if (stopped) return
        task = getDocument({ data: new Uint8Array(data), useSystemFonts: true })
        return task.promise
      })
      .then((document) => {
        if (!stopped && document) setPdf(document)
      })
      .catch(() => {
        if (!stopped) setError(true)
      })
    return () => {
      stopped = true
      void task?.destroy()
    }
  }, [blob])
  if (error)
    return (
      <p role="alert">
        Không đọc được PDF. Hãy tải file hoặc thử một bản PDF khác.
      </p>
    )
  if (!pdf) return <p role="status">Đang đọc PDF…</p>
  return (
    <div>
      <div className="actions pdf-controls">
        <button
          className="secondary"
          disabled={number === 1}
          onClick={() => setNumber(number - 1)}
        >
          Trang PDF trước
        </button>
        <span>
          Trang {number}/{pdf.numPages}
        </span>
        <button
          className="secondary"
          disabled={number === pdf.numPages}
          onClick={() => setNumber(number + 1)}
        >
          Trang PDF sau
        </button>
      </div>
      <Page key={number} pdf={pdf} number={number} />
    </div>
  )
}
