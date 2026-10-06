# pcba-bench

**How many manufacturable printed-circuit-board assemblies can an AI agent design from written briefs, unattended, in one hour?**

pcba-bench has ten boards, ranging from a single LED to a BLDC motor controller, an SDRAM tester and a USB-C PD supply. Each is a short customer brief plus numbered requirements. A **run** is one agent session with all ten briefs, a declared set of tools and **60 minutes** in total. The agent decides which boards to attempt and in what order. For each board it attempts, it must deliver:

- a KiCad 10 schematic and PCB;
- Gerbers and drill files;
- a BOM with orderable JLCPCB/LCSC parts, and a CPL;
- a `DECISIONS.md`.

**Scoring.**

- Each attempted board is scored 0–100 on a six-part rubric by **three judge models from three different vendors**: Claude Opus 5.5, GPT-6 Astra and GLM-5.3. Each runs in its own native harness and works blind from a deterministic evidence pack (KiCad ERC/DRC, copper-vs-schematic comparison, BOM resolution, renders). The per-criterion median is the official board score.
- Unattempted boards score 0. The **suite score** is the mean over all ten boards.
- A separate **Manufacturable** count records how many boards would pass fab with no further work.

Each run is an **agent + toolkit** pair, and any pairs can be compared. For example, a bare agent with only `kicad-cli` (say, Claude Opus 5.5 as-is) can go up against a different agent with a declared toolkit (say, Codex Astra 6.1 + some electronics toolkit). The leaderboard keys every row by agent, model version, toolkit and time allotment.

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

The boards are not a ladder. The hints come from each board's `board.toml`; measured difficulty will replace them.

## How a run works

Everything happens on one git branch, and no API tokens are needed. Agents and judges use their own logged-in native harnesses, and the grader is a local container. Details are in [PROTOCOL.md](PROTOCOL.md) and [JUDGING.md](JUDGING.md).

1. **Start.** `bench/start` creates branch `run/<run-id>` and an isolated workspace, outside the repo, with the ten briefs.
2. **Run.** Open the agent's harness in that workspace and send `PROMPT.md`. That's the [initial prompt](prompts/initial.md) plus your tools supplement. If the agent stops early, send only the [continue prompt](prompts/continue.md), or set it as the agent's goal or loop input. Stop at 60 minutes.
3. **Submit.** `bench/finish` snapshots the deliverables and transcript and **commits** them to the branch.
4. **Judge.** Open the same branch in each judge's harness (Claude Code, Codex CLI, opencode) and send the [judge session prompt](prompts/judge-session.md). Each judge commits its judgements. The last one to finish scores the run, adds its row to [results/RESULTS.md](results/RESULTS.md), and **opens the PR** to main.

## First evaluation matrix

Eight runs: four agents × two toolkits, one 60-minute suite run each.

| Agent | Harness | bare | kicad-tools |
|---|---|---|---|
| Claude Opus 5.5 | Claude Code | planned | planned |
| Claude Fable 5.1 | Claude Code | planned | planned |
| GPT-6.1 Sol | Codex CLI | planned | planned |
| GPT-6 Astra | Codex CLI | planned | planned |

- **bare:** the agent with `kicad-cli`, Python and the web ([prompts/tools/bare.md](prompts/tools/bare.md)).
- **kicad-tools:** bare plus the `kct` CLI and MCP server ([prompts/tools/kicad-tools.md](prompts/tools/kicad-tools.md)). The toolkit is identical for every agent, so harness-specific skills are excluded until kicad-tools ships them for every harness (kicad-tools#5951).

Judges: Claude Opus 5.5 (Claude Code), GPT-6 Astra (Codex CLI) and GLM-5.3 (opencode). Each has `kicad-cli` and kicad-tools for inspection.

## Status

**v0, protocol draft.** All of the following exists and has been tested end to end on a scratch clone:

- the input sets and prompts;
- the run scripts (`bench/start`, `bench/finish`);
- the grader (`judging/package`) and its mutation self-test (`judging/selftest`, 8/8 planted defects caught);
- the judge flow (`judging/prepare`, `judging/submit`, `judging/finalize`);
- the results table (`results/render`);
- the reference containers (`container/`, KiCad 10.0.6 pinned);
- an optional container driver for Claude Code (`bench/drive-claude-code`).

No real runs have been scored yet.

## Provenance

The boards come from the demo fleet of [kicad-tools](https://github.com/rjwalters/kicad-tools). Their reference implementations are public in that repo, so runs must not access it (PROTOCOL.md §7). The briefs describe function only, so they don't reveal those implementations.

## License

MIT
