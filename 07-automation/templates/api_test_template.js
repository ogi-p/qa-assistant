// API Test Template - Generated from Manual Test Case
// Framework: Manual QA Framework
// Generated: {{GENERATION_DATE}}

/**
 * API Test Information:
 * - Test Case ID: {{TEST_CASE_ID}}
 * - API Endpoint: {{API_ENDPOINT}}
 * - HTTP Method: {{HTTP_METHOD}}
 * - Related JIRA: {{JIRA_TICKET}}
 */

const { test, expect } = require('@playwright/test');
const { loadEnvironment } = require('../scripts/common/environment-loader');

// Load test environment configuration
const env = loadEnvironment(process.env.TEST_ENV || 'dev');

test.describe('API Tests - {{API_NAME}}', () => {
  
  let apiContext;
  let authToken;

  // Setup API context before all tests
  test.beforeAll(async ({ playwright }) => {
    // Create API request context
    apiContext = await playwright.request.newContext({
      baseURL: env.apiUrl,
      extraHTTPHeaders: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    // Authenticate and get token
    const response = await apiContext.post('/auth/login', {
      data: {
        email: env.users.{{USER_TYPE}}.email,
        password: process.env.USER_PASSWORD
      }
    });
    
    const authData = await response.json();
    authToken = authData.token;
  });

  /**
   * API Test: {{TEST_CASE_ID}} - {{TEST_CASE_TITLE}}
   * 
   * Endpoint: {{HTTP_METHOD}} {{API_ENDPOINT}}
   * Expected Status: {{EXPECTED_STATUS}}
   */
  test('{{TEST_CASE_ID}}: {{TEST_CASE_TITLE}}', async () => {
    // Make API request
    const response = await apiContext.{{HTTP_METHOD_LOWER}}('{{API_ENDPOINT}}', {
      headers: {
        'Authorization': `Bearer ${authToken}`
      },
      data: {{REQUEST_BODY}}
    });
    
    // Assert response status
    expect(response.status()).toBe({{EXPECTED_STATUS}});
    
    // Parse response body
    const responseBody = await response.json();
    
    // Assertions on response body
    {{RESPONSE_ASSERTIONS}}
    
    // Performance assertion
    const responseTime = response.headers()['x-response-time'];
    if (responseTime) {
      expect(parseInt(responseTime)).toBeLessThan({{MAX_RESPONSE_TIME_MS}});
    }
  });

  // Cleanup after all tests
  test.afterAll(async () => {
    await apiContext.dispose();
  });
});

/**
 * Traceability Information:
 * - Manual Test Case: {{TEST_CASE_ID}}
 * - JIRA Ticket: {{JIRA_TICKET}}
 * - API Endpoint: {{API_ENDPOINT}}
 * - Test Environment: {{ENVIRONMENT}}
 * - Date Generated: {{GENERATION_DATE}}
 */

