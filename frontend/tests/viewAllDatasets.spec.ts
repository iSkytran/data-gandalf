import { test, expect, defineConfig, type Page } from '@playwright/test';

export default defineConfig({
  // Run your local dev server before starting the tests
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: 'http://localhost:3000'
  }
});

test.beforeEach(async ({ page }) => {
  await page.goto('http://localhost:3000');
});

const TOPICS = [
  'sports',
  'academics',
  'realty',
  'finance',
  'health'
];

test.describe('View All Datasets', () => {
  test('Homepage should have Data Gandalf header', async({page}) => {
    await expect(page).toHaveTitle('Data Gandalf');
  });

  test('Homepage should have filter bar with specified topics', async({page}) => {
    const filterBar = page.getByPlaceholder('Filter By Topic');

    for (let i = 0; i < TOPICS.length; i++) {
      await expect(filterBar).toHaveAttribute('options', TOPICS[i]);
    }
  });

  test('Homepage should have a grid of available datasets', async({page}) => {
    
  });
});