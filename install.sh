#!/usr/bin/env bash
# Install the Agent Nervous System skills for Claude Code, Codex, or Cursor.
# Usage: ./install.sh [claude|codex|cursor]   (default: claude)
set -euo pipefail

target="${1:-claude}"
here="$(cd "$(dirname "$0")" && pwd)"

# submodule dir : installed skill name
skills=(
  "consciousness-loop:consciousness-loop"
  "octopus:open-source-octopus-investigation"
  "rem-sleep:rem-sleep"
  "immune-check:immune-check"
  "sunset:sunset"
  "playtime:playtime"
  "contemplation:contemplation"
  "proprioception:proprioception"
)

case "$target" in
  claude) dest="$HOME/.claude/skills" ; mode="skillmd" ;;
  codex)  dest="$HOME/.agents/skills" ; mode="skillmd" ;;
  cursor) dest="$HOME/.cursor/commands" ; mode="cursor" ;;
  *) echo "Unknown target: $target (use claude|codex|cursor)" >&2; exit 1 ;;
esac

echo "Installing Agent Nervous System → $dest ($target)"
for entry in "${skills[@]}"; do
  dir="${entry%%:*}"; name="${entry##*:}"
  if [ "$mode" = "skillmd" ]; then
    mkdir -p "$dest/$name"
    cp "$here/$dir/SKILL.md" "$dest/$name/SKILL.md"
    echo "  ✓ $name"
  else
    mkdir -p "$dest"
    # the cursor variant lives at <dir>/cursor/<name>.md
    cp "$here/$dir"/cursor/*.md "$dest/"
    echo "  ✓ $name (cursor)"
  fi
done
echo "Done. Invoke /consciousness-loop, /rem-sleep, /immune-check, /sunset, /playtime, /contemplation, /proprioception, /open-source-octopus-investigation."
