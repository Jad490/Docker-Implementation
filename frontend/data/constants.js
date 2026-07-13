// Application Constants and Static Data

// Environment-aware constants
const getAppSubtitle = () => {
    const env = ENV_CONFIG.DEBUG ? ' (Development Mode)' : '';
    return `Powered by DistilBERT • Analyze the emotional tone of any text${env}`;
};

const EXAMPLE_TEXTS = [
    "I love this course!",
    "This is absolutely fantastic!",
    "I hate waiting in long lines.",
    "The weather is okay today.",
    "What a wonderful day to be alive!"
];

const APP_CONFIG = {
    MAX_HISTORY_ITEMS: 10,
    TEXT_TRUNCATE_LENGTH: 50,
    APP_TITLE: "Sentiment Analysis",
    APP_SUBTITLE: getAppSubtitle(),
    PLACEHOLDER_TEXT: "Type your text here... e.g., 'I love this course!' (Ctrl+Enter to analyze)",
    TIMEOUT: ENV_CONFIG.TIMEOUT
};

const UI_MESSAGES = {
    EMPTY_TEXT_ERROR: "Please enter some text to analyze",
    LOADING_TEXT: "Analyzing...",
    ANALYZE_BUTTON: "Analyze Sentiment",
    HISTORY_EMPTY: "No analysis yet. Try entering some text!",
    CLEAR_HISTORY: "Clear History",
    EXAMPLES_LABEL: "Try these examples:",
    INPUT_LABEL: "Enter your text:",
    RECENT_ANALYSIS_TITLE: "Recent Analysis"
};