# Lab: SkillSpector scan

Guide to using [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) to scan agent skills, MCP servers, and tool definitions for risk before installing them.

## What it does

SkillSpector is a security scanner (Apache-2.0, NVIDIA) that inspects agent "skills" (Claude Code, Codex, Gemini CLI) and MCP servers **before installation** — as `SKILL.md` files, Git repos, zip archives, or local directories — looking for malicious patterns, excessive capability requests, and known-vulnerable dependencies.

It runs a two-stage analysis:

1. **Static analysis (fast, always on).** Regex patterns across 11 built-in analyzers, AST-based behavioral analysis flagging dangerous calls (`exec`, `eval`, `subprocess`), and known-vulnerability checks against [OSV.dev](https://osv.dev/) for any declared dependencies.
2. **Semantic LLM analysis (optional, on by default).** An LLM pass evaluates context and intent, filters static-analysis false positives, and produces human-readable explanations for each finding.

Between the two stages it checks for **71 vulnerability patterns across 17 categories**, including prompt injection, data exfiltration, privilege escalation, supply-chain risk, excessive agency, system-prompt leakage, memory poisoning, tool abuse, and YARA-based malware signatures — a close practical match to this repo's [OWASP LLM Top 10 pages](../../docs/owasp-llm/), particularly [LLM03](../../docs/owasp-llm/LLM03.md), [LLM04](../../docs/owasp-llm/LLM04.md), and [LLM08](../../docs/owasp-llm/LLM08.md).

Each scan produces a **risk score (0–100)**:

| Score | Severity | Recommendation |
|---|---|---|
| 0–20 | LOW | Considered safe |
| 21–50 | MEDIUM | Review before use |
| 51–80 | HIGH | Do not install without remediation |
| 81–100 | CRITICAL | Do not install |

## Installation

```bash
# Via uv (recommended)
uv tool install git+https://github.com/NVIDIA/skillspector.git

# Or via Docker, if you don't want Python tooling on the host
make docker-build
docker run --rm -v "$PWD:/scan" skillspector scan ./skill/
```

## Usage

```bash
# Static analysis only — fast, and keeps skill content local (no LLM call)
skillspector scan ./my-skill/ --no-llm

# Static + semantic LLM analysis (default)
skillspector scan ./my-skill/

# Machine-readable output
skillspector scan ./my-skill/ --format json --output report.json

# CI/CD-friendly output
skillspector scan ./my-skill/ --format sarif
```

Supported ecosystems: Python (PyPI), JavaScript (npm), and skills mixing both. Output formats: terminal, JSON, Markdown, and SARIF (for CI/CD integration — pairs naturally with this repo's [CI workflow](../../.github/workflows/ci.yml) if you want to gate skill installs on a scan).

## Worked example

```bash
# Scan a skill directory you're about to install, static-only first
skillspector scan ./candidate-skill/ --no-llm

# If the static pass looks clean, re-run with the LLM semantic pass for
# context-aware review before trusting it in an agent with real tool access
skillspector scan ./candidate-skill/ --format markdown --output candidate-skill-report.md
```

A report shows: overall score and severity, a recommendation (install / review / reject), the components analyzed, and each individual finding with its location in the scanned files, a confidence level, and a plain-language explanation.

## A privacy note before you scan

Stage 2 (semantic LLM analysis) sends the scanned file contents to whichever LLM provider you've configured (OpenAI, Anthropic, AWS Bedrock, NVIDIA Build, Ollama, Azure OpenAI, or a local CLI like `claude`/`codex`/`gemini`/`opencode`). If the skill you're scanning could contain sensitive data (internal paths, credentials accidentally left in example code, proprietary logic), run with `--no-llm` first and only enable the LLM pass once you've confirmed the content is safe to share with that provider — this is the same "assume it leaks" caution as [LLM08](../../docs/owasp-llm/LLM08.md) applied to your own scanning pipeline, not just the model you're building.

## References

*Accessed 2026-09-19.*

- [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) — official repository, README, and Apache-2.0 license text.
