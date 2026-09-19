# Policies

Example policies, hooks, and tool allowlists implementing the "observe → alert → block" gradual adoption model described in [docs/strategies/audit-without-blocking.md](../docs/strategies/audit-without-blocking.md), and the [framework](../docs/framework/)'s maturity model.

- [tool-allowlist.example.yaml](tool-allowlist.example.yaml) — a declarative version of the allow-by-name, deny-by-default pattern [labs/ai-jail](../labs/ai-jail/) implements in code, for [LLM03](../docs/owasp-llm/LLM03.md).
- [spend-cap.example.yaml](spend-cap.example.yaml) — hard spend/circuit-breaker caps plus separate early-warning alerts, for [LLM06](../docs/owasp-llm/LLM06.md).
- [escalation-matrix.md](escalation-matrix.md) — a template mapping severity to stage/action/who's-notified, so escalation isn't decided ad hoc when something fires.
- [hooks/scan_new_skills.sh](hooks/scan_new_skills.sh) — a CI gate that blocks a PR if [SkillSpector](../labs/skillspector-scan/) rates a changed skill HIGH/CRITICAL.
- [hooks/pre_deploy_injection_check.sh](hooks/pre_deploy_injection_check.sh) — a CI/pre-deploy gate wired to [labs/injection-tests](../labs/injection-tests/) (requires wiring a real target into that lab's mock function first).

None of these are meant to be dropped in and trusted blindly — each one names the "observe"/"alert" period it assumes you've already run before treating it as a hard gate. See [docs/framework/maturity-model.md](../docs/framework/maturity-model.md) for that progression.
