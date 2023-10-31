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

let datasets: Array<string> = [];
fetch("http://localhost:3000/api/datasets")
  .then((res) => res.json())
  .then((data) => {
    data.forEach((dataset: any) => {
      datasets.push(dataset.id + ' ' + dataset.topic + ' ' + dataset.title);      
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
    
    for (let i = 0; i < datasets.length; i++) {
      const id = datasets[i].substring(0, datasets[i].indexOf(' '));
      const temp = datasets[i].substring(datasets[i].indexOf(' ') + 1);
      const title = temp.substring(temp.indexOf(' ') + 1);

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
    
    for (let i = 0; i < datasets.length; i++) {
      const id = datasets[i].substring(0, datasets[i].indexOf(' '));
      const temp = datasets[i].substring(datasets[i].indexOf(' ') + 1);
      const topic = temp.substring(0, temp.indexOf(' '));

      if (topic === 'sports') {
        const gridItem = await grid.locator('_react=GridItem[key = \'' + id + '\']').innerHTML();

        await expect(gridItem).toContain('sports');
      }
    }
  });
});

test.describe('View Dataset from Homepage', () => {
  test('Page should have a grid of sports datasets', async({page}) => {
    
  });
});

test.describe('View Dataset from Filtered Results', () => {
  
});

test.describe('Rate Recommendation Exists', () => {
  
});

test.describe('Rate Recommendation as Good', () => {
  
});

test.describe('Rate Recommendation as Bad', () => {
  
});