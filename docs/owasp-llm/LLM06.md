# LLM06: Unbounded Consumption

**Layer:** Impact · [back to overview](README.md)

## Description

An attacker triggers disproportionately expensive computation at negligible cost to themselves ("cost asymmetry"), rooted in the pay-per-token/pay-per-compute pricing model. The 2026 edition widens this well beyond simple request-volume denial of service:

- Extended-thinking/reasoning models with loosely bounded output budgets.
- Multimodal models, where image/audio/video tokenization inflates per-request cost.
- Agentic architectures and tool-use protocols (OWASP explicitly names MCP), where one request can fan out into many downstream operations.
- Shared multi-tenant inference infrastructure as a supply-chain-adjacent surface.

OWASP states plainly that **traditional request-rate limiting alone is no longer sufficient**, pushing the mitigation posture toward token-aware cost controls, hard spend caps, agent-level circuit breakers, and continuous cost-attribution monitoring. This category jumped from LLM10:2025 (last place) to LLM06:2026 — the largest positional rise among the three "impact" risks in this repo's layering.

## Attack scenarios

- **Reasoning-loop / thinking-token exhaustion.** Short, benign-looking prompts force extended-thinking models into prolonged or non-terminating reasoning loops, consuming large thinking-token budgets while evading input-size filters (Li et al., 2025).
- **Sponge examples.** Gradient-based or gradient-free optimization crafts inputs that maximize compute cost (Shumailov et al., 2020; extended to adversarial visual perturbations against vision-language models by Gao et al., 2025).
- **Agentic tool-call fan-out ("denial of wallet").** A malicious tool — OWASP's own example describes one distributed via an open-source "Claude Skill" — triggers recursive or cyclical tool calls, letting a single task fan out into hundreds of downstream calls. In a long-lived agentic session, per-turn cost can climb sharply as context accumulates, with no single request tripping a rate limit even as aggregate spend grows across many concurrent sessions. *(This is OWASP's own worked example — the dollar figures are illustrative, not measured incident data.)*
- **Model extraction/distillation theft.** Querying an API to collect enough outputs to train a functionally-equivalent model; exposed logits/log-probabilities significantly accelerate this (Carlini et al., 2024).
- **Inference-serving-framework exploitation.** Unsafe deserialization, special-token injection, and injected chat templates against serving frameworks — OWASP explicitly names vLLM, TensorRT-LLM, SGLang, Triton, and Ollama.

## Mitigations

**Established, but insufficient alone:**
- Rate limiting / per-user quotas — necessary, but OWASP itself frames this as no longer sufficient on its own.

**Strong, newer consensus:**
- Hard, non-overridable spending caps per API key, user, team, or cloud account that **halt** inference (not just alert) when exceeded — alerting thresholds alone can be outpaced by fast agentic workloads before a human reacts.
- Agentic circuit breakers: step limits, recursion-depth limits, time limits, per-run cost ceilings, plus state-hashing to detect loops — the most agent-native control in this category.
- Keeping serving frameworks (vLLM, etc.) patched, disabling unsafe deserialization, restricting special-token passthrough, and requiring mandatory auth on inference endpoints.

**Emerging:**
- Pre-flight token estimation to reject expensive requests before inference begins.
- Cost-attribution monitoring across modalities and tool protocols — harder to do well since multimodal token costs vary by model, provider, and resolution.

## Testing & detection

- Simulate parallel/retry request patterns right at the rate-limit boundary; confirm rejected requests never reach the inference backend at all (the check must happen *before* spend, not after).
- Load/stress-test with variable-length inputs and near-context-limit payloads specifically — not just oversized payloads, since many APIs reject those outright.
- Adversarial-perturbation scanning for multimodal/vision inputs as a distinct test class from text-based denial-of-wallet testing.
- Agentic-loop testing: seed a test agent with a tool designed to trigger recursive/cyclical calls and confirm circuit breakers actually fire; establish tool-call baselines and alert on deviation.
- `[to verify]` No dedicated, widely-adopted "denial-of-wallet" testing tool was found in this research pass — this is currently covered by adapting standard load-testing tools (k6, Locust) with token-cost-aware assertions, plus manual agentic-circuit-breaker verification. Don't assume a purpose-built scanner exists.

## References

*Accessed 2026-09-19.*

- OWASP LLM06:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM06_UnboundedConsumption.md)
- Cloud Security Alliance, research note on the 2026 list and the companion Agent Control Standard — [labs.cloudsecurityalliance.org](https://labs.cloudsecurityalliance.org/research/csa-research-note-owasp-genai-top10-2026-agent-control-stand/)
- vLLM — [github.com](https://github.com/vllm-project/vllm) (reference serving framework named by OWASP as a hardening target)
- Carlini et al., "Stealing Part of a Production Language Model" (2024)
