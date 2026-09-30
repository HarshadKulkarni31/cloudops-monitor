from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI(
    title="CloudOps Monitoring API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "monitoring.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


@app.get("/")
def root():
    return {
        "service": "CloudOps Monitoring API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/checks")
def get_checks(limit: int = 100):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
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

    return [
        {
            "id": row[0],
            "service": row[1],
            "status": row[2],
            "http_status": row[3],
            "response_time_ms": row[4],
            "timestamp": row[5],
            "error": row[6]
        }
        for row in rows
    ]


@app.get("/services")
def get_services():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            service,
            status,
            http_status,
            response_time_ms,
            timestamp
        FROM health_checks
        WHERE id IN (
            SELECT MAX(id)
            FROM health_checks
            GROUP BY service
        )
        ORDER BY service
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "service": row[0],
            "status": row[1],
            "http_status": row[2],
            "response_time_ms": row[3],
            "timestamp": row[4]
        }
        for row in rows
    ]

@app.get("/uptime")
def get_uptime():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            service,
            COUNT(*) AS total_checks,
            SUM(CASE WHEN status = 'healthy' THEN 1 ELSE 0 END) AS healthy_checks,
            SUM(CASE WHEN status = 'degraded' THEN 1 ELSE 0 END) AS degraded_checks,
            SUM(CASE WHEN status = 'down' THEN 1 ELSE 0 END) AS down_checks
        FROM health_checks
        GROUP BY service
    """)

    rows = cursor.fetchall()
    conn.close()

    result = []

    for row in rows:
        service = row[0]
        total = row[1]
        healthy = row[2] or 0
        degraded = row[3] or 0
        down = row[4] or 0

        uptime = round(
            ((healthy + degraded) / total) * 100,
            2
        ) if total > 0 else 0

        result.append({
            "service": service,
            "total_checks": total,
            "healthy_checks": healthy,
            "degraded_checks": degraded,
            "down_checks": down,
            "uptime_percentage": uptime
        })

    return result