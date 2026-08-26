# Cyber Threat Intelligence Dashboard

Project ID: Inst31

This is a Phase 1 academic implementation of a cybersecurity threat intelligence dashboard built for DEPSTAR, CHARUSAT. The application centralizes IOC collection, normalization, risk scoring, dashboard analytics, threat search, and alert review in a local-first FastAPI + React stack.

## Overview

The dashboard provides a unified interface for monitoring malicious IPs, domains, URLs, hashes, and related intelligence. Phase 1 focuses on a demo-ready deployment that runs locally with SQLite, seeded threat data, JWT authentication, and a real free IP enrichment source via Shodan InternetDB.

## Phase 1 Features Implemented

- JWT-based authentication with register, login, and me endpoints
- Default demo users seeded automatically
- SQLite database with SQLAlchemy models
- IOC model, ThreatSource model, and Alert model
- Risk scoring engine with explainable scoring and severity mapping
- InternetDB IP enrichment integration without an API key
- Seeded realistic IOC data for charts, tables, filters, and alerts
- Dashboard statistics and Recharts visualizations
- Threat Explorer with filters and search
- IOC Search page with local lookup plus InternetDB enrichment for IPs
- Basic Alerts page with review action
- Responsive cybersecurity-themed React UI
- FastAPI Swagger docs at /docs

## Technology Stack

Frontend:

- React
- Vite
- Axios
- React Router
- Recharts

Backend:

- FastAPI
- SQLAlchemy
- Pydantic
- JWT authentication
- Passlib password hashing

Database:

- SQLite by default

## Project Structure

```text
cyber-threat-intelligence-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── integrations/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/
│   │   └── styles.css
│   └── package.json
└── README.md
```

## Installation Instructions

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

If you prefer to verify it with the configured interpreter on this machine:

```bash
C:/Python313/python.exe -m venv backend/venv
backend\venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload
```

The API will run at http://127.0.0.1:8000 and interactive docs will be available at http://127.0.0.1:8000/docs.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The React app will run at http://127.0.0.1:5173.

## Environment Variables

Copy `backend/.env.example` to `.env` if you want to customize settings.

```env
SECRET_KEY=change-me-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./cyber_threat_intel.db
VIRUSTOTAL_API_KEY=
ABUSEIPDB_API_KEY=
OTX_API_KEY=
```

## Demo Credentials

Administrator

- Email: admin@cti.local
- Password: Admin@123

Analyst

- Email: analyst@cti.local
- Password: Analyst@123

## API Documentation

FastAPI Swagger UI:

- /docs

## Demo Flow

1. Start the backend.
2. Start the frontend.
3. Log in with the administrator account.
4. Show dashboard cards and charts.
5. Open Threat Explorer and filter by Critical severity.
6. Search for 8.8.8.8 in IOC Search.
7. Review alerts from the Alerts page.

## Features Deferred to Phase 2

- Real VirusTotal integration
- Real AbuseIPDB integration
- Real AlienVault OTX integration
- Scheduled ingestion
- Background task scheduler
- Manual ingestion trigger
- Advanced administrator panel
- User management
- API source configuration
- Source reliability adjustment
- Advanced duplicate merging
- IOC historical risk timeline
- Wildcard search
- Email notifications
- Full alert resolution workflow
- CSV export
- PDF report generation
- Audit logs
- PostgreSQL migration
- Docker Compose production setup
- Deployment
- CI/CD
- Advanced RBAC
- Retry mechanisms for scheduled ingestion

## Notes

- The app is intentionally kept Phase 1 only.
- The backend is structured so PostgreSQL and richer source integrations can be added later without rebuilding the project.

## DevOps Setup

The project includes a Docker Compose deployment and GitHub Actions CI/CD pipeline without changing the existing application architecture.

```text
Developer -> GitHub Repository -> GitHub Actions
							  -> Frontend build
							  -> Backend validation
							  -> Compose validation
							  -> Docker image build and GHCR push
```

### Run with Docker Compose

Copy `.env.example` to `.env` and replace `SECRET_KEY` for anything beyond a local demo. Then run:

```bash
docker compose up --build
```

The frontend is available at http://localhost:8080 and proxies `/api` requests to the backend. The backend is also available at http://localhost:8000, with a public health check at `/health`.

Useful commands:

```bash
docker compose logs -f
docker compose down
docker compose up --build
```

SQLite data is stored in the named `backend-data` volume. No PostgreSQL or Redis service is required.

To run the published GHCR images, copy `.env.example` to `.env`, verify `GHCR_OWNER=kartik-015` and `GHCR_REPOSITORY=sgp-7th-sem`, authenticate with `docker login ghcr.io`, then run:

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

### Troubleshooting Docker

If Docker reports `dockerDesktopLinuxEngine` or `Docker Desktop Linux engine` is unavailable, start Docker Desktop and wait until its status says it is running. Verify it with:

```bash
docker info
```

The error `http: server gave HTTP response to HTTPS client` indicates a Docker Desktop proxy or registry configuration problem, not an application error. Check Docker Desktop Settings > Resources > Proxies, disable an incorrect proxy, and retry `docker pull nginx:1.27-alpine`. For GHCR, `denied` means the image is private or the namespace/tag is wrong; use the repository values from `.env` and authenticate with `docker login ghcr.io`.

### GitHub Actions and GHCR

The workflow in `.github/workflows/ci.yml` runs for pull requests and pushes to `main`. It installs frontend dependencies, builds the Vite app, installs backend dependencies, compiles the FastAPI application, validates Compose, and builds both Docker images. Pull requests build without pushing; pushes to `main` publish images to GHCR using the repository's automatic `GITHUB_TOKEN`.

Images are published as:

```text
ghcr.io/<owner>/<repository>-frontend
ghcr.io/<owner>/<repository>-backend
```

The workflow adds `latest` on the default branch and a `sha-<commit>` tag. GHCR package names are normalized to lowercase by Docker metadata. To use published images, authenticate to GHCR, pull the desired tags, and run Compose with matching image references in your deployment environment. The repository Actions workflow must retain `contents: read` and `packages: write` permissions; package visibility can be adjusted in GitHub under the published package settings.
