CREATE TABLE IF NOT EXISTS analysis_history (
    id BIGSERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    confidence REAL NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analysis_history_created_at
    ON analysis_history (created_at DESC);
