"""Simulates an agent issuing a mix of legitimate and malicious tool calls.

Run this to see the gateway from tool_gateway.py allow legitimate,
in-scope actions while denying (and logging) everything else — including
the kind of requests a successful prompt injection would try to issue
(see docs/owasp-llm/LLM01.md and LLM03.md).

    python demo_agent.py
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from tool_gateway import ToolDenied, build_demo_gateway

# Each tuple is (description, tool_name, kwargs). The last four simulate an
# agent that has been manipulated — by a poisoned document, a malicious tool
# response, or a direct jailbreak attempt — into trying something outside
# its intended scope.
SIMULATED_CALLS = [
    ("legitimate: write a scratch note", "write_note", {"path": "notes/todo.txt", "content": "buy milk"}),
    ("legitimate: read it back", "read_file", {"path": "notes/todo.txt"}),
    ("malicious: path traversal out of the workspace", "read_file", {"path": "../../etc/passwd"}),
    ("malicious: absolute-path escape", "read_file", {"path": "/etc/shadow"}),
    ("malicious: tool not in the allowlist at all", "run_shell", {"command": "rm -rf /"}),
    ("malicious: oversized write (denial-of-wallet-style abuse)", "write_note", {"path": "notes/spam.txt", "content": "x" * 50_000}),
]


def main() -> None:
    with TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        gateway = build_demo_gateway(workspace)

        results = []
        for description, tool_name, kwargs in SIMULATED_CALLS:
            try:
                output = gateway.call(tool_name, **kwargs)
                results.append((description, "ALLOWED", output))
            except ToolDenied as exc:
                results.append((description, "DENIED", str(exc)))

        print("\n--- Summary ---")
        for description, outcome, detail in results:
            print(f"[{outcome:7}] {description}\n           -> {detail}")


if __name__ == "__main__":
    main()
