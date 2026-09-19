# LLM02: Sensitive Information Disclosure

**Layer:** Impact · [back to overview](README.md)

## Description

Covers exposure of sensitive information across the full LLM lifecycle, not just in outputs:

- **Training-time** — a model or fine-tuned adapter reproducing memorized training content.
- **Inference-time** — leakage of live context: system prompts, RAG chunks, or another session's data.
- **Pipeline-time** — leakage via fine-tuning, distillation, synthetic data generation, gradients, SDKs, or observability tooling.
- **Observation-time side channels** — inferring facts from timing, token length, log-probabilities, or cache-hit behavior, without ever seeing the actual content.

"Output" is defined broadly here to include tool-call arguments, reasoning/thinking traces, embeddings, logs, and telemetry — not just the visible chat response. Two structural root causes are named: **upstream oversharing** (a RAG pipeline fed from unscoped drives or legacy permissions — the data surface itself is the bug, not the model) and **persistence** (once data touches weights, embeddings, or adapters, it resists deletion, straining GDPR/CCPA erasure duties). Relevant regulatory context: EU AI Act, GDPR, HIPAA, CCPA/CPRA, ISO/IEC 42001, NIST AI 600-1. Explicit boundary: autonomous, multi-step exfiltration is owned by [LLM03 Excessive Agency](LLM03.md), not this category.

## Attack scenarios

- **Training-data extraction.** A "divergence" attack made `gpt-3.5-turbo` emit 10,000+ unique memorized training examples for roughly US$200 (Nasr et al., 2023).
- **Inference-time context leakage.** The March 2023 ChatGPT Redis bug exposed payment PII for 1.2% of Plus subscribers; separately, 4,500+ shared ChatGPT conversations were indexed by Google in 2025 due to missing `noindex` directives.
- **Platform/ecosystem disclosure.** DeepSeek's exposed ClickHouse database (January 2025) leaked 1M+ rows of logs and API keys (Wiz Research).
- **Side-channel inference.** "Whisper Leak" (McDonald & Bar Or, 2025) classified conversation topics from *encrypted* LLM streaming traffic at over 98% AUPRC across 28 production models — without decrypting anything.
- **Litigation exhibits.** *NYT v. OpenAI* and *Getty v. Stability AI* both contain alleged instances of verbatim or near-verbatim training-data reproduction — these are allegations under active litigation, not adjudicated fact.

## Mitigations

**Established:**
- Authorize before retrieval — enforce access-control lists *inside* the vector-index query itself, not via post-hoc filtering.
- Query/session budgeting to blunt enumeration and membership-inference probing.
- Classifier-based redaction (NER + trained classifiers) over regex/blocklists — regex fails against cross-lingual, base64, or hex-encoded exfiltration.
- Treat reasoning traces and tool-call arguments as first-class outputs subject to redaction — a common real gap, since observability platforms often log full prompts/completions/traces by default.

**Emerging / partial:**
- DP-SGD training — differential privacy is necessary but not sufficient against adaptive, iterative-query re-identification attacks; pair it with rate-limiting and query-pattern detection.
- Confidential computing (Intel TDX, AMD SEV-SNP, AWS Nitro Enclaves) and privacy-preserving inference research — advanced, with real cost/latency tradeoffs, not default-ready.
- Verifiable unlearning/erasure, validated via post-unlearning extraction and membership-inference probing — emerging, not yet a mature standard.

## Testing & detection

- **Two-account/two-role probing:** create test accounts with different privileges and have the lower-privileged one request the other's data via direct questions, indirect descriptions, search, export, and known-identifier references.
- Map data flows before testing: which fields reach the model, provider retention terms, and who can retrieve stored conversations/traces.
- Disclosure red-teaming as a release gate: extraction, membership-inference, embedding-inversion, side-channel, and LoRA-extractability probes, aligned to MITRE ATLAS, measured quantitatively rather than pass/fail.
- [Microsoft Presidio](https://github.com/microsoft/presidio) for PII detection, redaction, and anonymization — appears active; exact current last-commit date not confirmed in this research pass, verify before relying on a specific release cadence.
- [NVIDIA/garak](https://github.com/NVIDIA/garak) — actively maintained, includes probes relevant to data leakage.
- Continuous secrets-scanning across repos/configs/pipelines to catch hardcoded credentials before they reach prompts or logs.

## References

*Accessed 2026-09-19.*

- OWASP LLM02:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM02_SensitiveInformationDisclosure.md)
- Nasr et al., "Scalable Extraction of Training Data from (Production) Language Models" (2023)
- Wiz Research, DeepSeek ClickHouse exposure (Jan 2025)
- McDonald & Bar Or, "Whisper Leak" side-channel research (2025)
- Microsoft Presidio — [github.com](https://github.com/microsoft/presidio)
- Cycode, OWASP Top 10 for LLM Applications commentary — [cycode.com](https://cycode.com/blog/owasp-top-10-llm-applications/)
