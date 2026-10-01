import sqlite3
from datetime import datetime
from database import init_db


DB_NAME = "monitoring.db"

services = [
    {
        "name": "Payment API",
        "url": "http://3.109.152.73:8000/health"
    },
    {
        "name": "Auth API",
        "url": "http://43.205.115.230:8000/health"
    },
    {
        "name": "Product API",
        "url": "http://43.205.215.11:8000/health"
    }
]

# Create required tables first
init_db()

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

for service in services:
    cursor.execute("""
        INSERT OR IGNORE INTO services (
            name,
            url,
            enabled,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        service["name"],
        service["url"],
        1,
        datetime.now().isoformat()
    ))

conn.commit()
conn.close()

print("Services seeded successfully.")