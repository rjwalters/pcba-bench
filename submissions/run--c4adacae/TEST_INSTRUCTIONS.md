# Test instructions: `run--c4adacae`

**Operator only.** Never show this file to the agent under test or to a judge. It names the condition.

| | |
|---|---|
| Agent / model | claude-code / claude-opus-5-5 |
| Harness | claude-code |
| Toolkit | **kicad-tools** (`prompts/tools/kicad-tools.md`) |
| Time | **60 minutes**, whole suite |
| Operator branch | `test-opus-kct` |
| Judge branch | `judge/run--c4adacae` (created by `bench/finish`; the only branch judges see) |
| Workspace | `~/pcba-bench-runs/run--c4adacae` |

## How this works

1. **Phase A, setup.** You or a setup agent prepare the environment. Ask any agent session to "follow Phase A of this file": it is mechanical and has verification commands.
2. **Phase B, the run.** Start a **fresh** harness session with the exact launch command below. Don't `/clear` the setup session: the isolation flags only take effect at launch, and the transcript has to begin with the test prompt.
3. **Phase C, submit.** Snapshot and commit at the deadline.

## Phase A: setup

```bash
cd ~/GitHub/pcba-bench && git fetch -q && git switch test-opus-kct && git pull -q
mkdir -p ~/pcba-bench-runs/.run--c4adacae
```

### A1. Toolkit: kicad-tools 0.22.0

```bash
uv tool install --force kicad-tools==0.22.0
~/.local/bin/kct build-native
~/.local/bin/kct --version             # must print: kicad-tools 0.22.0
~/.local/bin/kct build-native --check   # must print: C++ backend: available
```

Put `~/.local/bin` **first** on `PATH` for the run. The old Homebrew `kct` 0.12.0 in `/opt/homebrew/bin` must not win.

### A2. Harness: Claude Code, isolated

Only the declared tools may be visible. That means no claude.ai connectors, plugins, user skills, commands, hooks or user CLAUDE.md. The launch flags below enforce it. The MCP config lives outside the workspace:

```bash
cat > ~/pcba-bench-runs/.run--c4adacae/mcp.json <<'JSON'
{"mcpServers": {"kct": {"command": "/Users/rwalters/.local/bin/kct", "args": ["mcp", "serve"]}}}
JSON
```

### A3. Pre-flight checks

```bash
ls ~/pcba-bench-runs/run--c4adacae                       # boards/  deliverables/  PROMPT.md   (nothing else visible)
ls ~/pcba-bench-runs/run--c4adacae/boards | wc -l        # 10
find ~/pcba-bench-runs/run--c4adacae/deliverables -type f | wc -l   # 0
ls ~/.claude/CLAUDE.md ~/.codex/AGENTS.md 2>/dev/null   # global instruction files would leak in: move them aside for the run
```

- Run conditions **one at a time**. A running agent can read the filesystem, including sibling workspaces and this repo's other branches. `bench/finish` scans the transcript for any access to other runs, pcba-bench itself or kicad-tools `boards/`, and such a run is disqualified.
- For the strongest isolation, run under a dedicated macOS user account that holds only the workspace and the harness login.

## Phase B: the run

1. Open a terminal and launch a **fresh** session:

   ```bash
   cd ~/pcba-bench-runs/run--c4adacae && PATH=$HOME/.local/bin:$PATH claude --model claude-opus-5-5 --dangerously-skip-permissions --strict-mcp-config --mcp-config ~/pcba-bench-runs/.run--c4adacae/mcp.json --disable-slash-commands --setting-sources project
   ```

   In the new session, before sending the prompt, type `/mcp`: only `kct` may be listed.

2. Send the contents of `PROMPT.md` as the first message, verbatim, and **in the same moment** start the clock in a second terminal:

   ```bash
   ~/GitHub/pcba-bench/bench/finish run--c4adacae --mark-start
   ```

   It prints the deadline.
3. Until the deadline, the only message you may send is the continue prompt below. Send it whenever the agent stops early, with `{REMAINING}` filled in. Don't answer questions, approve anything, or give hints.

   ```text
   Time remaining: about {REMAINING} minutes (check your timer: `.timer-start`). Keep working on the boards in `boards/`: improve the ones you have started, or deliver more of them, whichever you judge will raise the run's score most. Keep every folder in `deliverables/` valid. Continue until time runs out.
   ```

4. **At the deadline, stop the agent** (Ctrl-C or Esc) and exit the session.

## Phase C: submit

```bash
cd ~/GitHub/pcba-bench && git switch test-opus-kct
T=$(ls -t ~/.claude/projects/*run--c4adacae*/*.jsonl | head -1)
bench/finish run--c4adacae --transcript "$T" --continues <number of continue prompts sent>
git push origin test-opus-kct judge/run--c4adacae
```

`bench/finish` copies `deliverables/` and the transcript, runs the leak scan and commits `Submission run--c4adacae`, and creates `judge/run--c4adacae` at the same commit. Give the judges **only** `judge/run--c4adacae` (JUDGING.md, `prompts/judge-session.md`), never `test-opus-kct`.
