#!/bin/bash
# Mesure latence Flash Review (5 runs) — respecte le rate-gate 15s.
set -euo pipefail
API="http://127.0.0.1:8787/api/run"
INPUT='function add(a,b){ return a+b }'
N=5
TMP=$(mktemp)
echo "Running $N Flash Review benchmarks..."
for i in $(seq 1 $N); do
  START=$(python3 -c "import time; print(int(time.time()*1000))")
  RESP=$(curl -sf -X POST "$API" \
    -H "Content-Type: application/json" \
    -d "{\"agent_id\":\"review\",\"input\":$(python3 -c "import json; print(json.dumps('$INPUT'))")}" 2>/dev/null) || { echo "run $i failed"; continue; }
  MS=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('latency_ms',0))" 2>/dev/null || echo 0)
  echo "$MS" | python3 -c "import sys; print(int(float(sys.stdin.read())))" >> "$TMP"
  echo "  run $i: ${MS}ms"
  [[ $i -lt $N ]] && sleep 16
done
python3 << PY
import statistics, pathlib
vals = [int(x) for x in pathlib.Path("$TMP").read_text().split() if x.strip()]
if not vals:
    print("NO_DATA")
else:
    vals.sort()
    def pct(p):
        i = max(0, int(len(vals)*p/100)-1)
        return vals[min(i, len(vals)-1)]
    print(f"P50={pct(50)} P95={pct(95)} P99={pct(99)} min={min(vals)} max={max(vals)} n={len(vals)}")
PY
rm -f "$TMP"