#!/bin/bash
# Record User Interactions and Generate Test Code
# Usage: ./record-test.sh -n folder-creation -o ./recordings/ -e dev

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m'

# Default values
OUTPUT_DIR="./recordings/"
ENVIRONMENT="dev"
START_URL=""

# Parse arguments
while getopts "n:o:e:u:" opt; do
  case $opt in
    n) TEST_NAME="$OPTARG";;
    o) OUTPUT_DIR="$OPTARG";;
    e) ENVIRONMENT="$OPTARG";;
    u) START_URL="$OPTARG";;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1;;
  esac
done

# Validate required arguments
if [ -z "$TEST_NAME" ]; then
    echo -e "${RED}❌ Error: Missing required argument: -n TEST_NAME${NC}"
    echo "Usage: $0 -n TEST_NAME [-o OUTPUT_DIR] [-e ENVIRONMENT] [-u START_URL]"
    echo "Example: $0 -n folder-creation -o ./recordings/ -e dev"
    exit 1
fi

echo -e "${CYAN}🎬 Playwright Test Recorder - Manual QA Framework${NC}"
echo -e "${CYAN}===================================================${NC}"
echo ""

# Determine script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$ROOT_DIR/config"
ENV_CONFIG_PATH="$CONFIG_DIR/test-environments.json"

# Load environment configuration
if [ ! -f "$ENV_CONFIG_PATH" ]; then
    echo -e "${RED}❌ Error: Environment configuration not found: $ENV_CONFIG_PATH${NC}"
    exit 1
fi

# Extract base URL from environment config
BASE_URL=$(cat "$ENV_CONFIG_PATH" | grep -A 10 "\"$ENVIRONMENT\"" | grep -oP '"url":\s*"\K[^"]+' | head -n 1)

if [ -z "$BASE_URL" ]; then
    echo -e "${RED}❌ Error: Environment '$ENVIRONMENT' not found in configuration${NC}"
    exit 1
fi

if [ -n "$START_URL" ]; then
    BASE_URL="$START_URL"
fi

echo -e "${CYAN}📝 Recording Configuration:${NC}"
echo -e "${WHITE}   Test Name: $TEST_NAME${NC}"
echo -e "${WHITE}   Environment: $ENVIRONMENT${NC}"
echo -e "${WHITE}   Start URL: $BASE_URL${NC}"
echo -e "${WHITE}   Output Directory: $OUTPUT_DIR${NC}"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate output file name
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
RECORDING_FILE_NAME="$TEST_NAME-$TIMESTAMP.spec.js"
RECORDING_PATH="$OUTPUT_DIR/$RECORDING_FILE_NAME"

echo -e "${YELLOW}🚀 Starting Playwright Test Recorder...${NC}"
echo ""
echo -e "${CYAN}📋 Instructions:${NC}"
echo -e "${WHITE}   1. A browser window will open${NC}"
echo -e "${WHITE}   2. Perform the actions you want to record${NC}"
echo -e "${WHITE}   3. Playwright will generate test code automatically${NC}"
echo -e "${WHITE}   4. Close the browser when done to save the recording${NC}"
echo ""
echo -e "${YELLOW}⏸️  Press Ctrl+C to cancel...${NC}"
echo ""

# Run Playwright codegen
echo -e "${YELLOW}💡 Note: This requires the Playwright MCP server for full functionality${NC}"
echo -e "${YELLOW}   Using direct npx codegen as fallback...${NC}"
echo ""

npx -y @playwright/test codegen \
  --target=playwright-test \
  --output="$RECORDING_PATH" \
  "$BASE_URL"

# Check if recording was saved
if [ -f "$RECORDING_PATH" ]; then
    echo ""
    echo -e "${GREEN}✅ Recording saved successfully!${NC}"
    echo -e "${WHITE}📁 Output: $RECORDING_PATH${NC}"
    echo ""
    echo -e "${CYAN}📝 Next Steps:${NC}"
    echo -e "${YELLOW}   1. Review the generated test code${NC}"
    echo -e "${YELLOW}   2. Add test assertions and validations${NC}"
    echo -e "${YELLOW}   3. Add test metadata (test case ID, requirements, etc.)${NC}"
    echo -e "${YELLOW}   4. Move to appropriate test suite folder${NC}"
    echo -e "${YELLOW}   5. Run the test: npm test $RECORDING_PATH${NC}"
    echo ""
else
    echo ""
    echo -e "${YELLOW}⚠️  Recording was cancelled or failed${NC}"
    echo ""
fi

echo -e "${GREEN}🎉 Happy Testing!${NC}"

