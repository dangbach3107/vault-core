import { useEffect, useRef, useState, type ReactNode } from 'react'
import './landing.css'
import Logo from '../../components/Logo'
import { LegalLinks } from '../legal/LegalPage'

const TRY_HREF = '#/vault'

const features = [
  {
    icon: 'M12 3 4 6v6c0 4.4 3.4 8.3 8 9 4.6-.7 8-4.6 8-9V6zM9 12l2 2 4-4',
    title: 'Trust Profile 3 lớp',
    text: 'Hồ sơ doanh nghiệp được chiếu thành ba lớp: ẩn danh, định danh và đầy đủ. Mỗi dữ kiện mang nhãn xác minh rõ ràng.',
  },
  {
    icon: 'M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z',
    title: 'Phòng dữ liệu theo thương vụ',
    text: 'Thư mục chuẩn, nhiều phiên bản tài liệu, xem trước PDF, Office và ảnh ngay trên trình duyệt.',
  },
  {
    icon: 'M3 7h18M3 7v12a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V7M3 7l2-3h14l2 3M9 11h6',
    title: 'Deal workspace từ A đến Z',
    text: 'Theo dõi một thương vụ từ yêu cầu của buyer đến closing trên cùng một màn hình, mỗi bước có người chịu trách nhiệm.',
  },
  {
    icon: 'M16 11a4 4 0 1 0-8 0 4 4 0 0 0 8 0zM4 21a8 8 0 0 1 16 0',
    title: 'Phân quyền theo vai trò',
    text: 'Buyer, Seller, Admin, Legal, Tech DD và Finance chỉ thấy đúng chức năng được giao.',
  },
  {
    icon: 'M12 8v5l3 2M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z',
    title: 'Cấp quyền có thời hạn',
    text: 'Quyền truy cập gắn với người, thương vụ, mục đích và ngày hết hạn. Hết hạn là tự khoá.',
  },
  {
    icon: 'M4 20V10M10 20V4M16 20v-7M22 20H2',
    title: 'Tech DD và phí dịch vụ',
    text: 'Ghi nhận phát hiện kỹ thuật, ký duyệt và các dòng phí của thương vụ ngay trong hệ thống.',
  },
]

const layers = [
  {
    key: 'L1',
    name: 'Lớp 1 · Ẩn danh',
    summary: 'Buyer thấy bức tranh tổng quan mà không biết đó là ai.',
    points: [
      'Ngành, khu vực, quy mô doanh thu theo khoảng',
      'Mã định danh thay cho tên doanh nghiệp',
      'Số dữ kiện đã được xác minh',
    ],
    rows: [
      ['Mã hồ sơ', 'VAULT-0142'],
      ['Ngành', 'Phần mềm'],
      ['Doanh thu', '50 – 100 tỷ'],
    ],
  },
  {
    key: 'L2',
    name: 'Lớp 2 · Định danh',
    summary: 'Sau khi ký NDA, buyer biết danh tính và số liệu chi tiết hơn.',
    points: [
      'Tên pháp lý và mã số thuế',
      'Số liệu tài chính từng năm',
      'Nhãn xác minh cho từng chỉ số',
    ],
    rows: [
      ['Tên pháp lý', 'Công ty ABC'],
      ['Mã số thuế', '01••••••67'],
      ['EBITDA', 'Đã xác minh'],
    ],
  },
  {
    key: 'L3',
    name: 'Lớp 3 · Đầy đủ',
    summary: 'Chỉ người được duyệt mới mở được thông tin nhạy cảm.',
    points: [
      'Cơ cấu cổ đông và người ra quyết định',
      'Mục đích sử dụng được phép',
      'Mọi truy cập đều có thời hạn',
    ],
    rows: [
      ['Cổ đông', 'Cần được duyệt'],
      ['Hết hạn', '30 ngày'],
      ['Người duyệt', 'Seller / Legal'],
    ],
  },
]

const steps = [
  ['Yêu cầu', 'Buyer gửi nhu cầu và khẩu vị đầu tư.'],
  ['Kết nối', 'Hệ thống gợi ý hồ sơ phù hợp theo lớp 1.'],
  ['NDA', 'Ký thoả thuận để mở lớp 2.'],
  ['Phòng dữ liệu', 'Seller mở tài liệu theo quyền được duyệt.'],
  ['Thẩm định', 'Tech DD và Legal rà soát, ký duyệt.'],
  ['Closing', 'Chốt thương vụ, ghi nhận phí và bàn giao.'],
]

const roles = [
  ['Buyer', 'Tìm hồ sơ, gửi yêu cầu truy cập, xem phòng dữ liệu được cấp.'],
  ['Seller', 'Quản lý hồ sơ của mình, duyệt yêu cầu, tải tài liệu.'],
  ['VAULT Admin', 'Vận hành thương vụ, mở phòng dữ liệu, theo dõi tiến độ.'],
  ['Legal', 'Rà soát NDA, duyệt hoặc từ chối quyền truy cập.'],
  ['Tech DD', 'Ghi nhận phát hiện kỹ thuật và ký duyệt thẩm định.'],
  ['Finance', 'Quản lý phí chuẩn bị, phí thành công và các dòng phí khác.'],
]

const stats: [number, string, string][] = [
  [3, '', 'lớp tiết lộ thông tin'],
  [6, '', 'vai trò phân quyền'],
  [15, '', 'bước từ yêu cầu đến closing'],
  [10, ' MB', 'tối đa cho mỗi tài liệu tải lên'],
]

const reduceMotion = () =>
  typeof matchMedia === 'function' &&
  matchMedia('(prefers-reduced-motion: reduce)').matches

function useInView<T extends HTMLElement>(once = true) {
  const ref = useRef<T>(null)
  const [seen, setSeen] = useState(
    () => typeof IntersectionObserver === 'undefined' || reduceMotion(),
  )
  useEffect(() => {
    const node = ref.current
    if (!node || typeof IntersectionObserver === 'undefined' || reduceMotion())
      return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setSeen(true)
          if (once) observer.disconnect()
        } else if (!once) setSeen(false)
      },
      { threshold: 0.15 },
    )
    observer.observe(node)
    return () => observer.disconnect()
  }, [once])
  return [ref, seen] as const
}

function Reveal({
  children,
  delay = 0,
  className = '',
}: {
  children: ReactNode
  delay?: number
  className?: string
}) {
  const [ref, seen] = useInView<HTMLDivElement>()
  return (
    <div
      ref={ref}
      className={`lp-reveal ${seen ? 'is-in' : ''} ${className}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  )
}

function Counter({ to, suffix }: { to: number; suffix: string }) {
  const [ref, seen] = useInView<HTMLSpanElement>()
  const [value, setValue] = useState(() => (reduceMotion() ? to : 0))
  useEffect(() => {
    if (!seen || reduceMotion()) return
    const start = performance.now()
    let frame = 0
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / 1400)
      setValue(Math.round(to * (1 - Math.pow(1 - t, 3))))
      if (t < 1) frame = requestAnimationFrame(tick)
    }
    frame = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(frame)
  }, [seen, to])
  return (
    <span ref={ref}>
      {value}
      {suffix}
    </span>
  )
}

function VideoIcon({ name }: { name: 'play' | 'pause' | 'sound' | 'muted' }) {
  return (
    <svg
      viewBox="0 0 24 24"
      width="18"
      height="18"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {name === 'play' && (
        <path d="M8.5 5.8v12.4a.6.6 0 0 0 .9.5l9.4-6.2a.6.6 0 0 0 0-1L9.4 5.3a.6.6 0 0 0-.9.5z" />
      )}
      {name === 'pause' && (
        <>
          <path d="M8.5 5.5v13" />
          <path d="M15.5 5.5v13" />
        </>
      )}
      {(name === 'sound' || name === 'muted') && (
        <path d="M4.5 9.7h2.9l4.1-3.6a.5.5 0 0 1 .8.4v11a.5.5 0 0 1-.8.4l-4.1-3.6H4.5a.5.5 0 0 1-.5-.5v-3.6a.5.5 0 0 1 .5-.5z" />
      )}
      {name === 'sound' && (
        <>
          <path d="M15.6 9.2a4 4 0 0 1 0 5.6" />
          <path d="M18.2 6.7a7.5 7.5 0 0 1 0 10.6" />
        </>
      )}
      {name === 'muted' && <path d="m16 9.8 4.4 4.4m0-4.4L16 14.2" />}
    </svg>
  )
}

function VideoShowcase() {
  const ref = useRef<HTMLVideoElement>(null)
  const [playing, setPlaying] = useState(false)
  const [muted, setMuted] = useState(true)
  const still = reduceMotion()
  // Sharper 1080p clip on wide screens, lighter 720p on phones and small windows.
  const [src] = useState(() =>
    typeof matchMedia === 'function' && matchMedia('(min-width: 900px)').matches
      ? '/vault-intro-1080.mp4'
      : '/vault-intro.mp4',
  )

  // Play while on screen, pause when scrolled away (saves battery and bandwidth).
  useEffect(() => {
    const video = ref.current
    if (!video || still || typeof IntersectionObserver === 'undefined') return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) video.play?.()?.catch?.(() => undefined)
        else video.pause?.()
      },
      { threshold: 0.45 },
    )
    observer.observe(video)
    return () => observer.disconnect()
  }, [still])

  const toggle = () => {
    const video = ref.current
    if (!video) return
    if (video.paused) video.play?.()?.catch?.(() => undefined)
    else video.pause?.()
  }

  // Browsers only allow sound after a user gesture, so the clip starts muted.
  const toggleSound = () => {
    const video = ref.current
    if (!video) return
    video.muted = !video.muted
    if (!video.muted) video.volume = 0.8
    setMuted(video.muted)
  }

  return (
    <div className="lp-video-frame">
      <video
        ref={ref}
        className="lp-video-el"
        src={src}
        poster="/vault-intro-poster.jpg"
        muted
        loop
        playsInline
        preload="metadata"
        controls={still}
        aria-label="Video giới thiệu VAULT"
        onPlay={() => setPlaying(true)}
        onPause={() => setPlaying(false)}
        onClick={still ? undefined : toggle}
      />
      {!still && (
        <div className="lp-video-ctrls">
          <button
            type="button"
            className="lp-video-btn lp-video-pause"
            onClick={toggle}
            data-tip={playing ? 'Tạm dừng' : 'Phát'}
            aria-label={playing ? 'Tạm dừng video' : 'Phát video'}
          >
            <VideoIcon name={playing ? 'pause' : 'play'} />
          </button>
          <button
            type="button"
            className="lp-video-btn"
            onClick={toggleSound}
            data-tip={muted ? 'Bật âm thanh' : 'Tắt âm thanh'}
            aria-pressed={!muted}
            aria-label={muted ? 'Bật âm thanh' : 'Tắt âm thanh'}
          >
            <VideoIcon name={muted ? 'muted' : 'sound'} />
          </button>
        </div>
      )}
    </div>
  )
}

function Svg({ d }: { d: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d={d} />
    </svg>
  )
}

export default function Landing({ signedIn }: { signedIn: boolean }) {
  const rootRef = useRef<HTMLDivElement>(null)
  const [scrolled, setScrolled] = useState(false)
  const [layer, setLayer] = useState(0)
  const [progress, setProgress] = useState(0)
  const stepsRef = useRef<HTMLOListElement>(null)

  useEffect(() => {
    document.title = 'VAULT — Phòng giao dịch M&A an toàn'
    let frame = 0
    const update = () => {
      frame = 0
      const y = window.scrollY
      setScrolled(y > 24)
      rootRef.current?.style.setProperty('--lp-scroll', String(y))
      const node = stepsRef.current
      if (node) {
        const rect = node.getBoundingClientRect()
        const ratio =
          (window.innerHeight * 0.7 - rect.top) / Math.max(rect.height, 1)
        setProgress(Math.max(0, Math.min(1, ratio)))
      }
    }
    const onScroll = () => {
      if (!frame) frame = requestAnimationFrame(update)
    }
    update()
    addEventListener('scroll', onScroll, { passive: true })
    return () => {
      removeEventListener('scroll', onScroll)
      if (frame) cancelAnimationFrame(frame)
    }
  }, [])

  const goTo = (id: string) => (event: React.MouseEvent) => {
    event.preventDefault()
    document
      .getElementById(id)
      ?.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth' })
  }
  const tryLabel = signedIn ? 'Vào ứng dụng' : 'Dùng thử ngay'
  const active = layers[layer]

  return (
    <div className="lp" ref={rootRef}>
      <header className={`lp-nav ${scrolled ? 'is-solid' : ''}`}>
        <a className="lp-brand" href="#/welcome" aria-label="VAULT trang chủ">
          <Logo variant="white" height={38} />
        </a>
        <nav className="lp-links" aria-label="Điều hướng chính">
          <a href="#lp-video" onClick={goTo('lp-video')}>
            Video
          </a>
          <a href="#lp-features" onClick={goTo('lp-features')}>
            Tính năng
          </a>
          <a href="#lp-layers" onClick={goTo('lp-layers')}>
            Bảo mật 3 lớp
          </a>
          <a href="#lp-how" onClick={goTo('lp-how')}>
            Quy trình
          </a>
          <a href="#lp-roles" onClick={goTo('lp-roles')}>
            Vai trò
          </a>
        </nav>
        <a className="lp-btn lp-btn-light" href={TRY_HREF}>
          {signedIn ? 'Vào ứng dụng' : 'Đăng nhập'}
        </a>
      </header>

      <section className="lp-hero">
        <div className="lp-orb lp-orb-a" aria-hidden="true" />
        <div className="lp-orb lp-orb-b" aria-hidden="true" />
        <div className="lp-grid" aria-hidden="true" />
        <div className="lp-hero-inner">
          <div className="lp-hero-copy">
            <p className="lp-pill lp-rise" style={{ animationDelay: '0ms' }}>
              <span className="lp-pill-dot" aria-hidden="true" />
              Verified Access to Unlisted Listings & Transactions
            </p>
            <h1 className="lp-rise" style={{ animationDelay: '90ms' }}>
              Phòng giao dịch M&A
              <br />
              <span className="lp-gradient-text">an toàn từng lớp.</span>
            </h1>
            <p className="lp-lead lp-rise" style={{ animationDelay: '180ms' }}>
              VAULT kết nối buyer và seller bằng hồ sơ doanh nghiệp đã xác minh,
              phòng dữ liệu có kiểm soát và một luồng thương vụ rõ ràng từ đầu
              đến cuối.
            </p>
            <div className="lp-cta lp-rise" style={{ animationDelay: '270ms' }}>
              <a className="lp-btn lp-btn-primary" href={TRY_HREF}>
                {tryLabel}
                <span aria-hidden="true">→</span>
              </a>
              <a
                className="lp-btn lp-btn-ghost"
                href="#lp-how"
                onClick={goTo('lp-how')}
              >
                Xem cách hoạt động
              </a>
            </div>
          </div>

          <div className="lp-visual" aria-hidden="true">
            <div className="lp-card lp-card-main">
              <div className="lp-card-head">
                <span className="lp-dots">
                  <i />
                  <i />
                  <i />
                </span>
                <span>Phòng dữ liệu · Dự án Alpha</span>
              </div>
              {[
                ['01 Pháp lý', '12 tài liệu', 'full'],
                ['02 Tài chính', '8 tài liệu', 'part'],
                ['03 Công nghệ', '5 tài liệu', 'part'],
                ['04 Nhân sự', '3 tài liệu', 'lock'],
              ].map(([name, count, state]) => (
                <div className="lp-row" key={name}>
                  <span className="lp-folder" />
                  <span className="lp-row-name">{name}</span>
                  <span className="lp-row-count">{count}</span>
                  <span className={`lp-badge lp-badge-${state}`}>
                    {state === 'lock'
                      ? 'Khoá'
                      : state === 'full'
                        ? 'Đã mở'
                        : 'Một phần'}
                  </span>
                </div>
              ))}
            </div>
            <div className="lp-card lp-card-float lp-float-a">
              <p className="lp-mini-label">Trust Profile</p>
              <strong>VAULT-0142</strong>
              <div className="lp-chips">
                <span className="is-on">L1</span>
                <span className="is-on">L2</span>
                <span>L3</span>
              </div>
            </div>
            <div className="lp-card lp-card-float lp-float-b">
              <p className="lp-mini-label">Quyền truy cập</p>
              <strong>Hết hạn sau 30 ngày</strong>
              <div className="lp-bar">
                <span />
              </div>
            </div>
          </div>
        </div>
        <a
          className="lp-scroll-hint"
          href="#lp-stats"
          onClick={goTo('lp-stats')}
          aria-label="Cuộn xuống"
        >
          <span />
        </a>
      </section>

      <section className="lp-stats" id="lp-stats">
        {stats.map(([value, suffix, label]) => (
          <Reveal key={label} className="lp-stat">
            <strong>
              <Counter to={value} suffix={suffix} />
            </strong>
            <span>{label}</span>
          </Reveal>
        ))}
      </section>

      <section className="lp-section lp-video" id="lp-video">
        <Reveal className="lp-head">
          <p className="lp-eyebrow">Xem nhanh 30 giây</p>
          <h2>VAULT hoạt động như thế nào.</h2>
        </Reveal>
        <Reveal>
          <VideoShowcase />
        </Reveal>
      </section>

      <section className="lp-section" id="lp-features">
        <Reveal className="lp-head">
          <p className="lp-eyebrow">Tính năng</p>
          <h2>Mọi thứ một thương vụ cần, trong một nơi.</h2>
        </Reveal>
        <div className="lp-feature-grid">
          {features.map((item, index) => (
            <Reveal key={item.title} delay={(index % 3) * 90}>
              <article className="lp-feature">
                <span className="lp-feature-icon">
                  <Svg d={item.icon} />
                </span>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="lp-section lp-dark" id="lp-layers">
        <Reveal className="lp-head">
          <p className="lp-eyebrow">Bảo mật 3 lớp</p>
          <h2>Tiết lộ đúng lúc, đúng người.</h2>
        </Reveal>
        <div className="lp-layers">
          <div
            className="lp-tabs"
            role="tablist"
            aria-label="Các lớp thông tin"
          >
            {layers.map((item, index) => (
              <button
                key={item.key}
                role="tab"
                aria-selected={index === layer}
                className={index === layer ? 'is-active' : ''}
                onClick={() => setLayer(index)}
                type="button"
              >
                <b>{item.key}</b>
                <span>{item.name.split(' · ')[1]}</span>
              </button>
            ))}
          </div>
          <div className="lp-layer-body" key={active.key} role="tabpanel">
            <div>
              <h3>{active.name}</h3>
              <p>{active.summary}</p>
              <ul>
                {active.points.map((point) => (
                  <li key={point}>{point}</li>
                ))}
              </ul>
            </div>
            <div className="lp-layer-card">
              {active.rows.map(([label, value]) => (
                <div key={label}>
                  <span>{label}</span>
                  <b>{value}</b>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="lp-section" id="lp-how">
        <Reveal className="lp-head">
          <p className="lp-eyebrow">Quy trình</p>
          <h2>Từ yêu cầu đến closing, từng bước có dấu vết.</h2>
        </Reveal>
        <ol className="lp-steps" ref={stepsRef}>
          <span className="lp-steps-line" aria-hidden="true">
            <span style={{ transform: `scaleY(${progress})` }} />
          </span>
          {steps.map(([title, text], index) => (
            <li key={title}>
              <Reveal delay={60}>
                <span
                  className={`lp-step-no ${progress * steps.length > index ? 'is-done' : ''}`}
                >
                  {index + 1}
                </span>
                <div>
                  <h3>{title}</h3>
                  <p>{text}</p>
                </div>
              </Reveal>
            </li>
          ))}
        </ol>
      </section>

      <section className="lp-section lp-tint" id="lp-roles">
        <Reveal className="lp-head">
          <p className="lp-eyebrow">Vai trò</p>
          <h2>Mỗi người một việc, không ai thấy thừa.</h2>
        </Reveal>
        <div className="lp-role-grid">
          {roles.map(([name, text], index) => (
            <Reveal key={name} delay={(index % 3) * 80}>
              <article className="lp-role">
                <h3>{name}</h3>
                <p>{text}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </section>

      <section className="lp-final">
        <div className="lp-orb lp-orb-c" aria-hidden="true" />
        <Reveal>
          <h2>Sẵn sàng bắt đầu một thương vụ?</h2>
          <p>
            Chọn vai trò của bạn và đi hết luồng từ yêu cầu đến closing trên một
            nền tảng duy nhất.
          </p>
          <a className="lp-btn lp-btn-primary" href={TRY_HREF}>
            {tryLabel}
            <span aria-hidden="true">→</span>
          </a>
        </Reveal>
      </section>

      <footer className="lp-footer">
        <span>
          © VAULT · Verified Access to Unlisted Listings & Transactions
        </span>
        <LegalLinks />
      </footer>
    </div>
  )
}
