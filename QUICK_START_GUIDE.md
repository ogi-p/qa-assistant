# QA Assistant - Quick Start Guide

**Welcome to the QA Assistant project!** This guide will help you set up the project on your computer in just a few minutes.

---

## 🚀 **Prerequisites**

Before you start, make sure you have:

- **Python 3.7 or higher** installed on your computer
- **Git** installed for cloning the repository
- **A Jira account** with API access (for Jira integration features)
- **Basic familiarity with command line/terminal**

---

## 📥 **Step 1: Clone the Repository**

Open your terminal and run:

```bash
git clone <repository-url>
cd qa_assistant_igor
```

Replace `<repository-url>` with the actual GitHub repository URL.

---

## 🐍 **Step 2: Set Up Python Environment**

### **Option A: Using Virtual Environment (Recommended)**

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **Option B: Using System Python**

```bash
# Install dependencies directly
pip3 install -r requirements.txt --break-system-packages
```

**Note:** If you get permission errors, you might need to use `pip3` instead of `pip`.

---

## ⚙️ **Step 3: Configure Jira Integration**

### **3.1: Get Your Jira API Token**

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **"Create API token"**
3. Give it a name (e.g., "QA Assistant")
4. Copy the generated token (you'll need it in the next step)

### **3.2: Create Environment File**

Create a `.env` file in the project root:

```bash
# Create the .env file
touch .env
```

**Or use the setup script:**
```bash
python3 setup.py
```
*This will create a `.env.template` file for you to copy and customize.*

### **3.3: Add Your Jira Credentials**

Open the `.env` file and add your Jira credentials:

```env
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@domain.com
JIRA_API_TOKEN=your-api-token-here
JIRA_DEFAULT_PROJECT=AP
```

**Replace with your actual values:**
- `your-domain.atlassian.net` → Your Jira server URL
- `your-email@domain.com` → Your Jira email address
- `your-api-token-here` → The API token you created in step 3.1
- `AP` → Your default project key (optional)

---

## ✅ **Step 4: Test Your Setup**

### **4.1: Test Jira Connection**

```bash
# Test reading a Jira ticket
python3 jira_scripts/jira_ticket_reader.py AP-20641
```

**Expected Output:**
```
🔍 Reading Ticket AP-20641...
============================================================
✅ Successfully read ticket AP-20641!

📋 Basic Information:
   🆔 Key: AP-20641
   📝 Summary: [FE] Add "Delete folder" modal
   📊 Status: Peer review
   ...
```

### **4.2: Test Your Workload**

```bash
# See your QA workload
python3 jira_scripts/qa_workload_reader.py --summary-only

# See all your assignments
python3 jira_scripts/my_assignments.py
```

---

## 🎯 **Step 5: Start Using the QA Assistant**

### **Quick Commands You'll Use Most:**

```bash
# Read any Jira ticket
python3 jira_scripts/jira_ticket_reader.py AP-XXXXX

# See your QA workload (active tickets only)
python3 jira_scripts/qa_workload_reader.py

# Complete assignment overview
python3 jira_scripts/my_assignments.py

# Interactive ticket reader
python3 jira_scripts/interactive_jira_reader.py
```

### **What Each Tool Does:**

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `jira_ticket_reader.py` | Read detailed ticket information | When you need to understand a specific ticket |
| `qa_workload_reader.py` | See your QA assignments | Daily to check your workload |
| `my_assignments.py` | See all your assignments | Weekly to understand your total workload |
| `interactive_jira_reader.py` | Read multiple tickets interactively | When you need to review several tickets |

---

## 📚 **Step 6: Learn the Documentation**

### **Essential Files to Read:**

1. **`jira_scripts/quick_reference.md`** - Quick reference for Jira statuses and labels
2. **`jira_scripts/jira_status_labels_mapping.md`** - Comprehensive Jira workflow guide
3. **`jira_scripts/README.md`** - Complete documentation for all tools

### **Project Structure:**

```
qa_assistant_igor/
├── jira_scripts/           # 🎯 Main tools you'll use
│   ├── jira_ticket_reader.py      # Read any ticket
│   ├── qa_workload_reader.py      # Your QA workload
│   ├── my_assignments.py          # All assignments
│   └── interactive_jira_reader.py # Interactive tool
├── templates/              # Reusable templates
├── local_docs/            # Project documentation
├── .env                   # ⚠️ Your credentials (keep private!)
└── requirements.txt       # Python dependencies
```

---

## 🚨 **Troubleshooting**

### **Common Issues and Solutions:**

#### **1. "Module not found" errors**
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### **2. "Authentication failed" errors**
- Check your `.env` file has correct credentials
- Verify your API token is valid
- Make sure your Jira server URL is correct

#### **3. "Permission denied" errors**
```bash
# On macOS/Linux, you might need:
chmod +x jira_scripts/*.py
```

#### **4. "pip not found" errors**
```bash
# Try using pip3 instead
pip3 install -r requirements.txt
```

### **Getting Help:**

1. **Check the error message** - Most scripts provide detailed error information
2. **Verify your `.env` file** - Make sure credentials are correct
3. **Test with a known ticket** - Try `AP-20641` which should work
4. **Check your internet connection** - Scripts need to connect to Jira

---

## 🎉 **You're Ready!**

### **Next Steps:**

1. **✅ Test the basic commands** above
2. **📖 Read the quick reference** (`jira_scripts/quick_reference.md`)
3. **🔧 Start using the tools** for your daily QA work
4. **📚 Explore the documentation** as you need it

### **Daily Workflow:**

```bash
# Start your day - check your workload
python3 jira_scripts/qa_workload_reader.py

# Read a specific ticket you're working on
python3 jira_scripts/jira_ticket_reader.py AP-XXXXX

# End your day - see your progress
python3 jira_scripts/my_assignments.py
```

---

## 📞 **Need Help?**

- **Check the documentation** in `jira_scripts/README.md`
- **Review the troubleshooting section** above
- **Test with known working tickets** like `AP-20641`
- **Verify your Jira credentials** are correct

---

**Welcome to the QA Assistant! 🚀**

*This tool will help you manage your QA workload more efficiently and stay organized with your Jira tickets.*
