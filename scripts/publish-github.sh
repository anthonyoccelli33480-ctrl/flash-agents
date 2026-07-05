#!/bin/bash
# Crée le repo GitHub (privé par défaut) et pousse le code.
# Usage: ./scripts/publish-github.sh [public|private]

set -euo pipefail

VISIBILITY="${1:-private}"
PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_NAME="flash-agents"

cd "$PROJECT"

if ! command -v gh >/dev/null 2>&1; then
  echo "Installe GitHub CLI: brew install gh && gh auth login"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Connecte-toi: gh auth login"
  exit 1
fi

if [[ ! -d .git ]]; then
  git init -b main
  git add .
  git commit -m "feat: Flash Agents v1.0 — 40 Cerebras one-shot agents"
fi

if gh repo view "$REPO_NAME" >/dev/null 2>&1; then
  echo "Repo $REPO_NAME existe déjà — push seulement"
else
  DESC="40 one-shot AI agents on Cerebras Inference — sub-second JSON tasks, vision, rate-safe"
  gh repo create "$REPO_NAME" \
    --"$VISIBILITY" \
    --source=. \
    --remote=origin \
    --description="$DESC" \
    --push
fi

# Topics SEO (bots + search)
TOPICS=(cerebras llm-agents ai-agents inference fastapi react python developer-tools code-review vision-llm open-source)
for t in "${TOPICS[@]}"; do
  gh repo edit --add-topic "$t" 2>/dev/null || true
done

git push -u origin main 2>/dev/null || git push

echo ""
echo "✓ Repo poussé: $(gh repo view --json url -q .url)"
echo ""
if [[ "$VISIBILITY" == "private" ]]; then
  echo "⚠️  REPO PRIVÉ — les bots GitHub ne le voient PAS."
  echo "   Pour des stars: gh repo edit --visibility public"
  echo "   Puis poste sur X/HN/Reddit r/LocalLLaMA avec démo"
else
  echo "🚀 Public — indexation GitHub active sous ~15 min"
fi