import { test, expect } from '@playwright/test';
test.beforeEach(async ({ request }) => { await request.post('/lab/reset'); });
test('starter console shows current system', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'HPE Lab Server Console' })).toBeVisible();
  await expect(page.locator('#system-name')).toHaveText('DL360-LAB-01');
  await expect(page.locator('#power')).toHaveText('On');
});
