#!/bin/bash
# Run Playwright Test Suite
# Usage: ./run-tests.sh -s regression -e staging -b chromium

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m'

# Default values
ENVIRONMENT="dev"
BROWSER="chromium"
SUITE=""
DEBUG=false
HEADED=false
REPORTER="html,list"

# Parse arguments
while getopts "s:e:b:r:dh" opt; do
  case $opt in
    s) SUITE="$OPTARG";;
    e) ENVIRONMENT="$OPTARG";;
    b) BROWSER="$OPTARG";;
    r) REPORTER="$OPTARG";;
    d) DEBUG=true;;
    h) HEADED=true;;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1;;
  esac
done

echo -e "${CYAN}🧪 Playwright Test Runner - Manual QA Framework${NC}"
echo -e "${CYAN}=================================================${NC}"
echo ""

# Determine script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$ROOT_DIR/config"
SCRIPTS_DIR="$ROOT_DIR/scripts"
CONFIG_PATH="$CONFIG_DIR/playwright.config.js"

# Validate config exists
if [ ! -f "$CONFIG_PATH" ]; then
    echo -e "${RED}❌ Error: Playwright configuration not found: $CONFIG_PATH${NC}"
    exit 1
fi

echo -e "${CYAN}📝 Test Execution Configuration:${NC}"
echo -e "${WHITE}   Environment: $ENVIRONMENT${NC}"
echo -e "${WHITE}   Browser: $BROWSER${NC}"
echo -e "${WHITE}   Suite: ${SUITE:-All tests}${NC}"
echo -e "${WHITE}   Debug Mode: $DEBUG${NC}"
echo -e "${WHITE}   Headed: $HEADED${NC}"
echo -e "${WHITE}   Reporter: $REPORTER${NC}"
echo ""

# Build test path
TEST_PATH="$SCRIPTS_DIR"
if [ -n "$SUITE" ]; then
    SUITE_PATH="$SCRIPTS_DIR/$SUITE"
    if [ -d "$SUITE_PATH" ]; then
        TEST_PATH="$SUITE_PATH"
    else
        echo -e "${YELLOW}⚠️  Warning: Suite directory not found: $SUITE_PATH${NC}"
        echo -e "${YELLOW}   Running all tests instead...${NC}"
        echo ""
    fi
fi

# Build playwright command
PLAYWRIGHT_CMD="npx -y @playwright/test test"
PLAYWRIGHT_CMD="$PLAYWRIGHT_CMD $TEST_PATH"
PLAYWRIGHT_CMD="$PLAYWRIGHT_CMD --project=$BROWSER"

# Add reporters
IFS=',' read -ra REPORTERS <<< "$REPORTER"
for r in "${REPORTERS[@]}"; do
    PLAYWRIGHT_CMD="$PLAYWRIGHT_CMD --reporter=$r"
done

# Add headed mode
if [ "$HEADED" = true ]; then
    PLAYWRIGHT_CMD="$PLAYWRIGHT_CMD --headed"
fi

# Add debug mode
if [ "$DEBUG" = true ]; then
    PLAYWRIGHT_CMD="$PLAYWRIGHT_CMD --debug"
    echo -e "${YELLOW}🐛 Debug Mode: Playwright Inspector will open${NC}"
    echo ""
fi

# Set environment variables
export TEST_ENV="$ENVIRONMENT"
export BASE_URL=""

# Load base URL from environment config
ENV_CONFIG_PATH="$CONFIG_DIR/test-environments.json"
if [ -f "$ENV_CONFIG_PATH" ]; then
    BASE_URL=$(cat "$ENV_CONFIG_PATH" | grep -A 10 "\"$ENVIRONMENT\"" | grep -oP '"url":\s*"\K[^"]+' | head -n 1)
    if [ -n "$BASE_URL" ]; then
        export BASE_URL="$BASE_URL"
        echo -e "${CYAN}🌐 Base URL: $BASE_URL${NC}"
        echo ""
    fi
fi

echo -e "${YELLOW}🚀 Starting Playwright tests...${NC}"
echo -e "${GRAY}Command: $PLAYWRIGHT_CMD${NC}"
echo ""
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Run Playwright tests
eval $PLAYWRIGHT_CMD
EXIT_CODE=$?

echo ""
echo -e "${GRAY}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo -e "${RED}❌ Some tests failed${NC}"
fi

echo ""
echo -e "${CYAN}📊 Test Reports:${NC}"

REPORT_DIR="$ROOT_DIR/reports"
if [ -d "$REPORT_DIR" ]; then
    HTML_REPORT="$REPORT_DIR/html/index.html"
    if [ -f "$HTML_REPORT" ]; then
        echo -e "${WHITE}   HTML Report: $HTML_REPORT${NC}"
        echo -e "${YELLOW}   Open with: open $HTML_REPORT${NC}"
    fi
    
    JSON_REPORT="$REPORT_DIR/results.json"
    if [ -f "$JSON_REPORT" ]; then
        echo -e "${WHITE}   JSON Report: $JSON_REPORT${NC}"
    fi
    
    JUNIT_REPORT="$REPORT_DIR/junit.xml"
    if [ -f "$JUNIT_REPORT" ]; then
        echo -e "${WHITE}   JUnit Report: $JUNIT_REPORT${NC}"
    fi
fi

echo ""
echo -e "${CYAN}📸 Screenshots & Videos:${NC}"
TEST_RESULTS_DIR="$ROOT_DIR/test-results"
if [ -d "$TEST_RESULTS_DIR" ]; then
    echo -e "${WHITE}   Test Results: $TEST_RESULTS_DIR${NC}"
fi

echo ""

exit $EXIT_CODE

