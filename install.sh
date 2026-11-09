#!/usr/bin/env bash
# 플러그인 대신 ~/.claude/skills 에 심볼릭 링크로 설치한다.
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)/skills/writing"
dest="$HOME/.claude/skills/writing"
mkdir -p "$HOME/.claude/skills"
if [ -e "$dest" ] && [ ! -L "$dest" ]; then
  echo "$dest 가 이미 있습니다. 옮기거나 지운 뒤 다시 실행하세요." >&2
  exit 1
fi
ln -sfn "$src" "$dest"
echo "설치함: $dest -> $src"
