# Lab: Injection tests

An educational corpus of prompt-injection test cases across the three delivery surfaces covered on [LLM01: Prompt Injection](../../docs/owasp-llm/LLM01.md) and [docs/strategies/prompt-injection.md](../../docs/strategies/prompt-injection.md): **direct**, **indirect** (retrieved content), and **tool-mediated** (agent/tool/MCP channel).

Every case in [`test_cases.yaml`](test_cases.yaml) is written from scratch for this repo — none of it is copy-pasted from an external source — but each follows a well-documented, publicly known technique category. These are meant to be read and adapted, not run as-is against a production system without your own review.

## Structure

Each case has:
- `category` — `direct`, `indirect`, or `tool_mediated`
- `technique` — a short name for the specific approach
- `payload` — the text to send, or to embed in simulated retrieved/tool content
- `injected_via` — for indirect/tool-mediated cases, what channel carries it
- `expected_safe_behavior` — what a correctly-defended system should do instead
- `mitigation_ref` — the doc in this repo covering the relevant fix

## Running it

```bash
pip install -r requirements.txt
python run_tests.py                     # all cases, against a no-op mock target
python run_tests.py --category direct   # just one category
```

Out of the box this runs against `mock_target()`, a stub that returns a placeholder — **you're expected to replace it** with a function that sends the payload to whatever you're actually testing (a raw model call, a full agent, an application endpoint) and returns the response as a string. For `indirect` and `tool_mediated` cases, wiring the payload into the right channel (a fake retrieved document, a fake tool response) is your target function's job — the harness just hands you the payload text.

The harness does a crude keyword check against a short list of "compliance signals" (phrases suggesting the target followed the injected instruction) and prints `REVIEW` when one matches. **This is a triage aid, not a verdict** — prompt injection defense is fuzzy enough that a human reading each response against `expected_safe_behavior` will catch far more than any keyword list. Treat every case as `REVIEW` if you're doing this seriously.

## Extending this

- Add new cases directly to `test_cases.yaml` following the same schema.
- For CI-integrated, more sophisticated automated red-teaming than this harness provides, see the tools listed in [resources/links.md](../../resources/links.md#2-automated-llm-red-teaming--adversarial-testing-frameworks) (promptfoo, garak, PyRIT) — this lab is meant as a small, readable starting point and a teaching aid, not a replacement for those.

## References

- [docs/owasp-llm/LLM01.md](../../docs/owasp-llm/LLM01.md), [LLM03.md](../../docs/owasp-llm/LLM03.md), [LLM07.md](../../docs/owasp-llm/LLM07.md), [LLM08.md](../../docs/owasp-llm/LLM08.md), [LLM09.md](../../docs/owasp-llm/LLM09.md) — the risk pages each test case maps back to.
- [docs/strategies/prompt-injection.md](../../docs/strategies/prompt-injection.md) — the strategy this corpus exercises.
