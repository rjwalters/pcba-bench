# pcba-bench base image: the pinned environment shared by every track and the grader.
#
#   docker build --platform linux/amd64 -t pcba-bench/base -f container/Dockerfile .
#
# KiCad is pinned by digest (official image; amd64 only, runs emulated on arm64 hosts).
# Track images (container/tracks/*.Dockerfile) build FROM this and add an agent
# CLI plus that track's declared toolkit. Nothing from rjwalters/kicad-tools
# `boards/` may ever enter an image (PROTOCOL.md §7).
FROM kicad/kicad:10.0.6-full@sha256:e36e29b5f4a638a1a7238eba3d2fcbc8e061ffed1e99a8f39cb722706c94a58e

USER root
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      ca-certificates curl git jq less procps \
      python3 python3-venv python3-pip \
      poppler-utils imagemagick \
 && rm -rf /var/lib/apt/lists/*

# Grader and run scripts. Board inputs ship too: the agent only ever sees the
# per-run workspace copy that bench/start makes, never this tree.
COPY bench/ /opt/pcba-bench/bench/
COPY judging/ /opt/pcba-bench/judging/
COPY prompts/ /opt/pcba-bench/prompts/
COPY boards/ /opt/pcba-bench/boards/
COPY RUBRIC.md PROTOCOL.md JUDGING.md /opt/pcba-bench/
RUN rm -rf /opt/pcba-bench/judging/out /opt/pcba-bench/judging/responses \
 && chmod +x /opt/pcba-bench/bench/* /opt/pcba-bench/judging/package /opt/pcba-bench/judging/selftest
ENV PATH="/opt/pcba-bench/bench:/opt/pcba-bench/judging:${PATH}" \
    KICAD_CLI=/usr/bin/kicad-cli

# The agent works in /work (a bind-mounted run workspace) as the unprivileged kicad user.
RUN mkdir -p /work && chown kicad:kicad /work \
 && gpasswd -d kicad sudo || true
USER kicad
WORKDIR /work
ENTRYPOINT []
CMD ["bash"]
