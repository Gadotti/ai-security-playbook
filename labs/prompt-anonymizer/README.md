# Lab: Prompt anonymizer (spike/PoC)

**Status: spike/PoC.** This lab is a working prototype of an idea, not a hardened tool — read "Known limitations" before considering it for anything beyond experimentation.

The idea: intercept a prompt before it reaches an LLM provider, mask personally identifiable or sensitive information (PII, secrets, customer data), send the masked version to the model, then re-hydrate the model's response back to the real values before showing it to the user. This is relevant to [LLM02: Sensitive Information Disclosure](../../docs/owasp-llm/LLM02.md) — specifically the "upstream oversharing" root cause described there.

## Survey of existing approaches

| Approach | Example | Verdict |
|---|---|---|
| Regex/blocklist masking | Hand-written patterns for emails, phone numbers, etc. | Cheap, but [LLM02's own research](../../docs/owasp-llm/LLM02.md#mitigations) notes regex fails against cross-lingual, base64, or otherwise encoded PII — brittle as a sole control. |
| NER/classifier-based masking | **Microsoft Presidio** (`presidio-analyzer` + `presidio-anonymizer`) | Actively maintained (confirmed via GitHub, Sept 2026), the most mature open-source option found in this space, and specifically named as a testing/detection tool on the LLM02 risk page. **Used for this PoC.** |
| Lightweight text-metrics/signal extraction | [whylabs/langkit](https://github.com/whylabs/langkit) | Active, but oriented at monitoring/observability signals rather than reversible masking — a different use case, listed in [resources/links.md](../../resources/links.md#5-piisecret-detection-and-masking-for-llm-pipelines). |
| All-in-one LLM security toolkit with PII masking | `protectai/llm-guard` | **Archived July 2026** — was previously an obvious candidate, no longer usable for new builds. See [resources/links.md](../../resources/links.md#3-llm-output-guardrails--content-filtering-libraries). |
| LLM-based PII detection (ask a model to find and redact PII) | — | Not used here: it defeats the purpose of *not* sending sensitive data to a model, and adds cost/latency for a task a dedicated NER pipeline already does well. |

Presidio was the clear choice for this PoC: actively maintained, purpose-built, and already independently verified as relevant during this repo's [LLM02 research](../../docs/owasp-llm/LLM02.md).

## How this PoC works

1. **`mask_prompt(text)`** runs Presidio's `AnalyzerEngine` over the prompt, and replaces each detected entity with a unique placeholder token (e.g. `John Smith` → `[[PERSON_1]]`), returning the masked text plus a `{token: original_value}` mapping.
2. The masked text — never the real values — is sent to the model via a pluggable `llm_fn` (a `mock_llm_call` stub is provided so this runs with no API key; swap in your actual Anthropic/OpenAI/Ollama client for real use).
3. **`rehydrate(response, mapping)`** replaces any placeholder tokens still present in the model's response with their real values, before the response reaches the user.

Run it:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
python anonymizer_poc.py
```

Expected output — the model never sees the real name or email, but the final response has them restored:

```
Original prompt:  Please draft a follow-up email to John Smith at john.smith@example.com about the invoice.
Masked prompt:    Please draft a follow-up email to [[PERSON_1]] at [[EMAIL_ADDRESS_1]] about the invoice.
Mapping:          {'[[PERSON_1]]': 'John Smith', '[[EMAIL_ADDRESS_1]]': 'john.smith@example.com'}

Final response:   Sure - I'll draft the follow-up email to John Smith now.
```

## Known limitations (read before reusing this pattern)

- **Re-hydration depends on the model preserving the token verbatim.** This PoC's rehydration step only works if the model echoes `[[PERSON_1]]` back unchanged. Real models sometimes paraphrase, translate, or reformat placeholders — a token that comes back as `[[Person 1]]` or gets dropped entirely won't be rehydrated. A real deployment needs an explicit system-prompt instruction to preserve placeholders exactly, and a fallback for when that instruction isn't followed (e.g., flagging the response for review instead of silently returning it with missing values).
- **Detection is probabilistic, not exhaustive.** Presidio's NER-based detection has false negatives (missed PII) and false positives (over-masking). This PoC uses a conservative default entity list (`PERSON`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, `LOCATION`) — extend it deliberately for your data, and don't treat "Presidio didn't flag it" as proof nothing sensitive is in the text.
- **No handling of multi-turn context.** Each call to `mask_prompt` is independent. In a real conversation, a name masked as `[[PERSON_1]]` in turn 1 needs to map to the *same* token in turn 3 for the model to reason about it consistently — this PoC doesn't persist mappings across turns.
- **Masking doesn't prevent inference from context.** If the surrounding text makes the masked entity's identity obvious anyway (e.g. "the CEO of `[[ORG_1]]`" where the org is uniquely identifiable), masking the literal string doesn't actually protect the underlying information — a known, hard, unsolved problem with this class of approach.
- **This is not a substitute for provider-level data handling agreements.** Masking reduces what an LLM provider sees; it doesn't replace reviewing that provider's actual data retention and training-use policies.

## References

*Accessed 2026-09-19.*

- Microsoft Presidio — [github.com/microsoft/presidio](https://github.com/microsoft/presidio) (project has since moved toward `data-privacy-stack/presidio` / `presidio.dataprivacystack.org` — check current org/docs location before depending on a specific URL)
- Presidio Analyzer docs — [presidio.dataprivacystack.org/analyzer](https://presidio.dataprivacystack.org/analyzer/)
- Presidio Anonymizer/Deanonymizer docs (reversible `encrypt`/`decrypt` operators, an alternative to this PoC's token-mapping approach) — [presidio.dataprivacystack.org/anonymizer](https://presidio.dataprivacystack.org/anonymizer/)
- [docs/owasp-llm/LLM02.md](../../docs/owasp-llm/LLM02.md) — the risk this lab addresses, and the source of the Presidio/langkit/llm-guard comparison above
