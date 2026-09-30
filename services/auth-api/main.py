from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Auth API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "service": "Auth API",
        "message": "Authentication service is running"
    }


@app.get("/health")
def health():
    return {
        "service": "Auth API",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/users")
def users():
    return {
        "service": "Auth API",
        "users": [
            {
                "id": 1,
                "name": "Demo User"
            },
            {
                "id": 2,
                "name": "Cloud User"
            }
        ]
    }