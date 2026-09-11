import { expect, test } from '@playwright/test'

test('browser connects through the frontend proxy to the real backend', async ({
  page,
}) => {
  const errors: string[] = []
  page.on('pageerror', (error) => errors.push(error.message))
  const responsePromise = page.waitForResponse(
    (response) =>
      response.url().endsWith('/api/v1/health') && response.status() === 200,
  )
  await page.goto('/#/health')
  const response = await responsePromise
  const health = await response.json()
  expect(health.status).toBe('ok')
  expect(health.scope).toBe('liveness')
  await expect(
    page.getByRole('heading', { name: 'Frontend đã kết nối backend' }),
  ).toBeVisible()
  await expect(
    page.getByText(health.service, { exact: true }).first(),
  ).toBeVisible()
  const retryResponse = page.waitForResponse(
    (candidate) =>
      candidate.url().endsWith('/api/v1/health') && candidate.status() === 200,
  )
  await page.getByRole('button', { name: /Kiểm tra lại/ }).click()
  await retryResponse
  await expect(
    page.getByRole('heading', { name: 'Frontend đã kết nối backend' }),
  ).toBeVisible()
  expect(errors).toEqual([])
  await page.screenshot({
    path: 'test-results/health-desktop.png',
    fullPage: true,
  })
  await page.setViewportSize({ width: 390, height: 844 })
  await expect(
    page.getByRole('heading', { name: 'Frontend đã kết nối backend' }),
  ).toBeVisible()
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true)
  await page.screenshot({
    path: 'test-results/health-mobile.png',
    fullPage: true,
  })
})
