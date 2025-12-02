# Playwright Integration Guide

## 🔗 Integration with Manual QA Framework

This guide explains how Playwright automation integrates with the existing Manual QA Framework components.

---

## 📋 Test Case Integration

### Automated Test Generation from Manual Test Cases

The framework provides seamless conversion from manual test cases to automated Playwright scripts.

#### Step 1: Create Manual Test Case

Use the enhanced test case template from `03-test-plans/template/test_case_template_enhanced.md`:

```markdown
## Test Case Header
**Test Case ID**: [TC-FOLDERS-001]
**Title**: [Create New Folder - Basic Flow]

## 1. Test Environment
**Environment:** [dev]
**Users:** [qa_admin@yourcompany.com]
**Application:** [main_app]

## 3. Preconditions
- User is logged in
- User has folder creation permissions
- No existing folder with the same name

## 4. Test Steps
1. Navigate to Folders page
2. Click "Create Folder" button
3. Enter folder name: "Test Folder 001"
4. Click "Save" button

## 5. Expected Results
- Folder is created successfully
- Success message is displayed
- Folder appears in the folder list
```

#### Step 2: Generate Automated Test

Run the generation command:

**PowerShell:**
```powershell
.\07-automation\commands\generate-test.ps1 `
    -TestCaseId "TC-FOLDERS-001" `
    -Output ".\07-automation\scripts\functional\folders\"
```

**Bash:**
```bash
bash ./07-automation/commands/generate-test.sh \
    -t TC-FOLDERS-001 \
    -o ./07-automation/scripts/functional/folders/
```

#### Step 3: Complete Generated Test

The generated test will contain TODO sections. Complete these with actual implementation:

```javascript
test('TC-FOLDERS-001: Create New Folder - Basic Flow', async ({ page }) => {
  // Navigate to Folders page
  await navigateViaMenu(page, 'folders');
  await waitForPageLoad(page);
  
  // Click "Create Folder" button
  const createButton = await waitForElement(page, selectors.folders.createButton);
  await createButton.click();
  
  // Enter folder name
  await page.fill(selectors.folders.folderNameInput, 'Test Folder 001');
  
  // Click Save button
  await page.click(selectors.folders.saveButton);
  
  // Assertions
  await assertSuccessMessage(page, 'Folder created successfully');
  await assertElementContainsText(page, selectors.folders.folderItem, 'Test Folder 001');
});
```

---

## 🐛 Bug Report Integration

### Automated Bug Report Generation from Test Failures

When automated tests fail, the framework can generate bug reports automatically.

#### Failure Detection

Test failures automatically capture:
- Screenshots of the failure state
- Page HTML at time of failure
- Console logs and errors
- Network requests and responses
- Stack traces

#### Bug Report Generation

Create a bug report generator utility:

```javascript
// 07-automation/scripts/common/bug-report-generator.js
async function generateBugReport(testInfo, page) {
  const bugReport = {
    summary: `[Automated Test Failure] ${testInfo.title}`,
    environment: process.env.TEST_ENV || 'dev',
    testCaseId: extractTestCaseId(testInfo.title),
    stepsToReproduce: extractTestSteps(testInfo.title),
    actualResult: testInfo.error.message,
    screenshots: testInfo.attachments.filter(a => a.name.includes('screenshot')),
    consoleErrors: await page.evaluate(() => window.consoleErrors || [])
  };
  
  return bugReport;
}
```

#### JIRA Integration

Use the framework's JIRA integration to create tickets from failures:

```javascript
// Create JIRA ticket from bug report
const jiraPayload = {
  fields: {
    project: { key: "AP" },
    issuetype: { name: "Bug" },
    summary: bugReport.summary,
    customfield_11332: { value: bugReport.environment },
    // ... other fields from bug report
  }
};

// Post to JIRA API
await fetch('https://yourcompany.atlassian.net/rest/api/3/issue', {
  method: 'POST',
  headers: {
    'Authorization': `Basic ${auth}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(jiraPayload)
});
```

---

## 📊 Traceability Matrix Integration

### Maintaining Test Traceability

Every automated test maintains links to:
- Original manual test case
- Requirements
- JIRA tickets
- Bug reports

#### Automated Traceability Updates

```javascript
// Update traceability matrix after test execution
async function updateTraceabilityMatrix(testResults) {
  const matrix = loadTraceabilityMatrix();
  
  for (const result of testResults) {
    const testCaseId = extractTestCaseId(result.test);
    
    matrix.testCases[testCaseId] = {
      ...matrix.testCases[testCaseId],
      lastExecuted: new Date().toISOString(),
      status: result.status,
      automationStatus: 'Automated',
      automatedTestPath: result.testPath
    };
  }
  
  saveTraceabilityMatrix(matrix);
}
```

#### Matrix Format

Use the enhanced traceability matrix from `05-utilities/traceability_matrix_template_enhanced.md`:

```markdown
| Test Case ID | Manual Test | Automated Test | Last Executed | Status |
|--------------|-------------|----------------|---------------|--------|
| TC-FOLDERS-001 | ✅ | ✅ | 2025-01-27 | Pass |
| TC-FOLDERS-002 | ✅ | 🔄 | 2025-01-27 | In Progress |
| TC-FOLDERS-003 | ✅ | ⏳ | N/A | Not Started |
```

---

## 🎯 Test Plan Integration

### Automated Test Execution in Test Plans

Include automated tests in your test plan documentation.

#### Test Plan Structure

In `03-test-plans/template/test_plan_template.md`, add automation section:

```markdown
## 3. Test Design & Approach

### Automation Strategy
- **Automated Tests**: Critical path and regression scenarios
- **Manual Tests**: Exploratory, usability, and edge cases
- **Hybrid Tests**: Initial manual verification, then automated for regression

### Test Case Overview
| Test Case ID | Title | Type | Automation Status |
|--------------|-------|------|-------------------|
| TC-FOLDERS-001 | Create Folder | Functional | ✅ Automated |
| TC-FOLDERS-002 | Delete Folder | Functional | 🔄 In Progress |
| TC-FOLDERS-003 | Folder Permissions | Security | ⏳ Manual Only |
```

#### Execution Workflow

```
1. Run automated regression suite
   └─> .\07-automation\commands\run-tests.ps1 -Suite regression -Environment staging

2. Review automated test results
   └─> Check HTML report: .\07-automation\reports\html\index.html

3. Execute manual test cases for areas not automated

4. Update traceability matrix with results

5. Generate test summary report
```

---

## 🔄 Continuous Integration Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/playwright-tests.yml
name: Playwright Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: |
        cd 07-automation
        npm install
        npx playwright install --with-deps
    
    - name: Run Playwright tests
      run: |
        cd 07-automation/commands
        bash ./run-tests.sh -e staging -b chromium
      env:
        TEST_ENV: staging
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: playwright-report
        path: 07-automation/reports/
        retention-days: 30
```

---

## 📈 Metrics and Reporting

### Combined Manual + Automated Metrics

Track comprehensive testing metrics:

```javascript
{
  "testingMetrics": {
    "totalTestCases": 50,
    "manualTests": 30,
    "automatedTests": 20,
    "automationCoverage": "40%",
    "passRate": "95%",
    "avgExecutionTime": "15 minutes",
    "criticalPathCoverage": "100%",
    "regressionSuiteCoverage": "80%"
  },
  "qualityMetrics": {
    "defectsFound": 5,
    "defectsByAutomation": 3,
    "defectsByManual": 2,
    "avgDefectDetectionTime": "2 hours",
    "falsePositiveRate": "2%"
  }
}
```

---

## 🎓 Best Practices

### 1. Test Case Selection for Automation

**Automate:**
- ✅ Repetitive test scenarios
- ✅ Regression test cases
- ✅ Data-driven test cases
- ✅ Critical path scenarios
- ✅ API/integration tests

**Keep Manual:**
- ⏳ Exploratory testing
- ⏳ Usability testing
- ⏳ Ad-hoc testing
- ⏳ New feature exploration
- ⏳ Visual design validation

### 2. Maintenance Strategy

- Review automated tests monthly
- Update selectors when UI changes
- Refactor common patterns into helpers
- Keep test data fresh and relevant
- Monitor flaky tests and fix immediately

### 3. Documentation Standards

- Keep manual and automated tests in sync
- Document automation decisions in test plans
- Maintain clear traceability links
- Update test case status regularly
- Include automation notes in manual test cases

### 4. Collaboration

- QA engineers write initial manual test cases
- Automation engineers convert to automated tests
- Both review and approve final automated tests
- Shared ownership of test maintenance
- Regular sync meetings for test strategy

---

## 📚 Additional Resources

- [Playwright Documentation](https://playwright.dev/)
- [ISTQB Test Automation Guidelines](https://www.istqb.org/)
- [Framework Test Plan Template](../03-test-plans/template/test_plan_template.md)
- [Enhanced Test Case Template](../03-test-plans/template/test_case_template_enhanced.md)
- [Traceability Matrix Template](../05-utilities/traceability_matrix_template_enhanced.md)

---

**Last Updated**: 2025-01-27  
**Version**: 1.0.0

