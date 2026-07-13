const { useState } = React;

const SentimentAnalyzer = () => {
    const [text, setText] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [history, setHistory] = useState([]);

    const handleAnalyze = async () => {
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await analyzeSentiment(text);
            setResult(data);
            setHistory(prev => [data, ...prev.slice(0, APP_CONFIG.MAX_HISTORY_ITEMS - 1)]);
        } catch (err) {
            setError(err.message);
            console.error('Analysis error:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        handleAnalyze();
    };

    const tryExample = (exampleText) => {
        setText(exampleText);
        setError(null);
    };

    const clearHistory = () => {
        setHistory([]);
    };

    return (
        <div className="container">
            {/* Header */}
            <div className="header">
                <div className="header-title">
                    <Heart />
                    <h1>{APP_CONFIG.APP_TITLE}</h1>
                </div>
                <p className="header-subtitle">{APP_CONFIG.APP_SUBTITLE}</p>
            </div>

            <div className="grid">
                {/* Input Section */}
                <div>
                    <div className="card">
                        <div className="form-group">
                            <label htmlFor="text-input" className="label">
                                {UI_MESSAGES.INPUT_LABEL}
                            </label>
                            <textarea
                                id="text-input"
                                value={text}
                                onChange={(e) => setText(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                                        e.preventDefault();
                                        handleSubmit(e);
                                    }
                                }}
                                placeholder={APP_CONFIG.PLACEHOLDER_TEXT}
                                className="textarea"
                                disabled={loading}
                            />
                        </div>

                        {/* Example texts */}
                        <div className="examples">
                            <p className="examples-label">{UI_MESSAGES.EXAMPLES_LABEL}</p>
                            <div className="examples-container">
                                {EXAMPLE_TEXTS.map((example, index) => (
                                    <button
                                        key={index}
                                        type="button"
                                        onClick={() => tryExample(example)}
                                        className="example-btn"
                                        disabled={loading}
                                    >
                                        "{example}"
                                    </button>
                                ))}
                            </div>
                        </div>

                        <button
                            type="button"
                            onClick={handleAnalyze}
                            disabled={loading || !text.trim()}
                            className="analyze-btn"
                        >
                            {loading ? (
                                <>
                                    <Loader2 />
                                    <span>{UI_MESSAGES.LOADING_TEXT}</span>
                                </>
                            ) : (
                                <>
                                    <Send />
                                    <span>{UI_MESSAGES.ANALYZE_BUTTON}</span>
                                </>
                            )}
                        </button>

                        {/* Error Display */}
                        {error && (
                            <div className="error">
                                <XCircle />
                                <p className="error-text">{error}</p>
                            </div>
                        )}

                        {/* Current Result */}
                        {result && (
                            <div className="result">
                                <h3 className="result-header">
                                    <CheckCircle />
                                    Analysis Result
                                </h3>

                                <div className="result-content">
                                    <div>
                                        <p className="result-text">Your text:</p>
                                        <p className="result-quote">"{result.text}"</p>
                                    </div>

                                    <div className="result-sentiment">
                                        <div className={`sentiment-badge ${getSentimentClass(result.sentiment)}`}>
                                            {getSentimentIcon(result.sentiment)}
                                            <span>{result.sentiment}</span>
                                        </div>

                                        <div className="confidence-container">
                                            <div className="confidence-header" style={{display: 'flex', justifyContent: 'space-between'}}>
                                                <span className="confidence-label">Confidence</span>
                                                <span className="confidence-value">{formatConfidence(result.confidence)}%</span>
                                            </div>
                                            <div className="confidence-bar">
                                                <div
                                                    className={`confidence-fill ${getConfidenceClass(result.sentiment)}`}
                                                    style={{ width: `${result.confidence * 100}%` }}
                                                ></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Results Section */}
                <div>
                    <AnalysisResult
                        history={history} 
                        onClearHistory={clearHistory} 
                    />
                </div>
            </div>
        </div>
    );
};

ReactDOM.render(<SentimentAnalyzer />, document.getElementById('root'));