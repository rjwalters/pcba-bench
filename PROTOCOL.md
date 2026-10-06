# Run protocol (v1)

This document is normative. A submission that doesn't follow it is not scored.

## 1. The task

Each of the ten boards in `boards/` is one independent task: design a manufacturable PCBA from a written brief. The boards differ widely in difficulty, but they are **not** a ladder. Run any subset, in any order. Difficulty is measured from results, not assumed in advance.

## 2. Input file set

The agent's workspace contains these files, copied from `boards/<id>/`, **and nothing else**:

| File | Purpose |
|---|---|
| `BRIEF.md` | Customer-style description of what the board must do |
| `requirements.toml` | Numbered requirements (`R1`…), each with `must`, `category`, `text` and the `evidence` a judge will look at |
| `board.toml` | Machine-readable constraints: `fab`, `assembly`, `max_layers`, optional `max_board_mm` |

The environment also provides:

- KiCad 10 (`kicad-cli` plus the standard symbol, footprint and 3D libraries), the same version for every track;
- whatever the submitter's **tools supplement** declares.

The workspace must be created **outside** your fork's checkout (`bench/start` does this), so the agent can't see other boards, other submissions, or this repo's history.

## 3. Prompts

Exactly two texts may reach the agent:

1. **Initial prompt.** Send `prompts/initial.md`, with `{BOARD_ID}`, `{RUN_ID}` and `{MINUTES}` filled in, followed by your tools supplement. It is sent once, as the first message of a fresh session.
2. **Continue prompt.** Send `prompts/continue.md`, with `{REMAINING}` filled in. You may send it verbatim whenever the agent stops before the deadline, as often as needed. You may instead configure it as the agent's built-in goal or loop input (for example a Claude Code Stop hook or `/loop`, or a Codex goal), with the same text and no additions.

Nothing else may be sent: no corrections, hints, grades, error excerpts or approvals. If the agent asks a question, answer it with the continue prompt. Permission prompts must be pre-approved (for example by running the agent in a sandbox in its auto-approve or bypass mode), not answered by hand.

### Tools supplement

Your supplement describes the tools available in your environment, using `prompts/tools/TEMPLATE.md` (600 words max). Write one supplement per **track**, and use the same text for all ten boards. Two reference supplements ship with the benchmark:

- `prompts/tools/bare.md`: KiCad 10 CLI, Python, web.
- `prompts/tools/kicad-tools.md`: bare plus kicad-tools.

A supplement must not contain design advice, board-specific content, or pointers to existing designs.

## 4. Time

- **Standard allotment: 120 minutes of wall-clock time per board**, measured from sending the initial prompt.
- At the deadline, `bench/finish` snapshots `deliverable/`. Anything produced later is ignored.
- The clock doesn't pause, whether for slow tools, rate limits or crashes. If the agent crashes, you may restart the same agent in the same workspace with the continue prompt; the clock keeps running.
- Results are reported per allotment. A non-standard allotment (for example 30 or 480 minutes) is allowed but goes on a separate leaderboard.

## 5. Running it (fork workflow)

```bash
# 1. Fork rjwalters/pcba-bench and clone your fork.
# 2. For each board in the run:
bench/start --board 03-usb-joystick --track kicad-tools --minutes 120 \
            --agent "claude-code 2.x / claude-opus-5-5" --tools prompts/tools/kicad-tools.md
#    → creates ~/pcba-bench-runs/<run-id>/ with the input set
#    → writes <run-id>/PROMPT.md (initial prompt + supplement, ready to paste)
# 3. Launch the agent with cwd = ~/pcba-bench-runs/<run-id>/, then in the same
#    moment send PROMPT.md and start the clock:
bench/finish <run-id> --mark-start
#    Use the continue prompt only as allowed in §3.
# 4. At the deadline:
bench/finish <run-id> --transcript path/to/session.jsonl --continues N
#    → copies deliverable/, transcript and run.json into submissions/<run-id>/
# 5. Commit submissions/<run-id>/ on a branch and open a PR to rjwalters/pcba-bench.
```

## 6. What a submission contains

`submissions/<run-id>/`:

- `deliverable/`: exactly as it was at the deadline.
- `run.json`: board, track, agent and model (name and version), tools supplement hash, prompt version, start and finish times, the number of continue prompts sent, and token or cost figures if available.
- `transcript.*`: the full session log, with timestamps if the agent produces them. Required for audit; never shown to judges.
- `tools.md`: the exact supplement used.

## 7. Disqualification

A run is disqualified if any of these is true:

- the agent received any message other than the two allowed prompts;
- the transcript shows it fetched an existing design of the benchmark boards, including the upstream `rjwalters/kicad-tools` `boards/` tree;
- the deliverable was modified after the deadline;
- the supplement breaks §3.

Maintainers audit transcripts before scoring.

## 8. Scoring

See `RUBRIC.md` and `JUDGING.md`. In short:

- A deterministic **evidence pack** (KiCad ERC, DRC, netlist comparison, renders and BOM resolution) is generated from the deliverable.
- Three judge models from three different vendors then score a multi-part rubric blind.
- The per-criterion **median** is the official score.
