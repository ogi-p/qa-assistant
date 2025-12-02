# 🤖 Automated Testing with Playwright

## Overview
This module integrates Playwright automation capabilities into the Manual QA Framework, enabling automated test generation, execution, and maintenance alongside manual testing workflows.

## 🎯 Purpose
- **Automated Test Generation**: Convert manual test cases into automated Playwright scripts
- **Test Recording**: Record user interactions and generate test code automatically
- **Regression Testing**: Automate repetitive test scenarios
- **Visual Testing**: Capture screenshots and compare UI changes
- **API Testing**: Test backend services and API endpoints
- **Cross-Browser Testing**: Run tests across Chrome, Firefox, Safari, Edge

## 📁 Structure

```
07-automation/
├── README.md                           # This file
├── scripts/                            # Automated test scripts
│   ├── common/                         # Shared utilities and helpers
│   │   ├── auth-helpers.js             # Authentication utilities
│   │   ├── navigation-helpers.js       # Navigation utilities
│   │   └── assertion-helpers.js        # Custom assertions
│   ├── functional/                     # Functional test scripts
│   │   ├── login/                      # Login tests
│   │   ├── search/                     # Search tests
│   │   └── folders/                    # Folders project tests
│   ├── regression/                     # Regression test suites
│   └── api/                            # API test scripts
├── templates/                          # Test generation templates
│   ├── playwright_test_template.js     # Basic test template
│   ├── api_test_template.js            # API test template
│   └── visual_test_template.js         # Visual regression template
├── recordings/                         # Recorded test sessions
│   └── .gitignore                      # Ignore recorded sessions
├── screenshots/                        # Test screenshots and evidence
│   ├── baseline/                       # Baseline images for comparison
│   ├── actual/                         # Current test screenshots
│   └── diff/                           # Visual difference images
├── reports/                            # Test execution reports
│   └── .gitignore                      # Ignore generated reports
├── commands/                           # CLI commands for automation
│   ├── generate-test.ps1               # Generate test from manual TC
│   ├── generate-test.sh                # Generate test (Bash)
│   ├── record-test.ps1                 # Record user interactions
│   ├── record-test.sh                  # Record test (Bash)
│   ├── run-tests.ps1                   # Execute test suite
│   └── run-tests.sh                    # Execute tests (Bash)
└── config/                             # Automation configuration
    ├── playwright.config.js            # Playwright configuration
    ├── test-environments.json          # Environment configurations
    └── selectors.json                  # Page object selectors
```

## 🚀 Key Features

### 1. Automated Test Generation
Convert existing manual test cases into automated Playwright scripts:
- Parse test case templates from `03-test-plans/`
- Generate executable Playwright code
- Maintain traceability to original manual test cases
- Include environment context and test data

### 2. Test Recording & Playback
Record user interactions and generate test code:
- Launch browser in recording mode
- Capture all user interactions
- Generate Playwright test code automatically
- Save recordings for future reference

### 3. Visual Regression Testing
Capture and compare screenshots for UI testing:
- Baseline screenshot management
- Automatic visual diff generation
- Pixel-perfect comparison
- Highlight visual changes

### 4. API Testing Integration
Test backend services alongside UI tests:
- REST API testing
- GraphQL testing
- Request/response validation
- Performance monitoring

### 5. Cross-Platform Support
Run tests on multiple platforms:
- Windows (PowerShell)
- macOS/Linux (Bash)
- CI/CD integration ready
- Docker container support

## 🔧 Integration with Framework

### Manual Test Case Linkage
Every automated test maintains traceability:
- Reference to original test case ID
- Link to requirements in traceability matrix
- Connection to JIRA tickets
- Environment and user context preservation

### Bug Report Integration
Automated tests can generate bug reports:
- Capture failure screenshots automatically
- Extract error messages and stack traces
- Generate bug report in company format
- Auto-fill JIRA fields with test context

### ISTQB Standards Compliance
All automation follows ISTQB best practices:
- Test design techniques applied
- Proper test data management
- Comprehensive test documentation
- Risk-based test automation

## 📊 Test Execution Workflow

```
Manual Test Case (03-test-plans/)
         ↓
Generate Automated Test (07-automation/commands/)
         ↓
Execute Test (Playwright MCP)
         ↓
Capture Results & Screenshots
         ↓
Update Traceability Matrix (05-utilities/)
         ↓
Generate Bug Report (if failed) → JIRA (01-jira-integration/)
```

## 🎯 Supported Test Types

### Functional Testing
- User authentication flows
- Search and filter functionality
- CRUD operations
- Navigation and routing
- Form submissions

### Non-Functional Testing
- Performance testing (page load times)
- Accessibility testing (ARIA, keyboard navigation)
- Security testing (XSS, CSRF)
- Compatibility testing (browsers, devices)

### Regression Testing
- Critical path automation
- Smoke tests for deployments
- Sanity checks after releases
- Build verification tests

## 📚 Quick Start

### 1. Generate Test from Manual Test Case
```powershell
# Windows
.\07-automation\commands\generate-test.ps1 -TestCaseId "TC-001" -Output ".\07-automation\scripts\functional\login\"

# Mac/Linux
bash ./07-automation/commands/generate-test.sh -t TC-001 -o ./07-automation/scripts/functional/login/
```

### 2. Record New Test
```powershell
# Windows
.\07-automation\commands\record-test.ps1 -TestName "folder-creation" -Output ".\07-automation\recordings\"

# Mac/Linux
bash ./07-automation/commands/record-test.sh -n folder-creation -o ./07-automation/recordings/
```

### 3. Run Test Suite
```powershell
# Windows
.\07-automation\commands\run-tests.ps1 -Suite "regression" -Environment "staging"

# Mac/Linux
bash ./07-automation/commands/run-tests.sh -s regression -e staging
```

## 🔐 Configuration

### Environment Setup
Configure test environments in `config/test-environments.json`:
```json
{
  "dev": {
    "url": "https://dev.yourapp.com",
    "apiUrl": "https://api-dev.yourapp.com",
    "users": {
      "admin": "qa_admin@yourcompany.com",
      "standard_user": "test_user@yourcompany.com"
    }
  },
  "staging": {
    "url": "https://staging.yourapp.com",
    "apiUrl": "https://api-staging.yourapp.com",
    "users": { ... }
  },
  "production": {
    "url": "https://app.yourapp.com",
    "apiUrl": "https://api.yourapp.com",
    "users": { ... }
  }
}
```

### Playwright Configuration
Main configuration in `config/playwright.config.js`:
- Browser configurations
- Timeout settings
- Screenshot options
- Report generation
- Retry strategies

## 📈 Reporting

### Test Execution Reports
Automated reports generated after each run:
- HTML report with screenshots
- JSON report for CI/CD integration
- JUnit XML for test management tools
- Custom report for traceability matrix

### Metrics Tracked
- Test execution time
- Pass/fail rates
- Coverage percentages
- Flaky test detection
- Performance benchmarks

## 🔗 Integration Points

### JIRA Integration
- Automated bug report creation from failures
- Test execution status updates
- Link test runs to JIRA tickets
- QA workload tracking

### Traceability Matrix
- Automated test → Manual test case mapping
- Requirement coverage tracking
- Bug report linkage
- Execution history

### CI/CD Pipeline
- GitHub Actions integration
- Azure DevOps compatibility
- Jenkins plugin support
- Docker containerization

## 🎓 ISTQB Competition Alignment

### Speed
- Rapid test generation from manual cases
- Parallel test execution
- Quick feedback on failures
- Automated bug report creation

### Quality
- Comprehensive test coverage
- Consistent test execution
- Detailed failure evidence
- Reproducible test results

### Innovation
- AI-powered test generation
- Visual regression testing
- Automatic element detection
- Self-healing test scripts

## 📝 Best Practices

### Test Maintenance
- Use page object pattern
- Avoid hardcoded waits
- Implement proper error handling
- Keep tests independent
- Use descriptive test names

### Test Data Management
- Separate test data from test logic
- Use fixtures for setup/teardown
- Implement data-driven testing
- Clean up test data after execution

### Debugging
- Use Playwright Inspector
- Capture screenshots on failure
- Log all actions and assertions
- Save network traffic for analysis

## 🆘 Troubleshooting

### Common Issues
1. **Test Timeouts**: Increase timeout in config or use explicit waits
2. **Element Not Found**: Use proper selectors, check page load
3. **Flaky Tests**: Add proper waits, check for race conditions
4. **Authentication Issues**: Verify credentials in environment config

### Debug Mode
Run tests in debug mode for step-by-step execution:
```powershell
$env:DEBUG="pw:api"
.\07-automation\commands\run-tests.ps1 -Debug
```

## 🔮 Future Enhancements

### Planned Features
- AI-powered test maintenance
- Self-healing selectors
- Automatic test optimization
- Advanced visual testing
- Mobile app testing support
- Performance regression detection

### Integration Roadmap
- Slack notifications for test failures
- TestRail integration
- Allure report generation
- Performance monitoring tools

---

**Built with ❤️ for the QA community**

*Automated Testing Module - Where Manual Meets Automation*

---

## 📞 Support

For questions or issues:
1. Check the [Playwright Documentation](https://playwright.dev/)
2. Review framework documentation in `06-documentation/`
3. Contact the automation team

**Last Updated**: 2025-01-27

