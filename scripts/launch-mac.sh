#!/bin/bash
# Démarre backend + frontend Flash Agents, ouvre le navigateur, vérifie Cerebras.

set -euo pipefail

# Repo root, derived from this script's location (portable — works wherever the repo is cloned).
PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$HOME/Library/Logs/Flash Agents"
FRONT_URL="http://127.0.0.1:5173"

mkdir -p "$LOG_DIR"

port_in_use() {
  lsof -iTCP:"$1" -sTCP:LISTEN -t >/dev/null 2>&1
}

http_ready() {
  local url=$1
  curl -sf --max-time 2 "$url" >/dev/null 2>&1
}

wait_for_http() {
  local label=$1
  shift
  local urls=("$@")
  for _ in $(seq 1 80); do
    for url in "${urls[@]}"; do
      if http_ready "$url"; then
        echo "$url"
        return 0
      fi
    done
    sleep 0.5
  done
  return 1
}

notify() {
  osascript -e "display notification \"$2\" with title \"Flash Agents\" subtitle \"$1\"" 2>/dev/null || true
}

open_browser() {
  local url=$1
  if open "$url" 2>/dev/null; then
    return 0
  fi
  open -a Safari "$url" 2>/dev/null || open -a "Google Chrome" "$url" 2>/dev/null || true
}

echo ""
echo "  ⚡ Flash Agents — démarrage"
echo "  ───────────────────────────"
echo ""

if [[ ! -x "$PROJECT/backend/.venv/bin/uvicorn" ]]; then
  echo "  Première installation (venv + npm)…"
  (cd "$PROJECT" && make install)
fi

if port_in_use 8787 && http_ready "http://127.0.0.1:8787/api/health"; then
  echo "  ✓ Backend déjà actif (port 8787)"
else
  if port_in_use 8787; then
    echo "  → Port 8787 occupé mais backend injoignable — redémarrage…"
    lsof -tiTCP:8787 -sTCP:LISTEN 2>/dev/null | xargs kill 2>/dev/null || true
    sleep 1
  fi
  echo "  → Backend Cerebras proxy…"
  (
    cd "$PROJECT/backend"
    nohup .venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8787 \
      >>"$LOG_DIR/backend.log" 2>&1 &
    echo $! >"$LOG_DIR/backend.pid"
  )
fi

FRONT_CANDIDATES=(
  "http://127.0.0.1:5173"
  "http://localhost:5173"
  "http://127.0.0.1:5174"
  "http://localhost:5174"
)

READY_URL=""
for url in "${FRONT_CANDIDATES[@]}"; do
  if http_ready "$url"; then
    READY_URL=$url
    break
  fi
done

if [[ -n "$READY_URL" ]]; then
  FRONT_URL=$READY_URL
  echo "  ✓ Frontend déjà actif ($FRONT_URL)"
else
  if port_in_use 5173 || port_in_use 5174; then
    echo "  → Port frontend occupé mais page injoignable — redémarrage…"
    lsof -tiTCP:5173 -sTCP:LISTEN 2>/dev/null | xargs kill 2>/dev/null || true
    lsof -tiTCP:5174 -sTCP:LISTEN 2>/dev/null | xargs kill 2>/dev/null || true
    sleep 1
  fi
  echo "  → Frontend React…"
  (
    cd "$PROJECT/frontend"
    nohup npm run dev >>"$LOG_DIR/frontend.log" 2>&1 &
    echo $! >"$LOG_DIR/frontend.pid"
  )
  if READY_URL=$(wait_for_http "frontend" "${FRONT_CANDIDATES[@]}"); then
    FRONT_URL=$READY_URL
    echo "  ✓ Frontend prêt ($FRONT_URL)"
  else
    echo "  ✗ Frontend n'a pas répondu — voir $LOG_DIR/frontend.log"
    notify "Erreur" "Frontend indisponible"
    exit 1
  fi
fi

echo "  → Connexion Cerebras…"
HEALTH=""
if HEALTH=$(wait_for_http "backend" "http://127.0.0.1:8787/api/health"); then
  HEALTH=$(curl -sf "http://127.0.0.1:8787/api/health")
else
  echo "  ✗ Backend injoignable — voir $LOG_DIR/backend.log"
  notify "Erreur" "Backend injoignable"
  exit 1
fi

KEY_OK=$(echo "$HEALTH" | python3 -c "import sys,json; print(json.load(sys.stdin).get('cerebras_key', False))" 2>/dev/null || echo "False")

echo ""
if [[ "$KEY_OK" == "True" ]]; then
  echo "  ✓ Clé Cerebras OK — prêt à lancer des agents"
  notify "Prêt" "Cerebras connecté · ouverture du navigateur"
else
  echo "  ○ Pas de clé API — l'onboarding s'ouvrira pour la configurer"
  notify "Configuration" "Ajoute ta clé Cerebras dans l'onboarding"
fi

if ! http_ready "$FRONT_URL"; then
  echo "  ✗ Page frontend injoignable sur $FRONT_URL"
  notify "Erreur" "Safari ne peut pas ouvrir — serveur pas prêt"
  exit 1
fi

echo "  → Ouverture $FRONT_URL"
open_browser "$FRONT_URL"

echo ""
echo "  Logs : $LOG_DIR"
echo "  Arrêt : double-clic sur « Arrêter Flash Agents.command » sur le Bureau"
echo ""
echo "  Appuyez sur Entrée pour fermer cette fenêtre (les serveurs restent actifs)."
read -r _