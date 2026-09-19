# ISO/IEC 42001 mapping

This page maps ISO/IEC 42001:2023 (the AI Management System standard) to the practices documented elsewhere in this repo — OWASP LLM Top 10 risk pages, the framework checklist, and the labs.

**This is a mapping and reference aid, not a conformance claim.** Nothing here certifies or implies that any organization — including this repo's practices — satisfies or implements a given control. Selecting and justifying Annex A controls against a real risk/impact assessment is an organization-specific exercise, out of scope for an educational OSS repo. Every link below should be read as "relevant to" or "useful input for" a control, never as "satisfies" it — and several of the repo sections referenced are still stubs, not finished content.

The standard's own text is copyrighted by ISO and not reproduced here; everything below is paraphrased from multiple independent secondary sources, cross-checked against each other, with anything single-sourced or uncertain flagged `[to verify]`.

## Management-system clauses (4–10)

ISO/IEC 42001 reuses the same harmonized high-level structure ("Annex SL") shared by other ISO management-system standards like 27001 and 9001 — confirmed identically across multiple independent sources, including an accredited certification body (Schellman):

| Clause | Focus |
|---|---|
| 4 — Context of the organization | Internal/external issues, interested parties' needs, AI Management System (AIMS) scope |
| 5 — Leadership | Top-management commitment, AI policy, roles/responsibilities/authorities |
| 6 — Planning | Risk-based thinking, AI risk assessment, AI impact assessment, measurable AI objectives |
| 7 — Support | Resources, competence, awareness, communication, documented information |
| 8 — Operation | Operational planning/control across the AI system lifecycle, including impact assessments for higher-risk systems, change management, incident handling |
| 9 — Performance evaluation | Monitoring, measurement, internal audit, management review |
| 10 — Improvement | Nonconformity/corrective action, continual improvement |

## Annex A control categories

Confirmed by multiple independent sources reading consistently: **Annex A has 38 controls grouped into 9 themes, numbered A.2 through A.10** (numbering starts at A.2 in every source checked — a slightly unusual but consistently-reported detail). Annexes B, C, and D are informative (not mandatory): B gives implementation guidance per Annex A control, C catalogs AI-related organizational objectives (fairness, transparency, safety, privacy) and risk sources, and D guides applying the AIMS across different business units, AI system types, and regulatory contexts — organizations select applicable controls based on their own risk/impact assessment, they aren't all mandatory by default. `[to verify]` — the Annex B/C/D descriptions come from a single source (Modulos.ai's docs) and weren't independently cross-checked.

| # | Theme | Approx. controls | Scope (paraphrased) |
|---|---|---|---|
| A.2 | Policies related to AI | 3 | Documented, leadership-approved AI policy; alignment with existing policies; a concern-reporting process |
| A.3 | Internal organization | 2 | Roles, responsibilities, and reporting mechanisms for AI concerns |
| A.4 | Resources for AI systems | 5 | Data, tooling, compute resources, and human competence needed for AI systems |
| A.5 | Assessing impacts of AI systems | 4 | Process to evaluate consequences on individuals, groups, and society; risk treatment |
| A.6 | AI system life cycle | 9 (largest) | Requirements, design, development, verification, deployment, operation, monitoring, documentation, event logging |
| A.7 | Data for AI systems | 5 | Data governance, quality, provenance, preparation |
| A.8 | Information for interested parties | 4 | Transparency/documentation so users and affected parties understand purpose, limitations, and how to report issues |
| A.9 | Use of AI systems | 3 | Responsible/intended use, operational monitoring, staying within defined limits |
| A.10 | Third-party and customer relationships | 3 | Allocation of responsibilities across the AI supply chain |

`[to verify]` One secondary source (hicomply.com) returned a materially different 11-category list with different titles. It could not be corroborated against any other source checked and was discarded as unreliable — likely a different framework or a stale/mistargeted page, not a valid alternative reading.

## Suggested cross-references (judgment calls, not verified facts)

These are reasonable connections between Annex A themes and this repo's sections — not a claim that any of them is complete or satisfies the control:

- **A.2 Policies related to AI** → [docs/framework/](../framework/) (policy-adoption guidance belongs in the maturity model/checklist)
- **A.3 Internal organization** (roles, concern-reporting) → [docs/strategies/audit-without-blocking.md](../strategies/audit-without-blocking.md) (the observe→alert→block model implies escalation paths and ownership); [docs/framework/](../framework/)
- **A.4 Resources for AI systems** (compute, tooling, competence) → [labs/ai-jail/](../../labs/ai-jail/) (sandboxing/allowlisting is directly about controlling and constraining the resources an AI agent can use)
- **A.5 Assessing impacts of AI systems** → the OWASP risk pages broadly, especially [LLM02](../owasp-llm/LLM02.md), [LLM06](../owasp-llm/LLM06.md), [LLM07](../owasp-llm/LLM07.md) (inputs to an impact assessment)
- **A.6 AI system life cycle** (design/dev/verify/deploy/monitor/log) → [labs/injection-tests/](../../labs/injection-tests/) (verification-stage testing); [labs/ai-jail/](../../labs/ai-jail/) (deployment/operational controls); [LLM04](../owasp-llm/LLM04.md) and [LLM05](../owasp-llm/LLM05.md) as lifecycle-stage risks
- **A.7 Data for AI systems** (governance, quality, provenance) → [labs/prompt-anonymizer/](../../labs/prompt-anonymizer/) (masking PII/secrets before data reaches the model is a direct data-governance control); [LLM02](../owasp-llm/LLM02.md), [LLM05](../owasp-llm/LLM05.md)
- **A.8 Information for interested parties** (transparency/documentation) → the OWASP risk pages themselves (risk + mitigations = transparency material); [docs/strategies/audit-without-blocking.md](../strategies/audit-without-blocking.md) (audit trail as evidence for interested parties)
- **A.9 Use of AI systems** (responsible use, operational monitoring) → [docs/strategies/audit-without-blocking.md](../strategies/audit-without-blocking.md) — the observe/alert/block model is close to a direct match for operational-use monitoring; [labs/ai-jail/](../../labs/ai-jail/); [LLM03](../owasp-llm/LLM03.md)
- **A.10 Third-party and customer relationships** → [LLM04 Supply Chain](../owasp-llm/LLM04.md); [docs/framework/](../framework/) (vendor/customer responsibility items)

## References

*Accessed 2026-09-19.*

- ISMS.online, Annex A controls overview — [isms.online](https://www.isms.online/iso-42001/annex-a-controls/)
- Konfirmity, ISO 42001 controls breakdown — [konfirmity.com](https://www.konfirmity.com/blog/iso-42001-controls)
- riskprofs.com, Annex A controls list — [riskprofs.com](https://riskprofs.com/iso-42001-annex-a-controls-list/)
- Modulos.ai docs, Annexes A–D overview — [docs.modulos.ai](https://docs.modulos.ai/frameworks/iso-42001/annexes-a-d)
- Schellman (accredited ISO certification body), clause-by-clause requirements breakdown — [schellman.com](https://www.schellman.com/blog/iso-certifications/what-are-iso-42001-requirements)
- ISO, official standard product page (content not independently verifiable — direct fetch blocked; linked as the canonical reference) — [iso.org](https://www.iso.org/standard/42001)
