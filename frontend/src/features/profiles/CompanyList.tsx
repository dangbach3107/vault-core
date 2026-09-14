import { useState } from 'react'
import type { Room, Summary } from '../../api/workspace'
import { LoadState } from '../../components/LoadState'
import { useLoad } from '../../hooks/useLoad'

function formatWhen(iso: string) {
  return new Date(iso).toLocaleString('vi-VN')
}

export default function CompanyList() {
  const [input, setInput] = useState('')
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(0)
  const listed = useLoad<Summary[]>(
    `/companies?q=${encodeURIComponent(query)}&offset=${page * 20}&limit=20`,
  )
  const rooms = useLoad<Room[]>('/rooms?limit=20')
  const rows = listed.data
  return (
    <section>
      <div className="page-heading">
        <div>
          <p className="eyebrow">01 / TRUST PROFILE</p>
          <p className="lede">
            Thông tin có nguồn, nhãn xác minh theo từng dữ kiện và ba lớp xem
            trước nội bộ.
          </p>
        </div>
        <a className="button-link" href="#/companies/new">
          Thêm doanh nghiệp
        </a>
      </div>
      <div className="stat-row">
        <div className="stat">
          <span>Hồ sơ trên trang này</span>
          <strong>{rows ? rows.length : '—'}</strong>
        </div>
        <div className="stat">
          <span>Phòng dữ liệu (tối đa 20)</span>
          <strong>{rooms.data ? rooms.data.length : '—'}</strong>
        </div>
      </div>
      <form
        className="search panel"
        onSubmit={(e) => {
          e.preventDefault()
          setQuery(input)
          setPage(0)
        }}
      >
        <div className="filter-bar">
          <label htmlFor="company-search">
            Tìm tên hoặc mã số thuế
            <input
              id="company-search"
              value={input}
              maxLength={200}
              onChange={(e) => setInput(e.target.value)}
            />
          </label>
          <button>Tìm kiếm</button>
        </div>
      </form>
      {!rows ? (
        <LoadState {...listed} />
      ) : (
        <>
          <p className="muted">
            {rows.length} hồ sơ trên trang này
            {query ? ` · từ khóa “${query}”` : ''}
          </p>
          {rows.length === 0 ? (
            <div className="empty panel">
              {query
                ? 'Không tìm thấy hồ sơ phù hợp. Thử từ khóa khác hoặc xóa bộ lọc.'
                : 'Chưa có hồ sơ. Chọn “Thêm doanh nghiệp” để tạo bản nháp.'}
            </div>
          ) : (
            <div className="table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Tên doanh nghiệp</th>
                    <th>Mã hồ sơ</th>
                    <th>Mã số thuế</th>
                    <th>Cập nhật</th>
                    <th>Hành động</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row) => (
                    <tr key={row.id}>
                      <td>
                        <h2>{row.name}</h2>
                      </td>
                      <td>{row.alias}</td>
                      <td>{row.tax_id || 'Chưa cung cấp'}</td>
                      <td>{formatWhen(row.updated_at)}</td>
                      <td>
                        <div className="row-actions">
                          <a href={`#/companies/${row.id}`}>Xem chi tiết</a>
                          <a href={`#/companies/${row.id}/edit`}>Chỉnh sửa</a>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
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
