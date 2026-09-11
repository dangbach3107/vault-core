import { useState } from 'react'
import type { Summary } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'

function Results({ query, page }: { query: string; page: number }) {
  const result = useLoad<Summary[]>(
    `/companies?q=${encodeURIComponent(query)}&offset=${page * 20}&limit=20`,
  )
  if (!result.data) return <LoadState {...result} />
  return (
    <>
      <p className="muted">{result.data.length} hồ sơ trên trang này</p>
      {result.data.length === 0 ? (
        <div className="empty panel">
          Chưa có hồ sơ phù hợp. Bạn có thể tạo một hồ sơ mới.
        </div>
      ) : (
        <div className="record-list">
          {result.data.map((row) => (
            <a
              className="record panel"
              key={row.id}
              href={`#/companies/${row.id}`}
            >
              <div>
                <span className="eyebrow">{row.alias}</span>
                <h2>{row.name}</h2>
                <p>MST: {row.tax_id || 'Chưa cung cấp'}</p>
              </div>
              <span>Xem hồ sơ →</span>
            </a>
          ))}
        </div>
      )}
    </>
  )
}

export default function CompanyList() {
  const [input, setInput] = useState('')
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(0)
  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">01 / TRUST PROFILE</p>
          <h1>Hồ sơ doanh nghiệp</h1>
          <p className="muted">Thông tin, nguồn dữ kiện và ba lớp hồ sơ.</p>
        </div>
        <a className="button-link" href="#/companies/new">
          Tạo hồ sơ
        </a>
      </div>
      <form
        className="search"
        onSubmit={(e) => {
          e.preventDefault()
          setQuery(input)
          setPage(0)
        }}
      >
        <label htmlFor="company-search">Tìm tên hoặc mã số thuế</label>
        <div className="actions">
          <input
            id="company-search"
            value={input}
            maxLength={200}
            onChange={(e) => setInput(e.target.value)}
          />
          <button>Tìm kiếm</button>
        </div>
      </form>
      <Results key={`${query}:${page}`} query={query} page={page} />
      <div className="actions">
        <button
          className="secondary"
          disabled={page === 0}
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
