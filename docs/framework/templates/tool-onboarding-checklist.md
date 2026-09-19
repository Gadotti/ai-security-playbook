# Tool / skill onboarding checklist (template)

Use this before connecting a new agent skill, MCP server, or tool integration — whether it's third-party or something your own team built. Pairs with [labs/skillspector-scan](../../../labs/skillspector-scan/) and [labs/ai-jail](../../../labs/ai-jail/).

## 1. Provenance

- [ ] Source (repo/publisher) identified and, if third-party, its reputation/activity checked (not just star count — see [resources/links.md](../../../resources/links.md) for how this repo evaluated tools)
- [ ] Scanned with [SkillSpector](../../../labs/skillspector-scan/) (or equivalent) before install — `skillspector scan <path> --no-llm` at minimum; note the score:
- [ ] If score is MEDIUM or above: remediation applied, or risk explicitly accepted by:
- [ ] Pinned to a specific version/commit, not a moving `latest` tag — see [LLM04](../../owasp-llm/LLM04.md)

## 2. Scope

- [ ] Exact list of capabilities this tool needs (not "what it offers," but what *this* integration actually requires):
- [ ] Any capability not needed for the above is disabled or not granted — see [LLM03](../../owasp-llm/LLM03.md)'s "excessive functionality"
- [ ] Credential/scope used is least-privilege for the listed capabilities (not a shared admin/service account) — [LLM03](../../owasp-llm/LLM03.md)

## 3. Containment

- [ ] Runs inside the sandboxing pattern from [labs/ai-jail](../../../labs/ai-jail/) (or your own equivalent): tool calls go through an allowlist gateway, execution is isolated (container/process boundary), filesystem/network access is scoped
- [ ] Tool *output* is treated as untrusted data by the calling agent, not as instructions — see [LLM01](../../owasp-llm/LLM01.md) and [LLM03](../../owasp-llm/LLM03.md)'s tool-mediated injection scenarios

## 4. Monitoring

- [ ] Every call to this tool is logged with the triggering context (what upstream content/prompt led to it) — see [docs/strategies/audit-without-blocking.md](../../strategies/audit-without-blocking.md)
- [ ] Current stage on the maturity model for this specific tool: Observe / Alert / Enforce / Continuously validated (circle one)

## 5. Sign-off

- Onboarded by:
- Date:
- Re-review date (don't onboard-and-forget — re-scan on updates):
