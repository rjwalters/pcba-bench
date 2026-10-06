# Run protocol (v2: suite runs)

This document is normative. A submission that doesn't follow it is not scored.

## 1. The task

A **run** is one agent session with a fixed total time (standard: **60 minutes**) and all ten boards in `boards/`. The agent designs as many manufacturable PCBAs as it can from the written briefs. It chooses which boards to attempt, in what order, and when to move on.

- Each attempted board is graded and judged on its own (`RUBRIC.md`) and scores 0–100.
- An unattempted board scores 0.
- The run's **suite score** is the mean over all ten boards. It is reported with the count of boards that pass the Manufacturable flag.

The boards differ widely in difficulty and are not a ladder. Difficulty is measured from results.

## 2. Input file set

The agent's workspace contains exactly this, and nothing else:

```
boards/<id>/BRIEF.md            customer-style description of what the board must do
boards/<id>/requirements.toml   numbered requirements (R1...) with must, category, text, evidence
boards/<id>/board.toml          fab, assembly, max_layers, optional max_board_mm
deliverables/<id>/              empty; the agent's output goes here
PROMPT.md                       the initial prompt (also sent as the first message)
```

There is one `boards/<id>/` and one `deliverables/<id>/` for each of the ten boards.

The environment also provides:

- **KiCad 10** (`kicad-cli` plus the standard symbol, footprint and 3D libraries), the same version for every submission. The grader always runs in the pinned container in `container/` (KiCad 10.0.6).
- Whatever the submitter's **tools supplement** declares, **installed before the clock starts**. Installing tools during a run counts against the run's time.

`bench/start` creates the workspace **outside** your fork's checkout, so the agent can't see this repository, other submissions or its history. Agents may run in their native harness on the host (no API tokens needed) or in a track container (`container/`, `bench/drive-claude-code`). Either way, the agent must not access existing designs of these boards (§7).

## 3. Prompts

Exactly two texts may reach the agent:

1. **Initial prompt.** Send `PROMPT.md` once, as the first message of a fresh session. It is `prompts/initial.md`, filled in by `bench/start`, plus your tools supplement.
2. **Continue prompt.** You may send `prompts/continue.md` verbatim, with `{REMAINING}` filled in, whenever the agent stops before the deadline, as often as needed. Alternatively, configure it as the agent's built-in goal or loop input (for example a Claude Code Stop hook or `/loop`, or a Codex goal), with the same text and no additions.

Nothing else may be sent: no corrections, hints, grades, error excerpts or approvals. If the agent asks a question, answer it with the continue prompt. Pre-approve permission prompts, for example with the harness's auto-approve or bypass mode; don't answer them by hand.

### Tools supplement

Your supplement describes the tools available to the agent, following `prompts/tools/TEMPLATE.md` (600 words max). There is one supplement per toolkit. Reference supplements:

- `prompts/tools/bare.md`: KiCad 10 CLI, Python and the web.
- `prompts/tools/kicad-tools.md`: bare plus kicad-tools.

A supplement must not contain design advice, board-specific content or pointers to existing designs.

## 4. Time

- **Standard allotment: 60 minutes of wall-clock time for the whole suite**, measured from sending the initial prompt. The prompt tells the agent to start its own timer.
- At the deadline, stop the agent and run `bench/finish`, which snapshots `deliverables/`. Anything produced later is ignored.
- The clock doesn't pause for slow tools, rate limits or crashes. After a crash you may restart the same agent in the same workspace with the continue prompt, and the clock keeps running.
- Results are grouped by allotment. A non-standard allotment, such as 30 or 240 minutes, is allowed but forms its own leaderboard group.

## 5. Running it (git-native: branch → run → three judges → PR)

```bash
# 0. Fork rjwalters/pcba-bench (or work on a branch of it) and clone it.
#    Build the grader image once: docker build --platform linux/amd64 -t pcba-bench/base -f container/Dockerfile .

# 1. Start: creates branch run/<run-id> and the workspace ~/pcba-bench-runs/<run-id>/
bench/start --track kicad-tools --agent "claude-code 2.x / claude-opus-5-5" \
            --tools prompts/tools/kicad-tools.md            # --minutes 60 by default

# 2. Run: open the agent's native harness with that workspace as cwd, send PROMPT.md,
#    and at the same moment start the clock:
bench/finish <run-id> --mark-start
#    Use only the continue prompt (§3) until the deadline.

# 3. Submit: at the deadline, snapshot and commit to the run branch
bench/finish <run-id> --transcript path/to/session.jsonl --continues N

# 4. Judge: open the SAME branch in each judge's native harness (JUDGING.md) and send
#    prompts/judge-session.md. Each judge adds one commit; the last one to finish scores
#    the run, adds its row to results/ and opens the PR to main.
```

All commits on the run branch are made by the scripts, with neutral messages and no tool trailers, so a judge can't learn the agent from the history.

## 6. What a submission contains

`submissions/<run-id>/` contains:

- `deliverables/<id>/`: each board's folder, exactly as it was at the deadline.
- `run.json`:
  - the boards and which were attempted;
  - toolkit, agent and model (name and version);
  - the hashes of the prompts and the supplement;
  - start and finish times, and the number of continue prompts sent;
  - the token or cost figures and the track image digest, if available;
  - the transcript leak scan (§7).
- `transcript.*`: the full session log, required for audit and never shown to judges.
- `tools.md`: the exact supplement used.

After judging, the run branch also contains `judgements/<vendor>/<id>.json` with each judge's `meta.json`, plus `score.json`. It adds one file, `results/rows/<run-id>.json`.

## 7. Disqualification

A run is disqualified if any of these is true:

- the agent received any message other than the two allowed prompts;
- the transcript shows it accessed an existing design of the benchmark boards, including the `boards/` tree of `rjwalters/kicad-tools`, upstream or in a local checkout (`bench/finish` scans the transcript for this);
- a deliverable was modified after the deadline;
- the supplement breaks §3.

Maintainers audit transcripts before merging a result PR.

## 8. Scoring

See `RUBRIC.md` and `JUDGING.md`. In short:

- The pinned grader container generates a deterministic **evidence pack** for each attempted board: KiCad ERC and DRC, a copper-vs-schematic comparison, BOM resolution and renders.
- Three judge models from three different vendors, each in its own native harness, score the six-part rubric blind for each board.
- The per-criterion **median** is the official board score. The suite score is the mean over all ten boards.
