"""Score aggregation (RUBRIC.md, JUDGING.md): evidence caps, criterion C, medians.

Shared by judging/score and judging/finalize. Stdlib only.
"""

from __future__ import annotations

import re
import statistics

CRITERIA = ("A", "B", "C", "D", "E", "F")
WEIGHTS = {"A": 25, "B": 25, "C": 20, "D": 15, "E": 10, "F": 5}
VERDICT_VALUE = {"met": 1.0, "partial": 0.5, "unmet": 0.0}


def evidence_caps(gates: dict) -> dict[str, tuple[int, str]]:
    """RUBRIC.md mechanical caps, derived from the evidence pack alone."""
    caps: dict[str, tuple[int, str]] = {}

    def cap(c: str, value: int, why: str) -> None:
        if c not in caps or value < caps[c][0]:
            caps[c] = (value, why)

    if not gates.get("pcb_present"):
        cap("B", 0, "no board.kicad_pcb")
        cap("D", 1, "no board.kicad_pcb")
        cap("E", 1, "no board.kicad_pcb")
    if (gates.get("erc_errors") or 0) > 0 or not gates.get("schematic_present"):
        cap("A", 3, "ERC errors > 0 or no schematic")
    if (gates.get("drc_errors") or 0) > 0:
        cap("B", 2, "DRC errors > 0 (grader fab rules)")
    if (gates.get("unconnected_items") or 0) > 0:
        cap("B", 2, "unrouted connections > 0")
    if gates.get("pcb_present") and not gates.get("lvs_matches"):
        cap("B", 1, "copper vs schematic mismatches > 0")
    return caps


def requirement_c(out: dict, musts: dict[str, bool]) -> float:
    """Criterion C from verdicts: 4 minus 1 per unmet must (partial = 0.5), floored at 0."""
    penalty = sum(1.0 - VERDICT_VALUE[r["verdict"]] for r in out["requirements"] if musts.get(r["id"], True))
    return max(0.0, 4.0 - penalty)


def aggregate(judgements: dict[str, dict], gates: dict, musts: dict[str, bool]) -> dict:
    caps = evidence_caps(gates)
    per_judge: dict[str, dict[str, float]] = {}
    clamps = []
    for vendor, out in judgements.items():
        scores = {c: float(out["criteria"][c]["score"]) for c in CRITERIA}
        scores["C"] = requirement_c(out, musts)
        if out.get("false_claims"):
            if scores["F"] > 0:
                clamps.append({"judge": vendor, "criterion": "F", "from": scores["F"], "to": 0,
                               "why": "judge reported a false claim in DECISIONS.md"})
            scores["F"] = 0.0
        for c, (limit, why) in caps.items():
            if scores[c] > limit:
                clamps.append({"judge": vendor, "criterion": c, "from": scores[c], "to": limit, "why": why})
                scores[c] = float(limit)
        per_judge[vendor] = scores

    medians = {c: statistics.median(s[c] for s in per_judge.values()) for c in CRITERIA}
    spreads = {c: max(s[c] for s in per_judge.values()) - min(s[c] for s in per_judge.values()) for c in CRITERIA}
    total = sum(WEIGHTS[c] * medians[c] / 4 for c in CRITERIA)
    req_ids = sorted({r["id"] for out in judgements.values() for r in out["requirements"]},
                     key=lambda s: int(re.sub(r"\D", "", s) or 0))
    consensus = {}
    for rid in req_ids:
        values = [VERDICT_VALUE[r["verdict"]] for out in judgements.values()
                  for r in out["requirements"] if r["id"] == rid]
        consensus[rid] = {1.0: "met", 0.5: "partial", 0.0: "unmet"}.get(statistics.median(values), "partial")
    return {
        "per_judge": per_judge,
        "evidence_caps": {c: {"max": v, "why": w} for c, (v, w) in caps.items()},
        "clamps": clamps,
        "median": medians,
        "spread": spreads,
        "total": round(total, 1),
        "requirements_consensus": consensus,
        "needs_human_review": sorted(c for c, s in spreads.items() if s >= 2),
    }
