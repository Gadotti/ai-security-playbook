# OWASP LLM Top 10 (2026)

One page per risk, using the official 2026 numbering (verified in [docs/notes/owasp-numbering-check.md](../notes/owasp-numbering-check.md)). Each page follows the same structure: description, attack scenarios, mitigations, tests, links. All research behind these pages was pulled directly from the [official OWASP GenAI LLM Top 10 2026 source](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10) plus independently-checked vendor/academic/incident sources — every page lists its references with an access date, and anything unverified is marked `[to verify]` inline.

| Code | Risk | Layer | Page |
|---|---|---|---|
| LLM01 | Prompt Injection | Entry vector | [LLM01.md](LLM01.md) |
| LLM02 | Sensitive Information Disclosure | Impact | [LLM02.md](LLM02.md) |
| LLM03 | Excessive Agency | Boundary | [LLM03.md](LLM03.md) |
| LLM04 | Supply Chain | Entry vector | [LLM04.md](LLM04.md) |
| LLM05 | Data and Model Poisoning | Entry vector | [LLM05.md](LLM05.md) |
| LLM06 | Unbounded Consumption | Impact | [LLM06.md](LLM06.md) |
| LLM07 | Misinformation | Impact | [LLM07.md](LLM07.md) |
| LLM08 | Hidden Context Exposure | Amplifier | [LLM08.md](LLM08.md) |
| LLM09 | Vector and Embedding Weaknesses | Amplifier | [LLM09.md](LLM09.md) |
| LLM10 | Improper Output Handling | Boundary | [LLM10.md](LLM10.md) |
