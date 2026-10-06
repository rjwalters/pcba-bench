<!--
INITIAL PROMPT — prompt version 3 (suite run).
Send this as the agent's FIRST and ONLY task message, verbatim. `bench/start`
fills in the {placeholders}. Append the submitter's tools supplement
(prompts/tools/*.md) after the marker line, unchanged. Do not edit anything
above the marker.
-->
You are an electronics engineer working alone. You have **{MINUTES} minutes** in total to design as many complete, manufacturable printed-circuit-board assemblies (PCBAs) as you can, from the {BOARD_COUNT} customer briefs in `boards/`:

{BOARD_LIST}

## Inputs, for each board `boards/<id>/`

- `BRIEF.md`: what the board must do.
- `requirements.toml`: the numbered requirements the board will be judged against.
- `board.toml`: fab, layer, size and assembly constraints.

Use only these files, the tools listed under "Tools available to you", and public datasheets and part catalogs. Do not look for, open or copy an existing design of any of these boards from anywhere, including outside this directory. A run that does is disqualified.

## What to deliver, for each board you attempt, in `deliverables/<id>/`

1. A KiCad 10 project: `board.kicad_pro`, `board.kicad_sch` and `board.kicad_pcb`. Hierarchical sheets are allowed. Any custom symbols and footprints go in `deliverables/<id>/lib/`.
2. Fabrication outputs in `deliverables/<id>/fab/`: Gerbers, drill files and a board outline that JLCPCB accepts.
3. Assembly outputs in `deliverables/<id>/fab/`: `bom.csv` with an LCSC part number on every line, and `cpl.csv`, the pick-and-place file.
4. `deliverables/<id>/DECISIONS.md`: the assumptions you made, the main design choices and why, and an honest list of anything that is incomplete or known to be wrong.

## How it will be scored

- Three independent reviewers score each attempted board against its `requirements.toml` and a published rubric. They look at:
  - electrical correctness;
  - layout completeness and manufacturability, including KiCad ERC/DRC results and whether the PCB copper matches the schematic;
  - each requirement;
  - BOM and assembly readiness;
  - design quality;
  - documentation honesty.
- A board scores 0–100. A board you don't attempt scores **0**.
- **The run's score is the mean over all {BOARD_COUNT} boards.** The number of boards that would pass fabrication with no further work is reported alongside.
- A false claim in a `DECISIONS.md` scores worse than an admitted gap.
- The boards differ widely in difficulty. Choosing which to do, in what order, and when to stop polishing one and start the next is part of the task.

## Rules

- **Start a timer before doing anything else.** Run `date -u +%s > .timer-start`. Whenever you need it (at least between boards and every few major steps), check what is left with `echo $(( {MINUTES} - ($(date -u +%s) - $(cat .timer-start)) / 60 )) minutes left`, and plan against that clock.
- Only what is in `deliverables/` when time runs out is scored. Keep each board's folder in a valid, openable state as you go: fab outputs regenerated from its final PCB, BOM and CPL matching it, `DECISIONS.md` current. Don't leave a board half-edited when you move on.
- Keep notes per board in its `DECISIONS.md`, not only in your head: long sessions may be compacted.
- No human is available. Don't ask questions or wait for confirmation. When something is ambiguous, choose the most reasonable interpretation and record it in that board's `DECISIONS.md`.
- Work autonomously until time runs out.

Run: **{RUN_ID}**.

---- TOOLS SUPPLEMENT (submitter-provided; see prompts/tools/) ----
