// Analysis Result Display Component (Right Column Only)
const AnalysisResult = ({ history, onClearHistory }) => {
    return (
        <>
            {/* History Section */}
            <div className="card">
                <h3 className="history-header">
                    <MessageCircle />
                    {UI_MESSAGES.RECENT_ANALYSIS_TITLE}
                </h3>

                {history.length === 0 ? (
                    <p className="history-empty">{UI_MESSAGES.HISTORY_EMPTY}</p>
                ) : (
                    <div className="history-items">
                        {history.map((item, index) => (
                            <div key={index} className="history-item">
                                <p className="history-text">
                                    "{truncateText(item.text)}"
                                </p>
                                <div className="history-meta" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                                    <div className={`history-sentiment ${getSentimentClass(item.sentiment)}`}>
                                        {getSentimentIcon(item.sentiment)}
                                        <span>{item.sentiment}</span>
                                    </div>
                                    <span className="history-confidence">{formatConfidence(item.confidence, 0)}%</span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {history.length > 0 && (
                    <button onClick={onClearHistory} className="clear-btn">
                        {UI_MESSAGES.CLEAR_HISTORY}
                    </button>
                )}
            </div>

            {/* API Info */}
            <div className="card api-info">
                <h3>API Information</h3>
                <div className="api-details">
                    <p><strong>Endpoint:</strong> {API_BASE_URL}</p>
                    <p><strong>Model:</strong> DistilBERT</p>
                    <p>
                        <strong>Status:</strong>
                        <span className="status-indicator">
                            <div className="status-dot"></div>
                            Ready
                        </span>
                    </p>
                </div>
            </div>
        </>
    );
};