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
