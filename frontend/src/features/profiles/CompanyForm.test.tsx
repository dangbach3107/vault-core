import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, test, vi } from 'vitest'
import CompanyForm from './CompanyForm'
import FactEditor from './FactEditor'
import { blankFact } from './fields'

test('keeps draft input after a save failure and allows retry', async () => {
  const user = userEvent.setup()
  const fetchMock = vi.fn().mockResolvedValue(
    new Response(JSON.stringify({ detail: 'Database unavailable' }), {
      status: 503,
    }),
  )
  vi.stubGlobal('fetch', fetchMock)
  render(<CompanyForm />)
  await user.type(screen.getByLabelText('Tên doanh nghiệp *'), 'Công ty mẫu')
  await user.click(screen.getByRole('button', { name: 'Lưu hồ sơ' }))
  expect(await screen.findByRole('alert')).toHaveTextContent(
    'Database unavailable',
  )
  expect(screen.getByLabelText('Tên doanh nghiệp *')).toHaveValue('Công ty mẫu')
  expect(screen.getByRole('button', { name: 'Lưu hồ sơ' })).toBeEnabled()
  const body = JSON.parse(fetchMock.mock.calls[0][1].body)
  expect(body.company_name.value).toBe('Công ty mẫu')
  expect(body.financials[0].revenue_vnd.value).toBeNull()
})

test('editing a reviewed fact resets its review label and reviewer', async () => {
  const user = userEvent.setup()
  const onChange = vi.fn()
  render(
    <FactEditor
      label="Tên"
      fact={{
        ...blankFact(),
        value: 'Old',
        verification: 'DOCUMENT_VERIFIED',
        reviewed_by: 'Reviewer',
        reviewed_on: '2025-01-01',
      }}
      onChange={onChange}
    />,
  )
  await user.type(screen.getByLabelText('Tên'), 'X')
  expect(onChange).toHaveBeenLastCalledWith(
    expect.objectContaining({
      value: 'OldX',
      verification: 'SELF_DECLARED',
      reviewed_by: '',
      reviewed_on: null,
    }),
  )
})

test('shows the three verification labels for each fact', async () => {
  const user = userEvent.setup()
  render(
    <FactEditor
      label="Tên"
      fact={{ ...blankFact(), value: 'Example' }}
      onChange={vi.fn()}
    />,
  )
  await user.click(screen.getByText(/Nguồn & xác minh/))
  expect(
    within(screen.getByLabelText('Nhãn xác minh'))
      .getAllByRole('option')
      .map((option) => option.textContent),
  ).toEqual(['Tự khai', 'Đã đối chiếu', 'Bên thứ ba xác nhận'])
})
