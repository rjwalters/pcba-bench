# Judging (v1)

## Panel

Three judge models from **three different vendors**:

| Vendor | Model | Native harness |
|---|---|---|
| Anthropic | `claude-opus-5-5` | Claude Code |
| OpenAI | `gpt-6-astra` | Codex CLI |
| Zhipu (Z.ai) | `glm-5.3` | opencode |

The panel is pinned by exact model ID in `judging/panel.toml`. Changing the panel bumps the judging version, and every existing submission is re-scored, so all leaderboard rows share one panel.

Self-preference bias is handled in three ways:

1. **Vendor diversity.** At most one judge can share a vendor with the agent under test.
2. **Median aggregation.** A single biased judge can't move a per-criterion median.
3. **Blinding.** Judges never see `run.json`, the transcript, the tools supplement, or the track. In native-harness mode, each judge works in a workspace built from the evidence bundle alone, never in the submission branch itself. The packager also strips agent-identifying text from the deliverable, such as "Generated with …" trailers and tool banners in file headers or `DECISIONS.md`.

Bias is also measured. For each judge we report its mean score on its own vendor's submissions minus the panel median on those submissions.

## What judges receive

`judging/package` builds one blinded bundle per submission, `judging/out/<run-id>/`:

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
- `deliverable/`: a blinded copy of the whole deliverable. Text files and the contents of zips are scrubbed of agent and tool identity, so a judge can open it with `kicad-cli`.

## Judge procedure (native harness; the default)

Each judge runs the same way a benchmark run does: a fresh session of its own native harness, a fixed prompt, a fixed time, and a file as its output.

```bash
judging/package submissions/<run-id>                         # evidence bundle -> judging/out/<run-id>/
judging/start-judging judging/out/<run-id> --judge anthropic  # blinded workspace in ~/pcba-bench-judging/
#   launch the judge's harness (panel.toml `harness`) with that workspace as cwd,
#   send JUDGE_PROMPT.md verbatim, and start the clock:
judging/finish-judging <workspace-id> --mark-start
#   ...the judge writes ./judgement.json and validates it with ./check-judgement...
judging/finish-judging <workspace-id> --transcript session.jsonl --continues N
#   repeat for the other two judges, then:
judging/score judging/out/<run-id>
```

- **The judge workspace** contains `inputs/`, the blinded `deliverable/`, `evidence/`, `renders/`, `RUBRIC.md`, `judgement.schema.json`, `./check-judgement` and `JUDGE_PROMPT.md`, and nothing else. The judge may inspect the design itself, including running `kicad-cli` read-only on a copy, but the evidence pack is ground truth.
- **Prompts.** The first message is `prompts/judge.md`. The only follow-up allowed is `prompts/judge-continue.md`, sent verbatim or set as the harness's goal or loop input. As in the benchmark, the judge starts a timer and has a fixed allotment, 30 minutes by default.
- **Output.** `judgement.json` matches `judgement.schema.json`:

  ```json
  {
    "requirements": [{"id": "R1", "verdict": "met|partial|unmet", "reason": "..."}],
    "criteria": {"A": {"score": 0, "reason": "..."}, "B": {}, "C": {}, "D": {}, "E": {}, "F": {}},
    "caps_applied": ["DRC errors > 0 -> B <= 2"],
    "false_claims": ["..."]
  }
  ```

- **Collection.** `finish-judging` rejects an invalid judgement, records timing, the prompt hash and the harness, and stores everything in `judging/responses/<run-id>/`. `judging/score` refuses a judgement whose recorded model differs from the pinned panel.

**API mode.** `judging/score --api` sends the same material in one structured-output request per judge, and `--dry-run` writes those requests without sending them. It exists for automation and testing; the native-harness judgements are the official ones.

## Aggregation

`judging/score` applies these steps:

1. It recomputes **C** from each judge's requirement verdicts: 4 minus 1 per unmet `must`, a partial counting half.
2. It sets **F = 0** for any judge that reported a false claim.
3. It clamps each judge's scores to the **mechanical caps** derived from the evidence pack and logs every clamp.
4. It takes the **per-criterion median** and the weighted 0–100 total.
5. It records each requirement's median verdict.

**Disagreement:** when any criterion has a judge spread ≥ 2 points, the submission is flagged for human review. A maintainer may then re-run that judge once, but may never edit a score.

Each judge scores each submission once. Effort or reasoning level is fixed per panel version. Sampling temperature is not used, because current reasoning models reject it.

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

Run it after every grader change, against any clean submission you have locally. No fixture is committed, because committing a clean solution to one of the ten boards would publish it.
