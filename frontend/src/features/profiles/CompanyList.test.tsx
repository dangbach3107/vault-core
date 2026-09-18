import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { expect, test, vi } from 'vitest'
import CompanyList from './CompanyList'
import type { Summary } from '../../api/workspace'

const mockCompanies: Summary[] = [
  {
    id: '11111111-1111-1111-1111-111111111111',
    alias: 'VAULT-TEST001',
    name: 'Công ty Cổ phần Công nghệ ABC',
    tax_id: '0101234567',
    updated_at: '2026-09-17T00:00:00Z',
    sector: 'SOFTWARE',
    region: 'NORTH',
    revenue_band: '200–dưới 500 tỷ',
    employee_band: '50–199',
    deal_type: 'PRIMARY',
    stake_percent: '30',
    verified_facts_count: 14,
    total_facts_count: 15,
  },
  {
    id: '22222222-2222-2222-2222-222222222222',
    alias: 'VAULT-TEST002',
    name: 'Công ty TNHH Cơ khí Chính xác XYZ',
    tax_id: '0309876543',
    updated_at: '2026-09-17T00:00:00Z',
    sector: 'MANUFACTURING',
    region: 'SOUTH',
    revenue_band: '50–dưới 100 tỷ',
    employee_band: '200–999',
    deal_type: 'SECONDARY',
    stake_percent: '100',
    verified_facts_count: 12,
    total_facts_count: 15,
  },
]

test('renders buyer discovery mode with deal cards and filters by sector', async () => {
  const user = userEvent.setup()
  const fetchMock = vi
    .fn()
    .mockResolvedValue(new Response(JSON.stringify(mockCompanies)))
  vi.stubGlobal('fetch', fetchMock)

  render(<CompanyList />)

  // Wait for companies to load
  expect(await screen.findByText('VAULT-TEST001')).toBeVisible()
  expect(screen.getByText('VAULT-TEST002')).toBeVisible()
  // In Buyer mode, real company names should NOT be displayed
  expect(screen.queryByText('Công ty Cổ phần Công nghệ ABC')).toBeNull()

  // Filter by sector: SOFTWARE
  await user.selectOptions(
    screen.getByLabelText('Ngành mục tiêu (Field/Sector)'),
    'SOFTWARE',
  )
  expect(screen.getByText('VAULT-TEST001')).toBeVisible()
  expect(screen.queryByText('VAULT-TEST002')).toBeNull()

  // Reset filters
  await user.click(screen.getByRole('button', { name: /Đặt lại bộ lọc/ }))
  expect(screen.getByText('VAULT-TEST002')).toBeVisible()

  // Switch to Admin mode
  await user.click(screen.getByRole('button', { name: /Chế độ Quản trị viên/ }))
  expect(screen.getByText('Công ty Cổ phần Công nghệ ABC')).toBeVisible()
  expect(screen.getByText(/0101234567/)).toBeVisible()
})
