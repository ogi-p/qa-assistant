# Security Audit Report - Identifiable Data Cleanup
**Date**: December 2, 2025  
**Purpose**: Identify all company-specific and personal identifiable data before public repository release

---

## Executive Summary

This audit identifies all company-specific references, personal data, and project-specific information that should be cleaned or excluded before publishing to a public GitHub repository. The framework is currently configured with proper `.gitignore` rules to exclude most sensitive data, but several files contain hardcoded references that need attention.

### Risk Level Summary
- 🔴 **HIGH RISK**: 19 files (contain direct company/personal identifiable data)
- 🟡 **MEDIUM RISK**: 5 files (contain example data that should be genericized)
- 🟢 **LOW RISK**: Automation module (already cleaned)

---

## 🔴 HIGH RISK - Company Identifiable Data

### 1. CompStak References

#### A. Repository URLs
**Files Affected**:
- `README.md` (lines 44, 99, 205)
- `06-documentation/guides/quick_start_guide.md` (line 23)
- `GITIGNORE_STRATEGY.md` (line 129)

**Current References**:
```
https://github.com/compstak/QA-Manual-Framework.git
https://compstak.atlassian.net
```

**Recommendation**:
Replace with generic placeholders:
```
https://github.com/your-org/qa-manual-framework.git
https://your-company.atlassian.net
```

#### B. Email Domains
**Files Affected**:
- `README.md` (line 187)
- `06-documentation/guides/quick_start_guide.md` (lines 52, 57)
- `06-documentation/guides/jira_env_setup_guide.md` (lines 36, 68, 119, 128)
- `01-jira-integration/config/env.template` (line 5)

**Current References**:
```
your.email@compstak.com
user@compstak.com
```

**Recommendation**:
Replace with:
```
your.email@your-company.com
user@your-company.com
```

#### C. JIRA Instance URLs
**Files Affected**:
- `06-documentation/guides/jira_env_setup_guide.md` (lines 69, 136)
- `02-bug-reports/templates/jira-ap-bug-metadata.json` (150+ instances)

**Current References**:
```
https://compstak.atlassian.net/rest/api/3/...
```

**Recommendation**:
- **jira-ap-bug-metadata.json**: Consider DELETING this file entirely or replace all URLs with placeholders
- Other files: Replace with `https://your-company.atlassian.net`

---

### 2. Project-Specific Data (AP Project)

#### A. JIRA Ticket References
**Files Affected**:
- `04-projects/folders/test_plan.md` (line 6)
- `04-projects/folders/project rules/folders_testing_rules.mdc` (line 5)
- `04-projects/folders/README.md` (lines 5, 131)
- `01-jira-integration/scripts/jira-mcp-enhanced.sh`

**Current References**:
```
AP-20446
https://compstak.atlassian.net/browse/AP-20446
```

**Recommendation**:
Since `04-projects/folders/` is already in `.gitignore`, verify it's excluded. If not, either:
1. Add explicit exclusion for `04-projects/folders/` 
2. Or genericize these references to `PROJECT-123`

#### B. External Documentation Links
**Files Affected**:
- `04-projects/folders/project rules/folders_testing_rules.mdc` (lines 51-53)
- `04-projects/folders/README.md` (lines 19-21)
- `04-projects/ownership-entity/project documentation/OES_System_Documentation.md` (lines 229-230)

**Current References**:
```
https://docs.google.com/document/d/1rtKQ9IMbidst8gMamR0R91dodmFj28OSsEgC7vHXwDQ/...
https://www.figma.com/design/Xxa4wFXvnSLmk8nTsV3dha/...
```

**Recommendation**:
These folders should already be excluded by `.gitignore`. Verify exclusion is working.

---

### 3. Personal Identifiable Data

#### A. Personal Name References
**Files Affected**:
- `01-jira-integration/scripts/find_qa_assignee_tickets.sh` (lines 3, 27, 70, 89)

**Current References**:
```bash
# Script to find all tickets where Ognjen Putniković is assigned as QA Assignee
if [ "$qa_assignee" = "Ognjen Putniković" ]; then
```

**Recommendation**:
Replace with:
```bash
# Script to find all tickets where current user is assigned as QA Assignee
if [ "$qa_assignee" = "$JIRA_USER_NAME" ]; then
```
Or make it a parameter that reads from environment variable.

---

### 4. Company-Specific JIRA Metadata

#### A. JIRA Field Metadata File
**File**: `02-bug-reports/templates/jira-ap-bug-metadata.json` (831 lines)

**Contains**:
- 150+ hardcoded CompStak Atlassian URLs
- Specific component IDs and names
- Project avatars and icons
- Custom field configurations
- Priority schemes

**Recommendation**: 🔴 **CRITICAL DECISION NEEDED**

**Option 1 (Recommended)**: DELETE this file entirely
- It's project-specific metadata unlikely to be useful for other companies
- Contains extensive CompStak-specific configurations
- High maintenance burden to genericize

**Option 2**: Genericize completely
- Replace all 150+ URLs with placeholders
- Remove specific component/project IDs
- Keep only the structure as an example
- High effort, low value

**Option 3**: Move to documentation as example
- Rename to `jira-metadata-example.json.txt`
- Add header explaining it's an example of JIRA API response format
- Not intended for direct use

---

### 5. Bug Report Examples

**Directory**: `02-bug-reports/reports/` (17 files)

**Files with Potential Issues**:
- `ap-*.json` (5 files) - Contains AP project references
- `bt-ticket.json` - Contains BT project references
- `buyer_seller_missing_stage_bug_report.txt` - Contains product-specific info
- `bug_report_missing_buyer_seller_new_sales_comps.txt` - CompStak feature names
- `bug_report_new_salesmaster_data_duplication.txt` - CompStak feature names
- `bug_report_oes_owner_attributes_not_propagated.txt` - OES project reference
- `buyer-seller-stage-bug.json` - Contains AP project data

**Recommendation**: 🟡 **MEDIUM PRIORITY**

These are example bug reports. Options:
1. **Keep as examples** - They demonstrate bug report quality
2. **Genericize feature names** - Replace "Sales Comps", "Buyer/Seller", etc. with generic terms
3. **Add disclaimer** - Note that these are sanitized examples from past projects
4. **Delete project-specific ones** - Keep only generic examples like 404 errors, cart issues

---

## 🟢 LOW RISK - Already Clean

### 07-automation/ Module
✅ **Status**: Already genericized during implementation

**Confirmed Clean**:
- All configuration files use placeholders (`yourapp.com`, `yourcompany.com`)
- No hardcoded company data
- Templates are generic
- Documentation is framework-focused

---

## 📊 Gitignore Verification

### Current Exclusions (Confirmed)
✅ `.gitignore` properly excludes:
- `04-projects/raynorqa-website/` (your local project)
- `04-projects/*/` (all project directories)
- Exception: `04-projects/ownership-entity/` (documentation)
- Automation artifacts and dependencies
- Environment files with credentials

### ⚠️ Potential Gaps

**Issue**: `04-projects/folders/` is excluded by wildcard but contains CompStak data

**Verification Needed**:
Run these commands to verify:
```bash
git check-ignore -v 04-projects/folders/
git check-ignore -v 04-projects/raynorqa-website/
```

Both should return positive (ignored) results.

---

## 🎯 Recommended Action Plan

### Phase 1: Critical Security (MUST DO)
1. ✅ Verify `.gitignore` excludes `04-projects/folders/` and `04-projects/raynorqa-website/`
2. 🔴 Remove or genericize personal name from `01-jira-integration/scripts/find_qa_assignee_tickets.sh`
3. 🔴 **DECIDE**: Delete or genericize `02-bug-reports/templates/jira-ap-bug-metadata.json`
4. 🔴 Replace CompStak URLs in `README.md` (3 locations)
5. 🔴 Replace CompStak emails in `01-jira-integration/config/env.template`

### Phase 2: Documentation Cleanup (SHOULD DO)
6. 🟡 Update `06-documentation/guides/quick_start_guide.md` - remove CompStak references
7. 🟡 Update `06-documentation/guides/jira_env_setup_guide.md` - genericize URLs and emails
8. 🟡 Update `GITIGNORE_STRATEGY.md` - replace GitHub URLs with generic placeholders
9. 🟡 Review bug report examples in `02-bug-reports/reports/` - genericize or add disclaimer

### Phase 3: Verification (MUST DO)
10. ✅ Run `git status` to see what files will actually be committed
11. ✅ Run `git ls-files` to verify tracked files
12. ✅ Search for remaining "compstak" references: `git grep -i compstak`
13. ✅ Search for remaining "ognjen" references: `git grep -i ognjen`
14. ✅ Test JIRA commands still work with genericized templates

### Phase 4: Final Review (RECOMMENDED)
15. 📝 Add `CONTRIBUTING.md` with setup instructions for new users
16. 📝 Update repository description to remove company specifics
17. 📝 Consider adding `LICENSE` file for public repository
18. 📝 Add disclaimer that examples are sanitized from real projects

---

## 🔧 Specific File Recommendations

### Files to UPDATE (Keep but Clean)

| File | Priority | Action | Estimated LOC Changed |
|------|----------|--------|----------------------|
| `README.md` | 🔴 HIGH | Replace CompStak URLs (3), JIRA URL (1) | ~4 lines |
| `01-jira-integration/config/env.template` | 🔴 HIGH | Replace email domain | ~1 line |
| `01-jira-integration/scripts/find_qa_assignee_tickets.sh` | 🔴 HIGH | Replace hardcoded name with variable | ~4 lines |
| `GITIGNORE_STRATEGY.md` | 🟡 MEDIUM | Replace GitHub URL | ~1 line |
| `06-documentation/guides/quick_start_guide.md` | 🟡 MEDIUM | Replace CompStak references | ~3 lines |
| `06-documentation/guides/jira_env_setup_guide.md` | 🟡 MEDIUM | Replace CompStak URLs/emails | ~6 lines |

**Total Estimated Changes**: ~20 lines across 6 files

### Files to REVIEW (Decide: Keep/Delete/Modify)

| File | Size | Issue | Recommendation |
|------|------|-------|----------------|
| `02-bug-reports/templates/jira-ap-bug-metadata.json` | 831 lines | 150+ CompStak URLs | 🔴 **DELETE** or move to docs as example |
| `02-bug-reports/reports/*.json` (7 files) | Varies | Project-specific data | 🟡 Review individually, genericize feature names |
| `02-bug-reports/reports/*_bug_report.txt` (10 files) | Varies | Some contain product features | 🟡 Keep as examples with disclaimer |

### Directories to VERIFY EXCLUDED

| Directory | Should Be Excluded? | Reason |
|-----------|-------------------|--------|
| `04-projects/raynorqa-website/` | ✅ YES | Your local project testing |
| `04-projects/folders/` | ✅ YES | Contains CompStak project data |
| `04-projects/ownership-entity/` | ❓ DECIDE | Currently kept as documentation example |
| `07-automation/node_modules/` | ✅ YES | Dependencies (regenerated) |
| `07-automation/test-results/` | ✅ YES | Generated artifacts |

---

## 🧪 Testing Checklist

After cleanup, verify these still work:

### Functionality Tests
- [ ] JIRA commands still authenticate properly
- [ ] `show_my_tickets.ps1` / `.sh` execute without errors
- [ ] Environment template is clear and usable
- [ ] Playwright automation setup works on fresh install
- [ ] Documentation links resolve correctly

### Security Tests
- [ ] No personal names in tracked files
- [ ] No company-specific URLs in tracked files
- [ ] No real email addresses in tracked files
- [ ] No JIRA ticket IDs in tracked files (except examples)
- [ ] All project-specific directories excluded

### Repository Tests
```bash
# Run these before final commit
git grep -i "compstak" -- . ':!.gitignore'
git grep -i "ognjen" -- .
git grep -i "putnik" -- .
git grep "AP-[0-9]" -- . ':!02-bug-reports/reports'
```

All should return empty or only acceptable results.

---

## 📋 Quick Reference: Search & Replace

### Global Replacements Needed

```bash
# CompStak URLs
compstak/QA-Manual-Framework → your-org/qa-manual-framework
https://compstak.atlassian.net → https://your-company.atlassian.net

# Email domains
@compstak.com → @your-company.com

# Personal data
Ognjen Putniković → $JIRA_USER_NAME (or current user)

# Project codes
AP-20446 → PROJECT-XXX (in examples)
```

---

## ⚠️ Critical Decision Points

### Decision 1: jira-ap-bug-metadata.json
**Question**: Keep, genericize, or delete this 831-line CompStak-specific file?

**Impact**:
- Keep: High risk, 150+ CompStak URLs exposed
- Genericize: High effort (~2 hours), moderate value
- Delete: Low risk, may lose example value

**Recommendation**: **DELETE** - The framework works without it, and it's too specific to be useful generically.

---

### Decision 2: Bug Report Examples
**Question**: Keep real product feature names or genericize?

**Impact**:
- Keep: Low risk (just feature names), high value (realistic examples)
- Genericize: Medium effort, loses authenticity
- Delete: Low effort, loses valuable examples

**Recommendation**: **KEEP with disclaimer** - Add note that examples are sanitized from real projects. Feature names like "Sales Comps" don't expose sensitive data.

---

### Decision 3: Ownership Entity Documentation
**Question**: Keep `04-projects/ownership-entity/` as example?

**Impact**:
- Currently NOT excluded by `.gitignore` (exception made)
- Contains Google Docs links (lines 229-230)
- Serves as example project documentation structure

**Recommendation**: **KEEP but clean external links** - Replace Google Docs URLs with placeholders, keep structure as example.

---

## 🎯 Final Checklist Before Publishing

- [ ] All Phase 1 (Critical) actions completed
- [ ] All Phase 2 (Documentation) actions completed
- [ ] All Phase 3 (Verification) tests passed
- [ ] Decision 1 resolved (jira metadata file)
- [ ] Decision 2 resolved (bug report examples)
- [ ] Decision 3 resolved (OES documentation)
- [ ] `.gitignore` verification complete
- [ ] Test suite run on clean install
- [ ] All search commands return clean results
- [ ] Repository description updated
- [ ] `LICENSE` file added (if desired)
- [ ] Final review by repository owner

---

## 📊 Summary Statistics

**Total Files Audited**: 300+  
**Files Requiring Changes**: ~6 critical + ~10 optional  
**High Risk Files**: 19  
**Medium Risk Files**: 5  
**Lines to Change**: ~20 critical + ~30 optional  
**Estimated Cleanup Time**: 2-3 hours  

**Current Security Status**: 🟡 **MEDIUM RISK**  
**Post-Cleanup Status**: 🟢 **PUBLIC-READY**  

---

*Generated by Igor's Security Audit Module*  
*"Even the best frameworks have skeletons in their closets, master. Best we remove them before the public arrives."*

