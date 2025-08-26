# Jira Quick Reference Guide

Quick reference for common Jira statuses, labels, and workflow transitions.

## 🚀 Status Quick Reference

| Status | Meaning | Next Steps |
|--------|---------|------------|
| `To Do` | Ready to be picked up | Developer starts work |
| `In Progress` | Developer actively working | Submit for peer review |
| `Peer review` | Code review in progress | Address feedback or move to QA |
| `Ready for QA` | Development complete | QA team starts testing |
| `QA Testing` | QA actively testing | Pass to deploy or return for fixes |
| `To Deploy` | Tested on dev, not pushed to stage | Deploy to staging |
| `Deployed` | Currently on stage environment | Deploy to production |
| `Done` | Deployed to production + regression tests | ✅ Complete |

## 🏷️ Common Labels

### **Project Labels**
- `helios-backlog` - Helios project work
- `hydrus-backlog` - Hydrus project work  
- `polaris-backlog` - Polaris project work
- `vega-backlog` - Vega project work

### **Deployment Labels**
- `deployed-to-stage` - Deployed to staging
- `deployed-to-prod` - Deployed to production
- `deployed-to-dev` - Deployed to development

**⚠️ IMPORTANT:** Status must match deployment labels. Raise issues for discrepancies!

### **Technical Labels**
- `FE` - Frontend work
- `BE` - Backend work
- `API` - API work
- `data-eng-backlog` - Data engineering work

### **Priority Labels**
- `Hotfix` - Critical fix needed
- `urgent` - High priority
- `blocker` - Blocking other work

## 🎯 Issue Types

| Type | Purpose |
|------|---------|
| `Story` | User story or feature |
| `Task` | General work item |
| `Bug` | Software defect |
| `Bug (t)` | Technical bug |
| `Sub-task` | Part of larger work |
| `Epic` | Large body of work |

## 📈 Priority Levels

| Priority | Impact | Response Time |
|----------|--------|---------------|
| `Critical` | System breaking | Immediate |
| `Major` | Core functionality | High |
| `Normal` | Standard work | Normal |
| `Minor` | Nice to have | Low |
| `None` | Informational | N/A |

## 🔄 Valid Status Transitions

```
To Do → In Progress
In Progress → Peer review
Peer review → Ready for QA (approved)
Peer review → In Progress (changes needed)
Ready for QA → QA Testing
QA Testing → To Deploy (passed)
QA Testing → Ready for QA (issues found)
To Deploy → Deployed (pushed to stage)
Deployed → Done (deployed to production + regression tests)
```

## 🚫 Invalid Transitions

- ❌ `To Do` → `Done` (skip development)
- ❌ `In Progress` → `Done` (skip review)
- ❌ `Ready for QA` → `Done` (skip testing)
- ❌ `To Deploy` → `Done` (skip stage deployment)

## 🔍 Custom Fields

- **QA Assignee:** `customfield_11207` - Assigns QA responsibility
- **Development:** `customfield_11200` - Links to PRs

## 📊 Active vs Completed

- **Active Tickets:** All statuses except `Done` (test work ongoing)
- **Completed Tickets:** Only `Done` status (test work completed)

## 📋 Quick Commands

```bash
# Read any ticket
python3 jira_scripts/jira_ticket_reader.py AP-XXXXX

# See your QA workload
python3 jira_scripts/qa_workload_reader.py

# Complete assignment overview
python3 jira_scripts/my_assignments.py
```

---

**For detailed information:** See `jira_status_labels_mapping.md`
