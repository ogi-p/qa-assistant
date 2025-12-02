# Record User Interactions and Generate Test Code
# Usage: .\record-test.ps1 -TestName "folder-creation" -Output ".\recordings\" -Environment "dev"

param(
    [Parameter(Mandatory=$true)]
    [string]$TestName,
    
    [Parameter(Mandatory=$false)]
    [string]$Output = ".\recordings\",
    
    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory=$false)]
    [string]$StartURL = ""
)

Write-Host "🎬 Playwright Test Recorder - Manual QA Framework" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# Paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir
$configDir = Join-Path $rootDir "config"
$envConfigPath = Join-Path $configDir "test-environments.json"

# Load environment configuration
if (!(Test-Path $envConfigPath)) {
    Write-Host "❌ Error: Environment configuration not found: $envConfigPath" -ForegroundColor Red
    exit 1
}

$envConfig = Get-Content $envConfigPath | ConvertFrom-Json

if (!$envConfig.$Environment) {
    Write-Host "❌ Error: Environment '$Environment' not found in configuration" -ForegroundColor Red
    exit 1
}

$baseURL = $envConfig.$Environment.url
if ($StartURL) {
    $baseURL = $StartURL
}

Write-Host "📝 Recording Configuration:" -ForegroundColor Cyan
Write-Host "   Test Name: $TestName" -ForegroundColor White
Write-Host "   Environment: $Environment" -ForegroundColor White
Write-Host "   Start URL: $baseURL" -ForegroundColor White
Write-Host "   Output Directory: $Output" -ForegroundColor White
Write-Host ""

# Create output directory
if (!(Test-Path $Output)) {
    New-Item -Path $Output -ItemType Directory -Force | Out-Null
}

# Generate output file names
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$recordingFileName = "$TestName-$timestamp.spec.js"
$recordingPath = Join-Path $Output $recordingFileName

Write-Host "🚀 Starting Playwright Test Recorder..." -ForegroundColor Yellow
Write-Host ""
Write-Host "📋 Instructions:" -ForegroundColor Cyan
Write-Host "   1. A browser window will open" -ForegroundColor White
Write-Host "   2. Perform the actions you want to record" -ForegroundColor White
Write-Host "   3. Playwright will generate test code automatically" -ForegroundColor White
Write-Host "   4. Close the browser when done to save the recording" -ForegroundColor White
Write-Host ""
Write-Host "⏸️  Press Ctrl+C to cancel..." -ForegroundColor Yellow
Write-Host ""

# Run Playwright codegen (requires @playwright/test to be installed)
try {
    # NOTE: This requires Node.js and Playwright to be installed
    # The actual MCP server provides the recording functionality
    # This script documents the intended usage pattern
    
    Write-Host "💡 Note: This requires the Playwright MCP server for full functionality" -ForegroundColor Yellow
    Write-Host "   Using direct npx codegen as fallback..." -ForegroundColor Yellow
    Write-Host ""
    
    $codegenArgs = @(
        "-y",
        "@playwright/test",
        "codegen",
        "--target=playwright-test",
        "--output=$recordingPath",
        $baseURL
    )
    
    & npx $codegenArgs
    
    if (Test-Path $recordingPath) {
        Write-Host ""
        Write-Host "✅ Recording saved successfully!" -ForegroundColor Green
        Write-Host "📁 Output: $recordingPath" -ForegroundColor White
        Write-Host ""
        Write-Host "📝 Next Steps:" -ForegroundColor Cyan
        Write-Host "   1. Review the generated test code" -ForegroundColor Yellow
        Write-Host "   2. Add test assertions and validations" -ForegroundColor Yellow
        Write-Host "   3. Add test metadata (test case ID, requirements, etc.)" -ForegroundColor Yellow
        Write-Host "   4. Move to appropriate test suite folder" -ForegroundColor Yellow
        Write-Host "   5. Run the test: npm test $recordingPath" -ForegroundColor Yellow
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "⚠️  Recording was cancelled or failed" -ForegroundColor Yellow
        Write-Host ""
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Error during recording: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Troubleshooting:" -ForegroundColor Cyan
    Write-Host "   1. Ensure Node.js is installed: node --version" -ForegroundColor Yellow
    Write-Host "   2. Ensure Playwright is installed: npx playwright --version" -ForegroundColor Yellow
    Write-Host "   3. Install Playwright browsers: npx playwright install" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "🎉 Happy Testing!" -ForegroundColor Green

