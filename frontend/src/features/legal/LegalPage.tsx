import Logo from '../../components/Logo'
import { privacy, terms, type LegalDoc } from './content'
import { siteInfo } from './siteInfo'
import type { LegalKind } from './paths'
import './legal.css'

export function LegalLinks({ className = '' }: { className?: string }) {
  return (
    <nav
      className={`legal-links ${className}`.trim()}
      aria-label="Thông tin pháp lý"
    >
      <a href="#/terms">Điều khoản sử dụng</a>
      <a href="#/privacy">Chính sách bảo mật</a>
      <a href="#/contact">Liên hệ</a>
    </nav>
  )
}

function Document({ doc }: { doc: LegalDoc }) {
  return (
    <>
      <h1>{doc.title}</h1>
      <p className="legal-meta">Cập nhật lần cuối: {siteInfo.updated}</p>
      <p className="legal-intro">{doc.intro}</p>
      {doc.sections.map((section) => (
        <section key={section.title}>
          <h2>{section.title}</h2>
          {section.body.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
        </section>
      ))}
    </>
  )
}

function Contact() {
  return (
    <>
      <h1>Liên hệ</h1>
      <p className="legal-intro">
        Bạn cần hỗ trợ tài khoản, có câu hỏi về dữ liệu hoặc muốn báo cáo sự cố
        bảo mật?
      </p>
      <section>
        <h2>Hỗ trợ</h2>
        {siteInfo.contactEmail ? (
          <p>
            Gửi email tới{' '}
            <a href={`mailto:${siteInfo.contactEmail}`}>
              {siteInfo.contactEmail}
            </a>
            . Chúng tôi thường phản hồi trong vòng 1–2 ngày làm việc.
          </p>
        ) : (
          <p>
            Vui lòng liên hệ quản trị viên {siteInfo.product} của tổ chức bạn để
            được hỗ trợ tài khoản và phân quyền.
          </p>
        )}
      </section>
      <section>
        <h2>Báo cáo sự cố bảo mật</h2>
        <p>
          Nếu bạn phát hiện lỗ hổng hoặc nghi ngờ dữ liệu bị truy cập trái phép,
          hãy báo ngay cho quản trị viên và không chia sẻ chi tiết công khai
          trước khi sự cố được xử lý.
        </p>
      </section>
    </>
  )
}

export default function LegalPage({ kind }: { kind: LegalKind }) {
  return (
    <div className="legal">
      <header className="legal-bar">
        <a href="#/welcome" aria-label="VAULT trang chủ">
          <Logo height={34} />
        </a>
        <a className="legal-back" href="#/welcome">
          ← Trang chủ
        </a>
      </header>
      <main className="legal-body">
        {kind === 'contact' ? (
          <Contact />
        ) : (
          <Document doc={kind === 'terms' ? terms : privacy} />
        )}
      </main>
      <footer className="legal-foot">
        <span>
          © {siteInfo.product} · {siteInfo.tagline}
        </span>
        <LegalLinks />
      </footer>
    </div>
  )
}
