# Framework

A simple, adoptable framework that consolidates this repo's OWASP risk pages, strategies, and labs into something a team can actually run with. Three parts:

1. **[checklist.md](checklist.md)** — a practical, per-layer checklist for assessing where your AI system stands today, with each item linked to the relevant OWASP risk page.
2. **[maturity-model.md](maturity-model.md)** — a 5-level maturity scale (Absent → Observe → Alert → Enforce → Continuously validated) you can apply per risk area, building directly on [docs/strategies/audit-without-blocking.md](../strategies/audit-without-blocking.md).
3. **[templates/](templates/)** — fillable Markdown templates for the recurring reviews this framework implies: a pre-launch risk review, a tool/skill onboarding checklist, and an incident log.

## How to use it

1. Run the **checklist** against your actual system. Be honest about "no" and "partially" — the point is an accurate baseline, not a passing score.
2. For each layer or risk area where the checklist found gaps, place it on the **maturity model**: is there no visibility at all (Level 0), logging but no action (Level 1), alerting (Level 2), enforcement (Level 3), or enforcement plus ongoing testing (Level 4)?
3. Use the **templates** to operationalize the next step — a risk review before shipping a new agent feature, an onboarding checklist before installing a new skill/MCP server, an incident log entry when something goes wrong.
4. Re-run the checklist periodically. The underlying OWASP list itself gets revised (this repo tracks the 2026 edition — see [docs/notes/owasp-numbering-check.md](../notes/owasp-numbering-check.md)), and your own system changes faster than any static document can track.

This framework doesn't replace the individual OWASP risk pages, the strategy docs, or the labs — it's the index that ties them together into something you can walk a team through in one sitting.
