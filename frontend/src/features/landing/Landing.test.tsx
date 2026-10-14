import { render, screen } from '@testing-library/react'
import { expect, test } from 'vitest'
import Landing from './Landing'

test('trial buttons lead to the app login route', () => {
  render(<Landing signedIn={false} />)
  const trials = screen.getAllByRole('link', { name: /Dùng thử ngay/ })
  expect(trials.length).toBeGreaterThan(0)
  for (const link of trials) expect(link).toHaveAttribute('href', '#/vault')
  expect(screen.getByRole('link', { name: 'Đăng nhập' })).toHaveAttribute(
    'href',
    '#/vault',
  )
})

test('signed-in users are offered the app instead of login', () => {
  render(<Landing signedIn />)
  expect(screen.queryByRole('link', { name: 'Đăng nhập' })).toBeNull()
  expect(
    screen.getAllByRole('link', { name: /Vào ứng dụng/ }).length,
  ).toBeGreaterThan(0)
})

test('shows the three disclosure layers', () => {
  render(<Landing signedIn={false} />)
  expect(screen.getByRole('tab', { name: /L1/ })).toBeVisible()
  expect(screen.getByRole('tab', { name: /L3/ })).toBeVisible()
})
