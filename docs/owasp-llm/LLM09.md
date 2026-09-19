# LLM09: Vector and Embedding Weaknesses

**Layer:** Amplifier · [back to overview](README.md)

## Description

Security weaknesses in the pipeline that turns content into numeric embeddings and retrieves context via similarity search — the embedding layer is part of the application's trust boundary, not neutral plumbing. These attacks exploit **embedding-space geometry and similarity-search mechanics**, as opposed to instruction-following (that's [LLM01](LLM01.md)).

Explicitly **out of scope** here, and handled by other categories: prompt injection carried via retrieved content ([LLM01](LLM01.md)), training-time model poisoning ([LLM05](LLM05.md)), vector-store serialization flaws ([LLM04](LLM04.md)), and agent-memory attacks that don't rely on embedding-space geometry (a separate agentic-risk category in OWASP's companion Agentic Top 10). OWASP names seven attack classes: cross-tenant leakage, embedding inversion, retrieval-time poisoning, retrieval jamming, membership inference, semantic cache poisoning, and multimodal poisoning.

## Attack scenarios

- **Retrieval-time poisoning.** Publicly published content (e.g. forum posts) is engineered so its embedding lands near common internal queries like "Q3 revenue projection"; when an employee asks that question, the poisoned content is retrieved as trusted context.
- **Cross-tenant leakage.** A SaaS RAG product filters by tenant at the application layer, but similarity search runs across the *full shared index* before that filter applies; an attacker infers another tenant's data existence/volume purely from timing, result counts, and similarity-score patterns — without ever seeing the actual documents.
- **Embedding inversion.** A leaked vector-database backup initially looks low-severity because the source documents remain encrypted — but zero-shot embedding-inversion techniques can reconstruct substantial source content. Academic work reports roughly 50–70% word-level reconstruction from sentence embeddings, and up to ~92% exact reconstruction of short (32-token) inputs.
- **Semantic cache poisoning.** Exploiting the cosine-similarity threshold used for cache hits/deduplication to serve poisoned or attacker-controlled responses to "close enough" queries from other users.

`[to verify]` These are OWASP's own illustrative, technique-grounded scenarios. No single named, publicly attributed real-world breach matching "cross-tenant vector leakage" specifically was found in this research pass — treat the scenarios above as illustrative of a real, published technique, not as a confirmed incident.

## Mitigations

**Established:**
- Enforce tenant/identity scoping **inside the index query itself** (pre-filtering), not as a post-retrieval filter — post-filtering still lets an attacker observe scores on restricted documents.
- Physically separate indexes/namespaces/collections for high-sensitivity workloads instead of relying on a shared index with metadata tags (supported by Pinecone, Weaviate, Qdrant, and Milvus per OWASP's RAG Security Cheat Sheet).
- Treat vector-DB backups, third-party-shipped embeddings, and embeddings in misconfigured cloud storage as equivalent in sensitivity to the underlying source documents, given inversion feasibility — encrypt at rest with separately managed keys.
- Content/provenance validation before embedding: normalize text (strip zero-width characters, Unicode homoglyphs), track provenance, human-review externally sourced content before it enters the index.

**Emerging:**
- Anomaly detection on the embedding/retrieval layer (flag vectors landing unusually close to high-value queries), avoid exposing raw similarity scores to clients, rate-limit embedding endpoints.
- Updating incident-response playbooks to treat "embeddings-only" exposure as a source-data breach for regulatory purposes, given embeddings are invertible — this is OWASP's own recommendation/reasoning, not established case law; no confirmed regulatory ruling on this was found.

## Testing & detection

- [promptfoo](https://www.promptfoo.dev/docs/red-team/plugins/rag-poisoning/)'s RAG-poisoning redteam plugin — actively maintained; generates poisoned document variants and runs automated scans for instruction injection, retrieval manipulation, data extraction, and prompt leakage via retrieval.
- [vec2text](https://github.com/vec2text/vec2text) — reference open-source implementation of embedding-inversion attacks (Morris et al., 2023); usable to test whether your own embeddings can be inverted back to source text.
- MITRE ATLAS technique [AML.T0070](https://atlas.mitre.org/techniques/AML.T0070) ("RAG poisoning") — useful for threat modeling and mapping test coverage.
- OWASP's [RAG Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html) CI/CD test-case checklist: poisoned-document retrieval tests, cross-tenant access-control violation tests ("verify zero cross-boundary results"), stale-permission-in-cache checks, cross-user cache-leakage tests.
- Manual cross-tenant test: probe a shared index as tenant A for content plausibly belonging to tenant B, and look for signal in latency, result counts, or similarity-score distributions even when content is correctly filtered.

## References

*Accessed 2026-09-19.*

- OWASP LLM09:2026 canonical text — [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM09_VectorAndEmbeddingWeaknesses.md)
- OWASP RAG Security Cheat Sheet — [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html)
- vec2text — [github.com](https://github.com/vec2text/vec2text)
- promptfoo RAG-poisoning plugin — [promptfoo.dev](https://www.promptfoo.dev/docs/red-team/plugins/rag-poisoning/)
- MITRE ATLAS AML.T0070 — [atlas.mitre.org](https://atlas.mitre.org/techniques/AML.T0070)
- Morris et al., "Text Embeddings Reveal (Almost) As Much As Text" — [arxiv.org](https://arxiv.org/abs/2310.06816)
