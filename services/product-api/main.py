from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="Product API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "service": "Product API",
        "message": "Product service is running"
    }


@app.get("/health")
def health():
    return {
        "service": "Product API",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/products")
def products():
    return {
        "service": "Product API",
        "products": [
            {
                "id": 101,
                "name": "Cloud Laptop",
                "price": 65000
            },
            {
                "id": 102,
                "name": "Developer Keyboard",
                "price": 3500
            },
            {
                "id": 103,
                "name": "USB-C Hub",
                "price": 1800
            }
        ]
    }