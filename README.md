# ☁️ CloudOps Monitor

> A cloud-based service monitoring platform for tracking API health, uptime, response time, and service incidents.

## ⏸️ Project Status

### ✅ Project Complete — Backend Currently Stopped

CloudOps Monitor is a completed project. The AWS backend is **intentionally stopped** to avoid unnecessary cloud compute costs while the project is not under active development.

- **Frontend:** Deployed on AWS Amplify
- **Backend:** Currently stopped
- **Monitoring:** Currently paused
- **Source code:** Available on GitHub
- **AWS configuration:** Preserved for future deployment

---

## 🌐 Links

**Live Frontend:**  
https://main.d3a5zsvffpnykc.amplifyapp.com/

**GitHub:**  
https://github.com/HarshadKulkarni31/cloudops-monitor

> ⚠️ Live monitoring is unavailable while the backend is stopped.

---

## 📌 Overview

CloudOps Monitor provides a centralized dashboard for monitoring web services. It periodically checks registered health endpoints and tracks their **availability, HTTP status, response time, and health state**.

The system can detect service failures and performance degradation and record status changes as incidents.

---

## ✨ Features

- 📊 Real-time service monitoring dashboard
- 🔍 Automated health checks
- 🟢 Healthy / 🟡 Degraded / 🔴 Down status
- ⚡ Response-time monitoring
- 📈 Uptime tracking
- 🚨 Incident detection
- ➕ Add and manage monitored services
- 🔄 Enable/disable monitoring
- 🐳 Dockerized services
- ☁️ AWS cloud deployment

### Health Rules

| Condition | Status |
|---|---|
| Successful response + normal latency | 🟢 Healthy |
| HTTP 4xx | 🟡 Degraded |
| Response time > 2000 ms | 🟡 Degraded |
| HTTP 5xx | 🔴 Down |
| Timeout / connection failure | 🔴 Down |

---

## 🏗️ Architecture

```text
        User
         │
         ▼
   AWS Amplify
   React Dashboard
         │
         ▼
    FastAPI API
         │
    ┌────┴────┐
    ▼         ▼
Health      REST API
Checker     Endpoints
    │         │
    └────┬────┘
         ▼
   SQLite + EFS
         │
    ┌────┴────┐
    ▼    ▼    ▼
 Payment Auth Product
   API    API    API
```

---

## 🧰 Tech Stack

**Frontend**
- React
- Vite
- Recharts
- Lucide React

**Backend**
- Python
- FastAPI
- Uvicorn
- HTTPX
- SQLite

**Cloud / DevOps**
- AWS Amplify
- Amazon ECS
- AWS Fargate
- Amazon ECR
- Amazon EFS
- Amazon CloudWatch
- Docker

---

## 📁 Project Structure

```text
cloudops-monitor/
├── services/
│   ├── payment-api/
│   ├── auth-api/
│   └── product-api/
│
├── monitor/
│   ├── health_checker.py
│   ├── database.py
│   ├── api.py
│   └── Dockerfile
│
├── dashboard/
│   ├── src/
│   └── package.json
│
└── README.md
```

---

## 🚀 Run Locally

### Backend

```bash
cd monitor
pip install -r requirements.txt
python -m uvicorn api:app --reload --port 8004
```

### Health Checker

```bash
python health_checker.py
```

### Frontend

```bash
cd dashboard
npm install
npm run dev
```

Create `dashboard/.env.local`:

```env
VITE_API_URL=http://localhost:8004
```

---

## 🔮 Future Improvements

- User authentication
- Multi-user monitoring
- Email / Slack / Discord alerts
- Historical analytics
- AWS Lambda-based monitoring
- EventBridge scheduling
- DynamoDB
- HTTPS and custom domains
- Serverless cost optimization

---


## 📄 License

For educational, portfolio, and demonstration purposes.
