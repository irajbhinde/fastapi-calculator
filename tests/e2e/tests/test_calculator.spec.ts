import { test, expect } from '@playwright/test';

test('calculator end-to-end operations', async ({ page }) => {
  await page.goto('/'); // works now because baseURL is set by root config
  const a = page.locator('#a');
  const b = page.locator('#b');
  const result = page.locator('#result');

  await a.fill('10');
  await b.fill('4');

  await page.click('#btn-add');
  await expect(result).toContainText('Result: 14');

  await page.click('#btn-subtract');
  await expect(result).toContainText('Result: 6');

  await page.click('#btn-multiply');
  await expect(result).toContainText('Result: 40');

  await page.click('#btn-divide');
  await expect(result).toContainText('Result: 2.5');
});
