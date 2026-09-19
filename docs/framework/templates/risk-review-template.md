# Pre-launch AI risk review (template)

Copy this into your own tracker before shipping a new LLM-backed feature or agent. Fill in every section — an empty section is a gap, not something to skip.

## 1. What is this feature/agent, in one paragraph?

<!-- What does it do, who uses it, what data and systems can it touch? -->

## 2. What can it act on, and with what authority?

| Tool / capability | What it can do | Credential / scope used | Reversible? |
|---|---|---|---|
| | | | |

Run this table against [LLM03: Excessive Agency](../../owasp-llm/LLM03.md) — for each row, could it be narrower (excessive functionality), less privileged (excessive permissions), or gated by human approval (excessive autonomy)?

## 3. What inputs does it process, and are any of them untrusted?

<!-- Direct user input is one thing. Retrieved documents, tool responses,
another agent's output, and RAG results are all untrusted-by-default per
LLM01 and LLM09 — list every channel here, not just the obvious one. -->

| Input source | Trusted? | How injected content would be treated |
|---|---|---|
| | | |

## 4. What sensitive data could pass through it?

<!-- See LLM02. Consider training-time, inference-time, pipeline-time
(logs/traces/observability), and side-channel exposure, not just "what's
in the prompt." -->

## 5. Checklist pass

Run the [full checklist](../checklist.md) against this specific feature (not your whole system) and paste the "No" and "Partial" rows here:

| Item | Status | Plan |
|---|---|---|
| | | |

## 6. Maturity level for this feature

Using [the maturity model](../maturity-model.md), what level is this feature at *today*, for its highest-risk area? What level does it need to be at before launch, and what level is acceptable to defer to post-launch with an explicit follow-up?

- Current level:
- Required level before launch:
- Deferred items (with owner + date):

## 7. Sign-off

- Reviewed by:
- Date:
- Known residual risk accepted (if any), and by whom:
