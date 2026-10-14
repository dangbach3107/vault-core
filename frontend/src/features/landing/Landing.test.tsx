import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
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

test('embeds the intro video muted with a poster', () => {
  render(<Landing signedIn={false} />)
  const video = screen.getByLabelText('Video giới thiệu VAULT')
  expect(video.getAttribute('src')).toMatch(/^\/vault-intro(-1080)?\.mp4$/)
  expect(video).toHaveAttribute('poster', '/vault-intro-poster.jpg')
  expect((video as HTMLVideoElement).muted).toBe(true)
})

test('video starts muted and the sound button toggles audio', async () => {
  const user = userEvent.setup()
  render(<Landing signedIn={false} />)
  const video = screen.getByLabelText(
    'Video giới thiệu VAULT',
  ) as HTMLVideoElement
  expect(video.muted).toBe(true)
  await user.click(screen.getByRole('button', { name: 'Bật âm thanh' }))
  expect(video.muted).toBe(false)
  expect(screen.getByRole('button', { name: 'Tắt âm thanh' })).toBeVisible()
  await user.click(screen.getByRole('button', { name: 'Tắt âm thanh' }))
  expect(video.muted).toBe(true)
})
