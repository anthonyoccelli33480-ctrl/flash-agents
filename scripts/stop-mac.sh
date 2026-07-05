#!/bin/bash
# Arrête backend + frontend Flash Agents.

set -euo pipefail

LOG_DIR="$HOME/Library/Logs/Flash Agents"

kill_port() {
  local port=$1
  local pids
  pids=$(lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
  if [[ -n "$pids" ]]; then
    echo "  → Arrêt port $port (PID $pids)"
    kill $pids 2>/dev/null || true
    sleep 0.5
    pids=$(lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
    [[ -n "$pids" ]] && kill -9 $pids 2>/dev/null || true
  fi
}

echo ""
echo "  ⏹ Flash Agents — arrêt"
echo "  ───────────────────────"
echo ""

kill_port 8787
kill_port 5173
kill_port 5174

rm -f "$LOG_DIR/backend.pid" "$LOG_DIR/frontend.pid" 2>/dev/null || true

osascript -e 'display notification "Backend et frontend arrêtés" with title "Flash Agents"' 2>/dev/null || true

echo "  ✓ Serveurs arrêtés"
echo ""
echo "  Appuyez sur Entrée pour fermer."
read -r _