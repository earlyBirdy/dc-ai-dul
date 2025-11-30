#!/usr/bin/env bash
set -e

# Always run from repo root
cd "$(dirname "$0")"

echo "[dc-ai-dul] Bootstrapping virtualenv..."
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "[dc-ai-dul] Installing Python dependencies..."
if [ -f requirements.txt ]; then
  pip install -r requirements.txt >/dev/null
fi
pip install -e . >/dev/null

if [ -d frontend ]; then
  echo "[dc-ai-dul] Building React frontend..."
  pushd frontend >/dev/null
  if [ ! -f package.json ]; then
    echo "[dc-ai-dul] WARNING: frontend/package.json not found. Skipping frontend build."
  else:
    npm install >/dev/null
    npm run build >/dev/null
  fi
  popd >/dev/null
else
  echo "[dc-ai-dul] No frontend/ directory found, skipping frontend build."
fi

echo "[dc-ai-dul] Starting FastAPI at http://localhost:8000/app ..."
uvicorn ai_dc_dul.api.server:app --reload
