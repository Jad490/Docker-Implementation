// Helper Functions for Sentiment Analysis
const getSentimentIcon = (sentiment) => {
    if (sentiment === 'POSITIVE') return <ThumbsUp />;
    if (sentiment === 'NEGATIVE') return <ThumbsDown />;
    return <MessageCircle />;
};

const getSentimentClass = (sentiment) => {
    if (sentiment === 'POSITIVE') return 'sentiment-positive';
    if (sentiment === 'NEGATIVE') return 'sentiment-negative';
    return 'sentiment-neutral';
};

const getConfidenceClass = (sentiment) => {
    if (sentiment === 'POSITIVE') return 'confidence-positive';
    if (sentiment === 'NEGATIVE') return 'confidence-negative';
    return 'confidence-neutral';
};

const truncateText = (text, maxLength = APP_CONFIG.TEXT_TRUNCATE_LENGTH) => {
    return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
};

const formatConfidence = (confidence, decimals = 1) => {
    return (confidence * 100).toFixed(decimals);
};