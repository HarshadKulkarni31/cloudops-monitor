# ☁️ CloudOps Monitor

> A cloud-based service monitoring and observability platform for tracking application health, response time, uptime, and service incidents.

[![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react\&logoColor=white)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python\&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker\&logoColor=white)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/Cloud-AWS-FF9900?logo=amazonaws\&logoColor=white)](https://aws.amazon.com/)
[![AWS Amplify](https://img.shields.io/badge/Frontend%20Hosting-AWS%20Amplify-FF9900?logo=awsamplify\&logoColor=white)](https://aws.amazon.com/amplify/)

---

## ⏸️ Project Status

### ✅ Project Complete — Backend Currently Stopped

CloudOps Monitor is a **completed working project**. The AWS backend infrastructure is currently **stopped intentionally** to avoid unnecessary cloud compute costs while the project is not under active development.

The project is **not abandoned or incomplete**. The source code, Docker images, AWS configurations, frontend, monitoring logic, and deployment setup have been preserved and can be resumed when required.

> **Frontend:** Deployed on AWS Amplify
> **Backend:** Currently stopped
> **Monitoring:** Currently paused

---

## 🌐 Live Demo

**Frontend:**
https://main.d3a5zsvffpnykc.amplifyapp.com/


> ⚠️ The frontend is deployed, but live monitoring data is unavailable while the backend infrastructure is stopped.

---

## 📌 Overview

CloudOps Monitor is a lightweight monitoring platform designed to track the health and availability of web services from a centralized dashboard.

Users can register services by providing a health-check URL. The monitoring engine periodically checks each enabled service and records its HTTP status, response time, availability, and health state.

The platform can detect service failures and performance degradation by comparing current results with previous states and recording incidents when status changes occur.

The project was built to demonstrate practical experience with **cloud computing, containerization, REST APIs, monitoring, persistent storage, and AWS deployment**.

---

# ✨ Features

### 📊 Service Monitoring

Monitor multiple web services from a single dashboard.

* Healthy / Degraded / Down status
* HTTP status codes
* Response time
* Last checked time
* Service availability

### 🔍 Automated Health Checks

The monitoring engine periodically sends HTTP requests to registered health endpoints and evaluates the response.

### 🚨 Incident Detection

Automatically detects service state changes such as:

```text
Healthy → Degraded
Healthy → Down
Degraded → Healthy
```

### ➕ Dynamic Service Management

Users can:

* Add services
* Delete services
* Enable/disable monitoring
* Refresh monitoring data

### 📈 Uptime Tracking

Tracks service availability based on recorded health-check results.

### ⚡ Latency Monitoring

Measures response time for every health check, allowing slow services to be identified even when they are technically available.

### 🐳 Dockerized Services

Demo services are packaged as independent Docker containers and deployed using AWS infrastructure.

---

# 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │   User Browser   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   AWS Amplify    │
                         │  React Dashboard │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   FastAPI API    │
                         │     :8004        │
                         └────────┬─────────┘
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                     ▼                         ▼
              ┌──────────────┐         ┌──────────────┐
              │ Health Check │         │  REST API    │
              │    Engine    │         │  Endpoints   │
              └──────┬───────┘         └──────┬───────┘
                     │                        │
                     └───────────┬────────────┘
                                 ▼
                        ┌──────────────────┐
                        │ SQLite + EFS     │
                        │ Monitoring Data   │
                        └──────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
                ▼                                 ▼
        ┌──────────────┐                  ┌──────────────┐
        │  Payment API │                  │    Auth API  │
        └──────────────┘                  └──────────────┘
                │
                ▼
        ┌──────────────┐
        │  Product API │
        └──────────────┘
```

---

# ☁️ AWS Infrastructure

The project uses AWS for cloud deployment and infrastructure.

| Service               | Purpose                        |
| --------------------- | ------------------------------ |
| **AWS Amplify**       | React frontend hosting         |
| **Amazon ECS**        | Container orchestration        |
| **AWS Fargate**       | Serverless container execution |
| **Amazon ECR**        | Docker image storage           |
| **Amazon EFS**        | Persistent monitoring storage  |
| **Amazon CloudWatch** | Container/application logs     |

### Containerized Services

```text
payment-api-service
auth-api-service
product-api-service
```

Docker images are stored in Amazon ECR.

---

# 🧰 Tech Stack

### Frontend

* React
* Vite
* JavaScript
* Recharts
* Lucide React
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* HTTPX
* SQLite

### Cloud & DevOps

* AWS Amplify
* Amazon ECS
* AWS Fargate
* Amazon ECR
* Amazon EFS
* Amazon CloudWatch
* Docker

### Version Control

* Git
* GitHub

---

# 📁 Project Structure

```text
cloudops-monitor/
│
├── services/
│   ├── payment-api/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   ├── auth-api/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── product-api/
│       ├── main.py
│       ├── requirements.txt
│       └── Dockerfile
│
├── monitor/
│   ├── health_checker.py
│   ├── database.py
│   ├── api.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── dashboard/
│   ├── package.json
│   ├── .env.example
│   └── src/
│       ├── App.jsx
│       └── index.css
│
└── README.md
```

---

# 🔄 How It Works

```text
User adds a service
        ↓
Service stored in database
        ↓
Health checker finds enabled services
        ↓
HTTP health request sent
        ↓
Response time + HTTP status measured
        ↓
Health status calculated
        ↓
Result stored
        ↓
Previous status compared
        ↓
Incident created if status changes
        ↓
Dashboard displays latest status
```

### Health Status

| Condition                            | Result      |
| ------------------------------------ | ----------- |
| Successful response + normal latency | 🟢 Healthy  |
| HTTP 4xx                             | 🟡 Degraded |
| Response time > 2000 ms              | 🟡 Degraded |
| HTTP 5xx                             | 🔴 Down     |
| Timeout / connection failure         | 🔴 Down     |

---

# 🚀 Run Locally

### Clone

```bash
git clone https://github.com/HarshadKulkarni31/cloudops-monitor.git
cd cloudops-monitor
```

### Start Backend

```bash
cd monitor
pip install -r requirements.txt
python -m uvicorn api:app --reload --port 8004
```

### Start Health Checker

In another terminal:

```bash
cd monitor
python health_checker.py
```

### Start Frontend

```bash
cd dashboard
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

### Environment Variable

Create:

```text
dashboard/.env.local
```

```env
VITE_API_URL=http://localhost:8004
```

---

# 🐳 Docker

Build the monitoring image:

```bash
docker build -t cloudops-monitor .
```

Run:

```bash
docker run -p 8004:8004 cloudops-monitor
```

The prototype container runs both the **FastAPI backend** and **health-check engine**.

---

# 💰 Cost-Conscious Architecture

The project was designed with cloud cost in mind.

The prototype uses AWS Fargate for containerized deployment. Since Fargate tasks consume compute resources while running, the backend has been intentionally stopped when the project is not under active development.

A future production version could move toward a serverless architecture:

```text
AWS Amplify
      │
      ▼
API Gateway
      │
      ▼
AWS Lambda
      │
      ▼
DynamoDB

EventBridge
      │
      ▼
Lambda Health Checker
      │
      ▼
Monitored Services
```

This would reduce the need for continuously running infrastructure and make the platform more suitable for low-traffic usage.

---

# 🔮 Future Improvements

* User authentication
* Multi-user service isolation
* HTTPS and custom domains
* Serverless monitoring
* AWS Lambda
* Amazon EventBridge
* DynamoDB
* Email/Slack/Discord alerts
* Historical latency analytics
* Error-rate monitoring
* Response-body validation
* API keys
* Role-based access control
* Advanced observability
* Cost optimization

---

# 🎯 What This Project Demonstrates

CloudOps Monitor demonstrates practical knowledge of:

* ☁️ Cloud infrastructure
* 🐳 Docker containerization
* ⚙️ REST API development
* 🔍 Automated service monitoring
* 🚨 Incident detection
* 📈 Performance tracking
* 💾 Persistent storage
* 🔗 Frontend/backend integration
* 🚀 AWS deployment
* 💰 Cloud cost optimization



---

## 📄 License

This project is intended primarily for educational, portfolio, and demonstration purposes.
