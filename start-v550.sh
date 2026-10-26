#!/bin/sh
set -eu
package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ -n "${V550_CODEX_CLI:-}" ]; then
  codex_cli=$V550_CODEX_CLI
elif command -v codex >/dev/null 2>&1; then
  codex_cli=$(command -v codex)
else
  echo "Codex CLI was not found. Open this folder in Codex Desktop instead." >&2
  exit 2
fi

if [ ! -x "$codex_cli" ]; then
  echo "Codex CLI is not executable: $codex_cli" >&2
  exit 2
fi

cd "$package_dir"
exec "$codex_cli" "$@"
