#!/usr/bin/env bash
# Single source of truth: edit files in shared/, then run this to fan them into each skill's references/.
set -euo pipefail
cd "$(dirname "$0")"
for skill in skills/*/; do
  [ -d "$skill/references" ] || continue
  for f in shared/*; do
    name="$(basename "$f")"
    if [ -e "$skill/references/$name" ]; then cp "$f" "$skill/references/$name"; fi
  done
done
echo "Synced shared/ into all skill references."
