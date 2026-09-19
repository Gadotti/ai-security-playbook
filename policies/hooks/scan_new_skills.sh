#!/usr/bin/env bash
# CI hook: block a PR that adds/modifies an agent skill directory if
# SkillSpector rates it HIGH or CRITICAL risk.
#
# This implements the "block" stage of docs/strategies/audit-without-blocking.md
# for labs/skillspector-scan. Run the "observe" and "alert" stages first
# (log scan output, then alert on MEDIUM+ without failing the build) for
# long enough to trust the signal before wiring this in as a hard gate.
#
# Requires `skillspector` installed (see labs/skillspector-scan/README.md).
# Wire CHANGED_SKILL_DIRS to your CI's diff detection, one directory per
# line, e.g.:
#   CHANGED_SKILL_DIRS="$(git diff --name-only origin/main... | xargs -n1 dirname | sort -u)"
#
# [to verify] SkillSpector's exact terminal/JSON output format may differ
# by version. This script greps for the severity words documented in its
# README (LOW/MEDIUM/HIGH/CRITICAL) rather than parsing a specific JSON
# schema, to stay robust across versions — verify against your installed
# version's actual output before relying on this in a real pipeline.

set -euo pipefail

: "${CHANGED_SKILL_DIRS:?Set CHANGED_SKILL_DIRS to a newline-separated list of skill directories to scan}"

failed=0

while IFS= read -r skill_dir; do
  [ -z "$skill_dir" ] && continue
  echo "Scanning $skill_dir ..."
  output="$(skillspector scan "$skill_dir" --no-llm || true)"
  echo "$output"

  if echo "$output" | grep -qiE '\b(HIGH|CRITICAL)\b'; then
    echo "BLOCKED: $skill_dir scored HIGH or CRITICAL risk." >&2
    failed=1
  fi
done <<< "$CHANGED_SKILL_DIRS"

exit $failed
