# Labs

Reproducible, runnable security labs. Each lab has its own `README.md` with setup, usage, and expected output.

- [skillspector-scan/](skillspector-scan/) — guide to scanning agent skills/tools for risk with NVIDIA SkillSpector
- [ai-jail/](ai-jail/) — a runnable, two-layer agent sandbox: an application-level tool-permission gateway plus container-level isolation
- [prompt-anonymizer/](prompt-anonymizer/) — spike/PoC using Microsoft Presidio to mask sensitive data in prompts and re-hydrate it in the response
- [injection-tests/](injection-tests/) — educational prompt injection test corpus (direct, indirect, tool-mediated) with a small pluggable test runner

Lab code defaults to Python; each lab lists its own dependencies (if any) in its own `requirements.txt`.
