from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os


# =========================
# APPLICATION
# =========================

app = FastAPI(
    title="CloudOps Monitoring API",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://main.d3a5zsvffpnykc.amplifyapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# DATABASE
# =========================

DB_NAME = os.getenv("DB_PATH", "monitoring.db")

def get_connection():
    return sqlite3.connect(DB_NAME)


# =========================
# MODELS
# =========================

class ServiceCreate(BaseModel):
    name: str
    url: str


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "service": "CloudOps Monitoring API",
        "status": "running"
    }


# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================
# HEALTH CHECK HISTORY
# =========================

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


# =========================
# SERVICES
# =========================

@app.get("/services")
def get_services():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.url,
            s.enabled,
            h.status,
            h.http_status,
            h.response_time_ms,
            h.timestamp
        FROM services s
        LEFT JOIN health_checks h
            ON h.id = (
                SELECT MAX(h2.id)
                FROM health_checks h2
                WHERE h2.service = s.name
            )
        ORDER BY s.id
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "service": row[1],
            "url": row[2],
            "enabled": bool(row[3]),
            "status": row[4] or "unknown",
            "http_status": row[5],
            "response_time_ms": row[6],
            "timestamp": row[7]
        }
        for row in rows
    ]


# =========================
# UPTIME
# =========================

@app.get("/uptime")
def get_uptime():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            service,
            COUNT(*) AS total_checks,
            SUM(
                CASE
                    WHEN status = 'healthy'
                    THEN 1
                    ELSE 0
                END
            ) AS healthy_checks,
            SUM(
                CASE
                    WHEN status = 'degraded'
                    THEN 1
                    ELSE 0
                END
            ) AS degraded_checks,
            SUM(
                CASE
                    WHEN status = 'down'
                    THEN 1
                    ELSE 0
                END
            ) AS down_checks
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


# =========================
# ADD SERVICE
# =========================

@app.post("/services")
def add_service(service: ServiceCreate):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO services (
                name,
                url,
                enabled,
                created_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            service.name,
            service.url,
            1,
            datetime.now().isoformat()
        ))

        conn.commit()

        service_id = cursor.lastrowid

    except sqlite3.IntegrityError:

        conn.close()

        raise HTTPException(
            status_code=409,
            detail="A service with this name already exists"
        )

    conn.close()

    return {
        "message": "Service added successfully",
        "id": service_id,
        "name": service.name,
        "url": service.url
    }


# =========================
# DELETE SERVICE
# =========================

@app.delete("/services/{service_id}")
def delete_service(service_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM services WHERE id = ?",
        (service_id,)
    )

    service = cursor.fetchone()

    if service is None:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    cursor.execute(
        "DELETE FROM services WHERE id = ?",
        (service_id,)
    )

    conn.commit()

    conn.close()

    return {
        "message": "Service deleted successfully",
        "service": service[0]
    }


# =========================
# TOGGLE SERVICE
# =========================

@app.patch("/services/{service_id}/toggle")
def toggle_service(service_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, enabled FROM services WHERE id = ?",
        (service_id,)
    )

    service = cursor.fetchone()

    if service is None:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    new_status = 0 if service[1] == 1 else 1

    cursor.execute(
        """
        UPDATE services
        SET enabled = ?
        WHERE id = ?
        """,
        (new_status, service_id)
    )

    conn.commit()

    conn.close()

    return {
        "message": "Service status updated",
        "service": service[0],
        "enabled": bool(new_status)
    }