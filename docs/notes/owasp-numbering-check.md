# Note: OWASP GenAI LLM Top 10 2026 — numbering check

**Date checked:** 2026-09-19
**Checked by:** repo setup (Claude Code session)

## Question

The concentric-layers diagram (`docs/assets/owasp-llm-diagram.png`) this repo is built around groups OWASP LLM Top 10 risks as follows:

1. **Entry Vectors:** LLM01 Prompt Injection, LLM04 Supply Chain, LLM05 Data and Model Poisoning
2. **Amplifiers / Machinery:** LLM08 Hidden Context Exposure, LLM09 Vector and Embedding Weaknesses
3. **Impacts:** LLM02 Sensitive Information Disclosure, LLM06 Unbounded Consumption, LLM07 Misinformation
4. **Border items** (dashed in the diagram): LLM03 Excessive Agency, LLM10 Improper Output Handling

Before writing any content, this numbering was checked against the official OWASP GenAI Security Project source, since risk numbering has changed between the 2025 and 2026 editions.

## Sources checked

- Official OWASP GenAI Security Project page: https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026 (accessed 2026-09-19) — confirms publication date August 2026, v1.0, but does not list individual items on the page itself.
- Official project GitHub repository: https://github.com/GenAI-Security-Project/GenAI-LLM-Top10 (accessed 2026-09-19) — lists the full 2026 ranking.
- Cross-check via web search summary of the 2026 release (accessed 2026-09-19).

## Result

The official 2026 list matches the diagram exactly:

| Code | Name |
|------|------|
| LLM01 | Prompt Injection |
| LLM02 | Sensitive Information Disclosure |
| LLM03 | Excessive Agency |
| LLM04 | Supply Chain |
| LLM05 | Data and Model Poisoning |
| LLM06 | Unbounded Consumption |
| LLM07 | Misinformation |
| LLM08 | Hidden Context Exposure |
| LLM09 | Vector and Embedding Weaknesses |
| LLM10 | Improper Output Handling |

**No divergence found.** The diagram's numbering and grouping is used as-is throughout `docs/owasp-llm/`.

## Caveat `[to verify]`

One secondary source (a news-aggregator article, not linked here to avoid pointing readers at a low-quality source) showed a different order for items 4–9 in what it claimed was the 2026 list. This did not match either the official project GitHub repo or the search-engine consensus, so it was treated as unreliable and discarded. If a future contributor finds an authoritative PDF of the 2026 standard that contradicts the table above, please update this note and `docs/owasp-llm/` accordingly.
