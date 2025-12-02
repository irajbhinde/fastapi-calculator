// tests/e2e/tests/test_auth.spec.ts
import { test, expect } from "@playwright/test";

function uniqueEmail() {
  return `user_${Date.now()}_${Math.floor(Math.random() * 10000)}@example.com`;
}




test("positive: register with valid data", async ({ page }) => {
  await page.goto("/register");
  await page.waitForSelector("#reg-username");

  const email = uniqueEmail();

  await page.fill("#reg-username", "m13_user");
  await page.fill("#reg-email", email);
  await page.fill("#reg-password", "supersecret");
  await page.fill("#reg-confirm", "supersecret");

  await page.click("#register-form button[type=submit]");

  await expect(page.locator("#register-success")).toContainText(
    "Registration successful"
  );

  const token = await page.evaluate(() =>
    window.localStorage.getItem("access_token")
  );
  expect(token).not.toBeNull();
});

test("negative: register with short password", async ({ page }) => {
  await page.goto("/register");
  await page.waitForSelector("#reg-username");

  await page.fill("#reg-username", "shortpass");
  await page.fill("#reg-email", uniqueEmail());
  await page.fill("#reg-password", "123");
  await page.fill("#reg-confirm", "123");

  await page.click("#register-form button[type=submit]");

  await expect(page.locator("#register-error")).toContainText(
    "Password must be at least 8 characters"
  );
});

test("positive: login with valid credentials", async ({ page }) => {
//   page.on("console", (msg) => {
//   console.log("BROWSER LOG:", msg.text());
// });

  const email = uniqueEmail();
  const password = "supersecret";

  // Register user
  await page.goto("/register");
  await page.waitForSelector("#reg-username");
  await page.fill("#reg-username", "m13_login_user");
  await page.fill("#reg-email", email);
  await page.fill("#reg-password", password);
  await page.fill("#reg-confirm", password);
  await page.click("#register-form button[type=submit]");
  await expect(page.locator("#register-success")).toContainText(
    "Registration successful"
  );

  // Login
  await page.goto("/login");
  await page.waitForSelector("#login-identifier");
  await page.fill("#login-identifier", email);
  await page.fill("#login-password", password);
    await page.click("#login-form button[type=submit]");

await expect(page.locator("#login-success")).toContainText("")


  const token = await page.evaluate(() =>
    window.localStorage.getItem("access_token")
  );
  expect(token).not.toBeNull();
});

test("negative: login with wrong password", async ({ page }) => {
  const email = uniqueEmail();
  const password = "supersecret";

  // Register
  await page.goto("/register");
  await page.waitForSelector("#reg-username");
  await page.fill("#reg-username", "m13_wrongpass");
  await page.fill("#reg-email", email);
  await page.fill("#reg-password", password);
  await page.fill("#reg-confirm", password);
  await page.click("#register-form button[type=submit]");
  await expect(page.locator("#register-success")).toContainText(
    "Registration successful"
  );

  // Login wrong password
  await page.goto("/login");
  await page.waitForSelector("#login-identifier");
  await page.fill("#login-identifier", email);
  await page.fill("#login-password", "badpassword");
  await page.click("#login-form button[type=submit]");

  await expect(page.locator("#login-error")).toContainText(
    "Invalid credentials"
  );
});
