"""Small reproducible benchmark for the in-memory reference model.

This benchmark reports measured local timings only; it makes no claim about
production infrastructure performance.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from aegis_state import ConflictError, InMemoryStore  # noqa: E402


def run(iterations: int) -> dict[str, object]:
    latencies_ms: list[float] = []
    conflicts = 0

    for index in range(iterations):
        store = InMemoryStore()
        initial = store.create(f"bench-{index}")
        tx_a = store.begin(initial.workflow_id, initial.revision)
        tx_b = store.begin(initial.workflow_id, initial.revision)
        tx_a.set("status", "ok")
        started = time.perf_counter()
        tx_a.commit()
        latencies_ms.append((time.perf_counter() - started) * 1000.0)
        tx_b.set("status", "stale")
        try:
            tx_b.commit()
        except ConflictError:
            conflicts += 1

    latencies_ms.sort()
    p95_index = max(0, min(len(latencies_ms) - 1, int(round(0.95 * (len(latencies_ms) - 1)))))
    return {
        "workload": "reference-w1-w2-mixed",
        "iterations": iterations,
        "conflicts_detected": conflicts,
        "conflict_detection_rate": conflicts / iterations,
        "commit_latency_ms": {
            "p50": statistics.median(latencies_ms),
            "p95": latencies_ms[p95_index],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.iterations <= 0:
        raise SystemExit("--iterations must be positive")

    result = run(args.iterations)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
