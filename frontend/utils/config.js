// Environment Configuration
const CONFIG = {
    development: {
        API_BASE_URL: '/api',
        DEBUG: true,
        TIMEOUT: 30000
    },
    production: {
        API_BASE_URL: '/api',
        DEBUG: false,
        TIMEOUT: 10000
    }
};

// Auto-detect environment
const getEnvironment = () => {
    if (
        window.location.hostname === 'localhost' ||
        window.location.hostname === '127.0.0.1'
    ) {
        return 'development';
    }

    return 'production';
};

// Export current environment config
const CURRENT_ENV = getEnvironment();
const ENV_CONFIG = CONFIG[CURRENT_ENV];

// Make API_BASE_URL globally available
const API_BASE_URL = ENV_CONFIG.API_BASE_URL;
