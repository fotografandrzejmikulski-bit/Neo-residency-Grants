"""Canonical Aegis demo: planner -> executor with conflict and recovery checks."""

from aegis_state import ConflictError, InMemoryStore


def main() -> None:
    store = InMemoryStore()
    initial = store.create("demo")

    planner = store.begin("demo", initial.revision)
    planner.set("task", "research")
    planner.append_event(
        "state.set",
        {"key": "task", "value": "research"},
        "planner",
    )
    planned = planner.commit()
    store.checkpoint("demo")

    executor_a = store.begin("demo", planned.revision)
    executor_b = store.begin("demo", planned.revision)

    executor_a.set("status", "running")
    executor_a.append_event(
        "state.set",
        {"key": "status", "value": "running"},
        "executor-a",
    )
    committed = executor_a.commit()

    executor_b.set("status", "stale-write")
    try:
        executor_b.commit()
    except ConflictError as exc:
        print(f"CONFLICT DETECTED: {exc}")

    recovered = store.resume("demo")
    print(f"REVISION: {committed.revision}")
    print(f"RECOVERED STATE: {recovered.data}")
    print(f"EVENTS: {len(recovered.events)}")


if __name__ == "__main__":
    main()
