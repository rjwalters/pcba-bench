<!--
CONTINUE PROMPT — prompt version 1.
This is the ONLY other message a run may send to the agent. Send it verbatim
(with {REMAINING} filled in) when the agent stops before time is up. It may
instead be set as the agent's built-in goal or loop input (for example a
Claude Code Stop hook or /loop, or a Codex goal), with the same text. Nothing
else may be added: no grades, no hints, no error excerpts, no encouragement.
-->
Time remaining: about {REMAINING} minutes. Keep working on the board described in `BRIEF.md`, aiming for a deliverable that meets every requirement in `requirements.toml`. Check your own work, fix what is wrong or missing, and keep `./deliverable/` valid. Keep going until every requirement is met or time runs out.
