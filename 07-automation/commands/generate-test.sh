#!/bin/bash
# Generate Automated Test from Manual Test Case
# Usage: ./generate-test.sh -t TC-001 -o ./scripts/functional/login/

# Colors for output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Default values
TEST_TYPE="functional"
TEMPLATE="playwright_test_template.js"

# Parse command line arguments
while getopts "t:o:y:m:" opt; do
  case $opt in
    t) TEST_CASE_ID="$OPTARG";;
    o) OUTPUT_DIR="$OPTARG";;
    y) TEST_TYPE="$OPTARG";;
    m) TEMPLATE="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1;;
  esac
done

# Validate required arguments
if [ -z "$TEST_CASE_ID" ] || [ -z "$OUTPUT_DIR" ]; then
    echo -e "${RED}❌ Error: Missing required arguments${NC}"
    echo "Usage: $0 -t TEST_CASE_ID -o OUTPUT_DIR [-y TEST_TYPE] [-m TEMPLATE]"
    echo "Example: $0 -t TC-001 -o ./scripts/functional/login/"
    exit 1
fi

echo -e "${CYAN}🤖 Playwright Test Generator - Manual QA Framework${NC}"
echo -e "${CYAN}=====================================================${NC}"
echo ""

# Determine script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
TEST_CASES_DIR="$(dirname "$ROOT_DIR")/03-test-plans"
TEMPLATES_DIR="$ROOT_DIR/templates"
TEMPLATE_PATH="$TEMPLATES_DIR/$TEMPLATE"

# Validate template exists
if [ ! -f "$TEMPLATE_PATH" ]; then
    echo -e "${RED}❌ Error: Template not found: $TEMPLATE${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Searching for test case: $TEST_CASE_ID...${NC}"

# Search for test case file
TEST_CASE_FILE=$(find "$TEST_CASES_DIR" -type f -name "*.md" -exec grep -l "Test Case ID.*$TEST_CASE_ID" {} \; | head -n 1)

if [ -z "$TEST_CASE_FILE" ]; then
    echo -e "${RED}❌ Error: Test case $TEST_CASE_ID not found in $TEST_CASES_DIR${NC}"
    echo -e "${YELLOW}💡 Make sure the test case exists and contains 'Test Case ID: $TEST_CASE_ID'${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found test case: $TEST_CASE_FILE${NC}"

# Parse test case content
TEST_CASE_CONTENT=$(<"$TEST_CASE_FILE")

# Extract test case information
TEST_CASE_TITLE=$(echo "$TEST_CASE_CONTENT" | grep -oP 'Title.*?:\s*\[\K[^\]]+' || echo "Unknown Test Case")
TEST_TYPE_PARSED=$(echo "$TEST_CASE_CONTENT" | grep -oP 'Test Type.*?:\s*\[\K[^\]]+' || echo "Functional")
PRIORITY=$(echo "$TEST_CASE_CONTENT" | grep -oP 'Priority.*?:\s*\[\K[^\]]+' || echo "Medium")
JIRA_TICKET=$(echo "$TEST_CASE_CONTENT" | grep -oP 'Jira Ticket.*?:\s*\[\K[^\]]+' || echo "N/A")
REQUIREMENTS=$(echo "$TEST_CASE_CONTENT" | grep -oP 'Requirements.*?:\s*\[\K[^\]]+' || echo "N/A")
ENVIRONMENT=$(echo "$TEST_CASE_CONTENT" | grep -oP 'Environment.*?:\s*\[\K[^\]]+' || echo "dev")
TEST_USER=$(echo "$TEST_CASE_CONTENT" | grep -oP 'Users.*?:\s*\[\K[^\]]+' || echo "qa_admin")

# Extract preconditions, steps, and results (simplified extraction)
PRECONDITIONS=$(echo "$TEST_CASE_CONTENT" | awk '/## 3. Preconditions/,/## 4./ {if (!/##/) print}')
TEST_STEPS=$(echo "$TEST_CASE_CONTENT" | awk '/## 4. Test Steps/,/## 5./ {if (!/##/) print}')
EXPECTED_RESULTS=$(echo "$TEST_CASE_CONTENT" | awk '/## 5. Expected Results/,/## 6./ {if (!/##/) print}')

echo ""
echo -e "${CYAN}📝 Test Case Information:${NC}"
echo -e "${WHITE}   Test ID: $TEST_CASE_ID${NC}"
echo -e "${WHITE}   Title: $TEST_CASE_TITLE${NC}"
echo -e "${WHITE}   Type: $TEST_TYPE_PARSED${NC}"
echo -e "${WHITE}   Priority: $PRIORITY${NC}"
echo -e "${WHITE}   JIRA: $JIRA_TICKET${NC}"
echo -e "${WHITE}   Requirements: $REQUIREMENTS${NC}"
echo -e "${WHITE}   Environment: $ENVIRONMENT${NC}"
echo -e "${WHITE}   User: $TEST_USER${NC}"
echo ""

# Load template
TEMPLATE_CONTENT=$(<"$TEMPLATE_PATH")

# Get user type from email (before @)
USER_TYPE=$(echo "$TEST_USER" | cut -d'@' -f1)

# Replace placeholders
TEST_CONTENT="$TEMPLATE_CONTENT"
TEST_CONTENT="${TEST_CONTENT//\{\{TEST_CASE_ID\}\}/$TEST_CASE_ID}"
TEST_CONTENT="${TEST_CONTENT//\{\{TEST_CASE_TITLE\}\}/$TEST_CASE_TITLE}"
TEST_CONTENT="${TEST_CONTENT//\{\{TEST_TYPE\}\}/$TEST_TYPE_PARSED}"
TEST_CONTENT="${TEST_CONTENT//\{\{PRIORITY\}\}/$PRIORITY}"
TEST_CONTENT="${TEST_CONTENT//\{\{JIRA_TICKET\}\}/$JIRA_TICKET}"
TEST_CONTENT="${TEST_CONTENT//\{\{REQUIREMENTS\}\}/$REQUIREMENTS}"
TEST_CONTENT="${TEST_CONTENT//\{\{ENVIRONMENT\}\}/$ENVIRONMENT}"
TEST_CONTENT="${TEST_CONTENT//\{\{TEST_USER\}\}/$TEST_USER}"
TEST_CONTENT="${TEST_CONTENT//\{\{USER_TYPE\}\}/$USER_TYPE}"
TEST_CONTENT="${TEST_CONTENT//\{\{PRECONDITIONS\}\}/$PRECONDITIONS}"
TEST_CONTENT="${TEST_CONTENT//\{\{TEST_STEPS\}\}/$TEST_STEPS}"
TEST_CONTENT="${TEST_CONTENT//\{\{EXPECTED_RESULTS\}\}/$EXPECTED_RESULTS}"
TEST_CONTENT="${TEST_CONTENT//\{\{GENERATION_DATE\}\}/$(date '+%Y-%m-%d %H:%M:%S')}"
TEST_CONTENT="${TEST_CONTENT//\{\{TEST_SUITE_NAME\}\}/$TEST_CASE_TITLE Tests}"
TEST_CONTENT="${TEST_CONTENT//\{\{TEST_IMPLEMENTATION\}\}/\/\/ TODO: Implement test steps based on manual test case}"
TEST_CONTENT="${TEST_CONTENT//\{\{ASSERTIONS\}\}/\/\/ TODO: Add assertions based on expected results}"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Generate output file name
OUTPUT_FILE_NAME="${TEST_CASE_ID}-$(echo "$TEST_CASE_TITLE" | tr -cs '[:alnum:]' '-').spec.js"
OUTPUT_PATH="$OUTPUT_DIR/$OUTPUT_FILE_NAME"

# Write test file
echo "$TEST_CONTENT" > "$OUTPUT_PATH"

echo -e "${GREEN}✅ Automated test generated successfully!${NC}"
echo -e "${WHITE}📁 Output: $OUTPUT_PATH${NC}"
echo ""
echo -e "${CYAN}📝 Next Steps:${NC}"
echo -e "${YELLOW}   1. Review and complete the TODO sections in the generated test${NC}"
echo -e "${YELLOW}   2. Implement test steps based on manual test case${NC}"
echo -e "${YELLOW}   3. Add assertions for expected results${NC}"
echo -e "${YELLOW}   4. Run the test: npm test $OUTPUT_PATH${NC}"
echo ""
echo -e "${GREEN}🎉 Happy Testing!${NC}"

