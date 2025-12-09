// tests/e2e/tests/stats.smoke.spec.ts
import { test, expect, Page } from '@playwright/test';

const STATS_USER = {
  username: 'stats_user',
  email: 'stats_user@example.com',
  password: 'Password123!',
};

// Reuse the same register/login pattern as auth.smoke.spec.ts
async function ensureLoggedIn(page: Page) {
  // --- Register (ok if already exists) ---
  await page.goto('/register');

  await page.locator('#reg-username').fill(STATS_USER.username);
  await page.locator('#reg-email').fill(STATS_USER.email);
  await page.locator('#reg-password').fill(STATS_USER.password);
  await page.locator('#reg-confirm').fill(STATS_USER.password);

  await page.getByRole('button', { name: /register/i }).click();
  // We don't assert here; user might already exist.

  // --- Login ---
  await page.goto('/login');

  await page.locator('#login-identifier').fill(STATS_USER.email);
  await page.locator('#login-password').fill(STATS_USER.password);
  await page.getByRole('button', { name: /login/i }).click();

  await expect(page.locator('#login-success')).toContainText(/login successful/i);
}

function getCreateForm(page: Page) {
  return {
    aInput: page.locator('#calc-a'),
    bInput: page.locator('#calc-b'),
    typeSelect: page.locator('#calc-type'),
    noteInput: page.locator('#calc-note'),
    submitButton: page.getByRole('button', { name: /create calculation/i }),
  };
}

test('stats panel loads and displays all fields', async ({ page }) => {
  await ensureLoggedIn(page);

  await page.goto('/calculations-ui');

  const statIds = [
    '#stat-total-calcs',
    '#stat-add-count',
    '#stat-subtract-count',
    '#stat-multiply-count',
    '#stat-divide-count',
    '#stat-avg-a',
    '#stat-avg-b',
    '#stat-avg-result',
  ];

  for (const id of statIds) {
    await expect(page.locator(id).first()).toBeVisible();
  }
});

test('stats update after adding a calculation', async ({ page }) => {
  await ensureLoggedIn(page);
  await page.goto('/calculations-ui');

  const totalBeforeText = await page.locator('#stat-total-calcs').first().innerText();
  const totalBefore = parseInt(totalBeforeText || '0', 10);

  const { aInput, bInput, typeSelect, noteInput, submitButton } = getCreateForm(page);

  await aInput.fill('10');
  await bInput.fill('20');
  await typeSelect.selectOption('add');
  await noteInput.fill('stats test');
  await submitButton.click();

  await expect(
    page.locator('#calc-table-body tr', { hasText: 'stats test' }).first(),
  ).toBeVisible();

  // Give the stats JS a moment to refresh
  await page.waitForTimeout(300);

  const totalAfterText = await page.locator('#stat-total-calcs').first().innerText();
  const totalAfter = parseInt(totalAfterText || '0', 10);

  expect(totalAfter).toBeGreaterThanOrEqual(totalBefore + 1);
});

test('stats failure is handled gracefully', async ({ page }) => {
  await ensureLoggedIn(page);

  // Force the stats API to fail
  await page.route('/api/calculations/stats', (route) =>
    route.fulfill({
      status: 500,
      body: JSON.stringify({ detail: 'Forced test error' }),
    }),
  );

  await page.goto('/calculations-ui');

  // calculations.js should show a friendly error when stats fail
  const error = page.locator('#calc-error').first();
  await expect(error).toContainText(/failed to load stats/i);
});
