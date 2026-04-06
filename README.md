# 🔗 QuickURL — URL Shortener

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)

A production-ready URL shortener built with **Flask + Redis**, containerized with **Docker**, monitored with **Prometheus + Grafana**, and deployed via a **Jenkins CI/CD pipeline**.

> 🎓 **DevOps Capstone Project**

---

## 🏗️ Architecture

```
┌──────────┐     ┌──────────────┐     ┌─────────────────────────────────┐
│          │     │              │     │         Docker Network          │
│  GitHub  ├────►│   Jenkins    ├────►│                                 │
│          │     │  (CI/CD)     │     │  ┌───────────┐  ┌───────────┐  │
└──────────┘     └──────────────┘     │  │  Flask    │  │  Redis    │  │
                                      │  │  App      ├──►  (Cache)  │  │
                                      │  │  :5050    │  │  :6379    │  │
                                      │  └─────┬─────┘  └───────────┘  │
                                      │        │                       │
                                      │        ▼                       │
                                      │  ┌───────────┐  ┌───────────┐ │
                                      │  │Prometheus │  │  Grafana  │ │
                                      │  │  :9090    ├──►  :3000    │ │
                                      │  └───────────┘  └───────────┘ │
                                      └─────────────────────────────────┘
```

---

## 📂 Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py          # App factory, Redis connection
│   ├── routes.py            # API endpoints
│   ├── utils.py             # Short code generation, URL validation
│   └── templates/
│       └── index.html       # Frontend UI
├── static/
│   ├── style.css            # Dark theme styling
│   └── script.js            # Client-side logic
├── tests/
│   └── test_app.py          # Pytest suite with fakeredis
├── Dockerfile               # Container image (python:3.11-slim)
├── docker-compose.yml       # Multi-service orchestration
├── Jenkinsfile              # CI/CD pipeline (6 stages)
├── prometheus.yml           # Prometheus scrape config
├── requirements.txt         # Python dependencies
├── .gitignore
├── README.md
└── run.py                   # App entry point
```

---

## ✅ Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- [Jenkins](https://www.jenkins.io/doc/book/installing/) (for CI/CD pipeline)
- Git

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
docker-compose up -d --build
```

That's it! All 4 services will start automatically.

---

## 🌐 Service URLs

| Service        | URL                          | Credentials         |
|--------------- |----------------------------- |--------------------- |
| **App**        | http://localhost:5050         | —                    |
| **Prometheus** | http://localhost:9090         | —                    |
| **Grafana**    | http://localhost:3000         | admin / admin123     |
| **Redis**      | localhost:6379               | —                    |

> ⚠️ **macOS Note:** If port 5050 is blocked by AirDrop, change the host port in `docker-compose.yml` to `5050:5050` and access at http://localhost:5050

---

## 🔌 API Endpoints

| Method | Endpoint         | Description                    |
|--------|------------------|--------------------------------|
| GET    | `/`              | Web UI                         |
| POST   | `/shorten`       | Shorten a URL                  |
| GET    | `/<short_code>`  | Redirect to original URL (302) |
| GET    | `/stats`         | Total URLs + health status     |

### Example Request

```bash
curl -X POST http://localhost:5050/shorten \
     -H "Content-Type: application/json" \
     -d '{"long_url": "https://www.google.com"}'
```

### Example Response

```json
{
  "short_url": "http://localhost:5050/aB3xYz",
  "short_code": "aB3xYz",
  "long_url": "https://www.google.com",
  "created_at": "2026-04-06T17:30:00+00:00"
}
```

---

## 🧪 Running Tests

```bash
# With virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -v

# Or with Docker
docker exec urlshortener-web python -m pytest tests/ -v
```

---

## 🏗️ Jenkins CI/CD Setup

### 1. Install Jenkins Plugins
- **Docker Pipeline**
- **Pipeline**
- **Git**
- **JUnit**

### 2. Create Pipeline Job
1. Open Jenkins → **New Item** → **Pipeline**
2. Under **Pipeline** section, select **Pipeline script from SCM**
3. Set SCM to **Git** and enter your repository URL
4. Script Path: `Jenkinsfile`
5. Click **Save** and **Build Now**

### 3. Pipeline Stages

| #  | Stage               | Description                          |
|----|---------------------|--------------------------------------|
| 1  | Checkout            | Clone source from SCM                |
| 2  | Install Dependencies| Create venv, install packages        |
| 3  | Run Tests           | Run pytest, generate JUnit XML       |
| 4  | Build Docker Image  | Build & tag with latest + build num  |
| 5  | Deploy              | docker-compose down → up -d          |
| 6  | Health Check        | Curl /stats, fail if unhealthy       |

---

## 📊 Grafana Dashboard Setup

1. Open **http://localhost:3000** and login with `admin` / `admin123`
2. Go to **Connections** → **Data Sources** → **Add data source**
3. Select **Prometheus**
4. Set URL to `http://prometheus:9090`
5. Click **Save & Test**
6. Go to **Dashboards** → **New Dashboard** → **Add Visualization**
7. Use PromQL queries like:
   - `urlshortener_total_urls` — Total shortened URLs
   - `up{job="urlshortener"}` — App health status

---

## ⚙️ Environment Variables

| Variable      | Description               | Default                   |
|---------------|---------------------------|---------------------------|
| `REDIS_URL`   | Redis connection string   | `redis://localhost:6379`  |
| `SECRET_KEY`  | Flask secret key          | `dev-secret-key`          |
| `GF_SECURITY_ADMIN_PASSWORD` | Grafana password | `admin123`          |

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.
