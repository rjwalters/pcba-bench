# Test instructions: `run--b7a732ee`

**Operator only.** Never show this file to the agent under test or to a judge. It names the condition.

| | |
|---|---|
| Agent / model | codex-cli / sol |
| Harness | codex-cli |
| Toolkit | **kicad-tools** (`prompts/tools/kicad-tools.md`) |
| Time | **60 minutes**, whole suite |
| Operator branch | `test-sol-kct` |
| Judge branch | `judge/run--b7a732ee` (created by `bench/finish`; the only branch judges see) |
| Workspace | `~/pcba-bench-runs/run--b7a732ee` |

> **Model ID to confirm:** `sol` is a placeholder. Replace it with the exact model ID in the launch command below and in `submissions/run--b7a732ee/run.json` before starting.

## How this works

1. **Phase A, setup.** You or a setup agent prepare the environment. Ask any agent session to "follow Phase A of this file": it is mechanical and has verification commands.
2. **Phase B, the run.** Start a **fresh** harness session with the exact launch command below. Don't `/clear` the setup session: the isolation flags only take effect at launch, and the transcript has to begin with the test prompt.
3. **Phase C, submit.** Snapshot and commit at the deadline.

## Phase A: setup

```bash
cd ~/GitHub/pcba-bench && git fetch -q && git switch test-sol-kct && git pull -q
mkdir -p ~/pcba-bench-runs/.run--b7a732ee
```

### A1. Toolkit: kicad-tools 0.22.0

```bash
uv tool install --force kicad-tools==0.22.0
~/.local/bin/kct build-native
~/.local/bin/kct --version             # must print: kicad-tools 0.22.0
~/.local/bin/kct build-native --check   # must print: C++ backend: available
```

Put `~/.local/bin` **first** on `PATH` for the run. The old Homebrew `kct` 0.12.0 in `/opt/homebrew/bin` must not win.

### A2. Harness: Codex CLI, isolated

A clean `CODEX_HOME` holds only your login and this run's config. Your other MCP servers (computer-use, node_repl, metta-pr-similarity), skills and AGENTS.md are left out:

```bash
mkdir -p ~/pcba-bench-runs/.run--b7a732ee/codex-home && cp ~/.codex/auth.json ~/pcba-bench-runs/.run--b7a732ee/codex-home/ && chmod 600 ~/pcba-bench-runs/.run--b7a732ee/codex-home/auth.json
cat > ~/pcba-bench-runs/.run--b7a732ee/codex-home/config.toml <<'TOML'
model = "sol"

[mcp_servers.kct]
command = "/Users/rwalters/.local/bin/kct"
args = ["mcp", "serve"]
TOML
CODEX_HOME=~/pcba-bench-runs/.run--b7a732ee/codex-home codex mcp list   # only kct
```

### A3. Pre-flight checks

```bash
ls ~/pcba-bench-runs/run--b7a732ee                       # boards/  deliverables/  PROMPT.md   (nothing else visible)
ls ~/pcba-bench-runs/run--b7a732ee/boards | wc -l        # 10
find ~/pcba-bench-runs/run--b7a732ee/deliverables -type f | wc -l   # 0
ls ~/.claude/CLAUDE.md ~/.codex/AGENTS.md 2>/dev/null   # global instruction files would leak in: move them aside for the run
```

- Run conditions **one at a time**. A running agent can read the filesystem, including sibling workspaces and this repo's other branches. `bench/finish` scans the transcript for any access to other runs, pcba-bench itself or kicad-tools `boards/`, and such a run is disqualified.
- For the strongest isolation, run under a dedicated macOS user account that holds only the workspace and the harness login.

## Phase B: the run

1. Open a terminal and launch a **fresh** session:

   ```bash
   cd ~/pcba-bench-runs/run--b7a732ee && PATH=$HOME/.local/bin:$PATH CODEX_HOME=~/pcba-bench-runs/.run--b7a732ee/codex-home codex -m sol --dangerously-bypass-approvals-and-sandbox
   ```

   In the new session, before sending the prompt, type `/mcp`: only `kct` may be listed.

2. Send the contents of `PROMPT.md` as the first message, verbatim, and **in the same moment** start the clock in a second terminal:

   ```bash
   ~/GitHub/pcba-bench/bench/finish run--b7a732ee --mark-start
   ```

   It prints the deadline.
3. Until the deadline, the only message you may send is the continue prompt below. Send it whenever the agent stops early, with `{REMAINING}` filled in. Don't answer questions, approve anything, or give hints.

   ```text
   Time remaining: about {REMAINING} minutes (check your timer: `.timer-start`). Keep working on the boards in `boards/`: improve the ones you have started, or deliver more of them, whichever you judge will raise the run's score most. Keep every folder in `deliverables/` valid. Continue until time runs out.
   ```

4. **At the deadline, stop the agent** (Ctrl-C or Esc) and exit the session.

## Phase C: submit

```bash
cd ~/GitHub/pcba-bench && git switch test-sol-kct
T=$(ls -t ~/pcba-bench-runs/.run--b7a732ee/codex-home/sessions/*/*/*/*.jsonl | head -1)
bench/finish run--b7a732ee --transcript "$T" --continues <number of continue prompts sent>
git push origin test-sol-kct judge/run--b7a732ee
```

`bench/finish` copies `deliverables/` and the transcript, runs the leak scan and commits `Submission run--b7a732ee`, and creates `judge/run--b7a732ee` at the same commit. Give the judges **only** `judge/run--b7a732ee` (JUDGING.md, `prompts/judge-session.md`), never `test-sol-kct`.
