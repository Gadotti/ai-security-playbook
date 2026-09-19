# Lab: AI jail (agent sandboxing)

A runnable, two-layer example of sandboxing an agent's tool execution, matching the "Established" mitigations on [LLM03: Excessive Agency](../../docs/owasp-llm/LLM03.md):

1. **Application-level tool gateway** ([`tool_gateway.py`](tool_gateway.py)) — the primary control. Every tool call is allow-listed by name, validated by argument, denied by default, and logged. This directly implements OWASP's "complete mediation" mitigation: authorization is enforced in a policy layer *external to the model*, not by asking the model nicely in a system prompt.
2. **Container-level isolation** ([`Dockerfile`](Dockerfile)) — defense in depth *underneath* the gateway. If the gateway is ever bypassed (a bug, a new tool registered without a validator, a compromised dependency per [LLM04](../../docs/owasp-llm/LLM04.md)), the container limits what that failure can reach: no root user, no writable filesystem outside an explicit scratch volume, and no network unless you opt in.

Neither layer is a substitute for the other — a gateway with no container around it is one bug away from a host compromise; a container with no gateway just gives an unrestrained agent root-equivalent access to *itself*.

## Run it directly (no Docker)

```bash
cd labs/ai-jail
python demo_agent.py
```

`demo_agent.py` simulates six tool calls — two legitimate, four that mimic what a successful prompt injection or a misbehaving agent would attempt (path traversal, an absolute-path read, a tool that was never registered at all, an oversized write). Expected output: the two legitimate calls print `ALLOWED`, the four attack simulations print `DENIED` with the specific reason, and every attempt (allowed or not) is logged to stderr via the `tool_gateway` logger — this log is exactly the kind of structured event trail described in [docs/strategies/audit-without-blocking.md](../../docs/strategies/audit-without-blocking.md).

## Run it in the container

```bash
cd labs/ai-jail
docker build -t ai-jail-demo .

# No network, read-only root filesystem, all capabilities dropped, the only
# writable path is the tmpfs scratch dir the gateway confines file access to.
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --tmpfs /home/agent/workspace:rw,size=10m \
  ai-jail-demo
```

If you drop `--read-only` or `--network none` to experiment, you're removing the *second* layer only — the gateway's own path confinement and allowlist still apply and should still deny the same four attack simulations.

## Extending this pattern

- Add a new tool by calling `gateway.register(name, handler, validate)` — anything not registered is denied by construction, so the default state is "deny," not "allow unless blocked."
- Keep validators narrow and specific (see `_validate_write`'s size cap) rather than trying to write a general-purpose "is this safe" check — narrow, testable rules are easier to reason about and to red-team.
- For a real deployment, replace the `logging` calls with your structured audit pipeline, and promote the container flags above (`--network none`, `--read-only`, `--cap-drop ALL`) to your actual container orchestrator's pod/task security context.

## References

- [docs/owasp-llm/LLM03.md](../../docs/owasp-llm/LLM03.md) — the mitigations this lab implements (minimize functionality/permissions, complete mediation, deny-by-default).
- [docs/owasp-llm/LLM04.md](../../docs/owasp-llm/LLM04.md) — why the container layer matters even if the gateway code itself is correct (a compromised dependency can still run).
- [docs/strategies/audit-without-blocking.md](../../docs/strategies/audit-without-blocking.md) — how to turn this gateway's logs into the observe/alert/block pipeline.
