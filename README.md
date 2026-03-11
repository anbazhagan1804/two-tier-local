# Two-Tier Web App with Docker and Jenkins (Local Ubuntu)

## Introduction

This repository provides a fully functional two-tier application for local DevOps environments:

- Tier 1: Flask web application (Python)
- Tier 2: MySQL database
- DevOps toolchain: Git, Docker, Docker Compose, Jenkins
- Runtime target: local Ubuntu server (no cloud services)

### Objectives

- Build and run a production-style Flask + MySQL stack in containers.
- Automate validation and deployment through Jenkins CI/CD.
- Keep all setup and operations local to an Ubuntu host.

### Tech Stack (Final)

- Ubuntu Server 22.04 LTS or 24.04 LTS
- Git 2.x
- Python 3.11+
- Flask 3.x
- MySQL 8.0
- Docker Engine + Docker Compose plugin
- Jenkins (system service)

### Recommended Local Server Specification

- CPU: 2 vCPU minimum (4 vCPU recommended)
- RAM: 4 GB minimum (8 GB recommended if Jenkins runs on same host)
- Disk: 20 GB minimum (40 GB recommended)
- Network: local static/private IP preferred for stable Jenkins webhook and team access

## Installation

### 1. Clone and enter the project

```bash
git clone https://github.com/anbazhagan1804/two-tier-local two-tier-local
cd two-tier-local
```

### 2. Prepare Ubuntu server tools

Run the provided setup script on Ubuntu:

```bash
chmod +x scripts/setup-local-ubuntu.sh
./scripts/setup-local-ubuntu.sh
```

What this script installs/configures:

- Docker Engine and Docker Compose plugin
- Git and Java runtime
- Jenkins package and systemd service
- Docker group access for current user and Jenkins user

After script completion, re-login once to refresh group membership for your account.

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with secure values for local use:

```dotenv
DB_ROOT_PASSWORD=<strong-root-password>
DB_NAME=appdb
DB_USER=appuser
DB_PASSWORD=<strong-app-password>
```

### 4. Validate Python dependencies (optional local test)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest -q
```

## Configuration

### Project Structure

```text
.
+-- app/
¦   +-- __init__.py
¦   +-- db.py
¦   +-- routes.py
¦   +-- static/styles.css
¦   +-- templates/index.html
+-- db/init.sql
+-- tests/test_health.py
+-- scripts/
¦   +-- setup-local-ubuntu.sh
¦   +-- deploy.sh
¦   +-- teardown.sh
+-- Dockerfile
+-- docker-compose.yml
+-- Jenkinsfile
+-- requirements.txt
+-- run.py
```

### Application Configuration

- Flask container reads DB settings from environment variables.
- MySQL container bootstraps schema from `db/init.sql`.
- App exposes:
  - `GET /health` for smoke checks
  - `GET /` to render UI and list messages
  - `POST /messages` to store a message

### Docker Compose Details

- Service `db`: MySQL 8 with persistent volume `db_data`
- Service `web`: Flask app image built from local Dockerfile
- Dependency control: `web` waits for healthy `db`
- Ports:
  - `5000` -> Flask app
  - `3306` -> MySQL (local access)

### Jenkins Configuration (Local)

1. Open Jenkins: `http://<ubuntu-server-ip>:8080`
2. Complete first-time unlock:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

3. Install suggested plugins.
4. Create a Pipeline job:
   - Definition: `Pipeline script from SCM`
   - SCM: Git
   - Script Path: `Jenkinsfile`

Pipeline stages implemented:

- Checkout
- Prepare `.env`
- Unit Tests (`pytest`)
- Build and Deploy (`docker compose up -d --build`)
- Smoke Test (`curl /health`)

## Deployment

### Option A: Manual deployment on Ubuntu

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

Verify services:

```bash
docker compose ps
curl http://localhost:5000/health
```

Expected health response:

```json
{"status":"ok"}
```

Open the app in a browser:

- `http://<ubuntu-server-ip>:5000`

### Option B: CI/CD deployment through Jenkins

1. Push repository changes.
2. Run Jenkins pipeline job.
3. Confirm stages are green.
4. Validate app endpoint:

```bash
curl http://<ubuntu-server-ip>:5000/health
```

### Rollback/Stop

```bash
chmod +x scripts/teardown.sh
./scripts/teardown.sh
```

## Conclusion

This project delivers a complete local DevOps implementation of a two-tier web application using Flask, MySQL, Docker Compose, and Jenkins on Ubuntu. It includes:

- Application source code and database bootstrap
- Containerized runtime with persistent storage
- Jenkins pipeline for test/build/deploy/smoke validation
- Local-first operational scripts and server setup automation

### Next Steps

1. Add integration tests against a temporary MySQL service.
2. Add secure secret handling (for example, Jenkins credentials + generated `.env`).
3. Add reverse proxy (Nginx) and TLS certificates for internal network usage.
