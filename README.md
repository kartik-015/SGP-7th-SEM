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

For Docker Compose, copy `.env.example` to `.env`. The Compose file stores SQLite at `/app/data` inside the container. If you run FastAPI directly on Windows instead, use `DATABASE_URL=sqlite:///./cyber_threat_intel.db` so the local process can create the database beside the backend application.

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

## Phase 2 Features Implemented

- Administrator-only user management with role and active-state controls
- Role-based access enforcement for administrator endpoints
- Alert lifecycle statuses: New, In Progress, Reviewed, Resolved, and False Positive
- Audit logging for user and alert changes
- Authenticated IOC CSV export from Threat Explorer
- Docker-compatible SQLite persistence and local Windows SQLite guidance

The remaining Phase 2 items that require separate credentials or infrastructure are external VirusTotal, AbuseIPDB, and OTX ingestion, scheduled background jobs, email delivery, PDF generation, and PostgreSQL deployment. They remain disabled by default so local development and CI do not depend on third-party services.

## Notes

- The app is intentionally kept Phase 1 only.
- The backend is structured so PostgreSQL and richer source integrations can be added later without rebuilding the project.

## DevOps Setup

The project includes a Docker Compose deployment and GitHub Actions CI/CD pipeline without changing the existing application architecture.

## Real-Time Host Telemetry

The dashboard now supports authorized command telemetry from Kali Linux, Android Termux, and other devices on the same network. The included `telemetry-agent/telemetry_agent.py` executes a locally authorized command, collects the command, device, user, shell, platform, source address, timestamp, and exit status, and sends the event to the FastAPI backend over HTTP JSON.

The backend requires the `X-Agent-Key` header, validates the payload with Pydantic, stores it in SQLite, and applies rule-based detections for network scanning, credential attacks, privilege escalation, dangerous file operations, and account changes. A detected command becomes a telemetry threat with a risk score and severity, and an IOC plus alert is created for review. Normal commands are stored as low-risk telemetry events.

### Configure the agent

Set the same key in the root `.env` used by Docker:

```env
TELEMETRY_AGENT_KEY=change-me-agent-key
```

For a real network device, replace `127.0.0.1` with the Windows host LAN address and use the published backend port `8000`. Only monitor devices and commands you are authorized to monitor, and do not log passwords, private keys, tokens, or other secrets.

### Run an agent on Kali Linux or Termux

Copy `telemetry-agent/telemetry_agent.py` to the authorized device. Python's standard library is sufficient:

```bash
pkg update -y
pkg install python -y
export CTI_API_URL="http://WINDOWS_HOST_IP:8000"
export TELEMETRY_AGENT_KEY="change-me-agent-key"
python3 telemetry_agent.py -- whoami
```

Run each `export` command separately. Do not paste the three commands together without line breaks. On Windows, find `WINDOWS_HOST_IP` with `ipconfig`; it is the IPv4 address of the Wi-Fi adapter, for example `192.168.1.100`. The phone and Windows computer must be on the same Wi-Fi network. Windows Firewall must allow inbound TCP port 8000 for Python/Docker on that private network.

To copy the agent from Windows to a phone with Termux, use a USB/file-sharing method or a private repository, then place it in Termux's home directory. From Termux, confirm connectivity before running the agent:

```bash
curl http://WINDOWS_HOST_IP:8000/health
```

The response must be `{"status":"healthy"}`. Then send a harmless command:

```bash
python3 telemetry_agent.py -- whoami
```

Open the dashboard at `http://localhost:8080`, select **Host Telemetry**, and the new phone event will appear automatically within five seconds.

The agent prints the command output and the backend's detection response. Use a controlled demonstration command only, such as:

```bash
python3 telemetry_agent.py -- nmap -sV 10.0.0.1
```

The command is executed locally on the authorized source device; the dashboard receives only the resulting telemetry metadata. Open **Host Telemetry** in the dashboard to review events. The detected command also appears in **Threat Explorer** and **Alerts**.

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
