# pcba-bench

**Can an AI agent design a manufacturable printed-circuit-board assembly from a written brief, unattended, in a fixed time?**

pcba-bench has ten boards, ranging from a single LED to a BLDC motor controller, an SDRAM tester and a USB-C PD supply. Each one is a short customer brief plus numbered requirements. The agent gets the brief, a declared set of tools and a fixed time budget, and nothing else. It must deliver:

- a KiCad 9 schematic and PCB;
- Gerbers and drill files;
- a BOM with orderable JLCPCB/LCSC parts, and a CPL;
- a `DECISIONS.md`.

Submissions are scored on a six-part rubric by **three judge models from three different vendors**, working blind from a deterministic evidence pack (KiCad ERC/DRC, copper-vs-schematic comparison, BOM resolution, renders). The per-criterion median is the official score. A separate **Manufacturable** flag records whether the board would pass fab with no further work.

The benchmark compares *agent + tools* combinations, for example a bare agent with only `kicad-cli` against the same agent with an electronics toolkit.

## Boards

| id | board | max layers | requirements | difficulty hint |
|---|---|---|---|---|
| 00 | Simple LED indicator | 2 | 10 | low |
| 01 | Voltage divider | 2 | 10 | low |
| 02 | Charlieplexed 3x3 LED grid | 2 | 13 | medium |
| 03 | USB joystick controller | 4 | 15 | high |
| 04 | STM32F103 development board | 2 | 12 | medium |
| 05 | Sensored BLDC motor controller | 4 | 13 | high |
| 06 | Four-channel LVDS link test coupon | 4 | 11 | low |
| 07 | SDRAM length-matched bus test vehicle | 6 | 14 | high |
| 08 | Four-channel precision acquisition | 4 | 12 | medium |
| 09 | USB-C PD 5 V power supply | 4 | 14 | medium |

The boards are independent tasks, **not a ladder**. The hints come from each board's `board.toml`; measured difficulty will replace them.

## How to run

The fork workflow is in [PROTOCOL.md](PROTOCOL.md):

1. Fork this repo, and pick an agent and a tools supplement.
2. `bench/start` builds an isolated workspace with only that board's input files.
3. Send the [initial prompt](prompts/initial.md) plus your tools supplement. If the agent stops early, send only the [continue prompt](prompts/continue.md), or set it as the agent's goal or loop input.
4. Stop at **120 minutes**. `bench/finish` snapshots the deliverable and transcript into `submissions/`.
5. Open a PR. Maintainers audit the transcript, then score it ([RUBRIC.md](RUBRIC.md), [JUDGING.md](JUDGING.md)).

## Status

**v0, protocol draft.** The following exist now:

- the input sets, the prompts, the rubric and the judging procedure;
- `bench/start` and `bench/finish`.

Not built yet:

- the evidence-pack generator (`judging/package`);
- the score aggregator (`judging/score`);
- a pinned judge panel;
- a reference container image.

Until those land, submissions can be collected but not scored.

## Provenance

The boards come from the demo fleet of [kicad-tools](https://github.com/rjwalters/kicad-tools). Their reference implementations are public in that repo, so runs must not access it (PROTOCOL.md §7). The briefs describe function only, so they don't reveal those implementations.

## License

MIT
