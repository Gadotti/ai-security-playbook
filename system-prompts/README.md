# System prompts

Versioned base system prompts for LLM agents/assistants, provider-agnostic.

Each prompt variant includes the prompt itself, a rationale table for each non-obvious instruction (what it defends against and why, linked to the relevant [OWASP LLM Top 10](../docs/owasp-llm/) page), and known limitations found during review.

- [base-assistant.md](base-assistant.md) — a general-purpose assistant with no tool access.
- [agentic-tool-use.md](agentic-tool-use.md) — extends the base prompt with constraints for tool/function-calling agents. Use together with [labs/ai-jail](../labs/ai-jail/) — the prompt is a second layer of defense, not a substitute for enforcing tool permissions in application code.

Neither prompt has been formally red-teamed against a specific model yet — see [labs/injection-tests](../labs/injection-tests/) for a starting point to test them against a real target.
