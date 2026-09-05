from aegis_state import ConflictError, InMemoryStore


def test_revisioned_write_rejects_stale_state():
    store = InMemoryStore()
    first = store.create("w1")

    tx1 = store.begin("w1", first.revision)
    tx2 = store.begin("w1", first.revision)

    tx1.set("status", "running")
    committed = tx1.commit()

    assert committed.revision == 1
    assert committed.data["status"] == "running"

    tx2.set("status", "incorrect-overwrite")
    try:
        tx2.commit()
    except ConflictError:
        pass
    else:
        raise AssertionError("stale write must be rejected")

    final = store.snapshot("w1")
    assert final.data["status"] == "running"
    assert final.revision == 1


def test_checkpoint_and_resume_restore_state():
    store = InMemoryStore()
    store.create("w2")

    tx = store.begin("w2")
    tx.set("step", 7)
    tx.commit()
    revision = store.checkpoint("w2")

    tx = store.begin("w2")
    tx.set("step", 8)
    tx.commit()

    restored = store.resume("w2", revision)
    assert restored.revision == revision
    assert restored.data == {"step": 7}


def test_events_are_ordered_and_snapshot_isolated():
    store = InMemoryStore()
    first = store.create("w3")
    tx = store.begin("w3", first.revision)
    tx.append_event("worker.started", {"worker": "planner"}, "planner")
    tx.append_event("task.created", {"task_id": "t-1"}, "planner")
    result = tx.commit()

    assert [event.sequence for event in result.events] == [1, 2]
    assert [event.event_type for event in result.events] == ["worker.started", "task.created"]

    result.data["mutated"] = True
    latest = store.snapshot("w3")
    assert "mutated" not in latest.data
