import logging
import os

import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS analysis_history (
    id BIGSERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    confidence REAL NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analysis_history_created_at
    ON analysis_history (created_at DESC);
"""


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "sentiment_db"),
        user=os.getenv("DB_USER", "sentiment_user"),
        password=os.getenv("DB_PASSWORD", "sentiment_password"),
        row_factory=dict_row,
    )


def ensure_database_schema():
    """Create the application schema when using a new database such as RDS."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SCHEMA_SQL)
    logger.info("Database schema is ready")


def save_analysis(text, sentiment, confidence):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO analysis_history (text, sentiment, confidence)
                VALUES (%s, %s, %s)
                """,
                (text, sentiment, confidence),
            )


def get_analysis_history(limit=10):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, text, sentiment, confidence, created_at
                FROM analysis_history
                ORDER BY created_at DESC, id DESC
                LIMIT %s
                """,
                (limit,),
            )
            return cursor.fetchall()


def clear_analysis_history():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM analysis_history")
            return cursor.rowcount


def database_is_healthy():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        return True
    except psycopg.Error:
        logger.exception("Database health check failed")
        return False
