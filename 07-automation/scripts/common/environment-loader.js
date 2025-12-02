// Environment Configuration Loader
// Loads test environment settings from config files

const fs = require('fs');
const path = require('path');

/**
 * Load environment configuration
 * @param {string} envName - Environment name (dev, staging, production)
 * @returns {object} Environment configuration
 */
function loadEnvironment(envName = 'dev') {
  const configPath = path.join(__dirname, '../../config/test-environments.json');
  
  try {
    const configData = fs.readFileSync(configPath, 'utf8');
    const environments = JSON.parse(configData);
    
    if (!environments[envName]) {
      throw new Error(`Environment '${envName}' not found in configuration`);
    }
    
    return environments[envName];
  } catch (error) {
    console.error(`Failed to load environment configuration: ${error.message}`);
    throw error;
  }
}

/**
 * Load selector configuration
 * @returns {object} Selector configuration
 */
function loadSelectors() {
  const selectorsPath = path.join(__dirname, '../../config/selectors.json');
  
  try {
    const selectorsData = fs.readFileSync(selectorsPath, 'utf8');
    return JSON.parse(selectorsData);
  } catch (error) {
    console.error(`Failed to load selectors configuration: ${error.message}`);
    throw error;
  }
}

/**
 * Get user credentials from environment
 * @param {object} user - User configuration object
 * @returns {object} User credentials
 */
function getUserCredentials(user) {
  // In production, integrate with Vault or secure credential storage
  // For now, use environment variables
  const password = process.env[`PASSWORD_${user.email.replace(/[@.]/g, '_').toUpperCase()}`];
  
  if (!password) {
    throw new Error(`Password not found for user: ${user.email}`);
  }
  
  return {
    email: user.email,
    password: password,
    vaultPath: user.vaultPath,
    roles: user.roles
  };
}

module.exports = {
  loadEnvironment,
  loadSelectors,
  getUserCredentials
};

