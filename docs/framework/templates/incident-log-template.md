# AI security incident log (template)

One entry per incident or significant near-miss. Structured logging here is what makes the [audit-without-blocking](../../strategies/audit-without-blocking.md) model actually work — an incident log that only has a prose summary loses the specific detail needed to fix the root cause.

## Incident

- **ID / date:**
- **Reported by:**
- **Which system/feature:**
- **Which OWASP risk category(ies) apply** (see [docs/owasp-llm/](../../owasp-llm/)):

## What happened

<!-- The triggering input/content, the action the system took, and the
actual outcome — three separate things. Don't collapse them into one
summary, since "the agent did X" hides whether X was caused by a bad
claim (LLM07), a manipulated tool call (LLM03), a leaked instruction
(LLM08), or something else entirely. -->

- **Triggering input/content:**
- **Action taken by the system:**
- **Actual outcome / impact:**

## Root cause

- **Which control was missing, insufficient, or bypassed?**
- **What maturity level was this control at before the incident** (per [the maturity model](../maturity-model.md))?

## Response

- **Immediate containment action:**
- **Was this reversible?** If not, what was the actual, irreversible impact?

## Follow-up

| Action | Owner | Target date | Status |
|---|---|---|---|
| | | | |

- **Target maturity level after remediation:**
- **Does this change anything in [the checklist](../checklist.md) or a system prompt / policy document?**
