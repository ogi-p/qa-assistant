# QA Assistant Workshop

A specialized AI assistant designed to help QA professionals with their daily work, including test case generation, bug reporting, and QA process guidance.

## Purpose

This project provides templates, tools, and guidance for quality assurance professionals to:
- Generate practical test cases and test scenarios
- Write clear, comprehensive bug reports
- Follow QA best practices and methodologies
- Leverage ISTQB testing knowledge

## Project Structure

```
cursor-workshop/
├── .cursor/
│   ├── Additional context/     # Reference materials
│   │   ├── pdfs/              # ISTQB syllabi and documentation
│   │   └── extracted/         # Extracted text content
│   └── rules/                 # AI assistant configuration
├── templates/                 # QA templates and examples
│   ├── bug_reports/          # Bug report templates
│   ├── test_cases/           # Test case templates
│   └── test_files/           # Sample test files
└── tools/                    # Utilities and scripts (future)
```

## Features

### Templates
- **Bug Reports**: Browser-focused templates with environment, steps, and severity
- **Test Cases**: Structured templates with preconditions, steps, and expected results
- **Test Files**: Sample test artifacts and examples

### Knowledge Base
- **ISTQB Foundation Level** (v4.0.1) - Complete syllabus content
- **ISTQB Advanced Test Analyst** (v4.0) - Advanced testing techniques
- **Best Practices Enforcement** - Automatic guidance and recommendations

### AI Assistant Capabilities
- Igor personality for engaging interactions
- Best practices validation and warnings
- Context-aware responses using ISTQB knowledge
- Template generation and customization

## Getting Started

1. **Clone or download** this repository
2. **Review templates** in the `templates/` directory
3. **Customize templates** for your specific needs
4. **Use the AI assistant** for QA guidance and generation

## Configuration

The AI assistant is configured through files in `.cursor/rules/`:
- `cursor_rules.mdc` - Main configuration and behavior
- `action_log.mdc` - Action tracking and context preservation

## Dependencies

For PDF extraction capabilities:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install PyPDF2
```

## Contributing

When adding new templates or documentation:
1. Follow the established directory structure
2. Maintain consistency with existing formats
3. Update this README if adding new features

## License

This project is designed for educational and professional QA purposes. ISTQB content is used under fair use guidelines with proper attribution.
