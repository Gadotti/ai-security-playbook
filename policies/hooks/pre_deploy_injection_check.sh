#!/usr/bin/env bash
# CI/pre-deploy hook: run this repo's educational injection-test corpus
# against a real target before it reaches production.
#
# labs/injection-tests/run_tests.py ships with a no-op mock target by
# design (see that lab's README) — you MUST wire mock_target() in that
# script to your actual model/agent/application before this hook means
# anything. Running it unmodified will always "pass" because nothing real
# is being tested.
#
# This belongs at the "block" stage of docs/strategies/audit-without-blocking.md,
# once you've run it in observe/alert mode long enough to trust the signal.

set -euo pipefail

cd "$(dirname "$0")/../../labs/injection-tests"
pip install -r requirements.txt --quiet

echo "Running injection-tests corpus against the wired target..."
output="$(python run_tests.py)"
echo "$output"

if echo "$output" | grep -q "verdict:  REVIEW"; then
  echo "BLOCKED: at least one case flagged REVIEW - a human must clear this before deploy." >&2
  exit 1
fi

echo "No compliance signals matched. (Reminder: this is a keyword triage, not a full review - see the lab's README.)"
