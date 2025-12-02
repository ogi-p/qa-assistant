# Run Playwright Test Suite
# Usage: .\run-tests.ps1 -Suite "regression" -Environment "staging" -Browser "chromium"

param(
    [Parameter(Mandatory=$false)]
    [string]$Suite = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory=$false)]
    [string]$Browser = "chromium",
    
    [Parameter(Mandatory=$false)]
    [switch]$Debug = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$Headed = $false,
    
    [Parameter(Mandatory=$false)]
    [string]$Reporter = "html,list"
)

Write-Host "🧪 Playwright Test Runner - Manual QA Framework" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $scriptDir
$configDir = Join-Path $rootDir "config"
$scriptsDir = Join-Path $rootDir "scripts"
$configPath = Join-Path $configDir "playwright.config.js"

# Validate config exists
if (!(Test-Path $configPath)) {
    Write-Host "❌ Error: Playwright configuration not found: $configPath" -ForegroundColor Red
    exit 1
}

Write-Host "📝 Test Execution Configuration:" -ForegroundColor Cyan
Write-Host "   Environment: $Environment" -ForegroundColor White
Write-Host "   Browser: $Browser" -ForegroundColor White
Write-Host "   Suite: $(if ($Suite) { $Suite } else { 'All tests' })" -ForegroundColor White
Write-Host "   Debug Mode: $Debug" -ForegroundColor White
Write-Host "   Headed: $Headed" -ForegroundColor White
Write-Host "   Reporter: $Reporter" -ForegroundColor White
Write-Host ""

# Build test path
$testPath = $scriptsDir
if ($Suite) {
    $suitePath = Join-Path $scriptsDir $Suite
    if (Test-Path $suitePath) {
        $testPath = $suitePath
    } else {
        Write-Host "⚠️  Warning: Suite directory not found: $suitePath" -ForegroundColor Yellow
        Write-Host "   Running all tests instead..." -ForegroundColor Yellow
        Write-Host ""
    }
}

# Build playwright command arguments
$playwrightArgs = @(
    "-y",
    "@playwright/test",
    "test"
)

# Add test path
$playwrightArgs += $testPath

# Add project (browser)
$playwrightArgs += "--project=$Browser"

# Add reporter
if ($Reporter) {
    $Reporter -split ',' | ForEach-Object {
        $playwrightArgs += "--reporter=$_"
    }
}

# Add headed mode if specified
if ($Headed) {
    $playwrightArgs += "--headed"
}

# Add debug mode if specified
if ($Debug) {
    $playwrightArgs += "--debug"
    Write-Host "🐛 Debug Mode: Playwright Inspector will open" -ForegroundColor Yellow
    Write-Host ""
}

# Set environment variables
$env:TEST_ENV = $Environment
$env:BASE_URL = ""

# Load base URL from environment config
$envConfigPath = Join-Path $configDir "test-environments.json"
if (Test-Path $envConfigPath) {
    $envConfig = Get-Content $envConfigPath | ConvertFrom-Json
    if ($envConfig.$Environment) {
        $env:BASE_URL = $envConfig.$Environment.url
        Write-Host "🌐 Base URL: $($env:BASE_URL)" -ForegroundColor Cyan
        Write-Host ""
    }
}

Write-Host "🚀 Starting Playwright tests..." -ForegroundColor Yellow
Write-Host "Command: npx $($playwrightArgs -join ' ')" -ForegroundColor Gray
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

# Run Playwright tests
try {
    & npx $playwrightArgs
    
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host ""
    
    if ($exitCode -eq 0) {
        Write-Host "✅ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host "❌ Some tests failed" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "📊 Test Reports:" -ForegroundColor Cyan
    
    $reportDir = Join-Path $rootDir "reports"
    if (Test-Path $reportDir) {
        $htmlReport = Join-Path $reportDir "html\index.html"
        if (Test-Path $htmlReport) {
            Write-Host "   HTML Report: $htmlReport" -ForegroundColor White
            Write-Host "   Open with: start $htmlReport" -ForegroundColor Yellow
        }
        
        $jsonReport = Join-Path $reportDir "results.json"
        if (Test-Path $jsonReport) {
            Write-Host "   JSON Report: $jsonReport" -ForegroundColor White
        }
        
        $junitReport = Join-Path $reportDir "junit.xml"
        if (Test-Path $junitReport) {
            Write-Host "   JUnit Report: $junitReport" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "📸 Screenshots & Videos:" -ForegroundColor Cyan
    $testResultsDir = Join-Path $rootDir "test-results"
    if (Test-Path $testResultsDir) {
        Write-Host "   Test Results: $testResultsDir" -ForegroundColor White
    }
    
    Write-Host ""
    
    exit $exitCode
    
} catch {
    Write-Host ""
    Write-Host "❌ Error running tests: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Troubleshooting:" -ForegroundColor Cyan
    Write-Host "   1. Ensure Node.js is installed: node --version" -ForegroundColor Yellow
    Write-Host "   2. Ensure Playwright is installed: npx playwright --version" -ForegroundColor Yellow
    Write-Host "   3. Install Playwright browsers: npx playwright install" -ForegroundColor Yellow
    Write-Host "   4. Check configuration: $configPath" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

