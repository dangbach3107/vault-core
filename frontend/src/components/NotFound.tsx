export default function NotFound() {
  return (
    <section className="panel not-found-card">
      <span className="code">404</span>
      <h2>Không tìm thấy trang</h2>
      <p>
        Đường dẫn bạn mở không tồn tại hoặc đã được chuyển đi. Hãy quay lại
        trang tổng quan để tiếp tục.
      </p>
      <div className="actions">
        <a className="button-link" href="#/vault">
          Về tổng quan
        </a>
      </div>
    </section>
  )
}
