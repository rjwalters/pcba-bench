# Judging (v1)

## Panel

Three judge models from **three different vendors**, for example one each from Anthropic, OpenAI and Google. The panel is pinned by exact model ID in `judging/panel.toml`. Changing the panel bumps the judging version, and every existing submission is re-scored, so all leaderboard rows share one panel.

Self-preference bias is handled in three ways:

1. **Vendor diversity.** At most one judge can share a vendor with the agent under test.
2. **Median aggregation.** A single biased judge can't move a per-criterion median.
3. **Blinding.** Judges never see `run.json`, the transcript, the tools supplement, or the track. The packager also strips agent-identifying text from the deliverable, such as "Generated with …" trailers and tool banners in file headers or `DECISIONS.md`.

Bias is also measured. For each judge we report its mean score on its own vendor's submissions minus the panel median on those submissions.

## What judges receive

`judging/package` builds one blinded bundle per submission:

- `BRIEF.md`, `requirements.toml` and `board.toml` for the board;
- the **evidence pack**, produced deterministically and identically for every submission:
  - `erc.json` from `kicad-cli sch erc`.
  - `drc.json`: KiCad DRC under the **submitter's own** rules, with zones refilled and schematic parity on. This shows design intent.
  - `drc_fab.json`: KiCad DRC under **grader-owned** fab rules. These **gate**. For each minimum, the grader takes the stricter of the submitter's setting and `judging/fab_rules/<fab>.toml` for the layer count, and resets rule severities and DRC exclusions to KiCad defaults (`fab_rules_applied.json` records what was dropped). A submission therefore can't pass by relaxing its own rules.
  - `lvs.json`: the schematic netlist (`kicad-cli sch export netlist`) against PCB pad nets, compared **by connectivity partition, not by net name**. It reports split nets, merged nets, and missing or extra footprints. KiCad's own `net_conflict` parity items also fire on name-only differences (`X` vs `/X`), so they are reported but do not gate; `lvs.json` covers wrong-net pads.
  - `bom_resolution.json`: each BOM line's LCSC lookup (exists, MPN, package), with package-vs-footprint marked `match`/`check`/`unknown`, plus BOM↔schematic reference coverage. Stock figures are LCSC distribution stock, which is advisory: it is not JLCPCB assembly stock.
  - `cpl.json`: SMD footprints missing from the CPL, and CPL references not on the PCB.
  - `fab.json`: Gerber, drill and outline files present, looking inside zips too.
  - `stats.json`: copper layers, board size, footprints (and how many are on the bottom), nets, tracks, vias and zones, checked against `board.toml` limits.
  - `summary.json`: the gates and the **Manufacturable** flag.
  - Renders: schematic pages, per-copper-layer PCB plots and top and bottom 3D views, as PNG.
- the deliverable's `board.kicad_sch`, `board.kicad_pcb`, `bom.csv`, `cpl.csv` and `DECISIONS.md`, as text.

## Judge procedure

Each judge receives `judging/judge-prompt.md`, the rubric and the bundle, and returns JSON:

```json
{
  "requirements": [{"id": "R1", "verdict": "met|partial|unmet", "reason": "…"}],
  "criteria": {"A": {"score": 0, "reason": "…"}, "B": {}, "C": {}, "D": {}, "E": {}, "F": {}},
  "caps_applied": ["DRC errors > 0 → B ≤ 2"],
  "false_claims": ["…"]
}
```

`judging/score` validates the output against the rubric caps. A judge score above a cap is clamped and logged. It then computes per-criterion medians, the total, and inter-judge spread.

**Disagreement:** when any criterion has a judge spread ≥ 2 points, the submission is flagged for human review. A maintainer may then re-run that judge once, but may never edit a score.

Each judge is run at temperature 0 where the API supports it. Each judge scores each submission once.

## Grader self-test

`judging/selftest <clean-submission>` checks that the grader catches planted defects. It packages a known-clean submission, which must come out Manufacturable. It then applies each mutation to a copy and requires the matching gate to flip and Manufacturable to become false:

| Mutation | Must flip |
|---|---|
| swap two pads' nets | `lvs_matches` |
| unroute a net (tracks, vias and its zones) | `unconnected_items` |
| delete a footprint | `lvs_matches` |
| draw a track between two different-net pads | `drc_errors` |
| the same short, plus relaxed submitter rules and severities set to `ignore` | `drc_errors` |
| replace an LCSC code with a nonexistent one | `bom_resolved` |
| delete the fab outputs | `fab_outputs_complete` |
| delete the PCB | `pcb_present` |

Run it after every grader change. The clean fixture must not be one of the ten benchmark boards, because the fixture would then publish a solution. Until a dedicated fixture lands, run it locally against any clean board.
