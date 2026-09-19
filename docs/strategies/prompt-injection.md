# Defending against prompt injection

Cross-cutting strategy notes for [LLM01: Prompt Injection](../owasp-llm/LLM01.md). This page pulls together current (2025–2026) defense strategy across the three delivery surfaces — direct, indirect (retrieved content), and tool/agent-channel (RAG, MCP, tool output) — rather than repeating the LLM01 risk page's scenario/mitigation catalog.

## The core problem, briefly

LLMs process instructions and data as the same token stream. There is no equivalent of a parameterized query to separate "what the developer told the model to do" from "what a document, tool response, or user happened to say." OWASP, NIST (2025), and the UK NCSC (2025) are explicit that **no reliable prevention mechanism exists today** for prompt injection itself — defense is about containment and blast-radius reduction, not making injection impossible. Any strategy that promises to "solve" prompt injection outright should be treated with skepticism.

## By delivery surface

### Direct injection

A user directly instructs the model to ignore its system prompt, roleplay past a restriction, or reveal hidden instructions.

- Least effective alone: instructing the model "don't do X" in the system prompt. OWASP itself flags prompt-based allow/deny lists as bypassable once an attacker infers the prompt (see [LLM08](../owasp-llm/LLM08.md) — assume hidden context leaks).
- More effective: keep anything a leaked system prompt would make dangerous (credentials, authorization logic, filtering rules whose disclosure enables a targeted bypass) out of the prompt entirely, and enforce those rules in deterministic code instead.
- Test with an adaptive attacker who already knows your defense — static, one-shot jailbreak tests overstate how safe a system is.

### Indirect injection (retrieved content, RAG, documents)

Instructions hidden in a webpage, PDF, email, or RAG-retrieved chunk get executed because the model can't distinguish "content to summarize" from "instructions to follow."

- Treat all retrieved content as untrusted input, same as user input — provenance-label it if your pipeline can (a "data" channel distinct from an "instructions" channel), while accepting OWASP's finding that this labeling only helps against non-adaptive attackers.
- Strip invisible Unicode (zero-width characters, tag-block characters, variation selectors) at ingest, since these are a known encoding vector for hiding injected instructions in text that looks clean to a human reviewer.
- For RAG specifically, pair this with the [LLM09](../owasp-llm/LLM09.md) mitigations — pre-filter by tenant/identity inside the index query, and validate/normalize content before it's embedded, since a poisoned retrieval and an injected instruction are often the same attack wearing two different OWASP labels.

### Tool/agent-channel injection (MCP, tool output, multi-agent)

The newest and, per the 2026 OWASP edition, the fastest-growing surface: a tool's response, a connected MCP server, or a peer agent's output carries the injected instruction.

- Meta's ["Agents Rule of Two"](https://ai.meta.com/blog/practical-ai-agent-security/) (Oct 2025): don't let one agent session simultaneously (1) process untrusted input, (2) access sensitive systems/data, and (3) take autonomous high-impact action. If a workflow genuinely needs all three, require per-action human approval instead of trusting the model to self-police.
- Simon Willison's ["lethal trifecta"](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) is the same idea from a different angle — private data + untrusted content + an external communication channel is the combination that turns injection into exfiltration.
- Pin, sign, and verify MCP servers and third-party tool packages before connecting them; audit tool descriptions themselves for hidden instructions. This isn't theoretical — a poisoned support-ticket field was used to trick a Supabase MCP server (via Cursor) into dumping a production database using a privileged service-role key ([General Analysis research, 2025](https://simonwillison.net/2025/Jul/6/supabase-mcp-lethal-trifecta/)), and a malicious npm package `postmark-mcp` silently BCC'd every email it handled to an attacker for months before discovery ([reported Sept 2025](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)).
- Execute every tool call in the *calling user's* actual authorization scope — not a shared, over-privileged service account — and preserve that scope across delegated/multi-agent calls rather than letting a downstream agent inherit broader trust than the original request warranted.

## Testing

- Baseline against a real benchmark before claiming a defense works: [AgentDojo](https://github.com/ethz-spylab/agentdojo) and [JailbreakBench](https://github.com/JailbreakBench/jailbreakbench) are both real, peer-reviewed (NeurIPS 2024) options — check their current activity before treating either as actively maintained for your specific need.
- [NVIDIA/garak](https://github.com/NVIDIA/garak) and [microsoft/PyRIT](https://github.com/microsoft/PyRIT) (use this URL, not the archived `Azure/PyRIT` mirror) are both active, general-purpose LLM red-teaming tools with injection-relevant probes.
- [promptfoo](https://github.com/promptfoo/promptfoo) is the most actively released option for CI/CD-integrated red-teaming of full agent/RAG applications, not just raw model endpoints — it's the natural fit if you want injection testing to run on every PR rather than as a one-off exercise.
- See [labs/injection-tests/](../../labs/injection-tests/) for hands-on educational test cases once that lab is written up.

## References

*Accessed 2026-09-19.*

- OWASP LLM01:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM01_PromptInjection.md)
- Meta, "Practical AI Agent Security" (Agents Rule of Two) — [ai.meta.com](https://ai.meta.com/blog/practical-ai-agent-security/)
- Simon Willison, "The Lethal Trifecta" — [simonwillison.net](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- Simon Willison, Supabase MCP incident writeup — [simonwillison.net](https://simonwillison.net/2025/Jul/6/supabase-mcp-lethal-trifecta/)
- The Hacker News, malicious MCP server (`postmark-mcp`) — [thehackernews.com](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)

See also: [LLM01](../owasp-llm/LLM01.md), [LLM08](../owasp-llm/LLM08.md), [LLM09](../owasp-llm/LLM09.md).
