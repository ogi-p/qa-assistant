// Navigation Helper Functions
// Handles page navigation and common UI interactions

const { loadSelectors } = require('./environment-loader');

/**
 * Wait for page to fully load
 * @param {Page} page - Playwright page object
 * @param {object} options - Wait options
 * @returns {Promise<void>}
 */
async function waitForPageLoad(page, options = {}) {
  const { timeout = 30000, waitUntil = 'networkidle' } = options;
  
  try {
    await page.waitForLoadState(waitUntil, { timeout });
    
    // Wait for loading spinner to disappear if present
    const selectors = loadSelectors();
    const loadingVisible = await page.isVisible(selectors.common.loadingSpinner, { timeout: 1000 });
    
    if (loadingVisible) {
      await page.waitForSelector(selectors.common.loadingSpinner, { 
        state: 'hidden',
        timeout 
      });
    }
  } catch (error) {
    console.warn(`Page load wait timed out: ${error.message}`);
  }
}

/**
 * Navigate to page with retry logic
 * @param {Page} page - Playwright page object
 * @param {string} url - URL to navigate to
 * @param {object} options - Navigation options
 * @returns {Promise<void>}
 */
async function navigateToPage(page, url, options = {}) {
  const { retries = 3, timeout = 30000 } = options;
  
  for (let i = 0; i < retries; i++) {
    try {
      await page.goto(url, { 
        waitUntil: 'networkidle',
        timeout 
      });
      
      await waitForPageLoad(page);
      console.log(`Successfully navigated to: ${url}`);
      return;
    } catch (error) {
      console.warn(`Navigation attempt ${i + 1} failed: ${error.message}`);
      
      if (i === retries - 1) {
        throw new Error(`Failed to navigate to ${url} after ${retries} attempts`);
      }
      
      // Wait before retrying
      await page.waitForTimeout(2000);
    }
  }
}

/**
 * Navigate using main menu
 * @param {Page} page - Playwright page object
 * @param {string} menuItem - Menu item to click
 * @returns {Promise<void>}
 */
async function navigateViaMenu(page, menuItem) {
  const selectors = loadSelectors();
  
  try {
    // Wait for main menu
    await page.waitForSelector(selectors.navigation.mainMenu);
    
    // Click menu item
    const linkSelector = selectors.navigation[`${menuItem}Link`];
    if (!linkSelector) {
      throw new Error(`Unknown menu item: ${menuItem}`);
    }
    
    await page.click(linkSelector);
    await waitForPageLoad(page);
    
    console.log(`Navigated via menu to: ${menuItem}`);
  } catch (error) {
    console.error(`Failed to navigate via menu: ${error.message}`);
    throw error;
  }
}

/**
 * Go back in browser history
 * @param {Page} page - Playwright page object
 * @returns {Promise<void>}
 */
async function goBack(page) {
  await page.goBack();
  await waitForPageLoad(page);
}

/**
 * Go forward in browser history
 * @param {Page} page - Playwright page object
 * @returns {Promise<void>}
 */
async function goForward(page) {
  await page.goForward();
  await waitForPageLoad(page);
}

/**
 * Reload current page
 * @param {Page} page - Playwright page object
 * @returns {Promise<void>}
 */
async function reloadPage(page) {
  await page.reload({ waitUntil: 'networkidle' });
  await waitForPageLoad(page);
}

/**
 * Wait for element to be visible and ready
 * @param {Page} page - Playwright page object
 * @param {string} selector - Element selector
 * @param {object} options - Wait options
 * @returns {Promise<ElementHandle>}
 */
async function waitForElement(page, selector, options = {}) {
  const { timeout = 10000, state = 'visible' } = options;
  
  await page.waitForSelector(selector, { state, timeout });
  return page.locator(selector);
}

/**
 * Scroll element into view
 * @param {Page} page - Playwright page object
 * @param {string} selector - Element selector
 * @returns {Promise<void>}
 */
async function scrollIntoView(page, selector) {
  await page.locator(selector).scrollIntoViewIfNeeded();
  await page.waitForTimeout(300); // Wait for scroll animation
}

/**
 * Wait for URL to match pattern
 * @param {Page} page - Playwright page object
 * @param {string|RegExp} urlPattern - URL pattern to match
 * @param {number} timeout - Timeout in milliseconds
 * @returns {Promise<void>}
 */
async function waitForURL(page, urlPattern, timeout = 10000) {
  await page.waitForURL(urlPattern, { timeout });
}

/**
 * Check if on expected page
 * @param {Page} page - Playwright page object
 * @param {string|RegExp} urlPattern - Expected URL pattern
 * @returns {Promise<boolean>}
 */
async function isOnPage(page, urlPattern) {
  const currentUrl = page.url();
  
  if (typeof urlPattern === 'string') {
    return currentUrl.includes(urlPattern);
  } else if (urlPattern instanceof RegExp) {
    return urlPattern.test(currentUrl);
  }
  
  return false;
}

module.exports = {
  waitForPageLoad,
  navigateToPage,
  navigateViaMenu,
  goBack,
  goForward,
  reloadPage,
  waitForElement,
  scrollIntoView,
  waitForURL,
  isOnPage
};

