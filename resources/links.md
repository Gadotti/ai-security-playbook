# Curated links

A curated shortlist — the best (or best two, where there's a genuine tradeoff) actively-maintained tool or resource per category, not an exhaustive re-listing of every entry in the big awesome-lists. Every maintenance-status claim below was checked against the actual repo (GitHub API where possible, otherwise release/commit pages) on the access date, not assumed from stars or reputation.

Source lists triaged for this page: [beyefendi/awesome-llm-security](https://github.com/beyefendi/awesome-llm-security), [corca-ai/awesome-llm-security](https://github.com/corca-ai/awesome-llm-security), [SecLists Ai/LLM_Testing](https://github.com/danielmiessler/SecLists/tree/master/Ai/LLM_Testing), [ShoumikSaha/agent-skill-security](https://github.com/ShoumikSaha/agent-skill-security), [TakSec/Prompt-Injection-Everywhere](https://github.com/TakSec/Prompt-Injection-Everywhere), [PayloadsAllTheThings/Prompt Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Prompt%20Injection).

**Up front:** several previously-obvious picks turned out to be archived/dead as of the check date — `protectai/llm-guard` (archived July 2026), `protectai/rebuff` (archived May 2025), and `Azure/PyRIT` (archived March 2026, moved to `microsoft/PyRIT`, which is active). Don't reach for these three in a new build.

*All entries checked 2026-09-19 unless noted otherwise.*

## 1. Prompt injection payload/testing collections

- **[TakSec/Prompt-Injection-Everywhere](https://github.com/TakSec/Prompt-Injection-Everywhere)** — curated prompt-injection payloads and ~15 bypass techniques (encoding, roleplay, translation, special characters) with mitigation notes. Active (last push 2026-09-11), 227 stars, MIT. Most focused and current payload list of the sources checked.
- **[PayloadsAllTheThings — Prompt Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Prompt%20Injection)** — one section of the large general pentest payload repo; covers direct/indirect injection and system-prompt-format abuse, with a 30+ tactic table linking onward to promptfoo, garak, and TakSec's list. Repo-wide very active (~81k stars); the Prompt Injection section itself is thinner than TakSec's — worth cross-linking as an entry point, not a replacement.

## 2. Automated LLM red-teaming / adversarial testing frameworks

- **[promptfoo](https://github.com/promptfoo/promptfoo)** — CLI/framework for testing and red-teaming prompts, agents, and RAG pipelines, CI/CD-integrated. Extremely active (near-daily releases; 0.123.1 shipped 2026-09-18), 25k+ stars. Broadest adoption, CI/CD-native.
- **[NVIDIA/garak](https://github.com/NVIDIA/garak)** — dedicated LLM vulnerability scanner ("nmap for LLMs"): jailbreak, toxicity, prompt-injection, and hallucination probes. Very active (v0.17.0 released 2026-09-09, added EU AI Act risk-category mapping), 9.3k stars. Deeper, more academically-grounded probe library than promptfoo — a genuine tradeoff (promptfoo = broad/CI-first, garak = deep/probe-first), worth having both.
- Also worth knowing: **[microsoft/PyRIT](https://github.com/microsoft/PyRIT)** — Microsoft's Python Risk Identification Tool, actively developed (not archived — the old `Azure/PyRIT` mirror is). Good fit for a Microsoft-stack shop.

## 3. LLM output guardrails / content filtering libraries

- **[NVIDIA/NeMo-Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)** — programmable "rails" (topical, safety, jailbreak, hallucination) around conversational LLM apps. Active (3,825 commits, 146 open issues). The most mature dedicated conversational-guardrail framework left standing since the direct in-list competitor was archived.
- **[guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails)** — structured input/output validation for LLM responses (schema enforcement, PII/toxicity/hallucination validators via a Guardrails Hub). Active (recent validator-migration announcement, 2026-07-06). Different tradeoff from NeMo — structured-output validation vs. conversational-flow rails.
- **Do not use for new builds:** `protectai/llm-guard` — archived 2026-07-09, README explicitly says no longer maintained. Was previously the obvious all-in-one pick (PII + injection-resistance + toxicity); now a legacy note only.

## 4. Agent tool-permission / sandboxing frameworks

This category is genuinely nascent — nothing found is battle-tested at scale yet.

- **[Tenuo](https://github.com/tenuo-ai/tenuo)** — cryptographic "warrants" scoping which tools/args an agent may call, to prevent privilege escalation during agent-to-agent delegation. Small (92 stars) but substantively engineered: 883 commits, claims "v0.2 Production/Stable," multi-language SDKs, formal verification (Alloy/Z3). Low community size means limited external scrutiny — verify independently before production use.
- **[Gram](https://github.com/speakeasy-api/gram)** (Speakeasy) — MCP control plane enforcing agent access policies and logging tool activity org-wide. Active (6,457 commits, 177 open PRs), backed by an established API-tooling company. Note: repo claims SOC2/ISO 27001 certification — this is a vendor claim, not independently verified here.
- **See also (different function — scanners, not sandboxes):** [cisco-ai-defense/mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) and [splx-ai/agentic-radar](https://github.com/splx-ai/agentic-radar), both active, scan MCP servers/agentic workflows for threats rather than enforcing runtime permission boundaries.

## 5. PII/secret detection and masking for LLM pipelines

- **[whylabs/langkit](https://github.com/whylabs/langkit)** — text-metrics toolkit extracting safety/security signals (including PII-adjacent signals) from prompts/responses for monitoring pipelines. Modest scale (997 stars), no archive notice, appears active.
- **[microsoft/presidio](https://github.com/microsoft/presidio)** — dedicated PII identification, masking, and anonymization for text, images, and structured data. Far more mature (10.9k stars, 1,635 commits, active), but **not found in any of the six source lists triaged for this page** — included anyway because in-list PII coverage is thin since the strongest in-list candidate (`llm-guard`) is now archived. Note: its README mentions an in-progress "moving to a new home" transition — the repo remains live as of the check date.

## 6. Vector store / RAG-specific security tooling

**No strong defensive-tooling candidate was found** in the source lists as of this check. What exists is attack-research, not deployable defense:

- **[sleeepeer/PoisonedRAG](https://github.com/sleeepeer/PoisonedRAG)** — USENIX Security 2025 companion repo demonstrating knowledge-corruption attacks against RAG systems. An attack PoC, not a defensive tool — useful for attack-awareness reading, not for deployment. No evidence of ongoing maintenance beyond the paper's publication window.

For actual RAG defensive practice, see [LLM09's mitigations](../docs/owasp-llm/LLM09.md#mitigations) (pre-filtering, index separation, provenance validation) — this is currently a practices/architecture problem more than a tooling one.

## 7. LLM security scanners for models/weights (supply chain / provenance)

- **[protectai/modelscan](https://github.com/protectai/modelscan)** — scans serialized ML model files (Pickle, PyTorch, etc.) for embedded unsafe/malicious code before load. Active (192 commits, active CI), no archive notice — this is a different ProtectAI repo than the now-archived `llm-guard`, don't assume org-wide abandonment. The most established, narrowly-scoped tool for this specific risk.
- **[ArseniiBrazhnyk/Veritensor](https://github.com/ArseniiBrazhnyk/Veritensor)** — broader AI-artifact scanner (models, datasets, notebooks) checking for prompt injection, data poisoning, RCE, PII leakage, license issues, and Hugging Face hash verification. Much smaller (85 stars) but 250 commits, active CI/CD, PyPI + Docker + pre-commit distribution. Genuine tradeoff with modelscan (narrow/established vs. broader/newer) rather than a popularity contest — verify independently given its smaller community.

## 8. SecLists — Ai/LLM_Testing corpus

**[danielmiessler/SecLists — Ai/LLM_Testing](https://github.com/danielmiessler/SecLists/tree/master/Ai/LLM_Testing)** is structured by test *methodology*, not payload type — complementary to the payload collections in #1, not redundant:

- `Bias_Testing/` — prompt templates probing gender/race/ethnicity/demographic bias.
- `Data_Leakage/` — prompts testing unintended memorization/training-data leakage.
- `Divergence_attack/` — divergence-attack prompts (getting a model to diverge into raw training-data repetition).
- `Ethical_and_Safety_Boundaries/` — safety/ethics-boundary prompts, including a jailbreak set sourced from an ACM CCS 2024 paper.
- `Memory_Recall_Testing/` — prompts probing whether specific training-set facts can be recalled.

All files use placeholders (e.g. `[GENDER]`, `[COUNTRY]`) meant to be substituted before use. The parent SecLists repo is very actively maintained (73.6k stars, 6,800+ commits); the LLM_Testing subfolder's own last-commit date wasn't separately confirmed, but repo-wide activity is clearly current.

## 9. Curated meta-lists worth cross-linking

- **[beyefendi/awesome-llm-security](https://github.com/beyefendi/awesome-llm-security)** — the more current of the two main awesome-lists: explicitly covers MCP and agentic security, separates main/emerging/deprecated/research entries. **Recommended as the primary cross-link.**
- **[corca-ai/awesome-llm-security](https://github.com/corca-ai/awesome-llm-security)** — older structure, organized mainly around academic papers by attack taxonomy, thinner tool coverage. Useful as a secondary academic-reading cross-link, not a replacement for beyefendi's list.
- **[Puliczek/awesome-mcp-security](https://github.com/Puliczek/awesome-mcp-security)** — dedicated MCP-security meta-list, very active (738 stars, 96 commits, entries through Aug 2025). Worth a dedicated cross-link given MCP security has become its own sub-specialty that the two general lists only partially cover.
