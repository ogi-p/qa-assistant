# Jira Status and Labels Mapping

This document provides a comprehensive mapping of Jira statuses and labels used across our projects. This mapping helps team members understand the workflow, project organization, and ticket categorization.

## 📊 Status Mapping

### **Core Workflow Statuses**

#### **🔄 Active Development Statuses**
- **`To Do`** - Ticket is planned and ready to be picked up by a developer
- **`In Progress`** - Developer is actively working on the ticket
- **`Peer review`** - Code has been submitted and is being reviewed by team members
- **`Ready for QA`** - Development is complete, ready for QA testing
- **`QA Testing`** - QA team is actively testing the feature/bug fix
- **`To Deploy`** - This ticket has been tested on the dev environment but hasn't been pushed to stage yet

#### **✅ Completion Statuses**
- **`Done`** - Ticket has been deployed to production and regression tests have been run
- **`Deployed`** - Ticket is currently on the stage environment
- **`Resolved`** - Issue has been resolved (alternative to Done)

#### **❌ Issue Statuses**
- **`Duplicated`** - Ticket is a duplicate of another existing ticket
- **`Won't Fix`** - Issue will not be addressed (rare, requires justification)
- **`Cannot Reproduce`** - Issue cannot be reproduced in current environment

#### **📋 Planning Statuses**
- **`Requirements Review`** - Requirements are being reviewed/refined
- **`Backlog`** - Ticket is in the backlog, not yet prioritized

### **Status Flow**
```
To Do → In Progress → Peer review → Ready for QA → QA Testing → To Deploy → Deployed → Done
```

**📋 Active vs Completed:**
- **Active Tickets:** All statuses except `Done` (test work is ongoing)
- **Completed Tickets:** Only `Done` status (test work completed)

## 🏷️ Labels Mapping

### **Project-Specific Labels**

#### **📁 Helios Project**
- **`helios-backlog`** - Tickets related to the Helios project backlog
- **`helios-maintenance`** - Maintenance tasks for Helios system
- **`helios-feature`** - New features for Helios

#### **📊 Hydrus Project**
- **`hydrus-backlog`** - Tickets related to the Hydrus project backlog
- **`hydrus-maintenance`** - Maintenance tasks for Hydrus system
- **`hydrus-feature`** - New features for Hydrus

#### **⭐ Polaris Project**
- **`polaris-backlog`** - Tickets related to the Polaris project backlog
- **`polaris-maintenance`** - Maintenance tasks for Polaris system
- **`polaris-feature`** - New features for Polaris

#### **🌊 Vega Project**
- **`vega-backlog`** - Tickets related to the Vega project backlog
- **`vega-maintenance`** - Maintenance tasks for Vega system
- **`vega-feature`** - New features for Vega

### **Deployment Labels**

#### **🚀 Environment Labels**
- **`deployed-to-stage`** - Feature has been deployed to staging environment
- **`deployed-to-prod`** - Feature has been deployed to production environment
- **`deployed-to-dev`** - Feature has been deployed to development environment

**⚠️ IMPORTANT:** Tickets should always be marked with `deployed-to-stage` or `deployed-to-prod` if they have been indeed deployed. If you notice a discrepancy between status and labels, raise an issue.

### **Issue Type Labels**

#### **🐛 Bug Labels**
- **`bug-frontend`** - Frontend-related bugs
- **`bug-backend`** - Backend-related bugs
- **`bug-api`** - API-related bugs
- **`bug-ui`** - User interface bugs
- **`bug-ux`** - User experience bugs

#### **🔧 Technical Labels**
- **`data-eng-backlog`** - Data engineering related tickets
- **`FE`** - Frontend related work
- **`BE`** - Backend related work
- **`API`** - API related work
- **`infrastructure`** - Infrastructure related work

### **Priority and Special Labels**

#### **🚨 Priority Labels**
- **`Hotfix`** - Critical fixes that need immediate attention
- **`urgent`** - High priority items
- **`blocker`** - Issues blocking other work

#### **📋 Process Labels**
- **`TB-issues`** - Team backlog issues
- **`oem-maintenance`** - OEM system maintenance
- **`ownership-entity`** - Ownership entity related work

## 🎯 Issue Type Mapping

### **Core Issue Types**
- **`Story`** - User story or feature request
- **`Task`** - General task or work item
- **`Bug`** - Software defect or issue
- **`Bug (t)`** - Technical bug (backend/infrastructure)
- **`Sub-task`** - Part of a larger story or task
- **`Epic`** - Large body of work containing multiple stories

### **Special Issue Types**
- **`Improvement`** - Enhancement to existing functionality
- **`New Feature`** - Brand new feature request
- **`Technical debt`** - Code quality improvements
- **`Documentation`** - Documentation updates

## 📈 Priority Levels

### **Priority Mapping**
- **`Critical`** - System-breaking issues, immediate attention required
- **`Major`** - Significant issues affecting core functionality
- **`Normal`** - Standard priority for most work items
- **`Minor`** - Low impact issues, nice-to-have improvements
- **`None`** - No priority set (usually for informational tickets)

## 🔍 Custom Fields

### **QA Assignee Field**
- **Field ID:** `customfield_11207`
- **Field Name:** "QA Assignee"
- **Purpose:** Assigns QA responsibility to specific team members
- **Usage:** Automatically populated when QA testing is required

### **Development Field**
- **Field ID:** `customfield_11200` (approximate)
- **Field Name:** "Development"
- **Purpose:** Links to pull requests and development progress
- **Usage:** Automatically updated when PRs are created/merged

## 📋 Workflow Guidelines

### **For Developers**
1. **Start with `To Do`** - Pick up tickets from this status
2. **Move to `In Progress`** - When actively working
3. **Submit for `Peer review`** - When code is ready for review
4. **Move to `Ready for QA`** - After peer review approval

### **For QA Team**
1. **Pick up from `Ready for QA`** - Start testing when development is complete
2. **Move to `QA Testing`** - When actively testing
3. **Move to `To Deploy`** - When testing passes
4. **Verify in `Done`** - After successful deployment

### **For Project Managers**
1. **Use labels** - To categorize and track project-specific work
2. **Monitor priorities** - Ensure critical items are addressed first
3. **Track deployments** - Use deployment labels to track release status

## 🔄 Status Transitions

### **Valid Status Transitions**
```
To Do → In Progress
In Progress → Peer review
Peer review → Ready for QA (if approved)
Peer review → In Progress (if changes needed)
Ready for QA → QA Testing
QA Testing → To Deploy (if passed)
QA Testing → Ready for QA (if issues found)
To Deploy → Deployed (when pushed to stage)
Deployed → Done (when deployed to production + regression tests)
```

### **Invalid Transitions**
- Cannot go directly from `To Do` to `Done`
- Cannot skip `Peer review` for code changes
- Cannot skip `QA Testing` for user-facing changes
- Cannot skip `Deployed` status (must go through stage before production)

## 📊 Reporting and Metrics

### **Status-Based Metrics**
- **Cycle Time:** Time from `In Progress` to `Done`
- **Lead Time:** Time from `To Do` to `Done`
- **QA Time:** Time from `Ready for QA` to `To Deploy`
- **Stage Time:** Time from `To Deploy` to `Deployed`
- **Production Time:** Time from `Deployed` to `Done`
- **Active Workload:** Count of tickets not in `Done` status

### **Label-Based Metrics**
- **Project Distribution:** Count by project labels
- **Bug Distribution:** Count by bug type labels
- **Deployment Tracking:** Count by deployment labels
- **Deployment Validation:** Verify status matches deployment labels

## 🎯 Best Practices

### **Label Usage**
- **Use project labels** - Always add relevant project label
- **Use deployment labels** - Update when deploying to environments
- **Use technical labels** - For better categorization
- **Avoid over-labeling** - Don't add unnecessary labels
- **Validate deployment labels** - Ensure status matches deployment labels
- **Raise issues for discrepancies** - If status doesn't match deployment labels

### **Status Management**
- **Update promptly** - Change status when work state changes
- **Use correct transitions** - Follow the defined workflow
- **Add comments** - Explain status changes when needed
- **Verify deployments** - Confirm status after deployment

### **Priority Management**
- **Set realistic priorities** - Don't mark everything as critical
- **Review regularly** - Update priorities as circumstances change
- **Communicate changes** - Notify team of priority changes

---

**Last Updated:** [Current Date]
**Maintained By:** QA Team
**Review Cycle:** Monthly
