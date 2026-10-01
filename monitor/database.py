import os
import sqlite3

DB_NAME = os.getenv("DB_PATH", "monitoring.db")

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Health check history
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

    # Registered services
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            url TEXT NOT NULL,
            enabled INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        )
    """)

    # Incident history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            previous_status TEXT,
            current_status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_result(result):
    conn = get_connection()
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
    conn = get_connection()
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


def save_incident(
    service,
    previous_status,
    current_status,
    timestamp
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents (
            service,
            previous_status,
            current_status,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        service,
        previous_status,
        current_status,
        timestamp
    ))

    conn.commit()
    conn.close()