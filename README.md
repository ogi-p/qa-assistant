# QA Assistant - Igor

A specialized AI assistant designed to help QA professionals generate test cases, write bug reports, and follow QA best practices with ISTQB knowledge.

## 🚀 Quick Start

**New to the project?** Start with the [Quick Start Guide](QUICK_START_GUIDE.md) for easy setup instructions!

### **1. Create a New Project**
```bash
# Create project folder
mkdir -p local_docs/projects/[ProjectID]_[Description]/
```

### **2. Add Context Data**
Place your project requirements, APIs, and test data in:
```
local_docs/projects/[ProjectID]/context/
```

### **3. Use the AI Assistant**
- **Test cases**: Describe a feature → Get structured test cases
- **Bug reports**: Describe an issue → Get Jira-ready bug report
- **QA guidance**: Ask for testing strategies and best practices

### **4. Jira Integration**
```bash
# Read any Jira ticket
python3 jira_scripts/jira_ticket_reader.py AP-XXXXX

# Check your QA workload
python3 jira_scripts/qa_workload_reader.py

# See all your assignments
python3 jira_scripts/my_assignments.py
```

## How to Use This System

### **For New Projects:**
1. **Create project folder**: `local_docs/projects/[ProjectID]_[Description]/`
2. **Add context data**: Place requirements, APIs, test data in `context/` folder
3. **Generate artifacts**: Use AI assistant to create test cases, bug reports, etc.
4. **Organize results**: Files are automatically saved to appropriate project folders

### **Context Organization:**
- **`.cursor/Additional context/`**: ISTQB materials (always accessible to AI)
- **`local_docs/projects/[Project]/context/`**: Project-specific requirements, APIs, test data
- **`local_docs/shared/context/`**: Common test data, standard configurations

### **File Naming Conventions:**
- **Test cases**: `[Feature]_[Date].md`
- **Bug reports**: `[BugID]_[Date].md`
- **Context files**: `[Type]_[Description].json/yaml`

### **AI Assistant Usage:**
- **Test case generation**: Provide feature description, get structured test cases
- **Bug reporting**: Describe issue, get formatted bug report ready for Jira
- **QA guidance**: Ask for testing strategies, best practices, ISTQB concepts

## Project Structure

```
QA Assistant - Igor/
├── .cursor/
│   ├── Additional context/     # ISTQB reference materials (AI-accessible)
│   │   ├── pdfs/              # ISTQB syllabi and documentation
│   │   └── extracted/         # Extracted text content
│   └── rules/                 # AI assistant configuration
├── templates/                 # QA templates and examples
│   ├── bug_reports/          # Bug report templates
│   ├── test_cases/           # Test case templates
│   └── test_files/           # Sample test files
├── local_docs/               # Project-specific documentation (git-ignored)
│   ├── projects/             # Individual project folders
│   │   └── [ProjectName]/    # Project-specific artifacts
│   │       ├── context/      # Project requirements, APIs, test data
│   │       ├── test_cases/   # Project test cases
│   │       ├── bug_reports/  # Project bug reports
│   │       ├── test_plans/   # Project test plans
│   │       ├── test_results/ # Test execution results
│   │       └── project_notes/ # Project documentation
│   └── shared/               # Shared resources
│       ├── context/          # Common test data, standard configs
│       ├── references/       # Shared reference materials
│       └── templates/        # Project-specific template variations
└── tools/                    # Utilities and scripts (future)
```

## Features

### **Templates**
- **Bug Reports**: Browser-focused templates with environment, steps, and severity
- **Test Cases**: Structured templates with preconditions, steps, and expected results
- **Test Files**: Sample test artifacts and examples

### **Knowledge Base**
- **ISTQB Foundation Level** (v4.0.1) - Complete syllabus content
- **ISTQB Advanced Test Analyst** (v4.0) - Advanced testing techniques
- **Best Practices Enforcement** - Automatic guidance and recommendations

### **AI Assistant Capabilities**
- Igor personality for engaging interactions
- Best practices validation and warnings
- Context-aware responses using ISTQB knowledge
- Template generation and customization

## Setup

### **Dependencies**
For PDF extraction capabilities:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install PyPDF2
```

### **Configuration**
The AI assistant is configured through files in `.cursor/rules/`:
- `cursor_rules.mdc` - Main configuration and behavior
- `action_log.mdc` - Action tracking and context preservation

## Contributing

When adding new templates or documentation:
1. Follow the established directory structure
2. Maintain consistency with existing formats
3. Update this README if adding new features

## Project To-Do List

### **🔥 Priority 1: Jira Integration (Critical)**
- [ ] **Jira API Setup**
  - [ ] Create Jira connection configuration system
  - [ ] Implement secure API token storage
  - [ ] Set up project and field mapping configurations
  - [ ] Create error handling and retry logic

- [ ] **Bug Report → Jira Ticket Automation**
  - [ ] Map bug report template fields to Jira fields
  - [ ] Implement automatic ticket creation from bug reports
  - [ ] Add severity/priority mapping (High/Medium/Low)
  - [ ] Create environment and component tagging
  - [ ] Add attachment support for screenshots/logs

- [ ] **Test Plan → Jira Integration**
  - [ ] Create test plan attachment to feature tickets
  - [ ] Implement test case linking to requirements
  - [ ] Add test execution status updates
  - [ ] Create progress tracking in Jira comments

- [ ] **Jira Integration Testing**
  - [ ] Test with sample bug reports and test plans
  - [ ] Validate field mappings and data integrity
  - [ ] Test error scenarios and edge cases
  - [ ] Performance testing with bulk operations

### **📋 Priority 2: Template System Enhancement**
- [ ] **Template Validation**
  - [ ] Create template quality scoring system
  - [ ] Implement mandatory field validation
  - [ ] Add template consistency checks
  - [ ] Create template improvement suggestions

- [ ] **Template Customization**
  - [ ] Add project-specific template variations
  - [ ] Create industry-specific templates (web, mobile, API)
  - [ ] Implement template versioning system
  - [ ] Add template import/export functionality

### **🔧 Priority 3: Automation & Scripts**
- [ ] **Project Management Automation**
  - [ ] Create automatic project folder generation
  - [ ] Implement project metadata tracking
  - [ ] Add project backup and archiving
  - [ ] Create project migration tools

- [ ] **File Organization Automation**
  - [ ] Implement automated file naming with timestamps
  - [ ] Create file structure validation scripts
  - [ ] Add duplicate detection and prevention
  - [ ] Implement file cleanup and maintenance

### **📊 Priority 4: Quality & Analytics**
- [ ] **Quality Metrics**
  - [ ] Create test case coverage analytics
  - [ ] Implement bug report quality scoring
  - [ ] Add project completion tracking
  - [ ] Create quality trend reporting

- [ ] **Performance Monitoring**
  - [ ] Add system usage analytics
  - [ ] Implement performance benchmarking
  - [ ] Create efficiency metrics
  - [ ] Add user feedback collection

### **🚀 Priority 5: Advanced Features**
- [ ] **AI Enhancement**
  - [ ] Improve ISTQB knowledge integration
  - [ ] Add automatic template selection
  - [ ] Implement context-aware responses
  - [ ] Create personality consistency validation

- [ ] **Integration Expansion**
  - [ ] Add TestRail integration
  - [ ] Implement Slack/Teams notifications
  - [ ] Create email reporting system
  - [ ] Add CI/CD pipeline integration

### **📚 Priority 6: Documentation & Training**
- [ ] **User Documentation**
  - [ ] Create comprehensive user guide
  - [ ] Add video tutorials and demos
  - [ ] Implement interactive help system
  - [ ] Create troubleshooting guides

- [ ] **Team Training**
  - [ ] Develop training materials
  - [ ] Create certification program
  - [ ] Implement best practices workshops
  - [ ] Add team adoption tracking

## License

This project is designed for educational and professional QA purposes. ISTQB content is used under fair use guidelines with proper attribution.
