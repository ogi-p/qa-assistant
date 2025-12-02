// Visual Testing Helper Functions
// Handles screenshot comparison and visual regression testing

const fs = require('fs');
const path = require('path');
const { PNG } = require('pngjs');
const pixelmatch = require('pixelmatch');

/**
 * Compare two screenshots
 * @param {Buffer} baseline - Baseline screenshot buffer
 * @param {Buffer} actual - Actual screenshot buffer
 * @param {object} options - Comparison options
 * @returns {object} Comparison result
 */
function compareScreenshots(baseline, actual, options = {}) {
  const {
    threshold = 0.1,
    includeAA = false,
    alpha = 0.1,
    diffMask = true
  } = options;
  
  // Parse PNG images
  const img1 = PNG.sync.read(baseline);
  const img2 = PNG.sync.read(actual);
  
  const { width, height } = img1;
  const diff = new PNG({ width, height });
  
  // Perform pixel comparison
  const numDiffPixels = pixelmatch(
    img1.data,
    img2.data,
    diff.data,
    width,
    height,
    { threshold, includeAA, alpha, diffMask }
  );
  
  const totalPixels = width * height;
  const diffPercentage = (numDiffPixels / totalPixels) * 100;
  
  return {
    numDiffPixels,
    totalPixels,
    diffPercentage,
    diffImage: PNG.sync.write(diff),
    passed: diffPercentage < (options.maxDiffPercentage || 0.1)
  };
}

/**
 * Save baseline screenshot
 * @param {Page} page - Playwright page object
 * @param {string} name - Screenshot name
 * @param {object} options - Screenshot options
 * @returns {Promise<string>} Path to saved screenshot
 */
async function saveBaselineScreenshot(page, name, options = {}) {
  const baselinePath = path.join(__dirname, '../../screenshots/baseline', `${name}.png`);
  
  // Ensure directory exists
  const dir = path.dirname(baselinePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  await page.screenshot({
    path: baselinePath,
    fullPage: options.fullPage || false,
    animations: 'disabled',
    ...options
  });
  
  console.log(`Baseline screenshot saved: ${baselinePath}`);
  return baselinePath;
}

/**
 * Take and compare screenshot
 * @param {Page} page - Playwright page object
 * @param {string} name - Screenshot name
 * @param {object} options - Comparison options
 * @returns {Promise<object>} Comparison result
 */
async function takeAndCompareScreenshot(page, name, options = {}) {
  const baselinePath = path.join(__dirname, '../../screenshots/baseline', `${name}.png`);
  const actualPath = path.join(__dirname, '../../screenshots/actual', `${name}.png`);
  const diffPath = path.join(__dirname, '../../screenshots/diff', `${name}-diff.png`);
  
  // Ensure directories exist
  [baselinePath, actualPath, diffPath].forEach(p => {
    const dir = path.dirname(p);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
  
  // Take actual screenshot
  await page.screenshot({
    path: actualPath,
    fullPage: options.fullPage || false,
    animations: 'disabled',
    ...options
  });
  
  // Check if baseline exists
  if (!fs.existsSync(baselinePath)) {
    console.warn(`Baseline not found: ${baselinePath}. Creating new baseline.`);
    fs.copyFileSync(actualPath, baselinePath);
    return {
      numDiffPixels: 0,
      totalPixels: 0,
      diffPercentage: 0,
      passed: true,
      message: 'Baseline created'
    };
  }
  
  // Load screenshots
  const baseline = fs.readFileSync(baselinePath);
  const actual = fs.readFileSync(actualPath);
  
  // Compare screenshots
  const result = compareScreenshots(baseline, actual, options);
  
  // Save diff image if there are differences
  if (result.numDiffPixels > 0) {
    fs.writeFileSync(diffPath, result.diffImage);
    console.log(`Diff image saved: ${diffPath}`);
  }
  
  return result;
}

/**
 * Hide dynamic elements before screenshot
 * @param {Page} page - Playwright page object
 * @param {string[]} selectors - Selectors of elements to hide
 * @returns {Promise<void>}
 */
async function hideDynamicElements(page, selectors = []) {
  const defaultSelectors = [
    '[data-dynamic="true"]',
    '.timestamp',
    '.date-time',
    '[data-testid="timestamp"]'
  ];
  
  const allSelectors = [...defaultSelectors, ...selectors];
  
  await page.addStyleTag({
    content: `
      ${allSelectors.join(',\n')} {
        visibility: hidden !important;
      }
    `
  });
}

/**
 * Mask sensitive data before screenshot
 * @param {Page} page - Playwright page object
 * @param {string[]} selectors - Selectors of elements to mask
 * @returns {Promise<void>}
 */
async function maskSensitiveData(page, selectors = []) {
  const defaultSelectors = [
    '[data-sensitive="true"]',
    '.email',
    '.phone',
    '.ssn',
    '[data-testid="sensitive"]'
  ];
  
  const allSelectors = [...defaultSelectors, ...selectors];
  
  await page.addStyleTag({
    content: `
      ${allSelectors.join(',\n')} {
        filter: blur(8px);
        background-color: #000 !important;
        color: transparent !important;
      }
    `
  });
}

/**
 * Take screenshot with retries
 * @param {Page} page - Playwright page object
 * @param {string} path - Screenshot path
 * @param {object} options - Screenshot options
 * @returns {Promise<void>}
 */
async function takeScreenshotWithRetry(page, path, options = {}) {
  const { retries = 3, delay = 1000 } = options;
  
  for (let i = 0; i < retries; i++) {
    try {
      await page.screenshot({ path, ...options });
      return;
    } catch (error) {
      console.warn(`Screenshot attempt ${i + 1} failed: ${error.message}`);
      
      if (i === retries - 1) {
        throw error;
      }
      
      await page.waitForTimeout(delay);
    }
  }
}

/**
 * Compare multiple viewport screenshots
 * @param {Page} page - Playwright page object
 * @param {string} name - Screenshot name
 * @param {Array} viewports - Array of viewport configurations
 * @returns {Promise<object>} Results for each viewport
 */
async function compareMultipleViewports(page, name, viewports = []) {
  const results = {};
  
  for (const viewport of viewports) {
    await page.setViewportSize(viewport);
    await page.waitForTimeout(500); // Wait for resize
    
    const screenshotName = `${name}-${viewport.name}`;
    const result = await takeAndCompareScreenshot(page, screenshotName);
    
    results[viewport.name] = result;
  }
  
  return results;
}

/**
 * Generate visual regression report
 * @param {object} results - Test results
 * @param {string} outputPath - Report output path
 * @returns {Promise<void>}
 */
async function generateVisualReport(results, outputPath) {
  const report = {
    timestamp: new Date().toISOString(),
    totalTests: Object.keys(results).length,
    passed: Object.values(results).filter(r => r.passed).length,
    failed: Object.values(results).filter(r => !r.passed).length,
    results: results
  };
  
  const reportHtml = `
<!DOCTYPE html>
<html>
<head>
  <title>Visual Regression Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .summary { background: #f0f0f0; padding: 15px; margin-bottom: 20px; }
    .test { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
    .passed { background: #d4edda; }
    .failed { background: #f8d7da; }
    .screenshot { max-width: 100%; border: 1px solid #ccc; }
  </style>
</head>
<body>
  <h1>Visual Regression Report</h1>
  <div class="summary">
    <p><strong>Generated:</strong> ${report.timestamp}</p>
    <p><strong>Total Tests:</strong> ${report.totalTests}</p>
    <p><strong>Passed:</strong> ${report.passed}</p>
    <p><strong>Failed:</strong> ${report.failed}</p>
  </div>
  ${Object.entries(results).map(([name, result]) => `
    <div class="test ${result.passed ? 'passed' : 'failed'}">
      <h3>${name}</h3>
      <p><strong>Status:</strong> ${result.passed ? 'PASSED' : 'FAILED'}</p>
      <p><strong>Diff Percentage:</strong> ${result.diffPercentage.toFixed(2)}%</p>
      <p><strong>Diff Pixels:</strong> ${result.numDiffPixels} / ${result.totalPixels}</p>
    </div>
  `).join('')}
</body>
</html>
  `;
  
  fs.writeFileSync(outputPath, reportHtml);
  console.log(`Visual regression report saved: ${outputPath}`);
}

module.exports = {
  compareScreenshots,
  saveBaselineScreenshot,
  takeAndCompareScreenshot,
  hideDynamicElements,
  maskSensitiveData,
  takeScreenshotWithRetry,
  compareMultipleViewports,
  generateVisualReport
};

