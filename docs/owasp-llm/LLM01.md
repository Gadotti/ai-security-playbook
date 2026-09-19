# LLM01: Prompt Injection

**Layer:** Entry vector · [back to overview](README.md)

## Description

Prompt injection happens when any input channel to an LLM — direct user text, a retrieved document, tool/API output, or a multimodal input — changes the model's behavior in a way the developer didn't intend. The root architectural problem is that LLMs process "instructions" and "data" in the same token stream, so there's no equivalent of a parameterized query to keep the two apart.

OWASP's 2026 edition frames attacks along three axes:
- **Delivery surface** — direct input, retrieved content, tool output, a tool-connection channel (e.g. MCP), or persistent memory.
- **Propagation** — single-shot, multi-step "kill chain," cross-session (via RAG or memory), or self-replicating across agents.
- **Encoding** — plaintext, obfuscated (Base64, ROT13), invisible Unicode, or multimodal/steganographic.

This edition is explicitly written for the "agentic era": compared to earlier editions, it puts much more weight on agent/tool/MCP-channel injection and cross-session memory poisoning. Prompt Injection has held the #1 spot since the very first OWASP LLM Top 10 draft.

## Attack scenarios

- **Indirect injection via RAG/web content.** A summarized webpage or RAG-retrieved document contains hidden instructions; the model complies and, for example, emits a Markdown image whose URL exfiltrates the conversation to an attacker-controlled domain. Cited research found as few as ~5 poisoned documents in a RAG corpus reaching ~90% attack success.
- **Trusted-channel / MCP injection.** Security researchers (General Analysis, 2025) showed a Supabase MCP server connected through Cursor could be tricked, via a poisoned support-ticket field, into dumping a production database using a privileged service-role key.
- **Malicious MCP package.** The npm package `postmark-mcp` (v1.0.16) silently BCC'd every email sent through it to an attacker address, affecting an estimated ~300 organizations (reported September 2025 by The Hacker News, Koi Security, and Snyk).
- **Agentic command execution.** In July 2025, a compromised system prompt was pushed into the AWS "Amazon Q" VS Code extension repository (caught before real damage), and a separate runtime prompt injection reportedly made Amazon Q execute arbitrary code (per AWS's own bulletins, as cited by OWASP — not independently re-verified for this repo).
- **Multimodal / steganographic injection.** Sub-perceptual instructions embedded in an image are extracted by a vision encoder and change model behavior.
- **Payload splitting.** Malicious instructions are fragmented across multiple input fields (e.g. resume fields) to evade per-field classifiers, then recombined by the model at evaluation time.

## Mitigations

**Established:**
- Keep credentials and any state-changing capability out of the model — enforce via a deterministic policy engine / application code, with least privilege per tool call.
- Require explicit human confirmation before irreversible, privileged, or externally-visible actions, showing the literal action being taken — not an LLM-generated summary of it.
- Strip invisible Unicode (tag-block characters, variation selectors, zero-width characters) at ingest and render boundaries.
- Pin, sign, and verify MCP servers and third-party tool packages; audit tool descriptions for hidden instructions — directly motivated by the `postmark-mcp` and Supabase incidents above.
- Meta's ["Agents Rule of Two"](https://ai.meta.com/blog/practical-ai-agent-security/) (Oct 2025): an agent session should satisfy at most two of {processes untrusted input, accesses sensitive data, can change state or communicate externally}; require per-action human approval if all three apply. Also referenced by NIST AI 100-2 and a joint CISA/FBI/NSA/ACSC advisory.

**Emerging / partial:**
- System-prompt-based allow/deny lists for role and capability constraints — OWASP itself flags this as bypassable once an attacker infers the prompt.
- A structurally separate "data" channel with provenance labels, distinct from the "instructions" channel — reduces attack success only against non-adaptive attackers.
- Treating agent memory writes as privileged operations that require review before persistence, to blunt cross-session poisoning.

OWASP, NIST (2025), and the UK NCSC (2025) are explicit that **no reliable prevention mechanism exists today** — defenses here are architectural and containment-based, not preventive.

## Testing & detection

- Test against adaptive attackers who already know the deployed defense — OWASP explicitly warns against trusting static-only attack-success claims.
- [AgentDojo](https://github.com/ethz-spylab/agentdojo) (NeurIPS 2024) and [JailbreakBench](https://github.com/JailbreakBench/jailbreakbench) (NeurIPS 2024) are real, still-referenced benchmarks for agent-security and jailbreak testing — check their current activity before treating either as "actively maintained" in a specific build.
- [microsoft/PyRIT](https://github.com/microsoft/PyRIT) — actively maintained (v1.1.0 released Sept 2026). Use this URL, not the old `Azure/PyRIT` mirror, which is archived.
- [NVIDIA/garak](https://github.com/NVIDIA/garak) — actively maintained (v0.17.0, Sept 2026, added EU AI Act risk-category mapping).
- [promptfoo](https://github.com/promptfoo/promptfoo) — very actively maintained (near-daily releases); CI/CD-integrated red-teaming for prompts, agents, and RAG pipelines.

## References

*Accessed 2026-09-19.*

- OWASP LLM01:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM01_PromptInjection.md)
- Meta, "Practical AI Agent Security" (Agents Rule of Two) — [ai.meta.com](https://ai.meta.com/blog/practical-ai-agent-security/)
- Simon Willison, Supabase MCP "lethal trifecta" writeup — [simonwillison.net](https://simonwillison.net/2025/Jul/6/supabase-mcp-lethal-trifecta/)
- The Hacker News, malicious MCP server (`postmark-mcp`) — [thehackernews.com](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)
- microsoft/PyRIT releases — [github.com](https://github.com/microsoft/PyRIT/releases)
- NVIDIA/garak — [github.com](https://github.com/NVIDIA/garak)
