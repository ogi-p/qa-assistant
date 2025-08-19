# Sample Bug Report: Address Verification Script

## Title
Script fails to process CSV when column indices are incorrect, causing IndexError

## Environment
- **Environment**: stage
- **APP**: Enterprise
- **Browser**: Chrome 120.0.6099.109

## Steps to Reproduce
1. Modify the script to use incorrect column indices (e.g., change ADDRESS_COLUMN from 2 to 10)
2. Ensure CSV file has fewer than 11 columns
3. Run the script: `/usr/bin/python3 process_addresses.py`
4. Observe the error

## Expected Result
Script should handle invalid column indices gracefully and provide a clear error message indicating the issue with column access.

## Actual Result
Script crashes with IndexError: list index out of range, providing no helpful information about the root cause.

## Severity/Priority
**Medium** - Script fails completely when column configuration is incorrect, but issue is easily preventable with proper validation.

## Notes/Attachments
- Error occurs in the main processing loop when trying to access `row[ADDRESS_COLUMN]`
- No validation is performed on column indices before processing
- Suggested fix: Add column count validation at script startup
