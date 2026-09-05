from __future__ import annotations

import argparse

from .core import ConflictError, InMemoryStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the canonical Aegis state demo")
    parser.add_argument("--workflow", default="demo")
    args = parser.parse_args()

    store = InMemoryStore()
    initial = store.create(args.workflow)

    planner = store.begin(args.workflow, initial.revision)
    planner.set("task", "research")
    planner.append_event("state.set", {"key": "task", "value": "research"}, "planner")
    planned = planner.commit()
    store.checkpoint(args.workflow)

    worker_a = store.begin(args.workflow, planned.revision)
    worker_b = store.begin(args.workflow, planned.revision)
    worker_a.set("status", "running")
    worker_a.append_event("state.set", {"key": "status", "value": "running"}, "executor-a")
    committed = worker_a.commit()

    worker_b.set("status", "unsafe-stale-write")
    try:
        worker_b.commit()
    except ConflictError as exc:
        print(f"CONFLICT DETECTED: {exc}")

    recovered = store.resume(args.workflow)
    print(f"REVISION: {committed.revision}")
    print(f"RECOVERED STATE: {recovered.data}")
    print(f"EVENTS: {len(recovered.events)}")


if __name__ == "__main__":
    main()
