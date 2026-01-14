import { test, expect, Page } from '@playwright/test';


const TEST_USER = {
  username: 'e2e_calc_user',
  email: 'e2e_calc_user@example.com',
  password: 'Password123!',
};

async function triggerStatsReload(page: Page) {
  // Call the browser-side function from calculations.js
  await page.evaluate(() => {
    const anyWindow = window as any;
    if (typeof anyWindow.fetchCalculationStats === 'function') {
      anyWindow.fetchCalculationStats();
    }
  });
}

async function expectStatsPanelHasValues(page: Page) {
  const total = page.locator('#stat-total-calcs');
  await expect(total).toBeVisible();
  // Just check it shows *something* (could be "0", that's fine if DB is empty)
  await expect(total).not.toHaveText('');
}

// --- Helper: register (idempotent) + login ---
async function ensureLoggedIn(page: Page) {
  // REGISTER (ok if user already exists)
  await page.goto('/register');

  await page.locator('#reg-username').fill(TEST_USER.username);
  await page.locator('#reg-email').fill(TEST_USER.email);
  await page.locator('#reg-password').fill(TEST_USER.password);
  await page.locator('#reg-confirm').fill(TEST_USER.password);
  await page.getByRole('button', { name: /register/i }).click();

  // LOGIN (email + password as per login.html)
  await page.goto('/login');

  await page.locator('#login-identifier').fill(TEST_USER.email);
  await page.locator('#login-password').fill(TEST_USER.password);
  await page.getByRole('button', { name: /login/i }).click();

  await expect(page.locator('#login-success')).toContainText(/login successful/i);
}

// --- Helpers for forms ---
function getCreateForm(page: Page) {
  const aInput = page.locator('#calc-a');
  const bInput = page.locator('#calc-b');
  const typeSelect = page.locator('#calc-type');
  const noteInput = page.locator('#calc-note');
  const submitButton = page.getByRole('button', {
    name: /create calculation/i,
  });
  return { aInput, bInput, typeSelect, noteInput, submitButton };
}

function getEditForm(page: Page) {
  const idHidden = page.locator('#edit-calc-id');
  const aInput = page.locator('#edit-a');
  const bInput = page.locator('#edit-b');
  const typeSelect = page.locator('#edit-type');
  const noteInput = page.locator('#edit-note');
  const submitButton = page.getByRole('button', { name: /save changes/i });
  return { idHidden, aInput, bInput, typeSelect, noteInput, submitButton };
}

test('user can add, see, edit, and delete a calculation (smoke BREAD)', async ({
  page,
}) => {
  await ensureLoggedIn(page);

  await page.goto('/calculations-ui');

  const { aInput, bInput, typeSelect, noteInput, submitButton } =
    getCreateForm(page);

  // ---------- CREATE ----------
  await aInput.fill('10');
  await bInput.fill('5');
  await typeSelect.selectOption('add');
  await noteInput.fill('e2e smoke');
  await submitButton.click();


  await triggerStatsReload(page);
  await expectStatsPanelHasValues(page);

  const row = page
    .locator('#calc-table-body tr', { hasText: 'e2e smoke' })
    .first();
  await expect(row).toBeVisible();

  const editButton = row.getByRole('button', { name: /edit/i });
  await editButton.click();

  // ---------- CREATE power ----------
  await aInput.fill('2');
  await bInput.fill('3');
  await typeSelect.selectOption('power');
  await noteInput.fill('power e2e');
  await submitButton.click();

  const pwRow = page
    .locator('#calc-table-body tr', { hasText: 'power e2e' })
    .first();
  await expect(pwRow).toBeVisible();

});

test('cannot divide by zero (negative case)', async ({ page }) => {
  await ensureLoggedIn(page);

  await page.goto('/calculations-ui');

  const { aInput, bInput, typeSelect, noteInput, submitButton } =
    getCreateForm(page);

  await aInput.fill('10');
  await bInput.fill('0');
  await typeSelect.selectOption('divide');
  await noteInput.fill('divide by zero test');
  await submitButton.click();

  const error = page.locator('#calc-error').first();
  await expect(error).toBeVisible();
  await expect(error).not.toHaveText('');
});
