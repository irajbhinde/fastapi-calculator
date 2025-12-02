// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e/tests",
  timeout: 30_000,

  use: {
    baseURL: "http://127.0.0.1:8000",
    headless: true,
  },

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],

  webServer: {
    // ✅ IMPORTANT: point to app.main:app, not root main.py
    command: "uvicorn app.main:app --host 127.0.0.1 --port 8000",
    url: "http://127.0.0.1:8000/health",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
