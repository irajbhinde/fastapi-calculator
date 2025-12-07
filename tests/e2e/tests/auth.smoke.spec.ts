// tests/e2e/tests/auth.smoke.spec.ts
import { test, expect } from '@playwright/test';

const TEST_USER = {
  username: 'e2e_user',
  email: 'e2e_user@example.com',
  password: 'Password123!',
};

test('user can register and then login (happy path)', async ({ page }) => {
  // ---------- REGISTER ----------
  await page.goto('/register');

  // Use the exact IDs from register.html
  await page.locator('#reg-username').fill(TEST_USER.username);
  await page.locator('#reg-email').fill(TEST_USER.email);
  await page.locator('#reg-password').fill(TEST_USER.password);
  await page.locator('#reg-confirm').fill(TEST_USER.password);

  await page.getByRole('button', { name: /register/i }).click();

  // Message element from register.html
  await expect(page.locator('#register-success')).toContainText(
    /registration successful/i,
  );

  // ---------- LOGIN ----------
  await page.goto('/login');

  // Login uses *email* as identifier (login-identifier + login-password)
  await page.locator('#login-identifier').fill(TEST_USER.email);
  await page.locator('#login-password').fill(TEST_USER.password);

  await page.getByRole('button', { name: /login/i }).click();

  await expect(page.locator('#login-success')).toContainText(/login successful/i);
});

test('login fails with wrong password (negative)', async ({ page }) => {
  // ---------- Ensure the user exists ----------
  await page.goto('/register');

  await page.locator('#reg-username').fill('e2e_user_negative');
  await page.locator('#reg-email').fill('e2e_user_negative@example.com');
  await page.locator('#reg-password').fill(TEST_USER.password);
  await page.locator('#reg-confirm').fill(TEST_USER.password);

  await page.getByRole('button', { name: /register/i }).click();
  // We don't care if it's "already exists" here, just that the user exists.

  // ---------- Try to login with WRONG password ----------
  await page.goto('/login');

  await page.locator('#login-identifier').fill('e2e_user_negative@example.com');
  await page.locator('#login-password').fill('WrongPassword!');

  await page.getByRole('button', { name: /login/i }).click();

  // From login.html + auth.js spec: "Invalid credentials"
  await expect(page.locator('#login-error')).toContainText(/invalid credentials/i);
});
