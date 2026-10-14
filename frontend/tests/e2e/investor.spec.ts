import { expect, test } from '@playwright/test'
import { loginAs } from './auth'

test('role login opens a clear persisted deal workspace on desktop and mobile', async ({
  page,
}) => {
  await loginAs(page, 'admin')
  await expect(
    page.getByRole('heading', { name: /một thương vụ mẫu/ }),
  ).toBeVisible()
  await expect(page.getByText(/Role hiện tại: VAULT_ADMIN/)).toBeVisible()
  await expect(page.getByRole('button', { name: 'Hoàn tất mẫu' })).toBeEnabled()
  await expect(page.getByText(/0% hoàn tất/)).toBeVisible()
  await page.screenshot({
    path: 'test-results/investor-red-desktop.png',
    fullPage: true,
  })
  await page.setViewportSize({ width: 390, height: 844 })
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true)
  await expect(
    page.getByRole('heading', { name: /một thương vụ mẫu/ }),
  ).toBeVisible()
  await page.screenshot({
    path: 'test-results/investor-red-mobile.png',
    fullPage: true,
  })
})
