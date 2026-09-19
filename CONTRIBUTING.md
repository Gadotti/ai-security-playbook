# Contributing to ai-security-playbook

Thanks for considering a contribution. This repo is a knowledge base, a reproducible lab environment, and a shareable framework for LLM/agent security — contributions to any of the three are welcome.

## Ground rules

- **Don't fabricate.** If a fact, link, tool status, or standard reference can't be verified, mark it `[to verify]` and say why.
- **Don't paste full external text.** Summarize in your own words and link the source. Cite sources with an access date wherever content is time-sensitive (tool status, standard versions, threat landscape).
- **Offensive security content is allowed** (attack payloads, working exploits, red-team techniques) as long as it serves an educational or defensive purpose. Injection test cases should be labeled as educational.
- **No real personal or customer data**, ever, in examples, logs, or screenshots — synthetic data only.
- Docs and code/identifiers are in English.

## Where things go

- `docs/owasp-llm/` — one page per OWASP LLM Top 10 2026 risk (LLM01–LLM10): description, attack scenarios, mitigations, tests, links.
- `docs/iso-42001/` — mapping between ISO/IEC 42001 controls and practices in this repo. This is a mapping/reference, not a conformance claim.
- `docs/strategies/` — cross-cutting strategy write-ups (prompt injection defense, audit-without-blocking, etc.).
- `docs/framework/` — the consolidated, adoptable framework (checklist, maturity levels, templates).
- `docs/notes/` — decisions, divergences from external sources, open questions.
- `system-prompts/` — versioned base system prompts, with rationale and tests.
- `labs/` — reproducible, runnable experiments. Each lab should have its own `README.md` with setup, usage, and expected output.
- `policies/` — example policies, hooks, and tool allowlists.
- `resources/links.md` — curated links, each with a one-line "why this one" note, access date, and maintenance status.

## Submitting changes

1. Open an issue first for anything non-trivial (new lab, new framework section) so scope can be agreed on.
2. Keep PRs focused — one topic per PR.
3. For labs: include a way to run/verify the example (script, `requirements.txt`, or container definition) rather than prose-only instructions.
4. For links/tools: check whether the project is still active/maintained before adding it, and note the check date.

## Code style

- Lab code is Python by default. Use `ruff` for linting where a lab has a linter configured.
- Prefer small, dependency-light scripts over frameworks unless the lab specifically needs one.
