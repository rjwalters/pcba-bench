# Track: Claude Code + kicad-tools (tools supplement: prompts/tools/kicad-tools.md).
#
#   docker build --platform linux/amd64 -t pcba-bench/claude-code-kicad-tools \
#     --build-arg KCT_VERSION=0.22.0 -f container/tracks/claude-code-kicad-tools.Dockerfile .

# Throwaway stage: fetch ONLY the /kct:* skill files from kicad-tools at the
# release tag. A sparse, blob-filtered clone never downloads boards/, and this
# stage is discarded, so no reference design can reach the final image.
# (Replace with `kct skills install` once kicad-tools#5950 ships skills in the wheel.)
FROM alpine/git:2.47.2 AS kct-skills
ARG KCT_VERSION=0.22.0
RUN git clone --depth 1 --filter=blob:none --sparse --branch "v${KCT_VERSION}" \
      https://github.com/rjwalters/kicad-tools.git /src \
 && git -C /src sparse-checkout set --no-cone /.claude/commands/kct/ \
 && test ! -e /src/boards

FROM pcba-bench/claude-code-bare
ARG KCT_VERSION=0.22.0
USER root
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends cmake g++ make python3-dev \
 && rm -rf /var/lib/apt/lists/*
USER kicad
# Toolkit is installed before the clock starts (PROTOCOL.md §2): a private venv on PATH.
RUN python3 -m venv /home/kicad/kct \
 && /home/kicad/kct/bin/pip install --no-cache-dir "kicad-tools==${KCT_VERSION}" \
 && /home/kicad/kct/bin/kct build-native \
 && /home/kicad/kct/bin/kct build-native --check
ENV PATH="/home/kicad/kct/bin:${PATH}"
# User-level skills: available as /kct:* in any Claude Code session in this image.
COPY --from=kct-skills --chown=kicad:kicad /src/.claude/commands/kct/ /home/kicad/.claude/commands/kct/
