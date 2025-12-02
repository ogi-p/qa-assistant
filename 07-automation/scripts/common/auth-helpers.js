// Authentication Helper Functions
// Handles user login and authentication flows

const { loadSelectors, getUserCredentials } = require('./environment-loader');

/**
 * Login as specified user
 * @param {Page} page - Playwright page object
 * @param {object} user - User configuration
 * @returns {Promise<void>}
 */
async function loginAsUser(page, user) {
  const selectors = loadSelectors();
  const credentials = getUserCredentials(user);
  
  try {
    // Wait for login page to be visible
    await page.waitForSelector(selectors.login.emailInput, { timeout: 10000 });
    
    // Fill email
    await page.fill(selectors.login.emailInput, credentials.email);
    
    // Fill password
    await page.fill(selectors.login.passwordInput, credentials.password);
    
    // Click submit button
    await page.click(selectors.login.submitButton);
    
    // Wait for navigation after login
    await page.waitForLoadState('networkidle');
    
    // Verify login success (check for profile menu or main navigation)
    const isLoggedIn = await page.isVisible(selectors.navigation.profileMenu, { timeout: 5000 });
    
    if (!isLoggedIn) {
      // Check for error message
      const errorVisible = await page.isVisible(selectors.login.errorMessage);
      if (errorVisible) {
        const errorText = await page.textContent(selectors.login.errorMessage);
        throw new Error(`Login failed: ${errorText}`);
      }
      throw new Error('Login failed: Unable to verify successful login');
    }
    
    console.log(`Successfully logged in as: ${credentials.email}`);
  } catch (error) {
    console.error(`Login failed for user ${credentials.email}: ${error.message}`);
    
    // Take screenshot of login failure
    await page.screenshot({ 
      path: `../../screenshots/failures/login-failure-${Date.now()}.png`,
      fullPage: true 
    });
    
    throw error;
  }
}

/**
 * Logout current user
 * @param {Page} page - Playwright page object
 * @returns {Promise<void>}
 */
async function logout(page) {
  const selectors = loadSelectors();
  
  try {
    // Click profile menu
    await page.click(selectors.navigation.profileMenu);
    
    // Wait for menu to expand
    await page.waitForTimeout(500);
    
    // Click logout button
    await page.click(selectors.navigation.logoutButton);
    
    // Wait for logout to complete
    await page.waitForLoadState('networkidle');
    
    // Verify logout success (login page should be visible)
    await page.waitForSelector(selectors.login.emailInput, { timeout: 5000 });
    
    console.log('Successfully logged out');
  } catch (error) {
    console.error(`Logout failed: ${error.message}`);
    throw error;
  }
}

/**
 * Check if user is logged in
 * @param {Page} page - Playwright page object
 * @returns {Promise<boolean>}
 */
async function isLoggedIn(page) {
  const selectors = loadSelectors();
  
  try {
    return await page.isVisible(selectors.navigation.profileMenu, { timeout: 2000 });
  } catch {
    return false;
  }
}

/**
 * Login with SSO (if applicable)
 * @param {Page} page - Playwright page object
 * @param {object} user - User configuration
 * @returns {Promise<void>}
 */
async function loginWithSSO(page, user) {
  const credentials = getUserCredentials(user);
  
  try {
    // Navigate to SSO login page
    await page.goto('/auth/sso');
    
    // Fill SSO email
    await page.fill('input[name="email"]', credentials.email);
    
    // Click continue to SSO
    await page.click('button:has-text("Continue with SSO")');
    
    // Wait for SSO provider redirect
    await page.waitForLoadState('networkidle');
    
    // Handle SSO provider authentication (implementation depends on SSO provider)
    // This is a placeholder - customize based on actual SSO flow
    await page.fill('input[name="username"]', credentials.email);
    await page.fill('input[name="password"]', credentials.password);
    await page.click('button[type="submit"]');
    
    // Wait for redirect back to application
    await page.waitForLoadState('networkidle');
    
    console.log(`Successfully logged in via SSO as: ${credentials.email}`);
  } catch (error) {
    console.error(`SSO login failed for user ${credentials.email}: ${error.message}`);
    throw error;
  }
}

module.exports = {
  loginAsUser,
  logout,
  isLoggedIn,
  loginWithSSO
};

