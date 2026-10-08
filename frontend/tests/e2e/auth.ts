import type { APIRequestContext, Page } from '@playwright/test'

export async function loginAs(page: Page, username = 'admin') {
  await page.goto('/#/investor-mvp')
  await page.getByLabel('Vai trò').selectOption(username)
  await page.getByLabel('Mật khẩu demo').fill('vault-demo')
  await page.getByRole('button', { name: 'Đăng nhập', exact: true }).click()
  await page.getByText(`· ${username}`, { exact: false }).first().waitFor()
}

export async function authHeaders(
  request: APIRequestContext,
  username = 'admin',
) {
  const response = await request.post('/api/v1/auth/login', {
    data: { username, password: 'vault-demo' },
  })
  const body = (await response.json()) as { access_token: string }
  return { Authorization: `Bearer ${body.access_token}` }
}
