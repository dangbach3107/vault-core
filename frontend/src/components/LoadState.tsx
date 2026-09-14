export function LoadState({
  error,
  retry,
}: {
  error: string
  retry: () => void
}) {
  return error ? (
    <div role="alert" className="error-box">
      <p>{error}</p>
      <button onClick={retry}>Thử lại</button>
    </div>
  ) : (
    <p role="status" className="muted">
      Đang tải dữ liệu…
    </p>
  )
}
