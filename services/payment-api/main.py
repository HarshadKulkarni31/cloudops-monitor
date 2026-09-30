from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Payment API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "service": "Payment API",
        "message": "Payment service is running"
    }


@app.get("/health")
def health():
    return {
        "service": "Payment API",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/payments")
def payments():
    return {
        "service": "Payment API",
        "payments": [
            {
                "id": "PAY001",
                "amount": 499,
                "status": "success"
            },
            {
                "id": "PAY002",
                "amount": 999,
                "status": "success"
            }
        ]
    }