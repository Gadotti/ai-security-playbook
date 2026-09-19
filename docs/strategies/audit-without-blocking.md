# Audit without blocking: a gradual adoption model

Most AI security controls fail to get adopted not because they're technically wrong, but because they're deployed as a hard block on day one, break a legitimate workflow, and get disabled by the first frustrated team. This page lays out a **gradual adoption model** — observe → alert → block — for rolling out policies, hooks, and tool allowlists without killing productivity, and how to log/audit along the way so the eventual "block" decision is backed by real data instead of a guess.

This is a general security-engineering pattern (similar in spirit to how WAFs, EDR, and CSP are usually rolled out in "monitor mode" first), applied here to LLM/agent-specific controls. It isn't unique to this repo, but the specific triggers below are drawn from the OWASP LLM Top 10 risk pages in this repo.

## The three stages

### 1. Observe

Log the event, take no action. The goal here is purely to answer "if this policy were enforced today, what would it have broken, and how often would it have fired?"

- Log structurally: what triggered the check, which tool/action was involved, the user/agent/session identity, a severity/category tag, and enough context to reconstruct the decision later (but see the note on sensitive data below).
- Run long enough to capture your actual traffic patterns, not just a demo scenario — a rule that looks safe on a week of low-traffic testing can behave very differently once real, varied usage hits it.
- This stage doubles as your baseline for [LLM06 Unbounded Consumption](../owasp-llm/LLM06.md) monitoring (tool-call volume, cost-per-session) and [LLM03 Excessive Agency](../owasp-llm/LLM03.md) monitoring (which tools get called, by which sessions, how often) — the same structured logs serve both purposes.

### 2. Alert

Surface the event to a human (a Slack channel, a dashboard, a ticket) without blocking the action. This stage is where you find out whether your rule has false positives, and whether the humans who'd act on the alert actually have the context to do so quickly.

- Alerting thresholds are not the same as hard limits, and shouldn't be treated as a substitute for one on the highest-consequence actions. OWASP's own [LLM06](../owasp-llm/LLM06.md) guidance is explicit that fast agentic workloads can rack up damage or cost faster than a human can react to an alert — a "process refund" agent that can already have paid out before someone reads the Slack message isn't meaningfully protected by that alert.
- Use this stage to tune severity: not every anomaly deserves a page. A rule that alerts too often trains people to ignore it, which defeats the point of eventually promoting it to a block.

### 3. Block (with graduated enforcement)

Once a rule's false-positive rate is known and acceptable, enforce it — but "block everything" and "block nothing" aren't the only two options. [LLM03's](../owasp-llm/LLM03.md) mitigation research points at a more useful middle ground: **graduated enforcement by reversibility**. Auto-approve actions that are cheap to undo (e.g. issuing store credit), and route irreversible or high-blast-radius actions (an external payout, a production database write, a permission change) to mandatory human approval or a hard block — regardless of how well-tested the rule is.

- For actions where the cost of a false positive is low and reversible, prefer a hard, non-overridable stop over an alert-and-hope approach — this mirrors the [LLM06](../owasp-llm/LLM06.md) finding that spend caps which actually halt inference outperform alerting thresholds for cost control.
- For actions where a false positive would break a legitimate workflow, keep a documented override/appeal path — a control nobody can safely bypass when it's wrong is a control people will quietly work around outside the system entirely.

## Logging and audit trail, done structurally

The audit trail is what makes stage 1 (observe) useful and what makes a later incident investigation possible. A few practical points that follow directly from the OWASP risk pages already in this repo:

- **Log the decision, not just the outcome.** For [LLM07 Misinformation](../owasp-llm/LLM07.md)-related risks specifically, log the claim, the evidence it was based on, and the downstream action taken together — so a bad outcome can be traced back to the specific unverified claim that caused it, not just to "the agent did X."
- **Treat logs and traces as sensitive data themselves.** [LLM02](../owasp-llm/LLM02.md) and [LLM08](../owasp-llm/LLM08.md) both call out that reasoning traces, tool-call arguments, and full prompt/completion logs are common, overlooked leak surfaces — observability tooling often logs everything by default. Apply the same redaction/access-control discipline to your audit logs that you'd apply to the data flowing through the system itself, and never write real personal or customer data into example logs when documenting this pattern.
- **Attribute every high-consequence tool call to a triggering context.** Per [LLM03's](../owasp-llm/LLM03.md) testing guidance, log which upstream content or prompt led to a tool call, so a manipulated action can be traced back to its cause, not just flagged after the fact.

## Where this fits in this repo

- [policies/](../../policies/) is planned to hold concrete examples of this model as hooks/allowlists (Phase 3).
- [LLM03](../owasp-llm/LLM03.md) and [LLM06](../owasp-llm/LLM06.md) are the risk pages this model most directly operationalizes.
- See also the [ISO/IEC 42001 mapping](../iso-42001/README.md), Annex A.9 ("Use of AI systems") — operational monitoring of AI systems in use is close to a direct match for the observe/alert/block model described here.

## References

This page synthesizes established security-operations practice (staged rollout of detective → preventive controls) with mitigation guidance already sourced and cited on this repo's OWASP risk pages — see [LLM03](../owasp-llm/LLM03.md#references), [LLM06](../owasp-llm/LLM06.md#references), [LLM02](../owasp-llm/LLM02.md#references), and [LLM07](../owasp-llm/LLM07.md#references) for the underlying citations (Meta's Agents Rule of Two, OWASP's own graduated-enforcement and spend-cap guidance, etc.). No additional external sources were used for the staged-rollout framing itself, which is a general security-engineering pattern rather than an OWASP-specific one.
