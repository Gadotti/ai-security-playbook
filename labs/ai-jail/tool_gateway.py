"""Application-level tool-permission gateway for a sandboxed agent.

Demonstrates the core mitigation from docs/owasp-llm/LLM03.md ("Excessive
Agency"): authorization is enforced in a deterministic policy layer *outside*
the model, not by asking the model nicely in a system prompt. Every call is
allow-listed by name and validated by argument, denied by default, and
logged regardless of outcome (feeds the "observe" stage described in
docs/strategies/audit-without-blocking.md).

This is a teaching example, not a production sandbox. Container-level
isolation (see Dockerfile in this directory) is what actually stops a
successful bypass of this gateway from reaching the host — the two layers
are meant to be used together (defense in depth), not as substitutes for
each other.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tool_gateway")


class ToolDenied(PermissionError):
    """Raised when a requested tool call is outside the allowlist or violates a rule."""


@dataclass
class ToolRule:
    """One allow-listed tool: its handler plus the checks run before it's invoked."""

    handler: Callable[..., str]
    # A rule takes the call's kwargs and either returns None (allowed) or
    # raises ToolDenied with a human-readable reason.
    validate: Callable[[dict], None] = field(default=lambda kwargs: None)


class ToolGateway:
    """Complete-mediation choke point: every tool call goes through .call()."""

    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        self._rules: dict[str, ToolRule] = {}

    def register(self, name: str, handler: Callable[..., str], validate=None) -> None:
        self._rules[name] = ToolRule(handler=handler, validate=validate or (lambda kwargs: None))

    def call(self, name: str, **kwargs) -> str:
        rule = self._rules.get(name)
        if rule is None:
            log.warning("DENIED (not allow-listed): %s(%s)", name, kwargs)
            raise ToolDenied(f"tool '{name}' is not in the allowlist")

        try:
            rule.validate(kwargs)
        except ToolDenied as exc:
            log.warning("DENIED (%s): %s(%s)", exc, name, kwargs)
            raise

        log.info("ALLOWED: %s(%s)", name, kwargs)
        return rule.handler(**kwargs)

    # ------------------------------------------------------------------
    # Path confinement helper, reused by validators below.
    # ------------------------------------------------------------------
    def _resolve_in_workspace(self, relative_path: str) -> Path:
        candidate = (self.workspace / relative_path).resolve()
        if self.workspace not in candidate.parents and candidate != self.workspace:
            raise ToolDenied(f"path '{relative_path}' escapes the workspace")
        return candidate


def build_demo_gateway(workspace: Path) -> ToolGateway:
    """A small, intentionally narrow allowlist — the point of LLM03's
    'minimize functionality' mitigation: each tool does exactly one thing,
    scoped to the workspace, with no shell/network primitive at all."""

    gateway = ToolGateway(workspace)

    def read_file(path: str) -> str:
        target = gateway._resolve_in_workspace(path)
        if not target.exists():
            raise ToolDenied(f"'{path}' does not exist in the workspace")
        return target.read_text(encoding="utf-8", errors="replace")

    def write_note(path: str, content: str) -> str:
        target = gateway._resolve_in_workspace(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"wrote {len(content)} bytes to {path}"

    def _validate_read(kwargs: dict) -> None:
        gateway._resolve_in_workspace(kwargs["path"])  # raises ToolDenied on escape

    def _validate_write(kwargs: dict) -> None:
        gateway._resolve_in_workspace(kwargs["path"])
        if len(kwargs.get("content", "")) > 10_000:
            raise ToolDenied("write exceeds the 10KB size limit for this demo")

    gateway.register("read_file", read_file, _validate_read)
    gateway.register("write_note", write_note, _validate_write)
    # Deliberately NOT registered: run_shell, fetch_url, delete_file — an
    # agent asking for any of these hits the "not allow-listed" branch above,
    # regardless of how it phrases the request or what injected it.
    return gateway
