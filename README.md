# QA Assistant - Igor

A specialized AI assistant designed to help QA professionals generate test cases, write bug reports, and follow QA best practices with ISTQB knowledge.

## Quick Start

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

## Future Enhancements & Recommendations

### **Template Improvements**
- [ ] Create generic templates for common testing scenarios (web, mobile, API)
- [ ] Add industry-specific template variations
- [ ] Develop template validation scripts
- [ ] Create template customization guidelines

### **Context Management**
- [ ] Implement automatic project folder creation
- [ ] Add context file validation and formatting
- [ ] Create context migration tools for existing projects
- [ ] Develop context search and indexing capabilities

### **AI Assistant Enhancements**
- [ ] Improve ISTQB knowledge integration
- [ ] Add automatic template selection based on project type
- [ ] Implement context-aware response generation
- [ ] Create personality consistency validation

### **File Organization**
- [ ] Add automated file naming with timestamps
- [ ] Implement project backup and archiving
- [ ] Create file structure validation scripts
- [ ] Add project metadata tracking

### **Quality Assurance**
- [ ] Add template quality scoring
- [ ] Implement best practices validation
- [ ] Develop quality metrics and reporting

## License

This project is designed for educational and professional QA purposes. ISTQB content is used under fair use guidelines with proper attribution.
