# Container-level isolation layer for an agent process.
#
# This is defense-in-depth *underneath* the application-level tool_gateway.py
# allowlist, not a replacement for it: if the gateway is ever bypassed (a bug,
# a new tool added without a validator, a dependency compromise per
# docs/owasp-llm/LLM04.md), these constraints limit what that failure can
# reach — no root, no writable filesystem outside the scratch dir, and no
# network unless explicitly opted into at `docker run` time.

FROM python:3.12-slim

# Run as a dedicated, unprivileged, non-root user.
RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin agent
WORKDIR /home/agent/app

COPY tool_gateway.py demo_agent.py ./
RUN chown -R agent:agent /home/agent

USER agent

# The workspace the gateway confines file access to. Mount this as a tmpfs
# or a throwaway volume at run time; everything else in the image should be
# mounted or run read-only (see the docker run example in README.md).
RUN mkdir -p /home/agent/workspace

CMD ["python", "demo_agent.py"]
