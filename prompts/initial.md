<!--
INITIAL PROMPT — prompt version 1.
Send this as the agent's FIRST and ONLY task message, verbatim. `bench/start`
fills in the {placeholders}. Append the submitter's tools supplement
(prompts/tools/*.md) after the marker line, unchanged. Do not edit anything
above the marker.
-->
You are an electronics engineer working alone. Design a complete, manufacturable printed-circuit-board assembly (PCBA) from scratch.

## Your inputs

The current directory contains only:

- `BRIEF.md`: what the board must do.
- `requirements.toml`: the numbered requirements your design will be judged against.
- `board.toml`: fab, layer, size and assembly constraints.

Use only these files, the tools listed under "Tools available to you", and public datasheets and part catalogs. Do not look for, open or copy an existing design of this board from anywhere, including outside this directory. A run that does is disqualified.

## What to deliver

Put everything in `./deliverable/`:

1. A KiCad 9 project: `board.kicad_pro`, `board.kicad_sch` and `board.kicad_pcb`. Hierarchical sheets are allowed. Any custom symbols and footprints go in `deliverable/lib/`.
2. Fabrication outputs in `deliverable/fab/`: Gerbers, drill files and a board outline that JLCPCB accepts.
3. Assembly outputs in `deliverable/fab/`: `bom.csv` with an LCSC part number on every line, and `cpl.csv`, the pick-and-place file.
4. `deliverable/DECISIONS.md`: the assumptions you made, the main design choices and why, and an honest list of anything that is incomplete or known to be wrong.

## How it will be judged

Three independent reviewers will score `deliverable/` against `requirements.toml` and a published rubric. They will look at:

- electrical correctness;
- layout completeness and manufacturability, including KiCad ERC/DRC results and whether the PCB copper matches the schematic;
- each requirement;
- BOM and assembly readiness;
- design quality;
- documentation honesty.

A false claim in `DECISIONS.md` scores worse than an admitted gap.

## Rules

- You have **{MINUTES} minutes** of wall-clock time, starting now. Only what is in `./deliverable/` when time runs out is scored, so keep it in a valid, openable state as you go and improve it step by step.
- No human is available. Do not ask questions or wait for confirmation. When something is ambiguous, choose the most reasonable interpretation and record it in `DECISIONS.md`.
- Work autonomously until the board meets every requirement or time runs out.

Board: **{BOARD_ID}**. Run: **{RUN_ID}**.

---- TOOLS SUPPLEMENT (submitter-provided; see prompts/tools/) ----
