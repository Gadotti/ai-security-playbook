# LLM05: Data and Model Poisoning

**Layer:** Entry vector · [back to overview](README.md)

## Description

An adversary manipulates training data or model artifacts — pretraining data, fine-tuning data, embeddings, RAG corpora, transfer-learning sources, or continuously-retrained pipelines — to embed harmful behavior, bias, or exploitable weaknesses. Unlike a typical software vulnerability, poisoning corrupts the learning process itself, so remediation usually means retraining/revalidating data or replacing the model, not patching code. It can be intentional (an attack) or the result of poor data hygiene.

`[to verify]` Renumbered from LLM04:2025 to LLM05:2026. The cited research skews heavily toward late-2025/2026 findings, which suggests the content was substantively refreshed alongside the renumbering — but this is an inference, not something confirmed directly from the source document's own changelog.

## Attack scenarios

- **Minimal-sample backdoors at scale.** Anthropic, together with the UK AI Security Institute and the Alan Turing Institute, trained 72 models and found that as few as ~250 poisoned documents can backdoor an LLM regardless of model size (600M–13B parameters) or total training-data volume — challenging the prior assumption that poisoning cost scales with dataset size (Oct/Nov 2025; independently reported by Engadget, Dark Reading, and BankInfoSecurity).
- **Chat-template/trigger poisoning.** A modified chat template with an embedded trigger reportedly degraded accuracy from 90% to 15% under trigger and caused 80%+ malicious-URL emission. *(Sourced from the OWASP document only, not independently re-verified.)*
- **RAG corpus poisoning.** Attacker-optimized text inserted into a retrieval corpus can override accurate content for a given query (Zhang et al., 2025, "Practical poisoning attacks against retrieval-augmented generation").
- **Sleeper-agent persistence.** Backdoors embedded during training can survive subsequent safety/alignment training (Hubinger et al., "Sleeper Agents," Anthropic 2024, with 2025–2026 follow-up work cited by OWASP; exact follow-up paper titles `[to verify]`).
- **Unsafe deserialization at load time.** Loading a poisoned model via the pickle format executes arbitrary code on the host — this overlaps directly with [LLM04 Supply Chain](LLM04.md).

## Mitigations

**Established:**
- Dedicated trigger-probing / backdoor-scanning after every alignment or fine-tuning cycle — do not assume safety alignment removes backdoors, a claim directly supported by the Sleeper Agents research lineage.
- SBOM/ML-BOM lineage tracking, signing, and continuous integrity verification of datasets and model artifacts (shared tooling with LLM04).
- Data versioning (e.g. [DVC](https://dvc.org)) for rollback and forensic analysis of training-data changes.
- Least privilege, network segmentation, and access control on training-data pipelines.

**Emerging / partial:**
- Anomaly detection on training loss and output drift to catch poisoning in continuous/online retraining pipelines — a sound principle, but no single mature off-the-shelf tool was identified.
- Treating inference-time artifacts (chat templates, tokenizer configs, LoRA/PEFT adapters) as security-sensitive code requiring signing, hashing, and static analysis.
- Sandboxing the model's interactions with unverified data/external tools — reduces blast radius, but doesn't prevent poisoning itself.

## Testing & detection

- Dedicated trigger-probing after each fine-tuning/alignment cycle, adapting red-teaming frameworks (PyRIT, garak — see [LLM01](LLM01.md)) to known trigger patterns.
- Compare model outputs against a trusted "clean" reference model or a held-out validation set to detect behavioral drift.
- Verify every training-data source and adapter against a signed ML-BOM before use.
- For RAG poisoning specifically: source-scoring and trust-boundary enforcement on retrieved content, tested by injecting known "canary" poisoned documents into a staging corpus and measuring retrieval/influence rate.
- `[to verify]` No widely-cited, actively maintained, dedicated open-source "data poisoning detector" independent of academic research code was found — a genuine tooling gap.

## References

*Accessed 2026-09-19.*

- OWASP LLM05:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM05_DataModelPoisoning.md)
- Anthropic, "A small number of samples can poison LLMs of any size" — [anthropic.com](https://www.anthropic.com/research/small-samples-poison)
- Dark Reading, independent coverage of the Anthropic poisoning study — [darkreading.com](https://www.darkreading.com/application-security/only-250-documents-poison-any-ai-model)
- Hubinger et al., "Sleeper Agents" (Anthropic, 2024) — foundational backdoor-persistence research (exact arXiv ID `[to verify]` before citing directly)
- DVC (Data Version Control) — [dvc.org](https://dvc.org)
