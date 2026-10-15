import { expect, test } from '@playwright/test'
import { loginAs } from './auth'

test('create, persist, edit and preview a company through the real API and PostgreSQL', async ({
  page,
}) => {
  const name = `Doanh nghiệp giả lập ${Date.now()}`
  const errors: string[] = []
  page.on('pageerror', (error) => errors.push(error.message))
  await loginAs(page)
  await page.goto('/#/companies')
  await page.getByRole('link', { name: /Tạo hồ sơ mới/ }).click()
  await page.getByLabel('Tên doanh nghiệp *', { exact: true }).fill(name)
  await page
    .getByLabel('Mã số thuế', { exact: true })
    .fill(`TEST-${Date.now()}`)
  await page
    .getByLabel('Ngành hoạt động', { exact: true })
    .selectOption('SOFTWARE')
  await page.getByLabel('Vùng hoạt động', { exact: true }).selectOption('SOUTH')
  await page.getByLabel('Địa chỉ', { exact: true }).fill('123 Địa chỉ riêng tư')
  await page
    .getByLabel('Doanh thu VND — dòng 1', { exact: true })
    .fill('25000000000.01')
  await page.getByRole('button', { name: 'Lưu bản nháp', exact: true }).click()
  await expect(
    page.getByRole('status').filter({ hasText: 'Đã lưu hồ sơ.' }),
  ).toBeVisible()
  await expect(page.getByRole('heading', { name, exact: true })).toBeVisible()
  await page.reload()
  await expect(page.getByRole('heading', { name, exact: true })).toBeVisible()
  await page.getByRole('button', { name: 'Xem trước công bố' }).first().click()
  await page.getByRole('button', { name: 'Lớp 1 · Ẩn danh' }).click()
  const layer1 = page.getByLabel('Nội dung lớp 1')
  await expect(layer1.getByText('20–dưới 50 tỷ', { exact: true })).toBeVisible()
  await expect(layer1).not.toContainText(name)
  await expect(layer1).not.toContainText('123 Địa chỉ riêng tư')
  await expect(layer1).not.toContainText('25000000000')
  await page.getByRole('link', { name: 'Chỉnh sửa' }).first().click()
  await page
    .getByLabel('Tên doanh nghiệp *', { exact: true })
    .fill(`${name} đã sửa`)
  await page.getByRole('button', { name: 'Lưu bản nháp', exact: true }).click()
  await expect(
    page.getByRole('heading', { name: `${name} đã sửa`, exact: true }),
  ).toBeVisible()
  await page.getByRole('button', { name: 'Xem trước công bố' }).first().click()
  await page.getByRole('button', { name: 'Lớp 3 · Hạn chế' }).click()
  await expect(page.getByLabel('Nội dung lớp 3')).toContainText(
    'Cổ đông & sở hữu',
  )
  await page.screenshot({
    path: 'test-results/profile-desktop.png',
    fullPage: true,
  })
  await page.setViewportSize({ width: 390, height: 844 })
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true)
  await page.screenshot({
    path: 'test-results/profile-mobile.png',
    fullPage: true,
  })
  await page.setViewportSize({ width: 1280, height: 900 })
  await page.goto('/#/companies')
  await page.getByRole('button', { name: /Danh sách quản trị/ }).click()
  await page.getByLabel('Tìm tên hoặc MST').fill(name)
  await expect(
    page.getByRole('heading', { name: `${name} đã sửa`, exact: true }),
  ).toBeVisible()
  expect(errors).toEqual([])
})
