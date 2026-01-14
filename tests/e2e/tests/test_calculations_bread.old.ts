import { test, expect } from "@playwright/test";

function uniqueEmail() {
  return `bread_${Date.now()}_${Math.floor(Math.random() * 10000)}@example.com`;
}

interface RegisterResult {
    email: string;
    password: string;
}

async function registerUser(page: import("@playwright/test").Page, username: string): Promise<RegisterResult> {
    const email = uniqueEmail();
    const password = "supersecret";

    await page.goto("/register");
    await page.fill("#reg-username", username);
    await page.fill("#reg-email", email);
    await page.fill("#reg-password", password);
    await page.fill("#reg-confirm", password);
    await page.click("#register-form button[type=submit]");

    // This text comes from auth.js
    await expect(page.locator("#register-success")).toContainText(
        "Registration successful"
    );

    // Sanity check that token is stored
    const token = await page.evaluate(() =>
        window.localStorage.getItem("access_token")
    );
    expect(token).not.toBeNull();

    return { email, password };
}

test.describe("Calculations BREAD UI", () => {
  test("positive: add, browse, read, edit, delete calculation", async ({
    page,
  }) => {
    // 1. Register user and get JWT stored
    await registerUser(page, "bread_positive");

    // 2. Go to BREAD UI
    await page.goto("/calculations-ui");

    // --- ADD / CREATE ---
    await page.fill("#calc-a", "2");
    await page.fill("#calc-b", "3");
    await page.selectOption("#calc-type", "add");
    await page.fill("#calc-note", "first calc");
    await page.click("#create-calc-form button[type=submit]");

    await expect(page.locator("#calc-success")).toContainText(
      "Calculation created successfully"
    );

    // --- BROWSE / LIST ---
    const rows = page.locator("#calc-table-body tr");
    await expect(rows).toHaveCount(1);

    // --- READ / VIEW ---
    await rows.nth(0).locator(".view-btn").click();
    await expect(page.locator("#calc-details")).toContainText("first calc");

    // --- EDIT / UPDATE ---
    await rows.nth(0).locator(".edit-btn").click();
    await page.fill("#edit-note", "updated note");
    await page.click("#edit-calc-form button[type=submit]");

    await expect(page.locator("#calc-success")).toContainText(
      "updated successfully"
    );

    // Reload and confirm updated note appears in table
    await page.click("#reload-calcs-btn");
    const updatedRow = page.locator("#calc-table-body tr").nth(0);
    await expect(updatedRow).toContainText("updated note");

    // --- DELETE ---
    page.once("dialog", (dialog) => dialog.accept());
    await updatedRow.locator(".delete-btn").click();

    await expect(page.locator("#calc-success")).toContainText("deleted");

    // After delete we should see "No calculations yet." row
    await expect(page.locator("#calc-table-body")).toContainText(
      "No calculations yet."
    );
  });

  test("negative: unauthorized + invalid input handling", async ({ page }) => {
    // Make sure no token exists
    await page.goto("/login");
    await page.evaluate(() => window.localStorage.clear());

    // 1. Unauthorized access to BREAD page
    await page.goto("/calculations-ui");

    // Message set in calculations.js when no token
    await expect(page.locator("#calc-error")).toContainText(
      "not logged in"
    );

    // Create button should be disabled when unauthorized
    await expect(
      page.locator("#create-calc-form button[type=submit]")
    ).toBeDisabled();

    // 2. Register to get a valid token
    await registerUser(page, "bread_negative");

    // Back to BREAD page with token present
    await page.goto("/calculations-ui");

    // 3. Invalid numeric input (client-side validation)
    await page.fill("#calc-a", "not-a-number");
    await page.fill("#calc-b", "5");
    await page.selectOption("#calc-type", "add");
    await page.click("#create-calc-form button[type=submit]");

    // Error message defined in calculations.js
    await expect(page.locator("#calc-error")).toContainText(
      "valid numeric values"
    );
  });
});
