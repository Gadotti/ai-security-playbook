# LLM08: Hidden Context Exposure

**Layer:** Amplifier · [back to overview](README.md)

## Description

Hidden Context Exposure is the unauthorized extraction, inference, or reconstruction of non-user-facing instructions or operational context assembled into a model's context window. This category **replaces** the 2025 edition's "System Prompt Leakage" (LLM07:2025), but with a much broader scope: it covers not just the literal system prompt, but developer instructions, retrieved RAG policy/knowledge text, stored configuration, user-profile data, agent/session memory, and tool/function schemas exposed to the model.

The design principle OWASP pushes is **"assume it leaks"** — severity depends on *what* you put into hidden context, not on *whether* disclosure happens; hidden context is explicitly framed as never a security boundary. This is a real shift from the 2025 framing, which implicitly treated the system prompt as something that could be kept confidential. The motivating history traces back to the 2023 Bing Chat "Sydney" persona leak and continues through more recent tool-schema extraction attacks.

## Attack scenarios

- **Credential/secret leakage.** A system prompt embeds API keys or tokens directly; extracting the prompt hands the attacker reusable credentials.
- **Tool/function schema extraction.** An attacker extracts the full list of available tools and their parameter schemas, then crafts inputs specifically shaped to steer or abuse the application's tool-calling logic.
- **Guardrail disclosure.** A system prompt encodes refusal/filtering rules (e.g. "refuse if X, redirect if Y"); once exposed, an attacker reverse-engineers the exact bypass phrasing needed for a targeted jailbreak.
- **Internal authorization-boundary disclosure**, e.g. via internal MCP servers — hidden directives about permission boundaries leak, revealing what an internal tool-serving layer will and won't allow.
- **Output-structure leakage.** Exposed formatting rules (e.g. a required JSON response schema) let attackers craft malformed or adversarial structured output that downstream systems mis-parse.
- **Broadened 2026 example.** An agent's tool-call *response* (a database query result, a memory retrieval) is echoed back into a visible completion, exposing another user's data or internal application state — in scope under the new definition even though it's not the system prompt at all.

## Mitigations

**Established:**
- Never place secrets in hidden context (credentials, connection strings, security-critical configuration) — OWASP's first-line rule.
- Don't delegate authorization/privilege decisions to the model — enforce privilege separation and authorization checks in deterministic application code, never via a system-prompt instruction the model "promises" to follow.
- Use deterministic guardrails/validators external to the model for behavior control, rather than relying on prompt-encoded rules — necessary, but explicitly not sufficient on its own.

**Emerging:**
- Design assuming disclosure: classify everything placed in hidden context by severity (informational → low; internal rules/filtering criteria → medium; embedded credentials/tokens → high; anything enabling RCE or privilege escalation → critical) and keep high/critical-tier content out of context entirely. This severity-tiering approach appears to be new 2026 OWASP guidance, not yet a widely standardized industry practice.
- Academic mitigation research: "system vectors" to reduce prompt leakage (Cao et al., 2025) and extraction-attack defenses (Das, Amini & Wu, 2025) — both still academic-stage, not yet productized.

## Testing & detection

- [NVIDIA/garak](https://github.com/NVIDIA/garak) — actively maintained (v0.17.0, Sept 2026); includes a dedicated system-prompt-extraction probe and a refusal detector.
- [promptfoo](https://github.com/promptfoo/promptfoo) redteam plugins — actively maintained; includes a "Prompt Leakage" test category alongside instruction-injection and data-extraction tests, covering tool-schema and agent-memory exposure under this expanded scope.
- [jujumilk3/leaked-system-prompts](https://github.com/jujumilk3/leaked-system-prompts) — a crowd-sourced corpus of real leaked system prompts, useful as a red-teaming reference corpus (maintenance status not independently checked).
- Manual approach: enumerate everything assembled into context (system prompt, RAG snippets, memory, tool schemas, profile data) and run an explicit "what happens if this specific piece leaks" severity assessment per the tiering above.

## References

*Accessed 2026-09-19.*

- OWASP LLM08:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM08_HiddenContextExposure.md)
- jujumilk3/leaked-system-prompts — [github.com](https://github.com/jujumilk3/leaked-system-prompts)
- NVIDIA/garak — [github.com](https://github.com/NVIDIA/garak)
- Giskard, commentary on the LLM07→LLM08 rename — [giskard.ai](https://www.giskard.ai/knowledge/owasp-top-10-for-llm-2026)
- Check Point, "Reading the signals in the OWASP LLM Top 10 2026" — [blog.checkpoint.com](https://blog.checkpoint.com/ai-security/reading-the-signals-in-the-owasp-llm-top-10-2026/amp/)
