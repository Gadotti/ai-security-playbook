# Escalation matrix (template)

Fill this in per control as you roll it out, following [docs/strategies/audit-without-blocking.md](../docs/strategies/audit-without-blocking.md). The point of writing this down explicitly is to stop "what should happen when X fires" from being decided ad hoc, differently, by whoever happens to be on call.

| Severity | Example trigger | Stage | Action | Who's notified | Response time expectation |
|---|---|---|---|---|---|
| Info | A tool call outside normal-but-not-suspicious patterns | Observe | Log only, structured | No one (reviewed in aggregate later) | N/A |
| Low | A single denied tool call ([labs/ai-jail](../labs/ai-jail/)'s gateway rejecting an out-of-scope request) | Alert | Log + surface in a daily/weekly digest | Team channel, async | Next business day |
| Medium | A skill scores MEDIUM on [SkillSpector](../labs/skillspector-scan/); a spend alert crosses 80% of a cap | Alert | Real-time notification, no block | On-call / feature owner | Same day |
| High | A skill scores HIGH/CRITICAL on SkillSpector; an agent attempts an irreversible action outside its allowlist | Enforce | Hard block, human approval required to proceed | On-call, paged | Immediate |
| Critical | A spend hard-cap is hit mid-session; a tool call pattern matches a known injection technique from [labs/injection-tests](../labs/injection-tests/) | Enforce | Hard stop, session/agent-run terminated | On-call, paged + incident opened | Immediate |

Use [docs/framework/templates/incident-log-template.md](../docs/framework/templates/incident-log-template.md) once something in the High/Critical rows actually fires, and revisit this table itself whenever a real incident shows the severity or action assigned to a trigger was wrong.
