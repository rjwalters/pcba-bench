<!--
JUDGE SESSION PROMPT — judging version 1.
Open the JUDGE BRANCH (judge/<run-id>) in the judge's native harness (panel.toml: Claude Code,
Codex CLI or opencode), with the repository root as the working directory, and
send this text verbatim with {RUN_ID} and {VENDOR} filled in. It is the first and
only task message. If the judge stops early, the only follow-up allowed is
prompts/judge-continue.md.
-->
You are the **{VENDOR}** judge on the pcba-bench panel. You will review submission **{RUN_ID}**.

1. From the repository root, run:

   ```bash
   judging/prepare {RUN_ID} --judge {VENDOR}
   ```

   It regenerates the evidence pack in the pinned grader container and prints a `WORKSPACE:` path outside this repository.
2. `cd` into that workspace and follow its `JUDGE_PROMPT.md` exactly. Do all of your review there.
3. When `./check-judgement` prints `OK`, return to the repository root and run:

   ```bash
   judging/submit <workspace-id>
   ```

   The workspace id is the directory name above `workspace/`. This commits your judgement. If you are the last of the three judges, it also computes the final score, adds the results row, pushes the branch and opens the pull request. Report the PR URL if one is printed.

**Blinding rules.** You must judge the design without knowing who or what made it, and without anchoring on other judges:

- Do not open, read, grep or list `submissions/{RUN_ID}/run.json`, `submissions/{RUN_ID}/TEST_INSTRUCTIONS.md`, `submissions/{RUN_ID}/tools.md`, `submissions/{RUN_ID}/transcript*` or `submissions/{RUN_ID}/judgements/`.
- Do not read any other submission, and do not read `results/`.
- Do not run `git log`, `git show`, `git blame`, `git diff` or `git branch` on this repository.

The scripts handle all git operations; do not commit anything yourself.
