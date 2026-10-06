"""Shared helpers for the git-native submit -> judge -> finalize flow (JUDGING.md)."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
BASE_IMAGE = "pcba-bench/base"
JUDGE_RUNS = Path(os.environ.get("PCBA_BENCH_JUDGE_RUNS", Path.home() / "pcba-bench-judging"))


def strip_comment(text: str) -> str:
    return re.sub(r"<!--.*?-->\s*", "", text, count=1, flags=re.S)


def panel() -> dict:
    return tomllib.loads((HERE / "panel.toml").read_text())


def judge_entry(vendor: str) -> dict:
    j = next((j for j in panel()["judge"] if j["vendor"] == vendor), None)
    if j is None:
        sys.exit(f"no judge {vendor!r} in judging/panel.toml")
    return j


def submission_dir(run_id: str) -> Path:
    d = REPO / "submissions" / run_id
    if not (d / "deliverables").is_dir() or not (d / "run.json").is_file():
        sys.exit(f"{d} is not a submission (no deliverables/ or run.json); is the run branch checked out?")
    return d


def attempted(run_id: str) -> list[str]:
    return json.loads((submission_dir(run_id) / "run.json").read_text()).get("attempted", [])


def git(*args: str, check: bool = True) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=check, capture_output=True, text=True).stdout.strip()


def commit(paths: list[Path], message: str) -> None:
    """Neutral, script-authored commit: no agent or tool trailers (blinding)."""
    git("add", "--", *[str(p.relative_to(REPO)) for p in paths])
    if subprocess.run(["git", "-C", str(REPO), "diff", "--cached", "--quiet"]).returncode == 0:
        print("nothing to commit")
        return
    git("commit", "-m", message)


def run_grader(run_id: str, out_root: Path, local: bool = False) -> dict[str, Path]:
    """Build an evidence pack per attempted board, in the pinned grader container.

    Falls back to the host's kicad-cli only with --local (the summary notes record the
    version). Returns {board: <out_root>/<board>/}.
    """
    out_root.mkdir(parents=True, exist_ok=True)
    sub = submission_dir(run_id)
    boards = attempted(run_id)
    if not boards:
        return {}
    have_image = (not local and shutil.which("docker") and subprocess.run(
        ["docker", "image", "inspect", BASE_IMAGE], capture_output=True).returncode == 0)
    if have_image:
        loop = " && ".join(f"package /sub/deliverables/{b} --board {b} -o /out" for b in boards)
        cmd = ["docker", "run", "--rm", "--platform", "linux/amd64",
               "-v", f"{sub}:/sub:ro", "-v", f"{out_root}:/out", BASE_IMAGE, "bash", "-c", loop]
        p = subprocess.run(cmd, capture_output=True, text=True)
        failed = p.returncode != 0
    elif local:
        failed, p = False, None
        for b in boards:
            p = subprocess.run([sys.executable, str(HERE / "package"), str(sub / "deliverables" / b),
                                "--board", b, "-o", str(out_root)], capture_output=True, text=True)
            failed |= p.returncode != 0
    else:
        sys.exit(f"grader image {BASE_IMAGE} not found; build it (container/README.md) or pass --local")
    bundles = {b: out_root / b for b in boards}
    missing = [b for b, d in bundles.items() if not (d / "evidence" / "summary.json").is_file()]
    if failed or missing:
        tail = (p.stdout[-2000:] + "\n" + p.stderr[-2000:]) if p else ""
        sys.exit(f"grader failed for {missing or boards}:\n{tail}")
    return bundles


def load_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.is_file() else {}
