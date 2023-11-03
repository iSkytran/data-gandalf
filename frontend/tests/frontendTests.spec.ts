import { test, expect, defineConfig, type Page } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('http://localhost:3000');
});

let topics: Array<string> = [];
fetch("http://localhost:3000/api/topics")
  .then((res) => res.json())
  .then((data) => {
    data.forEach((topic: string) => {
      topics.push(topic);
    });
  });

let datasets: Array<string[]> = [];
fetch("http://localhost:3000/api/datasets")
  .then((res) => res.json())
  .then((data) => {
    data.forEach((dataset: any) => {
      datasets.push([dataset.id, dataset.topic, dataset.title, dataset.description, dataset.licenses, dataset.tags]);    
    });
  });

test.describe('View Available Datasets', () => {
  test('Homepage should have title: Data Gandalf', async({page}) => {
    await expect(page).toHaveTitle('Data Gandalf');
  });

  test('Homepage should have filter bar with specified topics', async({page}) => {
    const filterBar = page.locator('_react=FilterBar');
    await expect(await filterBar.innerHTML()).toContain('Filter by Topic');

    await filterBar.click();

    const options = await filterBar.innerHTML();
    for (let i = 0; i < topics.length; i++) {
      await expect(options).toContain(topics[i]);
    }
  });

  test('Homepage should have a grid of available datasets', async({page}) => {
    const grid = page.locator('_react=Grid');

    for (let dataset of datasets) {
      const id = dataset[0];
      const title = dataset[2];

      const gridItem = await grid.locator('_react=GridItem[key = \'' + id + '\']').innerHTML();

      await expect(gridItem).toContain(title.replace('&', '&amp;'));
    }
  });
});

test.describe('Filter Available Datasets by Topic', () => {
  test('Page should have a grid of sports datasets', async({page}) => {
    const filterBar = page.locator('_react=FilterBar');
    await filterBar.click();
    
    const sportsLocators = await page.getByText('sports').all();
    const sportsTopic = sportsLocators[0];
    
    await sportsTopic.click();

    const grid = page.locator('_react=Grid');

    for (let dataset of datasets) {
      const id = dataset[0];
      const topic = dataset[1];

      if (topic === 'sports') {
        const gridItem = await grid.locator('_react=GridItem[key = \'' + id + '\']').innerHTML();

        await expect(gridItem).toContain('sports');
      }
    }
  });
});

test.describe('View Dataset from Homepage', () => {
  test('Dataset page should have appropriate dataset details displayed', async({page}) => {
    const grid = page.locator('_react=Grid');

    const dataset = datasets[0];
    const topic = dataset[1];
    const title = dataset[2];
    const description = dataset[3];
    const licenses:any = dataset[4];
    const tags:any = dataset[5];

    const gridItem = await grid.locator('_react=GridItem').first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(2000);

    const gridItemLarge = await page.locator('_react=GridItemLarge').innerHTML();

    await expect(gridItemLarge).toContain(title);
    await expect(gridItemLarge).toContain(topic);
    await expect(gridItemLarge).toContain(description);
    for (let license in licenses) {
      await expect(gridItemLarge).toContain(license);
    }
    for (let tag in tags) {
      await expect(gridItemLarge).toContain(tag);
    }
  });

  test('Dataset page should have recommendations displayed', async({page}) => {
    const grid = page.locator('_react=Grid');

    const dataset = datasets[0];
    const title = dataset[2];

    const gridItem = await grid.locator('_react=GridItem').first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(2000);

    const recommendationsGrid = page.locator('_react=Grid');
    const recommendations = await recommendationsGrid.locator('_react=GridItem').all();

    for (let i = 0; i < recommendations.length; i++) {
      const recommendationHTML = await recommendations[i].innerHTML();

      await expect(recommendationHTML).toContain('Similarity:');
    }
    
  });
});

test.describe('View Dataset from Filtered Results', () => {
  test('Dataset page should have appropriate dataset details displayed', async({page}) => {
    const filterBar = page.locator('_react=FilterBar');
    await filterBar.click();
    
    const sportsLocators = await page.getByText('sports').all();
    const sportsTopic = sportsLocators[0];
    
    await sportsTopic.click();

    const grid = page.locator('_react=Grid');

    const dataset = datasets[0];
    const topic = dataset[1];
    const title = dataset[2];
    const description = dataset[3];
    const licenses:any = dataset[4];
    const tags:any = dataset[5];

    const gridItem = await grid.locator('_react=GridItem').first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(2000);

    const gridItemLarge = await page.locator('_react=GridItemLarge').innerHTML();

    await expect(gridItemLarge).toContain(title);
    await expect(gridItemLarge).toContain(topic);
    await expect(gridItemLarge).toContain(description);
    for (let license in licenses) {
      await expect(gridItemLarge).toContain(license);
    }
    for (let tag in tags) {
      await expect(gridItemLarge).toContain(tag);
    }
  });

  test('Dataset page should have recommendations displayed', async({page}) => {
    const filterBar = page.locator('_react=FilterBar');
    await filterBar.click();
    
    const sportsLocators = await page.getByText('sports').all();
    const sportsTopic = sportsLocators[0];
    
    await sportsTopic.click();

    const grid = page.locator('_react=Grid');

    const dataset = datasets[0];
    const title = dataset[2];

    const gridItem = await grid.locator('_react=GridItem').first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(2000);

    const recommendationsGrid = page.locator('_react=Grid');
    const recommendations = await recommendationsGrid.locator('_react=GridItem').all();

    for (let i = 0; i < recommendations.length; i++) {
      const recommendationHTML = await recommendations[i].innerHTML();

      await expect(recommendationHTML).toContain('Similarity:');
    }
    
  });
});

test.describe('Rate Recommendation Exists', () => {
  
});

test.describe('Rate Recommendation as Good', () => {
  
});

test.describe('Rate Recommendation as Bad', () => {
  
});