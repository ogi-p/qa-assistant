# Git Ignore Strategy - Manual QA Framework

## Overview
This document explains the gitignore configuration for the Manual QA Framework, ensuring only essential framework files are version-controlled while all project-specific artifacts remain local.

## Core Principle
**Framework stays in Git, Projects stay local**

The framework is designed to be:
- **Portable**: Clone once, use for any project
- **Clean**: No project-specific test artifacts in version control
- **Lightweight**: No generated files, dependencies, or build artifacts
- **Secure**: No credentials, API keys, or sensitive data

---

## What Gets Committed to Git

### ✅ Framework Core (Always Committed)
```
07-automation/
├── .gitignore                    # Ignore rules
├── README.md                     # Documentation
├── INTEGRATION_GUIDE.md          # Integration docs
├── QUICK_START.md                # Quick start guide
├── IMPLEMENTATION_SUMMARY.md     # Implementation notes
├── package.json                  # Dependency list (NOT package-lock.json)
├── config/
│   ├── playwright.config.js      # Playwright settings
│   ├── selectors.json            # Selector definitions
│   └── test-environments.json    # Environment templates
├── templates/
│   ├── playwright_test_template.js
│   ├── api_test_template.js
│   └── visual_test_template.js
├── scripts/
│   └── common/                   # Shared helpers
│       ├── assertion-helpers.js
│       ├── auth-helpers.js
│       ├── environment-loader.js
│       ├── navigation-helpers.js
│       └── visual-helpers.js
└── commands/
    ├── generate-test.ps1
    ├── generate-test.sh
    ├── record-test.ps1
    ├── record-test.sh
    ├── run-tests.ps1
    └── run-tests.sh
```

### ✅ JIRA Integration & Documentation
```
01-jira-integration/              # JIRA configuration
02-bug-reports/                   # Bug report templates
03-test-plans/                    # Test plan templates
04-projects/ownership-entity/     # Example project (documented)
05-utilities/                     # Framework utilities
06-documentation/                 # Framework documentation
```

---

## What Stays Local (Never Committed)

### ❌ Project-Specific Test Implementations
```
07-automation/scripts/
├── functional/raynorqa/          # raynorqa.com tests
├── functional/yourproject/       # Your project tests
├── regression/project-xyz/       # Regression tests
└── api/project-abc/              # API tests

04-projects/
├── raynorqa-website/             # All project artifacts
│   ├── test_plan.md
│   ├── test_cases/
│   ├── TEST_EXECUTION_REPORT.md
│   └── ANALYSIS_AND_RECOMMENDATIONS.md
└── your-project/                 # Your project documentation
```

**Why?** Each project has unique tests. The framework provides templates; projects use them locally.

### ❌ Generated Artifacts
```
07-automation/
├── node_modules/                 # npm dependencies (reinstall)
├── package-lock.json             # Lock file (regenerate)
├── test-results/                 # Test execution results
├── playwright-report/            # HTML reports
├── screenshots/                  # Test screenshots
├── recordings/                   # Recorded sessions
└── reports/                      # Generated reports

.playwright-mcp/                  # Playwright cache (root)
screenshots/                      # Screenshots (root)
```

**Why?** These are regenerated on every machine. No need to bloat the repository.

### ❌ Sensitive & Environment-Specific
```
.env                              # Environment variables
.env.local                        # Local overrides
*.env                             # Any environment file
01-jira-integration/config/.env   # JIRA credentials
```

**Why?** Security. Credentials should never be in version control.

### ❌ System & IDE Files
```
.DS_Store                         # macOS files
Thumbs.db                         # Windows files
.vscode/                          # VS Code settings
.idea/                            # JetBrains IDEs
*.log                             # Log files
```

**Why?** Platform-specific noise that doesn't help anyone.

---

## Setup on New Machine

### Step 1: Clone Repository
```bash
git clone https://github.com/ogi-p/qa-assistant.git
cd qa-assistant
```

### Step 2: Install Dependencies
```bash
cd 07-automation
npm install
npx playwright install
```

### Step 3: Configure Environment
```bash
# Copy template and add your credentials
cp 01-jira-integration/config/env.template 01-jira-integration/config/.env
# Edit .env with your JIRA credentials
```

### Step 4: Create Your Project
```bash
mkdir -p 04-projects/my-project
mkdir -p 07-automation/scripts/functional/my-project
```

### Step 5: Generate Tests
```bash
# Record a test
cd 07-automation
./commands/record-test.ps1  # Windows
# or
./commands/record-test.sh   # Mac/Linux

# Generate from template
./commands/generate-test.ps1 -TestName "Login Test" -TestType "functional"
```

---

## File Size Comparison

### ❌ Without Proper Gitignore
```
Repository Size: ~500MB+
- node_modules/: ~300MB
- playwright-report/: ~50MB
- test-results/: ~100MB
- screenshots/: ~50MB
- All project files: varies
```

### ✅ With Proper Gitignore
```
Repository Size: ~5MB
- Framework code: ~2MB
- Documentation: ~2MB
- Templates & configs: ~1MB
- Zero bloat, pure framework
```

---

## Gitignore Hierarchy

### 1. Root `.gitignore`
- Global exclusions for entire repository
- Project-specific directories (`04-projects/*/`)
- Root-level cache files (`.playwright-mcp/`, `screenshots/`)
- JIRA credentials and environment files

### 2. `07-automation/.gitignore`
- Automation-specific exclusions
- Generated test artifacts
- Node dependencies
- Test execution results
- Project-specific test implementations

### 3. Benefits of Two-Level Approach
- **Clarity**: Root handles global, subfolder handles module
- **Maintainability**: Each module manages its own ignores
- **Portability**: `07-automation/` can be extracted as standalone
- **Flexibility**: Easy to add more modules with their own rules

---

## Common Scenarios

### Scenario 1: Adding a New Project
```bash
# Create project directory
mkdir -p 04-projects/new-project
mkdir -p 07-automation/scripts/functional/new-project

# No git add needed - it's automatically ignored
# Work locally, never commit project-specific files
```

### Scenario 2: Sharing Test Framework Updates
```bash
# Only framework changes are tracked
git add 07-automation/templates/new_template.js
git add 07-automation/scripts/common/new-helper.js
git commit -m "Add new template and helper"
git push

# Other users pull and get framework updates
# Their local projects remain untouched
```

### Scenario 3: Updating Framework Configuration
```bash
# Framework config is tracked
git add 07-automation/config/playwright.config.js
git commit -m "Update browser configurations"

# Environment-specific overrides stay local
# Each user maintains their own .env
```

---

## Verification Commands

### Check What's Tracked
```bash
git ls-files 07-automation/
```

### Check What's Ignored
```bash
git status --ignored
```

### Verify Gitignore Rules
```bash
git check-ignore -v 07-automation/node_modules/
git check-ignore -v 04-projects/raynorqa-website/
```

### Test Before Commit
```bash
git status --short
# Should only show framework files, never project files
```

---

## Best Practices

### ✅ DO
- Commit framework improvements
- Commit shared templates and helpers
- Commit documentation updates
- Keep `.gitkeep` files for directory structure
- Use `package.json` for dependency versions

### ❌ DON'T
- Commit `node_modules/` or `package-lock.json`
- Commit project-specific test scripts
- Commit test execution reports or screenshots
- Commit `.env` files or credentials
- Commit generated artifacts

---

## Troubleshooting

### Problem: Project files showing in git status
**Solution**: Run `git rm --cached -r 04-projects/your-project/` to remove from tracking

### Problem: node_modules in git status
**Solution**: Run `git rm --cached -r 07-automation/node_modules/`

### Problem: Gitignore not working
**Solution**: Clear git cache and re-add files
```bash
git rm -r --cached .
git add .
```

### Problem: Want to track a specific project
**Solution**: Add exception to `.gitignore`
```
04-projects/*/
!04-projects/important-project/
```

---

## Summary

The Manual QA Framework uses a strategic gitignore configuration to maintain a clean, portable, and secure repository:

- **Framework**: Committed and shared across all users
- **Projects**: Local to each QA tester's machine
- **Artifacts**: Generated locally, never committed
- **Credentials**: Never in version control

This approach ensures the framework remains lightweight, portable, and easy to maintain while allowing each QA tester to work on their own projects independently.

---

**Last Updated**: December 2, 2025  
**Framework Version**: 1.0 with Playwright Automation

