import { test, expect, defineConfig, type Page } from "@playwright/test";
//import { titleCase } from "title-case";
//import { processMetadata } from "../app/utilities";

test.beforeEach(async ({ page }) => {
  await page.goto("http://localhost:3000");
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
    data.forEach(async (dataset: any) => {
      //const util = await import("../app/utilities");
      dataset.title = dataset.title.replace(/,/g, ", ");
      dataset.topic = dataset.topic.replace(/,/g, ", ");
      dataset.licenses = dataset.licenses.replace(/,/g, ", ");
      dataset.tags = dataset.tags.replace(/,/g, ", ");
      /*
      dataset.title = titleCase(dataset.title);
      dataset.topic = titleCase(dataset.topic);
      dataset.licenses = titleCase(dataset.licenses);
      dataset.tags = titleCase(dataset.tags);
      */
      
      datasets.push([
        dataset.id,
        dataset.topic,
        dataset.title,
        dataset.description,
        dataset.licenses,
        dataset.tags,
      ]);
    });
  });

test.describe("View Available Datasets", () => {
  test("Homepage should have title: Data Gandalf", async ({ page }) => {
    await expect(page).toHaveTitle("Data Gandalf");
  });

  test("Homepage should have filter bar with specified topics", async ({
    page,
  }) => {
    const filterBar = page.locator("_react=FilterBar");
    await expect(await filterBar.innerHTML()).toContain("Filter by Topic");

    await filterBar.click();

    const options = await filterBar.innerHTML();
    for (let i = 0; i < topics.length; i++) {
      await expect(options.toLowerCase()).toContain(topics[i].toLowerCase());
    }
  });

  test("Homepage should have a grid of available datasets", async ({
    page,
  }) => {
    const grid = page.locator("_react=Grid");

    for (let dataset of datasets) {
      const id = dataset[0];
      const title = dataset[2];

      const gridItem = await grid
        .locator("_react=GridItem[key = '" + id + "']")
        .innerHTML();

      await expect(gridItem.toLowerCase()).toContain(title.replace("&", "&amp;").toLowerCase());
    }
  });
});

test.describe("Filter Available Datasets by Topic", () => {
  test("Page should have a grid of sports datasets", async ({ page }) => {
    const filterBar = page.locator("_react=FilterBar");
    await filterBar.click();

    const sportsLocators = await page.getByText("sports").all();
    const sportsTopic = sportsLocators[0];

    await sportsTopic.click();

    const grid = page.locator("_react=Grid");

    for (let dataset of datasets) {
      const id = dataset[0];
      const topic = dataset[1];

      if (topic === "sports") {
        const gridItem = await grid
          .locator("_react=GridItem[key = '" + id + "']")
          .innerHTML();

        await expect(gridItem.toLowerCase()).toContain("sports");
      }
    }
  });
});

test.describe("View Dataset from Homepage", () => {
  test("Dataset page should have appropriate dataset details displayed", async ({
    page,
  }) => {
    const grid = page.locator("_react=Grid");

    const dataset = datasets[0];
    const topic = dataset[1];
    const title = dataset[2];
    const description = dataset[3];
    const licenses: any = dataset[4];
    const tags: any = dataset[5];

    const gridItem = await grid.locator("_react=GridItem").first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(2000);
    await page.waitForSelector("_react=GridItemLarge");

    const gridItemLarge = await page
      .locator("_react=GridItemLarge")
      .innerHTML();

    await expect(gridItemLarge.toLowerCase()).toContain(title.toLowerCase());
    await expect(gridItemLarge.toLowerCase()).toContain(topic.toLowerCase());
    await expect(gridItemLarge.toLowerCase()).toContain(description.toLowerCase());
    /*
    for (let license in licenses) {
      await expect(gridItemLarge.toLowerCase()).toContain(license.toLowerCase());
    }
    
    for (let tag in tags) {
      await expect(gridItemLarge.toLowerCase()).toContain(tag.toLowerCase());
    }
    */
  });

  test("Dataset page should have recommendations displayed", async ({
    page,
  }) => {
    const grid = page.locator("_react=Grid");

    const dataset = datasets[0];
    const title = dataset[2];

    const gridItem = await grid.locator("_react=GridItem").first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(2000);
    await page.waitForSelector("_react=Grid");

    const recommendationsGrid = page.locator("_react=Grid");
    const recommendations = await recommendationsGrid
      .locator("_react=GridItem")
      .all();

    for (let i = 0; i < recommendations.length; i++) {
      const recommendationHTML = await recommendations[i].innerHTML();

      await expect(recommendationHTML).toContain("tooltip");
    }
  });
});

test.describe("View Dataset from Filtered Results", () => {
  test("Dataset page should have appropriate dataset details displayed", async ({
    page,
  }) => {
    const filterBar = page.locator("_react=FilterBar");
    await filterBar.click();

    const sportsLocators = await page.getByText("sports").all();
    const sportsTopic = sportsLocators[0];

    await sportsTopic.click();

    const grid = page.locator("_react=Grid");

    const dataset = datasets[0];
    const topic = dataset[1];
    const title = dataset[2];
    const description = dataset[3];
    const licenses: any = dataset[4];
    const tags: any = dataset[5];

    const gridItem = await grid.locator("_react=GridItem").first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(2000);
    await page.waitForSelector("_react=GridItemLarge");

    const gridItemLarge = await page
      .locator("_react=GridItemLarge")
      .innerHTML();

    await expect(gridItemLarge.toLowerCase()).toContain(title.toLowerCase());
    await expect(gridItemLarge.toLowerCase()).toContain(topic.toLowerCase());
    await expect(gridItemLarge.toLowerCase()).toContain(description.toLowerCase());
    /*
    for (let license in licenses) {
      await expect(gridItemLarge.toLowerCase()).toContain(license.toLowerCase());
    }
    
    for (let tag in tags) {
      await expect(gridItemLarge.toLowerCase()).toContain(tag.toLowerCase());
    }
    */
  });

  test("Dataset page should have recommendations displayed", async ({
    page,
  }) => {
    const filterBar = page.locator("_react=FilterBar");
    await filterBar.click();

    const sportsLocators = await page.getByText("sports").all();
    const sportsTopic = sportsLocators[0];

    await sportsTopic.click();

    const grid = page.locator("_react=Grid");

    const dataset = datasets[0];
    const title = dataset[2];

    const gridItem = await grid.locator("_react=GridItem").first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(2000);
    await page.waitForSelector("_react=Grid");

    const recommendationsGrid = page.locator("_react=Grid");
    const recommendations = await recommendationsGrid
      .locator("_react=GridItem")
      .all();

    for (let i = 0; i < recommendations.length; i++) {
      const recommendationHTML = await recommendations[i].innerHTML();

      await expect(recommendationHTML).toContain("tooltip");
    }
  });
});

test.describe("Rate Recommendation Exists", () => {
  test("Dataset page should have rate recommendation options", async ({
    page,
  }) => {
    const grid = page.locator("_react=Grid");

    const dataset = datasets[0];
    const title = dataset[2];

    const gridItem = await grid.locator("_react=GridItem").first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(2000);
    await page.waitForSelector("_react=Grid");

    const recommendationsGrid = page.locator("_react=Grid");
    const recommendations = await recommendationsGrid
      .locator("_react=GridItem")
      .all();

    for (let i = 0; i < recommendations.length; i++) {
      const recommendationHTML = await recommendations[i].innerHTML();

      await expect(recommendationHTML).toContain("thumbs-up");
      await expect(recommendationHTML).toContain("thumbs-down");
    }
  });
});

test.describe("Rate Recommendation as Good", () => {
  test("Can rate recommendation as good on dataset page", async ({
    page,
  }) => {
    const grid = page.locator("_react=Grid");

    const dataset = datasets[0];
    const title = dataset[2];

    const gridItem = await grid.locator("_react=GridItem").first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(5000);
    await page.waitForSelector("_react=Grid");

    const recommendationsGrid = page.locator("_react=Grid");
    const recommendations = await recommendationsGrid
      .locator("_react=GridItem")
      .all();

    const thumbsUp = page.locator('svg[data-icon="thumbs-up"]').first();  
    await expect(await thumbsUp.innerHTML()).toContain("empty");
     
    await thumbsUp.click();
    await page.waitForTimeout(2000);

    const newRating = await page.locator('svg[data-icon="thumbs-up"]').first();
    await expect(await newRating.innerHTML()).toContain("solid");
  });
});

test.describe("Rate Recommendation as Bad", () => {
  test("Can rate recommendation as bad on dataset page", async ({
    page,
  }) => {
    const grid = page.locator("_react=Grid");

    const dataset = datasets[0];
    const title = dataset[2];

    const gridItem = await grid.locator("_react=GridItem").first();

    const titleSelect = await gridItem.getByText(title).first();

    await titleSelect.click();
    await page.waitForTimeout(5000);
    await page.waitForSelector("_react=Grid");

    const recommendationsGrid = page.locator("_react=Grid");
    const recommendations = await recommendationsGrid
      .locator("_react=GridItem")
      .all();

    const thumbsDown = page.locator('svg[data-icon="thumbs-down"]').first();  
    await expect(await thumbsDown.innerHTML()).toContain("empty");
     
    await thumbsDown.click();
    await page.waitForTimeout(2000);

    const newRating = await page.locator('svg[data-icon="thumbs-down"]').first();
    await expect(await newRating.innerHTML()).toContain("solid");
  });
});
