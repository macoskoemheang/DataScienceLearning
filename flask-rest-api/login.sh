#!/usr/bin/env bash
# Log in to the Flask API and export the access token as $TOKEN.
#
# IMPORTANT: must be SOURCED, not executed, so the export reaches your shell:
#   source login.sh <username> <password>
#   . login.sh <username> <password>
#
# NOTE: local variables are named LOGIN_USER/LOGIN_PASS on purpose, not
# USERNAME/PASSWORD -- on some systems (e.g. AD-joined Macs) USERNAME is a
# protected/managed shell variable that silently resets itself.

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "Error: run this with 'source login.sh <username> <password>', not './login.sh ...'"
  echo "(a plain execution runs in a subshell, so the exported TOKEN would be lost)"
  exit 1
fi

BASE_URL="${BASE_URL:-http://127.0.0.1:5000}"
LOGIN_USER="$1"
LOGIN_PASS="$2"

if [[ -z "$LOGIN_USER" || -z "$LOGIN_PASS" ]]; then
  echo "Usage: source login.sh <username> <password>"
  return 1
fi

RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$LOGIN_USER\", \"password\": \"$LOGIN_PASS\"}")

ACCESS_TOKEN=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
REFRESH=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('refresh_token', ''))" 2>/dev/null)

if [[ -z "$ACCESS_TOKEN" ]]; then
  echo "Login failed: $RESPONSE"
  return 1
fi

export TOKEN="$ACCESS_TOKEN"
export REFRESH_TOKEN="$REFRESH"

echo "Logged in as $LOGIN_USER"
echo "TOKEN exported for this shell session."
echo
echo "Try it:"
echo "  curl \$BASE_URL/api/tasks -H \"Authorization: Bearer \$TOKEN\""
