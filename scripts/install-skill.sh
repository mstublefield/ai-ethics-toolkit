#!/usr/bin/env bash
# Install (or re-install) the ai-ethics skill into ~/.claude/skills/.
#
# Creates a symlink so edits in the repo show up in Claude Code immediately.
# Safe to re-run.

set -euo pipefail

SKILL_SRC="$(cd "$(dirname "$0")/.." && pwd)/skills/ai-ethics"
SKILL_DEST="$HOME/.claude/skills/ai-ethics"

if [[ ! -d "$SKILL_SRC" ]]; then
  echo "error: source skill not found at $SKILL_SRC" >&2
  exit 1
fi

mkdir -p "$HOME/.claude/skills"

if [[ -L "$SKILL_DEST" ]]; then
  current="$(readlink "$SKILL_DEST")"
  if [[ "$current" == "$SKILL_SRC" ]]; then
    echo "ai-ethics skill already installed (symlink up to date)."
    exit 0
  fi
  echo "removing existing symlink: $SKILL_DEST -> $current"
  rm "$SKILL_DEST"
elif [[ -e "$SKILL_DEST" ]]; then
  echo "error: $SKILL_DEST exists and is not a symlink. Move or remove it manually." >&2
  exit 1
fi

ln -s "$SKILL_SRC" "$SKILL_DEST"
echo "installed: $SKILL_DEST -> $SKILL_SRC"
echo
echo "Next: in Claude Code, say \"ethics review ...\" to trigger the skill."
echo "      Or run \`ethics --help\` from anywhere (uv installed) for the CLI."
