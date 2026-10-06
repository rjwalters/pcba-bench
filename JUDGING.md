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
3. **Blinding.** Judges don't see `run.json`, the transcript, the tools supplement, the toolkit or other judges' results.
   - Run ids are opaque (`run--<hex>`), and the scripts make every branch commit with a neutral message.
   - A judge opens the run branch only to run `judging/prepare`, then does the review in a workspace outside the repository that holds only blinded material.
   - The packager strips agent-identifying text from the deliverables, such as "Generated with …" trailers and tool banners in file headers or `DECISIONS.md`.
   - The judge session prompt forbids reading identity files, `judgements/` and git history.

   This is enforced by instruction, not by access control. A judge in its native harness can technically read the branch. The median over three vendors limits what any single leak can do. If that proves insufficient, the fallback is a separate blinded judging branch.

Bias is also measured. For each judge we report its mean score on its own vendor's submissions minus the panel median on those submissions.

## What judges receive

For each attempted board, `judging/package` (in the pinned grader container) builds one blinded bundle:

- `inputs/`: `BRIEF.md`, `requirements.toml` and `board.toml` for the board;
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

## Judge procedure (native harness, on the run branch)

Each judge runs much like a benchmark run: a fresh session of its own native harness, a fixed prompt, a fixed time, and committed files as its output.

1. **Open the run branch** (`run/<run-id>`) in the judge's harness, as listed in `panel.toml`, with the repository root as the working directory.
2. **Send `prompts/judge-session.md`** verbatim, with `{RUN_ID}` and `{VENDOR}` filled in. The only follow-up allowed is `prompts/judge-continue.md`, sent verbatim or set as the harness's goal or loop input. The session prompt has the judge:
   1. run `judging/prepare <run-id> --judge <vendor>`, which regenerates the evidence for every attempted board in the grader container and builds the blinded workspace in `~/pcba-bench-judging/`;
   2. follow that workspace's `JUDGE_PROMPT.md`, writing `boards/<id>/judgement.json` for each board and checking the results with `./check-judgement`. The judge has a 60-minute timer for all boards and writes a first judgement for every board before refining any.
   3. run `judging/submit <workspace-id>`. It validates the judgements and **commits** them to `submissions/<run-id>/judgements/<vendor>/`, along with a `meta.json` recording model, harness, prompt hash and timing.
3. **Finalize.** When `judging/submit` sees that all three panel judges have committed, it runs `judging/finalize`, which:
   1. re-grades for the gates;
   2. scores each board and the suite;
   3. writes `score.json` and `results/rows/<run-id>.json`, and re-renders `results/RESULTS.md`;
   4. commits, pushes and **opens the PR to main** (from a fork, to `rjwalters/pcba-bench`).

   `finalize` refuses judgements from any model other than the one the panel pins.

**Judge environment.** Each judge's harness has `kicad-cli` (KiCad 10) and kicad-tools at the version pinned in `panel.toml` (`kicad_tools_version`, currently 0.22.0) on `PATH`, and `judging/prepare` refuses a mismatched version. These are inspection aids for confirming DRC, connectivity or BOM questions on a copy of a deliverable. The evidence pack stays ground truth, and every submission is inspected with the same tools whatever toolkit produced it.

The workspace contains `boards/<id>/` for each attempted board, with `inputs/`, the blinded `deliverable/`, `evidence/`, `renders/` and `judgement.schema.json`, plus `RUBRIC.md`, `./check-judgement` and `JUDGE_PROMPT.md`, and nothing else. The judge may inspect a design itself, including running `kicad-cli` read-only on a copy, but the evidence pack is ground truth.

Each board's `judgement.json` matches its `judgement.schema.json`:

```json
{
  "requirements": [{"id": "R1", "verdict": "met|partial|unmet", "reason": "..."}],
  "criteria": {"A": {"score": 0, "reason": "..."}, "B": {}, "C": {}, "D": {}, "E": {}, "F": {}},
  "caps_applied": ["DRC errors > 0 -> B <= 2"],
  "false_claims": ["..."]
}
```

No API tokens are involved anywhere: agents and judges use their own logged-in harnesses, and the grader is a local container.

## Aggregation

For each attempted board, `judging/finalize` (via `judging/scoring.py`) applies these steps:

1. It recomputes **C** from each judge's requirement verdicts: 4 minus 1 per unmet `must`, a partial counting half.
2. It sets **F = 0** for any judge that reported a false claim.
3. It clamps each judge's scores to the **mechanical caps** derived from the evidence pack and logs every clamp.
4. It takes the **per-criterion median** and the weighted 0–100 total.
5. It records each requirement's median verdict.

Unattempted boards score 0. The **suite score** is the mean over all ten boards.

**Disagreement:** when any criterion on a board has a judge spread ≥ 2 points, that board is flagged for human review in the PR. A maintainer may then re-run that judge once, but may never edit a score.

Each judge scores each run once.

## Grader self-test

`judging/selftest <clean-dir>` checks that the grader catches planted defects. It packages a known-clean submission, which must come out Manufacturable. It then applies each mutation to a copy and requires the matching gate to flip and Manufacturable to become false:

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
