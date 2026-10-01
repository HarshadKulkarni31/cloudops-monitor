FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .

RUN mkdir -p /app/data

EXPOSE 8004

CMD ["sh", "-c", "python health_checker.py & exec uvicorn api:app --host 0.0.0.0 --port 8004"]