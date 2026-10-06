# Reference containers

Every track runs in a container built from one pinned base, so all tracks share the same KiCad version and every agent sees the same workspace view.

| Image | Dockerfile | Adds |
|---|---|---|
| `pcba-bench/base` | `container/Dockerfile` | KiCad **10.0.6** (official `kicad/kicad` image, pinned by digest), Python 3, poppler, ImageMagick, uv, and the grader (`package`, `selftest`, `score`, `start-judging`, `finish-judging` on `PATH`) |
| `pcba-bench/claude-code-bare` | `container/tracks/claude-code-bare.Dockerfile` | Claude Code CLI |
| `pcba-bench/claude-code-kicad-tools` | `container/tracks/claude-code-kicad-tools.Dockerfile` | kicad-tools (pip, with the C++ router built) and the `/kct:*` skills at user level |

```bash
docker build --platform linux/amd64 -t pcba-bench/base -f container/Dockerfile .
docker build --platform linux/amd64 -t pcba-bench/claude-code-bare -f container/tracks/claude-code-bare.Dockerfile .
docker build --platform linux/amd64 -t pcba-bench/claude-code-kicad-tools -f container/tracks/claude-code-kicad-tools.Dockerfile .
```

The KiCad image is published for amd64 only. On Apple-silicon hosts it runs under emulation: slower, but the same binaries.

## Rules for track images

- **Install the toolkit before the clock starts.** Anything a tools supplement declares must already be installed in the image. Installing during a run counts against the run's time.
- **No reference designs.** Nothing from `rjwalters/kicad-tools` `boards/` may enter an image. The kicad-tools track fetches only `.claude/commands/kct/` in a discarded build stage, using a sparse, blob-filtered clone, until kicad-tools ships skills in its wheel (kicad-tools#5950). KiCad's own stock `template/` and `demos/` directories are part of the standard install and are available to every track equally.
- **One image per track, the same for all ten boards.** A track's image is part of its declared toolkit; record its digest in the submission.

## Running

`bench/drive-claude-code <run-id> --image pcba-bench/claude-code-kicad-tools` runs one board end to end:

1. It mounts only `BRIEF.md`, `requirements.toml`, `board.toml` (read-only) and `deliverable/` at `/work`.
2. It starts the clock and sends the initial prompt.
3. It sends the continue prompt verbatim whenever the agent stops early, and kills the session at the deadline.
4. It keeps the stream-json transcript on the host, out of the agent's reach.
5. It calls `bench/finish`.

Grading uses the base image:

```bash
docker run --rm --platform linux/amd64 -v "$PWD:/data" pcba-bench/base package /data/submissions/<run-id> -o /data/judging/out
docker run --rm --platform linux/amd64 -v /path/to/clean-submission:/data pcba-bench/base selftest /data
```
