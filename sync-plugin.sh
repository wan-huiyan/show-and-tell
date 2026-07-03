#!/usr/bin/env bash
# The skill ships twice: at the repo root (git-clone / Cursor install) and under
# plugins/show-and-tell/skills/show-and-tell (Claude Code plugin install).
# The ROOT copy is the source of truth — run this after editing the skill so the
# plugin copy stays identical. CI (.github/workflows/check.yml) fails if they drift.
set -euo pipefail
cd "$(dirname "$0")"
dest="plugins/show-and-tell/skills/show-and-tell"
mkdir -p "$dest"
cp SKILL.md "$dest/SKILL.md"
for d in assets scripts references; do
  rm -rf "${dest:?}/$d"
  cp -R "$d" "$dest/$d"
done
echo "✓ plugin copy synced → $dest"
