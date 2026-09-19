"""Spike/PoC: mask sensitive entities in a prompt before it reaches an LLM,
then rehydrate the model's response back to the real values.

Status: PoC, not production-ready. See README.md for the survey of existing
approaches this was compared against, and the "Known limitations" section
before relying on this pattern for anything real.

Usage:
    pip install presidio-analyzer
    python -m spacy download en_core_web_lg   # Presidio's default NLP model
    python anonymizer_poc.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from presidio_analyzer import AnalyzerEngine

# A conservative default set — extend with Presidio's other built-in
# recognizers (US_SSN, CREDIT_CARD, IBAN_CODE, IP_ADDRESS, ...) depending on
# what your application actually handles. See:
# https://microsoft.github.io/presidio/supported_entities/ for the full list
# (Presidio has since moved to https://presidio.dataprivacystack.org/ — the
# supported-entities page there is the current source of truth).
DEFAULT_ENTITIES = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "LOCATION"]

_analyzer: AnalyzerEngine | None = None


def get_analyzer() -> AnalyzerEngine:
    """Lazily build the analyzer — loading the spaCy model is slow, so we
    only pay for it once per process, not once per call."""
    global _analyzer
    if _analyzer is None:
        _analyzer = AnalyzerEngine()
    return _analyzer


@dataclass
class MaskResult:
    masked_text: str
    mapping: dict[str, str]  # token -> original value


def mask_prompt(text: str, entities: list[str] | None = None, language: str = "en") -> MaskResult:
    """Detect sensitive entities and replace each with a unique placeholder
    token, e.g. "John Smith" -> "[[PERSON_1]]". Returns the masked text plus
    a mapping to reverse it later."""
    analyzer = get_analyzer()
    findings = sorted(
        analyzer.analyze(text=text, entities=entities or DEFAULT_ENTITIES, language=language),
        key=lambda r: r.start,
    )

    mapping: dict[str, str] = {}
    counters: dict[str, int] = {}
    replacements: list[tuple[int, int, str]] = []

    for result in findings:
        counters[result.entity_type] = counters.get(result.entity_type, 0) + 1
        token = f"[[{result.entity_type}_{counters[result.entity_type]}]]"
        mapping[token] = text[result.start : result.end]
        replacements.append((result.start, result.end, token))

    masked = text
    # Replace right-to-left so earlier offsets stay valid as the string shrinks/grows.
    for start, end, token in sorted(replacements, key=lambda r: r[0], reverse=True):
        masked = masked[:start] + token + masked[end:]

    return MaskResult(masked_text=masked, mapping=mapping)


def rehydrate(text: str, mapping: dict[str, str]) -> str:
    """Replace every placeholder token still present with its real value.
    Tokens the model didn't echo back verbatim are simply not replaced —
    see the "Known limitations" section in README.md for why that happens
    and what it means for this pattern."""
    result = text
    for token, original in mapping.items():
        result = result.replace(token, original)
    return result


def mock_llm_call(masked_prompt: str) -> str:
    """Stand-in for a real provider call (Anthropic/OpenAI/Ollama/etc.).
    Swap this for your actual client — the point of this PoC is the
    masking/rehydration wrapper, not this stub. A real system prompt should
    explicitly instruct the model to preserve any `[[TOKEN]]`-style
    placeholders in its response unchanged."""
    if "[[PERSON_1]]" in masked_prompt:
        return "Sure - I'll draft the follow-up email to [[PERSON_1]] now."
    return "Got it, working on that."


def anonymize_and_call(
    prompt: str,
    llm_fn: Callable[[str], str] = mock_llm_call,
    entities: list[str] | None = None,
) -> str:
    """The full round trip: mask -> call -> rehydrate."""
    masked = mask_prompt(prompt, entities=entities)
    raw_response = llm_fn(masked.masked_text)
    return rehydrate(raw_response, masked.mapping)


if __name__ == "__main__":
    prompt = (
        "Please draft a follow-up email to John Smith at john.smith@example.com "
        "about the invoice."
    )

    masked = mask_prompt(prompt)
    print("Original prompt: ", prompt)
    print("Masked prompt:   ", masked.masked_text)
    print("Mapping:         ", masked.mapping)
    print()

    final_response = anonymize_and_call(prompt)
    print("Model saw:       ", mask_prompt(prompt).masked_text)
    print("Final response:  ", final_response)
