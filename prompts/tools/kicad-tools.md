## Tools available to you

Everything in the bare track, plus:

- **kicad-tools (`kct`) 0.22.0**: an agent-oriented toolkit that reads and writes KiCad files directly. It covers:
  - schematic and PCB generation;
  - placement and autorouting (`kct route`);
  - zone fill;
  - DRC and manufacturer checks (`kct check --mfr jlcpcb`);
  - schematic↔PCB consistency checks;
  - BOM and part lookup;
  - fab export (`kct export`).

  It is already installed in this environment. Run `kct --help` and `kct <cmd> --help`; most commands support `--format json`. Run `kct build-native --check` to confirm the fast router backend is present.
- **kct MCP server** (`kct mcp`): the same capabilities as MCP tools, if your agent supports MCP.
- **`/kct:*` Claude Code skills** in `.claude/commands/kct/`. Run `/kct:help` to list them.
