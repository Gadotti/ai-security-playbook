# LLM04: Supply Chain

**Layer:** Entry vector · [back to overview](README.md)

## Description

Covers integrity failures anywhere in the chain of third-party components an LLM application depends on: pretrained models, datasets, PEFT/LoRA adapters, conversion/merge pipelines, and deployment platforms (e.g. Hugging Face). What sets this apart from generic software supply-chain risk (OWASP Top 10 A06:2021) is that the *artifacts themselves* — model weights, datasets, adapters — can be tampered with, poisoned, or maliciously substituted, not just code dependencies. OWASP cross-references MITRE ATLAS technique [AML.T0010](https://atlas.mitre.org/techniques/AML.T0010) ("AI supply chain compromise"); agentic-application-specific supply-chain threats are covered separately in OWASP's companion Agentic Top 10 document.

`[to verify]` This category was renumbered from LLM03:2025 to LLM04:2026 alongside Excessive Agency's move to #3; whether the risk description itself was substantively rewritten beyond the renumbering, versus just refreshed with newer examples, wasn't confirmed in this research pass.

## Attack scenarios

- **Malicious/compromised ML-ecosystem packages.** The `torchtriton` dependency-confusion attack (2022) exfiltrated data; Ray (CVE-2023-48022) and Ollama (CVE-2024-37032) were exploited in production. *(Sourced from OWASP's own citations, not independently re-verified for this repo.)*
- **Tampered model under a trusted name.** "PoisonGPT" (Mistral.ai security research, Huynh & Hardouin, 2023) — a model with safety tuning removed was uploaded to Hugging Face impersonating a legitimate namespace, demonstrating that detection can be evaded.
- **Hijacked conversion/merge service.** HiddenLayer (2024) documented a hijack of the Safetensors conversion bot on Hugging Face — a service meant to safely convert unsafe pickle-format models.
- **Namespace reuse.** An account is deleted and an attacker republishes a malicious model under the same, now-available path or name.
- **Compromised CI/CD pipeline** (e.g. build-cache poisoning, stolen credentials) producing an org-signed but malicious artifact that passes internal verification.

## Mitigations

**Established:**
- SBOM extended to AI-BOM/ML-BOM — CycloneDX has a defined ML-BOM schema (since spec v1.5); OWASP also publishes its own AI-BOM guidance.
- Cryptographic model signing with transparency logs — see [Sigstore's model-transparency project](https://github.com/sigstore/model-transparency) (OpenSSF Model Signing), which reached v1.0.
- SLSA (Supply-chain Levels for Software Artifacts) applied to ML build/release pipelines.
- Prefer safe serialization formats over pickle (pickle deserialization = arbitrary code execution) — though even "safe" formats like ONNX aren't immune to graph-level backdoors.

**Emerging / partial:**
- Treat AI-assisted-coding package hallucination ("slopsquatting" — an assistant suggesting a plausible but nonexistent package name that an attacker has pre-registered) as a supply-chain sub-risk requiring dependency verification before adoption.
- Behavioral validation and anomaly detection on third-party models in production, since static scanners can be evaded.

## Testing & detection

- Maintain and diff a signed AI-BOM/ML-BOM against expected hashes for every model, dataset, and adapter in the pipeline.
- Verify Sigstore/OMS signatures and transparency-log entries before loading any third-party model artifact.
- Red-team newly adopted third-party models for anomalous behavior before production use, and keep monitoring post-deployment.
- Audit CI/CD pipelines for cache-poisoning and credential-theft vectors using standard DevSecOps supply-chain testing (SLSA provenance verification), applied specifically to model build/release pipelines.
- [protectai/modelscan](https://github.com/protectai/modelscan) scans serialized model files (Pickle, PyTorch, etc.) for unsafe/malicious code before load.
- `[to verify]` No dedicated, actively maintained open-source scanner specifically for "is this Hugging Face model/LoRA backdoored" was found beyond commercial tooling (e.g. HiddenLayer) and generic pickle scanners — treat this as a real tooling gap, not a solved problem.

## References

*Accessed 2026-09-19.*

- OWASP LLM04:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM04_SupplyChain.md)
- Sigstore model-transparency — [github.com](https://github.com/sigstore/model-transparency)
- Sigstore blog, "Model Transparency v1.0" — [blog.sigstore.dev](https://blog.sigstore.dev/model-transparency-v1.0/)
- protectai/modelscan — [github.com](https://github.com/protectai/modelscan)
- The Hacker News, malicious MCP server (`postmark-mcp`, also a supply-chain-via-package case) — [thehackernews.com](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)
