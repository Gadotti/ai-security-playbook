# LLM07: Misinformation

**Layer:** Impact · [back to overview](README.md)

## Description

Incorrect, unsupported, or misleading model output becomes dangerous specifically when it is **trusted and acted upon** — by a human, an automated workflow, or another agent. The 2026 edition reframes this from the largely human-facing "hallucination + overreliance" framing of 2025 into a system-level, agentic failure mode.

OWASP explicitly carves out adjacent risks to keep this category focused:
- Where the root cause is prompt injection, data/model poisoning, or supply-chain compromise, those belong under [LLM01](LLM01.md), [LLM05](LLM05.md), or [LLM04](LLM04.md) respectively.
- Unsafe execution of generated code is [LLM10](LLM10.md).
- Registering a hallucinated package name as an attack is [LLM04 Supply Chain](LLM04.md).

New for 2026: "cross-agent misinformation propagation" and "forged/misattributed evidence" as example categories not present in the 2025 text. This category jumped from LLM09:2025 to LLM07:2026.

## Attack scenarios

- **Hallucinated package/dependency ("slopsquatting").** A coding assistant recommends a plausible but non-existent package name; an attacker has pre-registered that exact name with malicious code (Spracklen et al., 2025).
- **Incorrect state inference in agentic workflows.** OWASP's own examples: a customer-service agent misreads policy and approves a refund that violates the terms; a security agent misclassifies normal traffic as an intrusion and auto-blocks a production network segment, causing an outage.
- **Cross-agent trust failure.** One agent reports a customer as identity-verified when they are not, and a downstream payment agent trusts that state and releases funds.
- **Fabricated task completion.** An agent reports a nightly backup completed when it never ran; a later restore fails because no backup exists — a "silent" failure with delayed, compounding impact.
- **Adversarially induced misinformation.** An attacker seeds a public support forum with false remediation steps that a retrieval/troubleshooting agent later surfaces as a trusted recommendation.

## Mitigations

**Strong, newer consensus (agent-specific):**
- **"Claim-check-act"** — separate generation from execution, and verify claims before acting on them. This is the single most repeated 2026-era mitigation for this risk across OWASP and vendor commentary.
- Grounding requirements: outputs must cite or derive from authoritative, current sources before being trusted; validate tool-call arguments, authorization, preconditions, and current state before execution.

**Established:**
- Human-in-the-loop / approval workflows gating consequential agent actions.

**Emerging / partial:**
- Verification signals — groundedness and consistency checks — instead of raw model confidence scores. Conceptually sound, but there's no single mature, standardized metric industry-wide yet.
- Structured-output enforcement with mandatory fields, specifically to catch "omission failures" (e.g. a clinical summary silently dropping a contraindication).

## Testing & detection

- Build a fixed evaluation set with known-answer questions, deliberately missing information, conflicting sources, time-sensitive facts, and questions the system should decline to answer. Measure accuracy, citation validity, and appropriate refusal rate, and re-run after any model or prompt change.
- Log claims, evidence, and downstream outcome together (not just the final answer), so a wrong action can be traced back to the specific unverified claim that caused it.
- Adversarial/red-team scenario testing targeting the failure categories above (fabricated task completion, cross-agent trust failure, adversarially seeded false remediation) rather than generic hallucination benchmarks alone.
- [confident-ai/deepeval](https://github.com/confident-ai/deepeval) — actively maintained; provides hallucination/faithfulness/groundedness metrics.
- Ragas (RAG evaluation framework with faithfulness/groundedness metrics; the repo moved from `explodinggradients/ragas` to `vibrantlabsai/ragas`) — appears active, exact current last-commit date `[to verify]`.
- [NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) includes self-check fact-checking and hallucination-detection rails (renamed from `NVIDIA/NeMo-Guardrails`).
- Caution: reference general adversarial LLM testing via `microsoft/PyRIT` (active) — an older `Azure/PyRIT` mirror is archived; don't confuse the two.

## References

*Accessed 2026-09-19.*

- OWASP LLM07:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM07_Misinformation.md)
- Spracklen et al., research on package hallucination / "slopsquatting" (2025)
- confident-ai/deepeval — [github.com](https://github.com/confident-ai/deepeval)
- NVIDIA-NeMo/Guardrails — [github.com](https://github.com/NVIDIA-NeMo/Guardrails)
- Check Point, "Reading the signals in the OWASP LLM Top 10 2026" — [blog.checkpoint.com](https://blog.checkpoint.com/ai-security/reading-the-signals-in-the-owasp-llm-top-10-2026/amp/)
