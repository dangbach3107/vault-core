import { useMemo, useState } from 'react'

type Tab = 'buyer' | 'seller' | 'vault' | 'legal' | 'tech' | 'finance'
type DealState = {
  buyerRequest: boolean
  sellerProfile: boolean
  prepPackageFeeRecorded: boolean
  sellerL1Approval: boolean
  matchPrepared: boolean
  identityRequested: boolean
  ndaRecorded: boolean
  sellerL2Approval: boolean
  legalL3Approval: boolean
  crossBorderApproval: boolean
  noEscrowConfirmed: boolean
  sellerFileApproval: boolean
  vdrOpened: boolean
  techDdSigned: boolean
  indicativeLoiSubmitted: boolean
  loiSubmitted: boolean
  legalClosingChecklist: boolean
  dealClosed: boolean
  successFeeRecorded: boolean
  postDealHandoff: boolean
}

const initialDeal: DealState = {
  buyerRequest: false,
  sellerProfile: false,
  prepPackageFeeRecorded: false,
  sellerL1Approval: false,
  matchPrepared: false,
  identityRequested: false,
  ndaRecorded: false,
  sellerL2Approval: false,
  legalL3Approval: false,
  crossBorderApproval: false,
  noEscrowConfirmed: false,
  sellerFileApproval: false,
  vdrOpened: false,
  techDdSigned: false,
  indicativeLoiSubmitted: false,
  loiSubmitted: false,
  legalClosingChecklist: false,
  dealClosed: false,
  successFeeRecorded: false,
  postDealHandoff: false,
}

const completedDeal: DealState = Object.fromEntries(
  Object.keys(initialDeal).map((key) => [key, true]),
) as DealState

const tabs: { id: Tab; label: string; role: string }[] = [
  { id: 'buyer', label: 'Buyer', role: 'Doanh nghiệp Nhật / strategic buyer' },
  { id: 'seller', label: 'Seller', role: 'Founder doanh nghiệp Việt Nam' },
  { id: 'vault', label: 'VAULT Admin', role: 'Deal Lead điều phối toàn bộ' },
  { id: 'legal', label: 'Legal', role: 'Legal/Compliance kiểm soát rủi ro' },
  { id: 'tech', label: 'Tech DD', role: 'Reviewer kỹ thuật Rikkei' },
  { id: 'finance', label: 'Finance', role: 'Theo dõi phí, invoice, collected' },
]

const tabOwner: Record<Tab, string> = {
  buyer: 'Buyer',
  seller: 'Seller',
  vault: 'VAULT',
  legal: 'Legal',
  tech: 'Tech DD',
  finance: 'Finance',
}
const ownerTab: Record<string, Tab> = {
  Buyer: 'buyer',
  Seller: 'seller',
  VAULT: 'vault',
  Legal: 'legal',
  'Tech DD': 'tech',
  Finance: 'finance',
}

const whyItMatters: Record<Tab, string> = {
  buyer:
    'Buyer phải cam kết bằng Indicative LOI trước khi thấy hồ sơ nhạy cảm — bảo vệ seller và chi phí thẩm định của VAULT.',
  seller:
    'Seller kiểm soát từng lớp mở thông tin. Danh tính và file nhạy cảm chỉ mở khi seller duyệt, không tự động.',
  vault:
    'VAULT điều phối toàn bộ pipeline nhưng không tự quyết một mình — mỗi bên vẫn giữ quyền phê duyệt riêng.',
  legal:
    'Legal chặn Layer 3 và cross-border trước khi mở VDR, và xác nhận VAULT không giữ tiền/cổ phần.',
  tech: 'Tech DD quy đổi rủi ro công nghệ thành chi phí/tác động cụ thể trước khi buyer gửi Definitive Offer.',
  finance:
    'Phí gói chuẩn bị được ghi nhận sớm — VAULT có doanh thu trước khi biết deal có đóng hay không.',
}

const steps: { key: keyof DealState; label: string; owner: string }[] = [
  { key: 'buyerRequest', label: 'Buyer tạo request 4 trường', owner: 'Buyer' },
  { key: 'sellerProfile', label: 'Seller tạo hồ sơ mẫu', owner: 'Seller' },
  { key: 'prepPackageFeeRecorded', label: 'Finance ghi nhận phí gói chuẩn bị', owner: 'Finance' },
  { key: 'sellerL1Approval', label: 'Seller duyệt teaser L1', owner: 'Seller' },
  { key: 'matchPrepared', label: 'VAULT match buyer–seller', owner: 'VAULT' },
  { key: 'identityRequested', label: 'Buyer yêu cầu mở danh tính L2', owner: 'Buyer' },
  { key: 'ndaRecorded', label: 'VAULT ghi nhận NDA', owner: 'VAULT' },
  { key: 'sellerL2Approval', label: 'Seller duyệt buyer mở L2', owner: 'Seller' },
  { key: 'indicativeLoiSubmitted', label: 'Buyer nộp Indicative LOI trước khi mở VDR', owner: 'Buyer' },
  { key: 'legalL3Approval', label: 'Legal duyệt L3', owner: 'Legal' },
  { key: 'crossBorderApproval', label: 'Legal duyệt cross-border access', owner: 'Legal' },
  { key: 'noEscrowConfirmed', label: 'Legal xác nhận VAULT không giữ tiền', owner: 'Legal' },
  { key: 'sellerFileApproval', label: 'Seller duyệt file L3 cho buyer', owner: 'Seller' },
  { key: 'vdrOpened', label: 'VAULT mở VDR files được duyệt', owner: 'VAULT' },
  { key: 'techDdSigned', label: 'Tech DD ký checklist + findings', owner: 'Tech DD' },
  { key: 'loiSubmitted', label: 'Buyer gửi Definitive Offer', owner: 'Buyer' },
  { key: 'legalClosingChecklist', label: 'Legal checklist closing', owner: 'Legal' },
  { key: 'dealClosed', label: 'SPA signed / closing giả lập', owner: 'VAULT' },
  { key: 'successFeeRecorded', label: 'Finance ghi nhận success fee', owner: 'Finance' },
  { key: 'postDealHandoff', label: 'Post-deal handoff cho Rikkei', owner: 'VAULT' },
]

const macroStages: { id: string; label: string; keys: (keyof DealState)[]; tab: Tab }[] = [
  { id: 'request', label: 'Buyer Request', keys: ['buyerRequest'], tab: 'buyer' },
  {
    id: 'seller',
    label: 'Seller Profile & Prep Fee',
    keys: ['sellerProfile', 'sellerL1Approval', 'prepPackageFeeRecorded'],
    tab: 'seller',
  },
  {
    id: 'match',
    label: 'Match & Layer 2',
    keys: ['matchPrepared', 'identityRequested', 'ndaRecorded', 'sellerL2Approval'],
    tab: 'vault',
  },
  { id: 'loi', label: 'Indicative LOI', keys: ['indicativeLoiSubmitted'], tab: 'buyer' },
  {
    id: 'legal3',
    label: 'Legal & VDR (L3)',
    keys: ['legalL3Approval', 'crossBorderApproval', 'noEscrowConfirmed', 'sellerFileApproval', 'vdrOpened'],
    tab: 'legal',
  },
  { id: 'techdd', label: 'Tech DD', keys: ['techDdSigned'], tab: 'tech' },
  {
    id: 'offer',
    label: 'Definitive Offer & Closing',
    keys: ['loiSubmitted', 'legalClosingChecklist', 'dealClosed'],
    tab: 'buyer',
  },
  { id: 'handoff', label: 'Success Fee & Handoff', keys: ['successFeeRecorded', 'postDealHandoff'], tab: 'finance' },
]

const buyerBrief = [
  ['Năng lực cần mua', 'Phần mềm quản lý kho/vận hành B2B đã chạy tại nhà máy Việt Nam'],
  ['Mục tiêu 24 tháng', 'Bản địa hóa sản phẩm, giữ đội kỹ thuật, mở rộng vào khách hàng Nhật tại Việt Nam'],
  ['Ngân sách / cỡ deal', '70–150 tỷ VND EV; sở hữu mục tiêu 25–35%'],
  ['Timeline / decision path', 'LOI trong 90 ngày; closing 9–12 tháng; sponsor BU Nhật đã chỉ định'],
]

const sellerFacts = [
  ['Công ty mẫu', 'Công ty phần mềm kho vận B2B tại miền Nam'],
  ['Doanh thu L1', '50–100 tỷ VND'],
  ['Nhân sự L1', '50–200 nhân sự'],
  ['Deal intent', 'Tìm strategic partner Nhật, bán/gọi vốn 25–35%'],
]

const matchCriteria = [
  ['Ngành / use case', 5, 'Khớp nhu cầu warehouse B2B'],
  ['Capability buyer cần', 5, 'Có sản phẩm và đội kỹ thuật tại Việt Nam'],
  ['Quy mô deal', 4, 'EV nằm trong vùng buyer dự kiến'],
  ['Deal type / tỷ lệ', 4, '25–35% phù hợp minority strategic deal'],
  ['Tech readiness', 4, 'Có tài liệu kiến trúc và scope Tech DD'],
  ['Geography', 5, 'Miền Nam, gần tập khách hàng nhà máy'],
  ['Timeline', 3, 'Cần xác minh người ký cuối phía Nhật'],
  ['Legal blockers', 3, 'Cần cross-border data approval và IP review'],
]

const vdrFiles = [
  ['Legal', 'Giấy ĐKKD, điều lệ, shareholder register'],
  ['Financial', 'P&L 3 năm, revenue proof, debt summary'],
  ['Commercial', 'Top customers masked, pipeline, churn summary'],
  ['Technology/IP', 'Architecture, repo read-only pack, OSS/SBOM, SAST export'],
  ['HR', 'Org chart, key engineer dependency, compensation summary'],
  ['Q&A', 'Question, owner, deadline, answer, status'],
]

const techFindings = [
  ['Architecture scalability', 'Major', '6-month fix', '180 triệu VND'],
  ['OSS license evidence', 'High', 'pre-closing must-fix', '90 triệu VND'],
  ['Key-person dependency', 'Medium', 'defer', 'Không trừ giá; đưa vào condition'],
  ['Integration cost', 'Observation', 'growth investment', '320 triệu VND'],
]

const financeRows = [
  ['Prep package', '90 triệu', 'Record ngay sau seller ký chuẩn hóa hồ sơ', 'Không phụ thuộc deal có closing'],
  ['Success fee M&A', '2% x phần vốn giao dịch', 'Expected', 'Ghi nhận khi closing'],
  ['Tech DD', '250 triệu', 'Config owner', 'Chưa chốt VAULT/Rikkei'],
  ['Build-to-Buy', '600 triệu', 'Opportunity', 'Scope nhẹ sau Tech DD'],
]

export default function InvestorMvp() {
  const [activeTab, setActiveTab] = useState<Tab>('buyer')
  const [deal, setDeal] = useState<DealState>(initialDeal)
  const [overrideReason, setOverrideReason] = useState('')

  const progress = useMemo(() => {
    const done = steps.filter((step) => deal[step.key]).length
    return Math.round((done / steps.length) * 100)
  }, [deal])

  const matchScore = useMemo(
    () => matchCriteria.reduce((sum, [, score]) => sum + Number(score), 0),
    [],
  )
  const layer1Ready = deal.sellerL1Approval && deal.matchPrepared
  const layer2Ready = deal.identityRequested && deal.ndaRecorded && deal.sellerL2Approval
  const layer3Ready =
    layer2Ready &&
    deal.indicativeLoiSubmitted &&
    deal.legalL3Approval &&
    deal.crossBorderApproval &&
    deal.sellerFileApproval

  const nextStep = useMemo(() => steps.find((step) => !deal[step.key]), [deal])

  const complete = (key: keyof DealState) =>
    setDeal((current) => ({ ...current, [key]: true }))
  const reset = () => {
    setDeal(initialDeal)
    setOverrideReason('')
    setActiveTab('buyer')
  }
  const jumpTo = (tab: Tab) => setActiveTab(tab)

  return (
    <section className="az-workspace" aria-labelledby="az-title">
      <div className="hero-panel compact-hero">
        <div className="hero-top">
          <div>
            <p className="eyebrow">A–Z Deal Workspace · synthetic investor demo</p>
            <h1 id="az-title">VAULT Core — một thương vụ mẫu, đi từ A đến Z</h1>
          </div>
          <div className="hero-actions">
            <button className="secondary" onClick={reset}>Reset demo</button>
            <button onClick={() => setDeal(completedDeal)}>Hoàn tất mẫu</button>
          </div>
        </div>
        <p className="hero-sub">
          Japanese strategic buyer × Vietnamese warehouse-software seller — cùng một deal xuyên suốt
          Buyer, Seller, VAULT Admin, Legal, Tech DD và Finance. Dữ liệu giả lập, chưa phải production.
        </p>
      </div>

      <div className="panel deal-header-panel">
        <div className="section-title compact-title">
          <div>
            <p className="eyebrow">Sample deal</p>
            <h2>Japanese buyer × Vietnamese warehouse software seller</h2>
          </div>
          <span className="status-pill ready">{progress}% hoàn tất</span>
        </div>
        <progress max="100" value={progress} aria-label="Tiến độ deal" />

        <StageTimeline deal={deal} macroStages={macroStages} onJump={jumpTo} />

        <NextActionBanner nextStep={nextStep} onJump={() => nextStep && jumpTo(ownerTab[nextStep.owner])} />

        <div className="mvp-grid three compact-metrics">
          <Metric label="Layer 1" value={layer1Ready ? 'Open' : 'Locked'} note="Seller teaser approval" />
          <Metric label="Layer 2" value={layer2Ready ? 'Open' : 'Locked'} note="NDA + seller approval" />
          <Metric label="Layer 3" value={layer3Ready ? 'Open' : 'Locked'} note="Seller file + Legal/Compliance" />
        </div>
      </div>

      <DifferentiatorStrip deal={deal} />

      <details className="panel principles-details">
        <summary>Xem thêm nguyên tắc vận hành platform</summary>
        <div className="mvp-grid three">
          <article className="decision-card"><h3>Buyer-first</h3><p>Bắt đầu từ nhu cầu mua cụ thể, không dựng marketplace đăng tin hàng loạt.</p></article>
          <article className="decision-card"><h3>Mở theo lớp</h3><p>L1/L2/L3 có seller approval, NDA, Legal/Compliance và duyệt file riêng.</p></article>
          <article className="decision-card"><h3>Definitive Offer sau DD</h3><p>Đề nghị chính thức chỉ đến sau VDR và Tech DD, khác LOI sơ bộ trước VDR.</p></article>
          <article className="decision-card"><h3>Không production-ready</h3><p>Bản này dùng dữ liệu giả lập; cần auth, MFA, audit, VDR thật, watermark và scan file trước dữ liệu thật.</p></article>
        </div>
      </details>

      <nav className="role-tabs" aria-label="Deal workspace tabs">
        {tabs.map((tab) => (
          <RoleTabButton
            key={tab.id}
            tab={tab}
            active={activeTab === tab.id}
            deal={deal}
            nextStep={nextStep}
            onClick={() => setActiveTab(tab.id)}
          />
        ))}
      </nav>

      <div className="tab-layout">
        <div className="tab-main">
          {activeTab === 'buyer' && (
            <BuyerTab
              deal={deal}
              complete={complete}
              layer1Ready={layer1Ready}
              layer2Ready={layer2Ready}
              layer3Ready={layer3Ready}
            />
          )}
          {activeTab === 'seller' && <SellerTab deal={deal} complete={complete} />}
          {activeTab === 'vault' && (
            <VaultTab
              deal={deal}
              complete={complete}
              matchScore={matchScore}
              overrideReason={overrideReason}
              setOverrideReason={setOverrideReason}
              layer3Ready={layer3Ready}
            />
          )}
          {activeTab === 'legal' && <LegalTab deal={deal} complete={complete} />}
          {activeTab === 'tech' && <TechTab deal={deal} complete={complete} layer3Ready={layer3Ready} />}
          {activeTab === 'finance' && <FinanceTab deal={deal} complete={complete} />}
        </div>
        <NextGatesPanel tab={activeTab} deal={deal} />
      </div>
    </section>
  )
}

function StageTimeline({
  deal,
  macroStages: stages,
  onJump,
}: {
  deal: DealState
  macroStages: { id: string; label: string; keys: (keyof DealState)[]; tab: Tab }[]
  onJump: (tab: Tab) => void
}) {
  const currentIndex = stages.findIndex((stage) => stage.keys.some((key) => !deal[key]))
  return (
    <ol className="stage-timeline" aria-label="Tiến độ theo giai đoạn">
      {stages.map((stage, index) => {
        const status = currentIndex === -1 || index < currentIndex ? 'done' : index === currentIndex ? 'current' : 'locked'
        return (
          <li key={stage.id} className={`stage-${status}`}>
            <button type="button" onClick={() => onJump(stage.tab)}>
              <span className="stage-index">{status === 'done' ? '✓' : index + 1}</span>
              <span className="stage-label">{stage.label}</span>
            </button>
          </li>
        )
      })}
    </ol>
  )
}

function NextActionBanner({
  nextStep,
  onJump,
}: {
  nextStep: { key: keyof DealState; label: string; owner: string } | undefined
  onJump: () => void
}) {
  if (!nextStep) {
    return <div className="next-action-banner is-done">🎉 Deal đã hoàn tất A–Z — tất cả 20 bước đã xong.</div>
  }
  return (
    <div className="next-action-banner">
      <div>
        <span className="eyebrow">Bước tiếp theo</span>
        <p><strong>{nextStep.owner}</strong> · {nextStep.label}</p>
      </div>
      <button className="secondary" onClick={onJump}>Đi tới tab {nextStep.owner}</button>
    </div>
  )
}

function DifferentiatorStrip({ deal }: { deal: DealState }) {
  const items = [
    {
      title: 'Doanh thu sớm, không chỉ success fee',
      body: 'Phí gói chuẩn bị ghi nhận ngay sau khi seller chuẩn hóa hồ sơ — không đợi closing.',
      done: deal.prepPackageFeeRecorded,
    },
    {
      title: 'Cam kết trước, mở VDR sau',
      body: 'Buyer phải nộp Indicative LOI (non-binding) trước khi thấy hồ sơ nhạy cảm và trước Tech DD.',
      done: deal.indicativeLoiSubmitted,
    },
    {
      title: 'Rủi ro kỹ thuật hóa thành chi phí',
      body: 'Tech DD lượng hóa rủi ro công nghệ thành cost impact trước khi buyer gửi Definitive Offer.',
      done: deal.techDdSigned,
    },
  ]
  return (
    <div className="mvp-grid three differentiator-strip">
      {items.map((item, index) => (
        <article key={item.title} className={item.done ? 'differentiator-card is-live' : 'differentiator-card'}>
          <span className="differentiator-index">{index + 1}</span>
          <h3>{item.title}</h3>
          <p>{item.body}</p>
          <span className={item.done ? 'status-pill ready' : 'status-pill'}>
            {item.done ? 'Đã xảy ra trong deal này' : 'Chưa tới bước này'}
          </span>
        </article>
      ))}
    </div>
  )
}

function RoleTabButton({
  tab,
  active,
  deal,
  nextStep,
  onClick,
}: {
  tab: { id: Tab; label: string; role: string }
  active: boolean
  deal: DealState
  nextStep: { key: keyof DealState; owner: string } | undefined
  onClick: () => void
}) {
  const owner = tabOwner[tab.id]
  const pending = steps.filter((step) => step.owner === owner && !deal[step.key])
  const dotState = pending.length === 0 ? 'done' : nextStep?.owner === owner ? 'active' : 'waiting'
  return (
    <button className={active ? 'active' : 'secondary'} onClick={onClick}>
      <span className="tab-top-row">
        <span className={`tab-dot tab-dot-${dotState}`} aria-hidden="true" />
        {tab.label}
      </span>
      <span>{tab.role}</span>
    </button>
  )
}

function NextGatesPanel({ tab, deal }: { tab: Tab; deal: DealState }) {
  const owner = tabOwner[tab]
  const pending = steps.filter((step) => step.owner === owner && !deal[step.key])
  return (
    <aside className="side-panel">
      <div className="side-block">
        <p className="eyebrow">Next required gates</p>
        {pending.length === 0 ? (
          <p className="side-empty">Không còn gate nào của {owner} đang chờ.</p>
        ) : (
          <ul className="gate-list">
            {pending.map((step) => (
              <li key={step.key}>{step.label}</li>
            ))}
          </ul>
        )}
      </div>
      <div className="side-block">
        <p className="eyebrow">Why this matters</p>
        <p>{whyItMatters[tab]}</p>
      </div>
    </aside>
  )
}

function BuyerTab({
  deal,
  complete,
  layer1Ready,
  layer2Ready,
  layer3Ready,
}: {
  deal: DealState
  complete: (key: keyof DealState) => void
  layer1Ready: boolean
  layer2Ready: boolean
  layer3Ready: boolean
}) {
  return (
    <section className="panel">
      <RoleHeader label="Buyer" title="1. Tạo nhu cầu mua và đi qua các lớp thông tin" />
      <div className="mvp-grid two">
        <article className="decision-card">
          <h3>Buyer Request — 4 trường MVP</h3>
          <dl className="compact-dl">
            {buyerBrief.map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
          </dl>
          <ActionButton done={deal.buyerRequest} onClick={() => complete('buyerRequest')}>
            Lưu buyer request
          </ActionButton>
        </article>
        <article className="decision-card">
          <h3>Layer 1 teaser</h3>
          <p>
            {layer1Ready
              ? 'Buyer đã được xem teaser ẩn danh: ngành, vùng, revenue band, employee band, deal intent.'
              : 'Chờ Seller duyệt teaser và VAULT match buyer–seller.'}
          </p>
          <ActionButton
            done={deal.identityRequested}
            disabled={!layer1Ready}
            lockedHint="Cần Seller duyệt Layer 1 và VAULT match buyer–seller trước."
            onClick={() => complete('identityRequested')}
          >
            Request identity / mở Layer 2
          </ActionButton>
        </article>
      </div>

      <div className="mvp-grid two">
        <article className="decision-card">
          <h3>Layer 2 CIM</h3>
          <p>
            {layer2Ready
              ? 'Đã mở CIM định danh. Top customers vẫn masked dạng Client A/B/C.'
              : 'Cần Buyer request identity, NDA recorded và Seller approval.'}
          </p>
        </article>
        <article className="decision-card">
          <h3>Indicative LOI trước VDR</h3>
          <p>
            Trước khi VAULT mở toàn bộ VDR và bỏ chi phí Tech DD, buyer phải có cam kết tối thiểu
            bằng văn bản để bảo vệ seller và chi phí VAULT.
          </p>
          <ActionButton
            done={deal.indicativeLoiSubmitted}
            disabled={!layer2Ready}
            lockedHint="Cần Layer 2 mở đủ điều kiện (NDA + Seller duyệt) trước."
            onClick={() => complete('indicativeLoiSubmitted')}
          >
            Submit Indicative LOI (non-binding + đề nghị độc quyền đàm phán ngắn hạn)
          </ActionButton>
        </article>
      </div>

      <article className="decision-card">
        <h3>Layer 3 VDR files</h3>
        {layer3Ready ? (
          <ul>
            {vdrFiles.map(([folder, file]) => (
              <li key={folder}><strong>{folder}:</strong> {file}</li>
            ))}
          </ul>
        ) : (
          <p>
            Cần Indicative LOI + Legal/Compliance + Seller duyệt file nhạy cảm trước khi buyer xem L3.
            Cam kết trước, mở hồ sơ sau.
          </p>
        )}
      </article>

      <article className="decision-card">
        <h3>Buyer final action</h3>
        <p>
          Sau khi có đầy đủ thông tin từ VDR và Tech DD, Buyer gửi Đề nghị chính thức
          (Definitive Offer). Đây khác với Indicative LOI sơ bộ nộp trước khi thấy hồ sơ nhạy cảm.
        </p>
        <ActionButton
          done={deal.loiSubmitted}
          disabled={!deal.techDdSigned}
          lockedHint="Cần Tech DD reviewer sign-off trước."
          onClick={() => complete('loiSubmitted')}
        >
          Submit Definitive Offer
        </ActionButton>
      </article>
    </section>
  )
}

function SellerTab({ deal, complete }: { deal: DealState; complete: (key: keyof DealState) => void }) {
  return (
    <section className="panel">
      <RoleHeader label="Seller" title="2. Tạo hồ sơ, duyệt từng lớp mở thông tin" />
      <div className="mvp-grid two">
        <article className="decision-card">
          <h3>Seller profile mẫu</h3>
          <dl className="compact-dl">
            {sellerFacts.map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
          </dl>
          <ActionButton done={deal.sellerProfile} onClick={() => complete('sellerProfile')}>
            Tạo seller profile từ sample data
          </ActionButton>
        </article>
        <article className="decision-card">
          <h3>Seller approvals</h3>
          <div className="stacked-actions">
            <ActionButton
              done={deal.sellerL1Approval}
              disabled={!deal.sellerProfile}
              lockedHint="Cần tạo seller profile trước."
              onClick={() => complete('sellerL1Approval')}
            >
              Approve L1 teaser
            </ActionButton>
            <ActionButton
              done={deal.sellerL2Approval}
              disabled={!deal.identityRequested || !deal.ndaRecorded}
              lockedHint="Cần buyer request identity và NDA recorded trước."
              onClick={() => complete('sellerL2Approval')}
            >
              Approve buyer mở Layer 2
            </ActionButton>
            <ActionButton
              done={deal.sellerFileApproval}
              disabled={!deal.sellerL2Approval || !deal.indicativeLoiSubmitted}
              lockedHint="Cần Layer 2 approved và Indicative LOI trước."
              onClick={() => complete('sellerFileApproval')}
            >
              Approve từng file Layer 3 cho buyer
            </ActionButton>
          </div>
        </article>
      </div>
      <article className="decision-card">
        <h3>Seller sees buyer interest</h3>
        <p>
          {deal.loiSubmitted
            ? 'Buyer đã gửi LOI. Seller có thể xem điều kiện chính và chuẩn bị closing checklist.'
            : 'Chưa có LOI. Seller thấy trạng thái buyer request, NDA, approvals và Tech DD.'}
        </p>
      </article>
    </section>
  )
}

function VaultTab({
  deal,
  complete,
  matchScore,
  overrideReason,
  setOverrideReason,
  layer3Ready,
}: {
  deal: DealState
  complete: (key: keyof DealState) => void
  matchScore: number
  overrideReason: string
  setOverrideReason: (value: string) => void
  layer3Ready: boolean
}) {
  const openTasks = steps.filter((step) => !deal[step.key]).slice(0, 6)
  return (
    <section className="panel">
      <RoleHeader label="VAULT Admin" title="3. Trung tâm điều phối pipeline / matching / approvals / VDR / Tech DD / Finance" />
      <div className="mvp-grid two">
        <article className="decision-card">
          <h3>Task list theo role</h3>
          <ul>
            {openTasks.map((task) => (
              <li key={task.key}><strong>{task.owner}:</strong> {task.label}</li>
            ))}
          </ul>
          {openTasks.length === 0 && <p>Tất cả task A–Z đã hoàn tất.</p>}
        </article>
        <article className="decision-card">
          <h3>Matching rule-based</h3>
          <p><strong>Score:</strong> {matchScore}/40</p>
          <p><strong>Lý do match:</strong> buyer cần warehouse B2B, seller có sản phẩm và đội kỹ thuật, cỡ deal khớp.</p>
          <p><strong>3 risks:</strong> người ký cuối, IP/code ownership, cross-border data.</p>
          <ActionButton
            done={deal.matchPrepared}
            disabled={!deal.buyerRequest || !deal.sellerL1Approval}
            lockedHint="Cần buyer request và seller L1 approval trước."
            onClick={() => complete('matchPrepared')}
          >
            Prepare match buyer–seller
          </ActionButton>
        </article>
      </div>

      <div className="mvp-grid two">
        <article className="decision-card">
          <h3>Approvals console</h3>
          <div className="stacked-actions">
            <ActionButton
              done={deal.ndaRecorded}
              disabled={!deal.identityRequested}
              lockedHint="Cần buyer request identity trước."
              onClick={() => complete('ndaRecorded')}
            >
              Record signed NDA
            </ActionButton>
            <ActionButton
              done={deal.vdrOpened}
              disabled={!layer3Ready}
              lockedHint="Cần Layer 3 đủ điều kiện (Indicative LOI + Legal + seller file approval)."
              onClick={() => complete('vdrOpened')}
            >
              Open approved VDR files
            </ActionButton>
            <ActionButton
              done={deal.dealClosed}
              disabled={!deal.legalClosingChecklist || !deal.loiSubmitted}
              lockedHint="Cần Definitive Offer và Legal closing checklist trước."
              onClick={() => complete('dealClosed')}
            >
              Mark SPA signed / deal closed
            </ActionButton>
            <ActionButton
              done={deal.postDealHandoff}
              disabled={!deal.dealClosed}
              lockedHint="Cần deal closed trước."
              onClick={() => complete('postDealHandoff')}
            >
              Post-deal handoff to Rikkei
            </ActionButton>
          </div>
        </article>
        <article className="decision-card">
          <h3>Override with reason</h3>
          <p>Admin không override im lặng. Nếu cần vượt chặn demo, phải nhập lý do.</p>
          <textarea
            rows={4}
            value={overrideReason}
            onChange={(event) => setOverrideReason(event.target.value)}
            placeholder="Ví dụ: Sponsor phê duyệt tạm để demo investor, chưa dùng dữ liệu thật."
          />
          <span className={overrideReason ? 'status-pill warning' : 'status-pill'}>
            {overrideReason ? 'Override reason recorded' : 'No override reason'}
          </span>
        </article>
      </div>
    </section>
  )
}

function LegalTab({ deal, complete }: { deal: DealState; complete: (key: keyof DealState) => void }) {
  return (
    <section className="panel">
      <RoleHeader label="Legal/Compliance" title="4. Kiểm soát L3, cross-border data, escrow và closing" />
      <div className="mvp-grid two">
        <article className="decision-card">
          <h3>Legal approvals</h3>
          <div className="stacked-actions">
            <ActionButton
              done={deal.legalL3Approval}
              disabled={!deal.sellerL2Approval || !deal.indicativeLoiSubmitted}
              lockedHint="Cần Layer 2 approved và Indicative LOI trước."
              onClick={() => complete('legalL3Approval')}
            >
              Approve Layer 3 access
            </ActionButton>
            <ActionButton
              done={deal.crossBorderApproval}
              disabled={!deal.sellerL2Approval || !deal.indicativeLoiSubmitted}
              lockedHint="Cần Layer 2 approved và Indicative LOI trước."
              onClick={() => complete('crossBorderApproval')}
            >
              Approve cross-border data access
            </ActionButton>
            <ActionButton done={deal.noEscrowConfirmed} onClick={() => complete('noEscrowConfirmed')}>
              Confirm VAULT does not hold money/shares
            </ActionButton>
            <ActionButton
              done={deal.legalClosingChecklist}
              disabled={!deal.loiSubmitted}
              lockedHint="Cần Definitive Offer trước."
              onClick={() => complete('legalClosingChecklist')}
            >
              Complete LOI/closing checklist
            </ActionButton>
          </div>
        </article>
        <article className="decision-card">
          <h3>Book B locked</h3>
          <p>
            Huy động rộng/cổ tức/mua lại không được mở như sản phẩm. MVP chỉ ghi risk/checklist;
            nghĩa vụ trả thuộc bên phát hành, không thuộc VAULT.
          </p>
          <p className="notice">Nếu cross-border chưa approve, Buyer không được xem L2/L3 trong demo chuẩn.</p>
        </article>
      </div>
    </section>
  )
}

function TechTab({
  deal,
  complete,
  layer3Ready,
}: {
  deal: DealState
  complete: (key: keyof DealState) => void
  layer3Ready: boolean
}) {
  return (
    <section className="panel">
      <RoleHeader label="Tech DD" title="5. Checklist 6 trục, findings và remediation cost" />
      <p className="notice">
        Tech DD bắt đầu sau khi buyer đã nộp Indicative LOI và được mở L3/VDR. Output MVP = checklist + findings + remediation cost;
        report builder để phase sau.
      </p>
      <div className="table-scroll">
        <table className="mvp-table">
          <thead>
            <tr><th>Finding</th><th>Severity</th><th>Remediation class</th><th>Cost / deal impact</th></tr>
          </thead>
          <tbody>
            {techFindings.map((row) => (
              <tr key={row[0]}>{row.map((cell) => <td key={cell}>{cell}</td>)}</tr>
            ))}
          </tbody>
        </table>
      </div>
      <ActionButton
        done={deal.techDdSigned}
        disabled={!layer3Ready}
        lockedHint="Cần Layer 3/VDR mở đủ điều kiện trước."
        onClick={() => complete('techDdSigned')}
      >
        Tech DD reviewer sign-off
      </ActionButton>
    </section>
  )
}

function FinanceTab({ deal, complete }: { deal: DealState; complete: (key: keyof DealState) => void }) {
  return (
    <section className="panel">
      <RoleHeader label="Finance" title="6. Tracking phí, invoice, collected, overdue" />
      <article className="decision-card highlight-card">
        <h3>Phí gói chuẩn bị</h3>
        <p>
          Phí này thu ngay khi seller ký hợp đồng chuẩn hóa hồ sơ, không phụ thuộc deal sau này
          có đóng hay không. VAULT có doanh thu từ giai đoạn chuẩn bị, không chỉ ăn success fee.
        </p>
        <ActionButton
          done={deal.prepPackageFeeRecorded}
          disabled={!deal.sellerProfile}
          lockedHint="Cần tạo seller profile trước."
          onClick={() => complete('prepPackageFeeRecorded')}
        >
          Record prep package fee
        </ActionButton>
      </article>

      <div className="table-scroll">
        <table className="mvp-table">
          <thead>
            <tr><th>Revenue line</th><th>Amount/default</th><th>Status</th><th>Note</th></tr>
          </thead>
          <tbody>
            {financeRows.map((row) => (
              <tr key={row[0]}>{row.map((cell) => <td key={cell}>{cell}</td>)}</tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mvp-grid two">
        <article className="decision-card">
          <h3>Closing state</h3>
          <p>{deal.dealClosed ? 'SPA signed / deal closed giả lập.' : 'Chưa closing. Cần LOI + legal closing checklist.'}</p>
        </article>
        <article className="decision-card">
          <h3>Success fee</h3>
          <p>Phí gói chuẩn bị đã ghi ở bước 2.5; màn này tổng hợp thêm success fee/Tech DD/Build-to-Buy phát sinh khi đóng deal. Không sync Excel model; app tracking actuals.</p>
          <ActionButton
            done={deal.successFeeRecorded}
            disabled={!deal.dealClosed}
            lockedHint="Cần deal closed trước."
            onClick={() => complete('successFeeRecorded')}
          >
            Record success fee
          </ActionButton>
        </article>
      </div>
    </section>
  )
}

function RoleHeader({ label, title }: { label: string; title: string }) {
  return (
    <div className="section-title">
      <div>
        <p className="eyebrow">{label}</p>
        <h2>{title}</h2>
      </div>
    </div>
  )
}

function Metric({ label, value, note }: { label: string; value: string; note: string }) {
  return (
    <article className="metric-card small">
      <span>{label}</span>
      <strong>{value}</strong>
      <p>{note}</p>
    </article>
  )
}

function ActionButton({
  done,
  disabled,
  lockedHint,
  onClick,
  children,
}: {
  done: boolean
  disabled?: boolean
  lockedHint?: string
  onClick: () => void
  children: React.ReactNode
}) {
  const state = done ? 'done' : disabled ? 'locked' : 'available'
  return (
    <div className="action-slot">
      <button className={`action-btn state-${state}`} disabled={done || disabled} onClick={onClick}>
        <span className="action-btn-state">
          {state === 'done' ? '✓ Hoàn tất' : state === 'locked' ? '🔒 Khoá' : '● Sẵn sàng'}
        </span>
        <span className="action-btn-label">{children}</span>
      </button>
      {state === 'locked' && lockedHint && <p className="locked-hint">{lockedHint}</p>}
    </div>
  )
}
