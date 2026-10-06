# Track: Claude Code, bare (tools supplement: prompts/tools/bare.md).
#
#   docker build --platform linux/amd64 -t pcba-bench/claude-code-bare -f container/tracks/claude-code-bare.Dockerfile .
FROM pcba-bench/base

USER root
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs npm \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @anthropic-ai/claude-code \
 && npm cache clean --force
USER kicad
