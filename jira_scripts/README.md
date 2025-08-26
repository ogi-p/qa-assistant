# Jira Integration Scripts

This directory contains all Jira integration tools for the QA Assistant project. All scripts are tested and working.

## 🚀 Quick Start

### **Core Scripts (Most Used)**
```bash
# Read any Jira ticket
python3 jira_scripts/jira_ticket_reader.py AP-XXXXX

# See your QA workload (active tickets only)
python3 jira_scripts/qa_workload_reader.py

# Complete assignment overview (active tickets only)
python3 jira_scripts/my_assignments.py

# Interactive ticket reader
python3 jira_scripts/interactive_jira_reader.py
```

## 📁 Script Organization

### **🔧 Core Scripts**
- **`jira_ticket_reader.py`** - Read any Jira ticket with comprehensive data extraction
- **`interactive_jira_reader.py`** - Interactive menu system for multiple ticket reading
- **`qa_workload_reader.py`** - Find and analyze tickets where you are QA Assignee
- **`my_assignments.py`** - Complete overview of all assignments (regular + QA)

### **🛠️ Utility Scripts**
- **`simple_qa_workload.py`** - Simple view of assignments with QA field
- **`find_qa_assignments.py`** - Search strategies for QA assignments
- **`test_jql_search.py`** - JQL search testing and validation

### **📚 Documentation**
- **`README.md`** - This file - complete documentation
- **`jira_status_labels_mapping.md`** - Comprehensive mapping of Jira statuses and labels
- **`quick_reference.md`** - Quick reference guide for common workflows
- **`PR_SUMMARY.md`** - PR summary for reviewers

## 🎯 Script Details

### **`jira_ticket_reader.py`**
**Purpose:** Read any Jira ticket and extract all available information
```bash
python3 jira_scripts/jira_ticket_reader.py AP-20641
```
**Features:**
- Basic ticket information (summary, status, priority, labels)
- People information (assignee, reporter, QA assignee)
- Custom fields with proper field name mapping
- Comments with authors and timestamps
- Timeline information (created, updated, due dates)
- Metadata (votes, watches, progress, time tracking)

### **`interactive_jira_reader.py`**
**Purpose:** Interactive interface to read multiple tickets
```bash
python3 jira_scripts/interactive_jira_reader.py
```
**Features:**
- User-friendly interface with clear prompts
- Read multiple tickets in one session
- Graceful error handling
- Easy exit with 'quit' or 'exit'

### **`qa_workload_reader.py`**
**Purpose:** Find tickets where you are QA Assignee
```bash
python3 jira_scripts/qa_workload_reader.py
python3 jira_scripts/qa_workload_reader.py --summary-only
python3 jira_scripts/qa_workload_reader.py --status "To Do"
```
**Features:**
- Finds all tickets where you are QA Assignee
- Excludes completed tickets (Done status)
- Workload summary by status, type, and priority
- Filter by status, project, or show summary only

### **`my_assignments.py`**
**Purpose:** Complete overview of all your assignments
```bash
python3 jira_scripts/my_assignments.py
```
**Features:**
- Shows both regular assignee and QA assignee tickets
- Excludes completed tickets (Done status)
- Complete breakdown by status, type, and priority
- Summary statistics for workload planning

### **`simple_qa_workload.py`**
**Purpose:** Simple view of tickets where you are assignee with QA field
```bash
python3 jira_scripts/simple_qa_workload.py
```
**Features:**
- Quick overview of your assignments
- Shows QA Assignee field for each ticket
- Simple, clean output

### **`find_qa_assignments.py`**
**Purpose:** Search strategies to find QA assignments
```bash
python3 jira_scripts/find_qa_assignments.py
```
**Features:**
- Different search strategies for QA assignments
- Useful for debugging QA assignment issues
- Shows search process and results

### **`test_jql_search.py`**
**Purpose:** Test JQL search capabilities
```bash
python3 jira_scripts/test_jql_search.py
```
**Features:**
- Test various JQL queries
- Validate custom field accessibility
- Debug search issues

## 📊 Current Capabilities

### **✅ Data Extraction**
- Basic ticket information (summary, status, priority, labels)
- People information (assignee, reporter, QA assignee)
- Custom fields with proper field name mapping
- Comments with authors and timestamps
- Timeline information (created, updated, due dates)
- Metadata (votes, watches, progress, time tracking)

### **✅ Workload Analysis**
- Total assignment counts
- Breakdown by assignment type (regular vs QA)
- Status distribution analysis
- Issue type and priority analysis
- Recently updated tickets tracking

### **✅ QA-Specific Features**
- Automatic QA Assignee field detection
- QA workload filtering and analysis
- QA assignment tracking across projects
- QA-specific status monitoring

## 🔧 Technical Implementation

### **✅ Error Handling**
- Comprehensive error handling for API failures
- Graceful degradation when fields are missing
- Clear error messages and debugging information
- Rate limiting considerations

### **✅ Configuration**
- Environment-based configuration (`.env` file)
- YAML configuration support
- Flexible field mapping
- Extensible architecture

### **✅ Documentation**
- Complete README with usage examples
- Comprehensive status and label mapping
- Quick reference guide
- Best practices documentation

## 🎯 Use Cases

### **For QA Team**
- Track QA assignments across all projects
- Monitor workload and capacity
- Understand ticket status and progress
- Generate workload reports

### **For Developers**
- Read ticket details quickly
- Understand QA requirements
- Track development progress
- Monitor peer review status

### **For Project Managers**
- Monitor team workload
- Track project progress
- Understand status distributions
- Generate project reports

## 📋 Requirements

### **Dependencies**
- Python 3.7+
- `requests` library
- `python-dotenv` library
- `PyYAML` library

### **Configuration**
- `.env` file with Jira credentials
- Jira server URL, email, and API token
- Proper permissions to read tickets

### **Installation**
```bash
pip3 install -r requirements.txt
```

## 🚨 Troubleshooting

### **Common Issues**
1. **Authentication Error (401):** Check your API token in `.env`
2. **Permission Error (403):** Verify you have access to the tickets
3. **Connection Error:** Check your Jira server URL
4. **Import Error:** Ensure all dependencies are installed

### **Debug Mode**
Most scripts provide detailed error messages. Check the output for specific error details.

## 🔮 Future Development

These scripts are part of the larger Jira integration system. Future versions will include:
- Ticket creation capabilities
- Comment posting functionality
- Status change operations
- Bulk operations
- Integration with the main QA Assistant workflow

## 📝 Notes

- All scripts are well-documented and tested
- Error handling is comprehensive
- Configuration is flexible and environment-based
- Documentation is complete and user-friendly
- Code follows Python best practices

---

**For detailed information:** See `jira_status_labels_mapping.md` and `quick_reference.md`
