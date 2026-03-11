# Local Ubuntu Deployment Runbook

## Introduction

This runbook documents end-to-end setup and deployment of the two-tier app using Flask, MySQL, Docker, Docker Compose, and Jenkins on a local Ubuntu server.

## Installation

1. Install dependencies via `scripts/setup-local-ubuntu.sh`.
2. Clone the repository.
3. Create `.env` from `.env.example`.
4. Run unit tests with `pytest`.

## Configuration

1. Set strong credentials in `.env`.
2. Ensure `jenkins` user is in `docker` group.
3. Confirm Docker and Jenkins services are active:

```bash
sudo systemctl status docker
sudo systemctl status jenkins
```

## Deployment

Use one of the following:

- Manual: `./scripts/deploy.sh`
- Automated: Jenkins pipeline from `Jenkinsfile`

Health check:

```bash
curl http://localhost:5000/health
```

## Conclusion

The stack is fully local and designed for repeatable deployment, validation, and team collaboration in a DevOps lab or on-prem environment.
