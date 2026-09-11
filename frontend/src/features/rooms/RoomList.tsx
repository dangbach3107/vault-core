import { useState } from 'react'
import { request, type Room, type Summary } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'

function CompanyMatches({
  query,
  onChoose,
}: {
  query: string
  onChoose: (company: Summary) => void
}) {
  const result = useLoad<Summary[]>(
    `/companies?q=${encodeURIComponent(query)}&limit=20`,
  )
  if (!result.data) return <LoadState {...result} />
  return (
    <>
      <p className="muted">
        Tối đa 20 kết quả. Nhập tên hoặc mã số thuế để thu hẹp.
      </p>
      {result.data.length === 0 && (
        <p>
          Chưa có doanh nghiệp. <a href="#/companies/new">Tạo hồ sơ trước</a>.
        </p>
      )}
      <div className="company-options">
        {result.data.map((company) => (
          <button
            type="button"
            className="secondary"
            key={company.id}
            onClick={() => onChoose(company)}
          >
            {company.name} · {company.tax_id || company.alias}
          </button>
        ))}
      </div>
    </>
  )
}

function NewRoom({ company }: { company: Summary }) {
  const [title, setTitle] = useState('')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  async function create(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      const room = await request<Room>('/rooms', {
        method: 'POST',
        body: JSON.stringify({ company_id: company.id, title }),
      })
      location.hash = `/rooms/${room.id}?created=1`
    } catch (reason) {
      setError((reason as Error).message)
    } finally {
      setSaving(false)
    }
  }
  return (
    <form className="panel" onSubmit={create}>
      <h2>Phòng mới cho {company.name}</h2>
      <p className="muted">
        Mỗi phòng đại diện cho một thương vụ của doanh nghiệp này.
      </p>
      <label>
        Tên thương vụ / phòng dữ liệu
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          maxLength={200}
          disabled={saving}
          placeholder="Ví dụ: Thương vụ hợp tác 2026 — giả lập"
        />
      </label>
      {error && (
        <p className="error-box" role="alert">
          {error}
        </p>
      )}
      <button disabled={saving}>
        {saving ? 'Đang tạo…' : 'Tạo phòng dữ liệu'}
      </button>
    </form>
  )
}

function Rooms({ companyId, page }: { companyId?: string; page: number }) {
  const result = useLoad<Room[]>(
    `/rooms?offset=${page * 20}&limit=20${companyId ? `&company_id=${companyId}` : ''}`,
  )
  if (!result.data) return <LoadState {...result} />
  return result.data.length === 0 ? (
    <p className="empty panel">Chưa có phòng dữ liệu trên trang này.</p>
  ) : (
    <div className="record-list">
      {result.data.map((room) => (
        <a className="record panel" href={`#/rooms/${room.id}`} key={room.id}>
          <div>
            <p>{room.company_name}</p>
            <h2>{room.title}</h2>
            <p>Tạo {new Date(room.created_at).toLocaleDateString('vi-VN')}</p>
          </div>
          <span>Mở phòng →</span>
        </a>
      ))}
    </div>
  )
}

export default function RoomList({ companyId }: { companyId?: string }) {
  const [selected, setSelected] = useState<Summary | null>(null)
  const [creating, setCreating] = useState(false)
  const [page, setPage] = useState(0)
  const [query, setQuery] = useState('')
  const [search, setSearch] = useState('')
  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">02 / VIRTUAL DATA ROOM</p>
          <h1>Phòng dữ liệu</h1>
          <p className="muted">
            Tài liệu theo thương vụ · Sáu nhóm thư mục · Giữ lại các phiên bản
          </p>
        </div>
        <button onClick={() => setCreating(!creating)}>
          {creating ? 'Đóng form tạo phòng' : 'Thêm phòng dữ liệu'}
        </button>
      </div>
      {companyId && (
        <p>
          Đang lọc theo doanh nghiệp. <a href="#/rooms">Xem tất cả phòng</a> ·{' '}
          <a href={`#/companies/${companyId}`}>Về hồ sơ</a>
        </p>
      )}
      {creating && (
        <>
          <div className="panel">
            <label htmlFor="room-company-search">
              Tìm doanh nghiệp để tạo phòng
            </label>
            <div className="actions">
              <input
                id="room-company-search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                maxLength={200}
              />
              <button type="button" onClick={() => setSearch(query)}>
                Tìm doanh nghiệp
              </button>
            </div>
            <CompanyMatches
              key={search}
              query={search}
              onChoose={setSelected}
            />
          </div>
          {selected && <NewRoom key={selected.id} company={selected} />}
        </>
      )}
      <Rooms key={`${companyId}:${page}`} companyId={companyId} page={page} />
      <div className="actions">
        <button
          className="secondary"
          disabled={!page}
          onClick={() => setPage(page - 1)}
        >
          Trang trước
        </button>
        <span>Trang {page + 1}</span>
        <button className="secondary" onClick={() => setPage(page + 1)}>
          Trang sau
        </button>
      </div>
    </section>
  )
}
