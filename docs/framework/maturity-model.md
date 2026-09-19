# Maturity model

A 5-level scale, applied per risk area (an OWASP risk, a layer, or a specific control) rather than as one number for your whole system — most real systems are at different levels for different risks, and pretending otherwise hides where the actual gaps are.

This builds directly on the observe → alert → block progression from [docs/strategies/audit-without-blocking.md](../strategies/audit-without-blocking.md); levels 1-3 map onto that model's three stages, with level 0 and level 4 as the honest endpoints most maturity models skip.

| Level | Name | What it looks like | Typical failure mode below this level |
|---|---|---|---|
| 0 | **Absent** | No visibility, no logging, no control. If something goes wrong, you find out from the user, a customer complaint, or a public incident — not from your own system. | You can't tell whether you have a problem, let alone how big it is. |
| 1 | **Observe** | Structured logging exists for the relevant events (tool calls, retrieved documents, spend, claims-and-actions), but nothing acts on it automatically. This is where you build your baseline — see [audit-without-blocking's "observe" stage](../strategies/audit-without-blocking.md#1-observe). | You have data but no one is looking at it; an incident is discoverable in hindsight but wasn't caught in time. |
| 2 | **Alert** | Anomalies and policy violations are surfaced to a human (dashboard, Slack, ticket) without blocking the action. You're actively tuning false-positive rates at this level. | For anything with a fast blast radius (agentic loops, spend), the alert can arrive after the damage is done — see [audit-without-blocking's "alert" stage](../strategies/audit-without-blocking.md#2-alert). |
| 3 | **Enforce (graduated)** | Hard, non-overridable stops exist for high-consequence actions; low-consequence/reversible actions are auto-approved rather than blanket-blocked. This is the level most of this repo's mitigations (LLM03's graduated enforcement, LLM06's hard spend caps) describe as the target state. | A control that blocks everything indiscriminately gets disabled by the first team it breaks — enforcement without graduation doesn't survive contact with real usage. |
| 4 | **Continuously validated** | Enforcement from level 3 is regularly re-tested — red-teaming (promptfoo/garak/PyRIT, or this repo's [injection-tests](../../labs/injection-tests/)), adaptive-attacker testing per [LLM01](../owasp-llm/LLM01.md), and revisiting controls as the threat landscape and the OWASP list itself change. | Controls that were correct when built silently rot as attack techniques, your system's architecture, or the underlying OWASP guidance evolves — this repo's own [2025→2026 renumbering](../notes/owasp-numbering-check.md) is a concrete example of guidance changing under you. |

## Using this per risk area

Copy this table and fill in a row per OWASP risk (or per layer, if you want a coarser first pass) you assessed with the [checklist](checklist.md):

| Risk / area | Current level | Target level | Evidence / notes |
|---|---|---|---|
| LLM01 Prompt Injection | | | |
| LLM02 Sensitive Information Disclosure | | | |
| LLM03 Excessive Agency | | | |
| LLM04 Supply Chain | | | |
| LLM05 Data and Model Poisoning | | | |
| LLM06 Unbounded Consumption | | | |
| LLM07 Misinformation | | | |
| LLM08 Hidden Context Exposure | | | |
| LLM09 Vector and Embedding Weaknesses | | | |
| LLM10 Improper Output Handling | | | |

A reasonable rollout order is usually: reach level 1 (observe) everywhere first, then prioritize level 2-3 for whichever risks the [checklist](checklist.md) shows the most "No" answers on, rather than pushing one risk area to level 4 while others sit at level 0.
