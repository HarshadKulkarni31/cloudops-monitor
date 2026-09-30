import sqlite3

DB_NAME = "monitoring.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            status TEXT NOT NULL,
            http_status INTEGER,
            response_time_ms REAL,
            timestamp TEXT NOT NULL,
            error TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_result(result):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO health_checks (
            service,
            status,
            http_status,
            response_time_ms,
            timestamp,
            error
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        result.get("service"),
        result.get("status"),
        result.get("http_status"),
        result.get("response_time_ms"),
        result.get("timestamp"),
        result.get("error")
    ))

    conn.commit()
    conn.close()


def get_recent_results(limit=100):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            service,
            status,
            http_status,
            response_time_ms,
            timestamp,
            error
        FROM health_checks
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return rows