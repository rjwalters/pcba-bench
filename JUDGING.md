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
  - `erc.json` and `drc.json` from `kicad-cli`, with zones refilled before DRC;
  - `lvs.json`: PCB copper connectivity compared against the netlist exported from the submitted schematic, which yields unrouted and mismatched connections;
  - `bom_resolution.json`: each BOM line's LCSC lookup, stock, and package vs footprint;
  - `stats.json`: layer count, board size, nets, footprints, vias and track length;
  - renders: schematic PDF→PNG pages, plus per-layer and 3D PCB PNGs;
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
