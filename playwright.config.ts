import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: 'tests/e2e/tests',
  timeout: 30_000,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:8000',
    trace: 'on-first-retry',
    headless: true,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
