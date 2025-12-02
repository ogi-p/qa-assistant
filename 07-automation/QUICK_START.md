# 🚀 Playwright Automation - Quick Start Guide

Get started with Playwright automation in the Manual QA Framework in 5 minutes!

---

## ✅ Prerequisites

1. **Node.js** installed (v18 or higher)
   ```bash
   node --version
   ```

2. **Git** repository cloned
   ```bash
   cd qa-manual-framework
   ```

3. **Playwright MCP Server** installed and configured (verified ✅)

---

## 📋 Quick Start Steps

### Step 1: Generate Your First Automated Test

Convert an existing manual test case to an automated Playwright script:

**Windows (PowerShell):**
```powershell
cd 07-automation\commands
.\generate-test.ps1 -TestCaseId "TC-001" -Output "..\scripts\functional\login\"
```

**Mac/Linux (Bash):**
```bash
cd 07-automation/commands
bash ./generate-test.sh -t TC-001 -o ../scripts/functional/login/
```

**What happens:**
- ✅ Searches for test case TC-001 in `03-test-plans/`
- ✅ Extracts test steps, preconditions, and expected results
- ✅ Generates executable Playwright test script
- ✅ Saves to specified output directory

---

### Step 2: Record a New Test

Record user interactions and generate test code automatically:

**Windows (PowerShell):**
```powershell
.\record-test.ps1 -TestName "folder-creation" -Environment "dev"
```

**Mac/Linux (Bash):**
```bash
bash ./record-test.sh -n folder-creation -e dev
```

**What happens:**
- ✅ Opens browser in recording mode
- ✅ Captures all your interactions
- ✅ Generates test code automatically
- ✅ Saves recording to `../recordings/`

**Recording Tips:**
- Perform actions slowly and deliberately
- Wait for elements to load before clicking
- Use clear, identifiable selectors when possible
- Close the browser to save the recording

---

### Step 3: Complete the Generated Test

Open the generated test file and complete the TODO sections:

```javascript
// Find TODO sections in the generated test
// TODO: Implement test steps based on manual test case
// TODO: Add assertions based on expected results

// Example completion:
test('TC-001: Login with valid credentials', async ({ page }) => {
  // Navigate to login page
  await page.goto(env.url + '/login');
  
  // Fill login form
  await page.fill(selectors.login.emailInput, 'qa_admin@yourcompany.com');
  await page.fill(selectors.login.passwordInput, process.env.USER_PASSWORD);
  
  // Submit form
  await page.click(selectors.login.submitButton);
  
  // Assertions
  await assertURLContains(page, '/dashboard');
  await assertElementVisibility(page, selectors.navigation.profileMenu, true);
});
```

---

### Step 4: Run Your Tests

Execute the test suite:

**Windows (PowerShell):**
```powershell
.\run-tests.ps1 -Suite "functional" -Environment "dev" -Browser "chromium"
```

**Mac/Linux (Bash):**
```bash
bash ./run-tests.sh -s functional -e dev -b chromium
```

**Command Options:**
- `-Suite / -s`: Test suite to run (functional, regression, api)
- `-Environment / -e`: Environment to test (dev, staging, production)
- `-Browser / -b`: Browser to use (chromium, firefox, webkit)
- `-Debug / -d`: Enable debug mode with Playwright Inspector
- `-Headed / -h`: Run tests in headed mode (visible browser)

**What happens:**
- ✅ Loads test environment configuration
- ✅ Runs all tests in the specified suite
- ✅ Captures screenshots on failures
- ✅ Generates HTML, JSON, and JUnit reports
- ✅ Displays results in terminal

---

### Step 5: View Test Results

After test execution, view the results:

**HTML Report:**
```bash
# Windows
start 07-automation\reports\html\index.html

# Mac/Linux
open 07-automation/reports/html/index.html
```

**Report Contents:**
- ✅ Test execution summary
- ✅ Pass/fail status for each test
- ✅ Screenshots of failures
- ✅ Execution time metrics
- ✅ Error messages and stack traces

---

## 🎯 Common Use Cases

### Use Case 1: Regression Testing

Run full regression suite before releases:

```bash
# Windows
.\run-tests.ps1 -Suite "regression" -Environment "staging" -Browser "chromium"

# Mac/Linux
bash ./run-tests.sh -s regression -e staging -b chromium
```

### Use Case 2: Cross-Browser Testing

Test across multiple browsers:

```bash
# Run on all browsers
bash ./run-tests.sh -s functional -e dev -b chromium
bash ./run-tests.sh -s functional -e dev -b firefox
bash ./run-tests.sh -s functional -e dev -b webkit
```

### Use Case 3: Debug Failing Test

Debug a specific test with Playwright Inspector:

```bash
# Windows
.\run-tests.ps1 -Suite "functional\login" -Debug

# Mac/Linux
bash ./run-tests.sh -s functional/login -d
```

### Use Case 4: Visual Regression Testing

Compare UI screenshots:

```javascript
// Use visual test template
const { takeAndCompareScreenshot } = require('../scripts/common/visual-helpers');

test('Visual check - Dashboard', async ({ page }) => {
  await page.goto('/dashboard');
  
  const result = await takeAndCompareScreenshot(page, 'dashboard', {
    fullPage: true,
    maxDiffPercentage: 0.1
  });
  
  expect(result.passed).toBe(true);
});
```

---

## 🛠️ Configuration

### Environment Configuration

Edit `config/test-environments.json` to add/modify test environments:

```json
{
  "dev": {
    "url": "https://dev.yourapp.com",
    "apiUrl": "https://api-dev.yourapp.com",
    "users": {
      "admin": {
        "email": "qa_admin@yourcompany.com",
        "vaultPath": "qa/users/admin"
      }
    }
  }
}
```

### Selector Configuration

Edit `config/selectors.json` to add/modify page selectors:

```json
{
  "login": {
    "emailInput": "input[name='email']",
    "passwordInput": "input[name='password']",
    "submitButton": "button[type='submit']"
  }
}
```

### Playwright Configuration

Edit `config/playwright.config.js` for advanced settings:

```javascript
module.exports = defineConfig({
  timeout: 30 * 1000,
  retries: 2,
  use: {
    baseURL: process.env.BASE_URL,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  }
});
```

---

## 📚 Next Steps

### Learn More

1. **Read the full documentation**: [README.md](README.md)
2. **Integration guide**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
3. **Playwright docs**: [https://playwright.dev/](https://playwright.dev/)

### Explore Templates

- **Functional tests**: `templates/playwright_test_template.js`
- **API tests**: `templates/api_test_template.js`
- **Visual tests**: `templates/visual_test_template.js`

### Helper Utilities

- **Authentication**: `scripts/common/auth-helpers.js`
- **Navigation**: `scripts/common/navigation-helpers.js`
- **Assertions**: `scripts/common/assertion-helpers.js`
- **Visual testing**: `scripts/common/visual-helpers.js`

---

## 🆘 Troubleshooting

### Browser Not Installed

```bash
npx playwright install
npx playwright install-deps
```

### Test Timeout

Increase timeout in `config/playwright.config.js`:

```javascript
timeout: 60 * 1000  // 60 seconds
```

### Element Not Found

- Check selector in `config/selectors.json`
- Use Playwright Inspector to find correct selector:
  ```bash
  npx playwright codegen https://your-app.com
  ```

### Authentication Failed

- Verify credentials in environment variables
- Check user configuration in `config/test-environments.json`
- Ensure password is set: `$env:PASSWORD_QA_ADMIN=your_password`

---

## 💡 Pro Tips

1. **Use Page Object Pattern**: Create reusable page classes for common pages
2. **Data-Driven Testing**: Use fixtures for test data
3. **Parallel Execution**: Run tests in parallel for faster execution
4. **Screenshot Baseline**: Create baseline screenshots for visual testing
5. **CI/CD Integration**: Add tests to your deployment pipeline

---

## 🎉 You're Ready!

You've successfully set up Playwright automation in the Manual QA Framework!

**What's next:**
- ✅ Convert more manual test cases to automated tests
- ✅ Create project-specific test suites
- ✅ Integrate with CI/CD pipeline
- ✅ Build comprehensive regression suite

**Need help?** Check the documentation or reach out to the QA team!

---

**Last Updated**: 2025-01-27  
**Version**: 1.0.0

