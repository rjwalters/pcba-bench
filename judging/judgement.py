#!/usr/bin/env python3
"""Judgement schema and validator, shared by judging/score and the judge workspace.

In a judge workspace (copied there by judging/prepare as ./check-judgement):
    ./check-judgement            # validates boards/<id>/judgement.json for every board in the workspace
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

CRITERIA = ("A", "B", "C", "D", "E", "F")
VERDICTS = ("met", "partial", "unmet")


def output_schema(requirement_ids: list[str]) -> dict:
    criterion = {"type": "object", "additionalProperties": False, "required": ["score", "reason"],
                 "properties": {"score": {"type": "integer", "enum": [0, 1, 2, 3, 4]},
                                "reason": {"type": "string"}}}
    return {
        "type": "object", "additionalProperties": False,
        "required": ["requirements", "criteria", "caps_applied", "false_claims"],
        "properties": {
            "requirements": {"type": "array", "items": {
                "type": "object", "additionalProperties": False, "required": ["id", "verdict", "reason"],
                "properties": {"id": {"type": "string", "enum": requirement_ids},
                               "verdict": {"type": "string", "enum": list(VERDICTS)},
                               "reason": {"type": "string"}}}},
            "criteria": {"type": "object", "additionalProperties": False, "required": list(CRITERIA),
                         "properties": {c: criterion for c in CRITERIA}},
            "caps_applied": {"type": "array", "items": {"type": "string"}},
            "false_claims": {"type": "array", "items": {"type": "string"}},
        },
    }


def validate(out, requirement_ids: list[str]) -> list[str]:
    """Return a list of problems; empty means the judgement is well-formed."""
    if not isinstance(out, dict):
        return ["top level must be a JSON object"]
    problems = []
    for key in ("requirements", "criteria", "caps_applied", "false_claims"):
        if key not in out:
            problems.append(f"missing key {key!r}")
    extra = set(out) - {"requirements", "criteria", "caps_applied", "false_claims"}
    if extra:
        problems.append(f"unexpected keys {sorted(extra)}")
    reqs = out.get("requirements", [])
    ids = [r.get("id") for r in reqs if isinstance(r, dict)]
    if sorted(map(str, ids)) != sorted(requirement_ids):
        missing = sorted(set(requirement_ids) - set(ids))
        dup_or_unknown = sorted({str(i) for i in ids if ids.count(i) > 1 or i not in requirement_ids})
        problems.append(f"requirements must cover each id exactly once (missing {missing}, "
                        f"duplicate/unknown {dup_or_unknown})")
    for r in reqs:
        if not isinstance(r, dict) or r.get("verdict") not in VERDICTS or not str(r.get("reason", "")).strip():
            problems.append(f"requirement entry {r!r} needs verdict in {VERDICTS} and a non-empty reason")
    crit = out.get("criteria", {})
    for c in CRITERIA:
        entry = crit.get(c) if isinstance(crit, dict) else None
        score = entry.get("score") if isinstance(entry, dict) else None
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 4:
            problems.append(f"criteria.{c}.score must be an integer 0-4 (got {score!r})")
        if not isinstance(entry, dict) or not str(entry.get("reason", "")).strip():
            problems.append(f"criteria.{c}.reason must be non-empty")
    for key in ("caps_applied", "false_claims"):
        if key in out and not (isinstance(out[key], list) and all(isinstance(x, str) for x in out[key])):
            problems.append(f"{key} must be a list of strings")
    return problems


def requirement_ids(requirements_toml: Path) -> list[str]:
    return [r["id"] for r in tomllib.loads(requirements_toml.read_text())["requirement"]]


def check_board(board_dir: Path) -> list[str]:
    path = board_dir / "judgement.json"
    if not path.is_file():
        return ["judgement.json not written yet"]
    try:
        out = json.loads(path.read_text())
    except ValueError as exc:
        return [f"not valid JSON: {exc}"]
    return validate(out, requirement_ids(board_dir / "inputs" / "requirements.toml"))


def main() -> int:
    boards = sorted(p for p in (Path.cwd() / "boards").glob("*") if (p / "inputs").is_dir())
    if not boards:
        print("no boards/<id>/inputs found; run this from the judge workspace root")
        return 1
    bad = 0
    for b in boards:
        problems = check_board(b)
        if problems:
            bad += 1
            print(f"INVALID boards/{b.name}/judgement.json:\n" + "\n".join(f"  - {p}" for p in problems))
        else:
            print(f"ok      boards/{b.name}/judgement.json")
    if bad:
        print(f"{bad} of {len(boards)} board judgements need fixing")
        return 1
    print(f"OK: all {len(boards)} board judgements are well-formed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
