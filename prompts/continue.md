<!--
CONTINUE PROMPT — prompt version 3 (suite run).
This is the ONLY other message a run may send to the agent. Send it verbatim
(with {REMAINING} filled in) when the agent stops before time is up. It may
instead be set as the agent's built-in goal or loop input (for example a
Claude Code Stop hook or /loop, or a Codex goal), with the same text. Nothing
else may be added: no grades, no hints, no error excerpts, no encouragement.
-->
Time remaining: about {REMAINING} minutes (check your timer: `.timer-start`). Keep working on the boards in `boards/`: improve the ones you have started, or deliver more of them, whichever you judge will raise the run's score most. Keep every folder in `deliverables/` valid. Continue until time runs out.
