# LLM10: Improper Output Handling

**Layer:** Boundary (dashed border — can originate or manifest at any layer) · [back to overview](README.md)

## Description

Covers what happens to an LLM's output **after** generation and **before** it reaches a user, a browser, a terminal/IDE, or a downstream system — insufficient validation, sanitization, or encoding. Because model output can itself be steered by attacker-controlled input (including via prompt injection), failing to treat LLM output as untrusted is functionally equivalent to giving users indirect access to whatever downstream functionality consumes it.

Distinguished from its neighbors: [LLM07 Misinformation](LLM07.md) is about output that's *wrong or misleading* (a content-quality problem), while LLM10 is about output that's *unsafe or executable* regardless of whether it's true (a handling problem); input-side validation is [LLM01](LLM01.md)'s job.

The 2026 edition broadened this category (it was LLM05 in 2025) to explicitly absorb the insecure code that AI coding assistants generate at scale, plus two newer sink types: terminal/log/IDE panes that interpret ANSI escape sequences (enabling clipboard hijacking via OSC 52 or visual spoofing), and chat UIs that auto-render Markdown images, link previews, or iframes — which can exfiltrate data merely by fetching an attacker-controlled URL.

## Attack scenarios

- **Classic code-execution.** LLM output fed directly into a shell/exec/eval call leads to remote code execution; or LLM-generated SQL run without parameterization leads to SQL injection.
- **Classic web scenario.** LLM generates JavaScript or Markdown that's rendered client-side without encoding, leading to stored/reflected XSS — a recognized, testable vulnerability class (e.g. documented in PortSwigger's Web Security Academy).
- **Real incident — GitHub Copilot RCE via prompt injection**, CVE-2025-53773 (Rehberger/embracethered.com, Aug 2025) — cited by OWASP for both LLM01 and LLM10.
- **Real incident — terminal/ANSI escape sequence attacks** ("Terminal DiLLMa," Rehberger, Dec 2024): unsanitized LLM output written to a terminal or log viewer can hijack the terminal, spoof output, or exfiltrate data via OSC 52 clipboard writes.
- **Real incident — Markdown image/link-preview exfiltration** (Rehberger, June 2024; ongoing tracking via Simon Willison's "markdown-exfiltration" archive): a chat UI that auto-fetches an image URL referenced in model output lets an attacker who controls part of the context leak conversation data via the image URL's hostname or query string.
- **Unreviewed auto-deployed code.** An application compiles and ships LLM-generated code straight to production with no human review or security testing — reflecting the 2026 scope broadening toward coding assistants.

## Mitigations

**Established:**
- Treat model output as untrusted input to everything downstream (zero-trust framing); see OWASP ASVS for detailed guidance.
- Context-aware output encoding (HTML encoding for web, JS encoding for script contexts, SQL parameterization for queries).
- Parameterized queries/prepared statements for any database operation touching LLM output.
- Content Security Policy (CSP) as defense-in-depth against XSS, even if encoding is missed somewhere.

**Emerging / partial (responding to newer sink types):**
- Sanitizing control characters (ANSI/OSC/BEL/backspace/CR) before writing model output to terminals, logs, or IDE panes, or visibly encoding them if they must be preserved — tooling support is still uneven across terminal emulators and log viewers.
- Disabling auto-rendering of Markdown images/link-previews/iframes in chat UIs by default, or proxying fetches through a server-side fetcher that strips data-bearing query parameters — not yet uniformly adopted by chat-UI vendors.
- Logging/monitoring for anomalous LLM output patterns and rate-limiting output-triggered actions — inherently detective, not preventive.

## Testing & detection

- PortSwigger Web Security Academy's ["Exploiting insecure output handling in LLMs"](https://portswigger.net/web-security/llm-attacks/lab-exploiting-insecure-output-handling-in-llms) lab — a free, hands-on test environment specifically for this vulnerability class.
- [promptfoo](https://github.com/promptfoo/promptfoo) and [garak](https://github.com/NVIDIA/garak) both include output-handling-adjacent probes (testing whether unsafe payloads get echoed back unsanitized) as part of their broader vulnerability category sets.
- Sink-by-sink manual review: for every sink that consumes LLM output (shell, SQL, browser DOM, terminal, log viewer, email template, file path, auto-compiled/deployed code), test what happens when the model is coaxed — via direct prompting or injected content — into emitting a crafted payload targeting that sink.
- For newer sink types specifically: test terminal/IDE/log integrations by attempting to get the model to emit raw ANSI/OSC sequences and observing whether the rendering surface interprets them; test chat UIs by attempting to get the model to emit a Markdown image/link pointing to an attacker-controlled URL and checking whether the client auto-fetches it.

## References

*Accessed 2026-09-19.*

- OWASP LLM10:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM10_ImproperOutputHandling.md)
- Rehberger, "Terminal DiLLMa" — [embracethered.com](https://embracethered.com/blog/posts/2024/terminal-dillmas-prompt-injection-ansi-sequences/)
- Rehberger, GitHub Copilot Chat Markdown-image exfiltration — [embracethered.com](https://embracethered.com/blog/posts/2024/github-copilot-chat-prompt-injection-data-exfiltration/)
- Rehberger, GitHub Copilot RCE via prompt injection (CVE-2025-53773) — [embracethered.com](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/)
- PortSwigger Web Security Academy lab — [portswigger.net](https://portswigger.net/web-security/llm-attacks/lab-exploiting-insecure-output-handling-in-llms)
- Simon Willison, "markdown-exfiltration" tag archive — [simonwillison.net](https://simonwillison.net/tags/markdown-exfiltration/)
