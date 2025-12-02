# Generate Automated Test from Manual Test Case
# Usage: .\generate-test.ps1 -TestCaseId "TC-001" -Output ".\scripts\functional\login\"

param(
    [Parameter(Mandatory=$true)]
    [string]$TestCaseId,
    
    [Parameter(Mandatory=$true)]
    [string]$Output,
    
    [Parameter(Mandatory=$false)]
    [string]$TestType = "functional",
    
    [Parameter(Mandatory=$false)]
    [string]$Template = "playwright_test_template.js"
)

Write-Host "🤖 Playwright Test Generator - Manual QA Framework" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# Paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir
$testCasesDir = Join-Path (Split-Path -Parent $rootDir) "03-test-plans"
$templatesDir = Join-Path $rootDir "templates"
$templatePath = Join-Path $templatesDir $Template

# Validate template exists
if (!(Test-Path $templatePath)) {
    Write-Host "❌ Error: Template not found: $Template" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Searching for test case: $TestCaseId..." -ForegroundColor Yellow

# Search for test case file
$testCaseFile = Get-ChildItem -Path $testCasesDir -Recurse -Filter "*.md" | 
    Where-Object { $_.BaseName -match $TestCaseId -or (Get-Content $_.FullName -Raw) -match "Test Case ID.*$TestCaseId" } | 
    Select-Object -First 1

if (!$testCaseFile) {
    Write-Host "❌ Error: Test case $TestCaseId not found in $testCasesDir" -ForegroundColor Red
    Write-Host "💡 Make sure the test case exists and contains 'Test Case ID: $TestCaseId'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found test case: $($testCaseFile.FullName)" -ForegroundColor Green

# Parse test case content
$testCaseContent = Get-Content $testCaseFile.FullName -Raw

# Extract test case information using regex
$testCaseTitle = if ($testCaseContent -match '##\s*Test Case Header.*?Title.*?:\s*\[(.*?)\]') { $Matches[1] } else { "Unknown Test Case" }
$testType = if ($testCaseContent -match 'Test Type.*?:\s*\[(.*?)\]') { $Matches[1] } else { "Functional" }
$priority = if ($testCaseContent -match 'Priority.*?:\s*\[(.*?)\]') { $Matches[1] } else { "Medium" }
$jiraTicket = if ($testCaseContent -match 'Jira Ticket.*?:\s*\[(.*?)\]') { $Matches[1] } else { "N/A" }
$requirements = if ($testCaseContent -match 'Requirements.*?:\s*\[(.*?)\]') { $Matches[1] } else { "N/A" }
$environment = if ($testCaseContent -match 'Environment.*?:\s*\[(.*?)\]') { $Matches[1] } else { "dev" }
$testUser = if ($testCaseContent -match 'Users.*?:\s*\[(.*?)\]') { $Matches[1] } else { "qa_admin" }

# Extract preconditions
$preconditions = ""
if ($testCaseContent -match '##\s*3\.\s*Preconditions(.*?)##\s*4\.') {
    $preconditionsSection = $Matches[1]
    $preconditionsArray = $preconditionsSection -split '\n' | Where-Object { $_ -match '^\s*-' }
    $preconditions = ($preconditionsArray | ForEach-Object { " * $_" }) -join "`n"
}

# Extract test steps
$testSteps = ""
if ($testCaseContent -match '##\s*4\.\s*Test Steps(.*?)##\s*5\.') {
    $testStepsSection = $Matches[1]
    $testStepsArray = $testStepsSection -split '\n' | Where-Object { $_ -match '^\s*\d+\.' }
    $testSteps = ($testStepsArray | ForEach-Object { " * $_" }) -join "`n"
}

# Extract expected results
$expectedResults = ""
if ($testCaseContent -match '##\s*5\.\s*Expected Results(.*?)##\s*6\.') {
    $expectedResultsSection = $Matches[1]
    $expectedResultsArray = $expectedResultsSection -split '\n' | Where-Object { $_ -match '^\s*-' }
    $expectedResults = ($expectedResultsArray | ForEach-Object { " * $_" }) -join "`n"
}

Write-Host ""
Write-Host "📝 Test Case Information:" -ForegroundColor Cyan
Write-Host "   Test ID: $TestCaseId" -ForegroundColor White
Write-Host "   Title: $testCaseTitle" -ForegroundColor White
Write-Host "   Type: $testType" -ForegroundColor White
Write-Host "   Priority: $priority" -ForegroundColor White
Write-Host "   JIRA: $jiraTicket" -ForegroundColor White
Write-Host "   Requirements: $requirements" -ForegroundColor White
Write-Host "   Environment: $environment" -ForegroundColor White
Write-Host "   User: $testUser" -ForegroundColor White
Write-Host ""

# Load template
$templateContent = Get-Content $templatePath -Raw

# Replace placeholders
$testContent = $templateContent `
    -replace '{{TEST_CASE_ID}}', $TestCaseId `
    -replace '{{TEST_CASE_TITLE}}', $testCaseTitle `
    -replace '{{TEST_TYPE}}', $testType `
    -replace '{{PRIORITY}}', $priority `
    -replace '{{JIRA_TICKET}}', $jiraTicket `
    -replace '{{REQUIREMENTS}}', $requirements `
    -replace '{{ENVIRONMENT}}', $environment `
    -replace '{{TEST_USER}}', $testUser `
    -replace '{{USER_TYPE}}', $testUser.Split('@')[0] `
    -replace '{{PRECONDITIONS}}', $preconditions `
    -replace '{{TEST_STEPS}}', $testSteps `
    -replace '{{EXPECTED_RESULTS}}', $expectedResults `
    -replace '{{GENERATION_DATE}}', (Get-Date -Format "yyyy-MM-dd HH:mm:ss") `
    -replace '{{TEST_SUITE_NAME}}', "$testCaseTitle Tests" `
    -replace '{{TEST_IMPLEMENTATION}}', "// TODO: Implement test steps based on manual test case" `
    -replace '{{ASSERTIONS}}', "// TODO: Add assertions based on expected results"

# Create output directory if it doesn't exist
if (!(Test-Path $Output)) {
    New-Item -Path $Output -ItemType Directory -Force | Out-Null
}

# Generate output file name
$outputFileName = "$TestCaseId-$($testCaseTitle -replace '[^a-zA-Z0-9]', '-').spec.js"
$outputPath = Join-Path $Output $outputFileName

# Write test file
Set-Content -Path $outputPath -Value $testContent

Write-Host "✅ Automated test generated successfully!" -ForegroundColor Green
Write-Host "📁 Output: $outputPath" -ForegroundColor White
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Review and complete the TODO sections in the generated test" -ForegroundColor Yellow
Write-Host "   2. Implement test steps based on manual test case" -ForegroundColor Yellow
Write-Host "   3. Add assertions for expected results" -ForegroundColor Yellow
Write-Host "   4. Run the test: npm test $outputPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 Happy Testing!" -ForegroundColor Green

