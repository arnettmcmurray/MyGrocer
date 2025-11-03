#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE:-http://127.0.0.1:5001/api/v1}"
curl -sS "$BASE/health/" || true
