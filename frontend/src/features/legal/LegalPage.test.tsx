import { render, screen } from '@testing-library/react'
import { expect, test } from 'vitest'
import LegalPage, { LegalLinks } from './LegalPage'
import { legalPaths } from './paths'

test('maps the public legal routes', () => {
  expect(legalPaths['/terms']).toBe('terms')
  expect(legalPaths['/privacy']).toBe('privacy')
  expect(legalPaths['/contact']).toBe('contact')
})

test('terms page shows its sections and a way home', () => {
  render(<LegalPage kind="terms" />)
  expect(
    screen.getByRole('heading', { level: 1, name: 'Điều khoản sử dụng' }),
  ).toBeVisible()
  expect(
    screen.getByRole('heading', { name: /Quyền truy cập theo từng lớp/ }),
  ).toBeVisible()
  expect(screen.getByRole('link', { name: /Trang chủ/ })).toHaveAttribute(
    'href',
    '#/welcome',
  )
})

test('privacy page names the infrastructure providers', () => {
  render(<LegalPage kind="privacy" />)
  expect(
    screen.getByRole('heading', { level: 1, name: 'Chính sách bảo mật' }),
  ).toBeVisible()
  expect(screen.getByText(/Render/)).toBeVisible()
})

test('contact page works without a configured email', () => {
  render(<LegalPage kind="contact" />)
  expect(
    screen.getByRole('heading', { level: 1, name: 'Liên hệ' }),
  ).toBeVisible()
  expect(screen.getByText(/quản trị viên VAULT/)).toBeVisible()
})

test('legal links point at the three pages', () => {
  render(<LegalLinks />)
  expect(
    screen.getByRole('link', { name: 'Điều khoản sử dụng' }),
  ).toHaveAttribute('href', '#/terms')
  expect(
    screen.getByRole('link', { name: 'Chính sách bảo mật' }),
  ).toHaveAttribute('href', '#/privacy')
  expect(screen.getByRole('link', { name: 'Liên hệ' })).toHaveAttribute(
    'href',
    '#/contact',
  )
})
