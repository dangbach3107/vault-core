import type { APIRequestContext, Page } from '@playwright/test'

const ACCOUNT_NAMES: Record<string, string> = {
  buyer: 'Buyer',
  buyer2: 'Buyer 2',
  seller: 'Seller',
  seller2: 'Seller 2',
  admin: 'VAULT Admin',
  legal: 'Legal',
  tech: 'Tech DD',
  finance: 'Finance',
}

export async function loginAs(page: Page, username = 'admin') {
  await page.goto('/#/vault')
  await page.evaluate(() => localStorage.removeItem('vault.auth'))
  await page.reload()
  await page
    .locator(`.lg-role`)
    .filter({ hasText: ACCOUNT_NAMES[username] })
    .first()
    .click()
  await page.getByPlaceholder('Nhập mật khẩu').fill('vault-demo')
  await page.getByRole('button', { name: /Đăng nhập/ }).click()
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
