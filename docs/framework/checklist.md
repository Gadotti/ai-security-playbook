# Security checklist

Organized by [this repo's concentric layers](../../README.md#mental-model-concentric-layers). Each item links to the OWASP risk page or lab it comes from — read that page before marking an item "done," since a checkbox without understanding the underlying risk is worse than no checklist at all.

This is meant to be copied into your own tracker (an issue, a spreadsheet, a wiki page) and scored honestly: **Yes / Partial / No**, not just checked off.

## Entry vectors

- [ ] Retrieved content, tool output, and any input that isn't the direct user is treated as *data*, not as instructions — see [LLM01](../owasp-llm/LLM01.md), [docs/strategies/prompt-injection.md](../strategies/prompt-injection.md)
- [ ] MCP servers and third-party tool packages are pinned, signed, or otherwise verified before being connected — [LLM01](../owasp-llm/LLM01.md), [LLM04](../owasp-llm/LLM04.md)
- [ ] Model weights, datasets, and adapters are tracked via a signed AI-BOM/ML-BOM, or you know explicitly that you aren't doing this yet — [LLM04](../owasp-llm/LLM04.md)
- [ ] Pickle/unsafe serialization formats are avoided for model artifacts in favor of safer formats — [LLM04](../owasp-llm/LLM04.md)
- [ ] Fine-tuning/training data pipelines have access control, versioning, and provenance tracking — [LLM05](../owasp-llm/LLM05.md)
- [ ] Models are probed for backdoor triggers after fine-tuning/alignment cycles, rather than assuming safety training removed them — [LLM05](../owasp-llm/LLM05.md)

## Amplifiers

- [ ] Nothing that would be dangerous if disclosed (secrets, bypassable authorization logic) is placed in a system prompt, RAG document, or agent memory — [LLM08](../owasp-llm/LLM08.md)
- [ ] Authorization is enforced in application code, never delegated to the model's own judgment about what it should reveal — [LLM08](../owasp-llm/LLM08.md)
- [ ] Vector-index queries enforce tenant/identity scoping *inside* the query itself, not as a post-retrieval filter — [LLM09](../owasp-llm/LLM09.md)
- [ ] High-sensitivity RAG data lives in a physically separate index/namespace, not a shared index with metadata tags — [LLM09](../owasp-llm/LLM09.md)
- [ ] Vector-DB backups and third-party embeddings are treated as sensitive as the underlying source documents (embeddings are invertible) — [LLM09](../owasp-llm/LLM09.md)

## Impacts

- [ ] PII/secret redaction uses classifier-based detection (e.g. Presidio), not regex/blocklists alone — [LLM02](../owasp-llm/LLM02.md), [labs/prompt-anonymizer](../../labs/prompt-anonymizer/)
- [ ] Reasoning traces, tool-call arguments, and full prompt/completion logs are treated as sensitive outputs subject to redaction, not left to observability-tool defaults — [LLM02](../owasp-llm/LLM02.md)
- [ ] Inference cost has a **hard** cap (halts, not just alerts) per session/user/agent-run, in addition to ordinary rate limits — [LLM06](../owasp-llm/LLM06.md)
- [ ] Agentic loops have circuit breakers: step limits, recursion-depth limits, time limits, per-run cost ceilings — [LLM06](../owasp-llm/LLM06.md)
- [ ] Consequential agent actions follow a "claim-check-act" pattern — claims are verified against a source of truth before being acted on — [LLM07](../owasp-llm/LLM07.md)
- [ ] Multi-agent pipelines re-verify a peer agent's claims rather than propagating trust transitively — [LLM07](../owasp-llm/LLM07.md)

## Boundary risks

- [ ] Agent tools are scoped to the minimum functionality the task needs — no open-ended "run shell command" or "fetch any URL" primitives — [LLM03](../owasp-llm/LLM03.md), [labs/ai-jail](../../labs/ai-jail/)
- [ ] Tool credentials use least-privilege downstream ACLs (DB grants, OAuth scopes), not a shared over-privileged service account — [LLM03](../owasp-llm/LLM03.md)
- [ ] Irreversible or externally-visible actions require human approval, with reversible/low-impact actions auto-approved (graduated enforcement) — [LLM03](../owasp-llm/LLM03.md), [docs/strategies/audit-without-blocking.md](../strategies/audit-without-blocking.md)
- [ ] All LLM output is treated as untrusted before reaching any sink (shell, SQL, browser DOM, terminal, auto-deployed code) — [LLM10](../owasp-llm/LLM10.md)
- [ ] Chat/agent UIs don't auto-render Markdown images, link previews, or iframes from model output by default — [LLM10](../owasp-llm/LLM10.md)

## Cross-cutting

- [ ] New controls are rolled out observe → alert → block, not deployed straight to a hard block — [docs/strategies/audit-without-blocking.md](../strategies/audit-without-blocking.md)
- [ ] Logging is structured (trigger, action, identity, severity, context) and itself treated as sensitive data — [docs/strategies/audit-without-blocking.md](../strategies/audit-without-blocking.md)
- [ ] System prompts document their rationale and known limitations rather than being treated as a finished security boundary — [system-prompts/](../../system-prompts/)
- [ ] Agent skills and MCP servers are scanned before installation — [labs/skillspector-scan](../../labs/skillspector-scan/)
- [ ] Prompt-injection defenses are tested against an adaptive attacker who knows the deployed defense, not just a static payload list — [labs/injection-tests](../../labs/injection-tests/)
