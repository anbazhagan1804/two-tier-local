#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

docker compose down --remove-orphans || true
docker compose up -d --build

echo "Deployment completed."
echo "Application URL: http://<ubuntu-server-ip>:5000"
