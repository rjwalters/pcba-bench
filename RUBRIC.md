# Scoring rubric (v1)

Each submission (one board, one run) is scored on six criteria. Each criterion gets an integer 0–4 from every judge. The official criterion score is the **median of the three judges**. The total is the weighted sum, normalized to 0–100.

| # | Criterion | Weight | Anchors (0 / 2 / 4) |
|---|---|---|---|
| A | **Electrical correctness**: does the schematic implement the brief correctly? Includes power, pin usage, required passives (decoupling, pull-ups, protection) and plausible values. | 25 | 0: missing, or fundamentally wrong. 2: mostly right, with defects that would stop the board working until reworked. 4: would work as designed; no blocking errors. |
| B | **Layout completeness and manufacturability**: placement, routing and fab readiness. | 25 | 0: no PCB, or mostly unrouted. 2: fully routed but with DRC errors or copper that disagrees with the schematic. 4: 100% routed, 0 DRC errors, copper matches the schematic, within fab limits. |
| C | **Requirement compliance**: each `requirements.toml` item rated met, partial or unmet. | 20 | Computed from per-requirement verdicts: 4 = every `must` met; −1 per unmet `must` (floor 0); partial = half; `must = false` items break ties within a band. |
| D | **BOM and assembly readiness**: real orderable parts matching their footprints, LCSC numbers, CPL consistent with the PCB. | 15 | 0: no BOM. 2: BOM present, some parts unresolvable or mismatched. 4: every line resolves to an in-stock part whose package matches its footprint; the CPL matches. |
| E | **Design quality**: placement logic, power and return paths, thermal care, silkscreen and polarity marks, testability. Graded as an experienced reviewer would. | 10 | 0: careless. 2: acceptable. 4: what a strong human engineer would ship. |
| F | **Documentation honesty**: `DECISIONS.md` records assumptions and choices and admits gaps. | 5 | 0: missing, or makes false claims. 2: present but thin. 4: clear, and every claim agrees with the evidence. |

## Mechanical caps (applied to judge scores before taking the median)

Judges must respect these, so evidence outranks impressions:

- No `board.kicad_pcb` → **B = 0**, D ≤ 1, E ≤ 1.
- ERC errors > 0 → A ≤ 3.
- DRC errors > 0 → B ≤ 2. Unrouted connections > 0 → B ≤ 2. Copper vs schematic mismatches > 0 → B ≤ 1.
- A `DECISIONS.md` claim contradicted by the evidence pack → **F = 0**.

## The "Manufacturable" flag

Separately from the score, the evidence pack sets a binary **Manufacturable** flag. It is true only when all of these hold: ERC 0 errors, DRC 0 errors (zones refilled), 100% of connections routed, copper matches the schematic, every BOM line resolves, and fab outputs are present. The leaderboard reports both the rubric score and the Manufacturable flag.

## Aggregates

- **Board score:** the rubric total for one attempted board (0–100). An unattempted board scores 0.
- **Suite score:** the mean board score over all ten boards in a run. A run is one session with a fixed total time (PROTOCOL.md §1).
- **Manufacturable count:** the number of the run's boards (of 10) whose Manufacturable flag is true.
- **Leaderboard:** runs are grouped by agent, toolkit and time allotment, and repeated runs are averaged (`results/RESULTS.md`).
