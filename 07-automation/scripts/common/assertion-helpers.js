// Assertion Helper Functions
// Custom assertions for common test scenarios

const { expect } = require('@playwright/test');
const { loadSelectors } = require('./environment-loader');

/**
 * Assert element is visible and contains text
 * @param {Page} page - Playwright page object
 * @param {string} selector - Element selector
 * @param {string} expectedText - Expected text content
 * @returns {Promise<void>}
 */
async function assertElementContainsText(page, selector, expectedText) {
  const element = page.locator(selector);
  await expect(element).toBeVisible();
  await expect(element).toContainText(expectedText);
}

/**
 * Assert element has specific attribute value
 * @param {Page} page - Playwright page object
 * @param {string} selector - Element selector
 * @param {string} attribute - Attribute name
 * @param {string} expectedValue - Expected attribute value
 * @returns {Promise<void>}
 */
async function assertElementHasAttribute(page, selector, attribute, expectedValue) {
  const element = page.locator(selector);
  await expect(element).toHaveAttribute(attribute, expectedValue);
}

/**
 * Assert page title matches expected
 * @param {Page} page - Playwright page object
 * @param {string} expectedTitle - Expected page title
 * @returns {Promise<void>}
 */
async function assertPageTitle(page, expectedTitle) {
  await expect(page).toHaveTitle(expectedTitle);
}

/**
 * Assert URL contains expected path
 * @param {Page} page - Playwright page object
 * @param {string} expectedPath - Expected URL path
 * @returns {Promise<void>}
 */
async function assertURLContains(page, expectedPath) {
  await expect(page).toHaveURL(new RegExp(expectedPath));
}

/**
 * Assert element count matches expected
 * @param {Page} page - Playwright page object
 * @param {string} selector - Element selector
 * @param {number} expectedCount - Expected element count
 * @returns {Promise<void>}
 */
async function assertElementCount(page, selector, expectedCount) {
  const elements = page.locator(selector);
  await expect(elements).toHaveCount(expectedCount);
}

/**
 * Assert success message is displayed
 * @param {Page} page - Playwright page object
 * @param {string} expectedMessage - Expected success message
 * @returns {Promise<void>}
 */
async function assertSuccessMessage(page, expectedMessage) {
  const selectors = loadSelectors();
  const successToast = page.locator(selectors.common.successToast);
  
  await expect(successToast).toBeVisible({ timeout: 5000 });
  if (expectedMessage) {
    await expect(successToast).toContainText(expectedMessage);
  }
}

/**
 * Assert error message is displayed
 * @param {Page} page - Playwright page object
 * @param {string} expectedMessage - Expected error message
 * @returns {Promise<void>}
 */
async function assertErrorMessage(page, expectedMessage) {
  const selectors = loadSelectors();
  const errorToast = page.locator(selectors.common.errorToast);
  
  await expect(errorToast).toBeVisible({ timeout: 5000 });
  if (expectedMessage) {
    await expect(errorToast).toContainText(expectedMessage);
  }
}

/**
 * Assert element is enabled/disabled
 * @param {Page} page - Playwright page object
 * @param {string} selector - Element selector
 * @param {boolean} shouldBeEnabled - Whether element should be enabled
 * @returns {Promise<void>}
 */
async function assertElementEnabled(page, selector, shouldBeEnabled = true) {
  const element = page.locator(selector);
  
  if (shouldBeEnabled) {
    await expect(element).toBeEnabled();
  } else {
    await expect(element).toBeDisabled();
  }
}

/**
 * Assert element is checked/unchecked
 * @param {Page} page - Playwright page object
 * @param {string} selector - Element selector
 * @param {boolean} shouldBeChecked - Whether element should be checked
 * @returns {Promise<void>}
 */
async function assertElementChecked(page, selector, shouldBeChecked = true) {
  const element = page.locator(selector);
  
  if (shouldBeChecked) {
    await expect(element).toBeChecked();
  } else {
    await expect(element).not.toBeChecked();
  }
}

/**
 * Assert element is visible or hidden
 * @param {Page} page - Playwright page object
 * @param {string} selector - Element selector
 * @param {boolean} shouldBeVisible - Whether element should be visible
 * @returns {Promise<void>}
 */
async function assertElementVisibility(page, selector, shouldBeVisible = true) {
  const element = page.locator(selector);
  
  if (shouldBeVisible) {
    await expect(element).toBeVisible();
  } else {
    await expect(element).toBeHidden();
  }
}

/**
 * Assert API response has expected status and body
 * @param {APIResponse} response - API response object
 * @param {number} expectedStatus - Expected status code
 * @param {object} expectedBodySubset - Expected body properties
 * @returns {Promise<void>}
 */
async function assertAPIResponse(response, expectedStatus, expectedBodySubset = null) {
  // Assert status code
  expect(response.status()).toBe(expectedStatus);
  
  // Assert response body if provided
  if (expectedBodySubset) {
    const body = await response.json();
    
    // Check each expected property
    for (const [key, value] of Object.entries(expectedBodySubset)) {
      expect(body).toHaveProperty(key, value);
    }
  }
}

/**
 * Assert dropdown has specific options
 * @param {Page} page - Playwright page object
 * @param {string} selector - Dropdown selector
 * @param {string[]} expectedOptions - Expected option values
 * @returns {Promise<void>}
 */
async function assertDropdownOptions(page, selector, expectedOptions) {
  const dropdown = page.locator(selector);
  await expect(dropdown).toBeVisible();
  
  const options = await dropdown.locator('option').allTextContents();
  expect(options).toEqual(expectedOptions);
}

/**
 * Assert table row count
 * @param {Page} page - Playwright page object
 * @param {string} tableSelector - Table selector
 * @param {number} expectedRowCount - Expected number of rows
 * @returns {Promise<void>}
 */
async function assertTableRowCount(page, tableSelector, expectedRowCount) {
  const rows = page.locator(`${tableSelector} tbody tr`);
  await expect(rows).toHaveCount(expectedRowCount);
}

/**
 * Assert console has no errors
 * @param {Page} page - Playwright page object
 * @returns {Promise<void>}
 */
async function assertNoConsoleErrors(page) {
  const consoleErrors = [];
  
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });
  
  // Wait a bit to collect any console errors
  await page.waitForTimeout(1000);
  
  expect(consoleErrors).toHaveLength(0);
}

/**
 * Assert page performance metrics
 * @param {Page} page - Playwright page object
 * @param {number} maxLoadTime - Maximum acceptable page load time (ms)
 * @returns {Promise<void>}
 */
async function assertPagePerformance(page, maxLoadTime = 3000) {
  const performanceData = await page.evaluate(() => {
    const perfData = window.performance.timing;
    return {
      loadTime: perfData.loadEventEnd - perfData.navigationStart,
      domReady: perfData.domContentLoadedEventEnd - perfData.navigationStart,
      responseTime: perfData.responseEnd - perfData.requestStart
    };
  });
  
  expect(performanceData.loadTime).toBeLessThan(maxLoadTime);
  console.log(`Page load time: ${performanceData.loadTime}ms`);
}

module.exports = {
  assertElementContainsText,
  assertElementHasAttribute,
  assertPageTitle,
  assertURLContains,
  assertElementCount,
  assertSuccessMessage,
  assertErrorMessage,
  assertElementEnabled,
  assertElementChecked,
  assertElementVisibility,
  assertAPIResponse,
  assertDropdownOptions,
  assertTableRowCount,
  assertNoConsoleErrors,
  assertPagePerformance
};

