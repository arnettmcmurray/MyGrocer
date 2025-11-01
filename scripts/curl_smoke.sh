#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE:-http://localhost:5001/api}"

# Register + login
curl -s -X POST "$BASE/auth/register" -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"password"}' || true
TOKENS=$(curl -s -X POST "$BASE/auth/login" -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"password"}')
ACCESS=$(echo "$TOKENS" | python - <<'PY'
import sys, json; print(json.load(sys.stdin)["access_token"])
PY
)

# Lists
echo "Lists:"
curl -s "$BASE/lists" -H "Authorization: Bearer $ACCESS" | python -m json.tool

# Recipes with match
echo "Recipes:"
curl -s "$BASE/recipes?time_max=30" -H "Authorization: Bearer $ACCESS" | python -m json.tool

# Plan a recipe for today
TODAY=$(date +%F)
RID=$(curl -s "$BASE/recipes?time_max=30" -H "Authorization: Bearer $ACCESS" | python - <<'PY'
import sys,json
print(json.load(sys.stdin)[0]['id'])
PY
)
curl -s -X POST "$BASE/plan" -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d "{"recipe_id": $RID, "day": "$TODAY"}" | python -m json.tool

# Build grocery list from plan window
curl -s -X POST "$BASE/grocery/from-plan" -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json" -d "{"from":"$TODAY","to":"$TODAY"}" | python -m json.tool
