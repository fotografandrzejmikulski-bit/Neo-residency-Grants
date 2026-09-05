# MVP Specification

## Objective

Build a usable infrastructure primitive that a developer can integrate into a small multi-agent workflow in less than one day.

## MVP API

```python
workflow = aegis.create_workflow("research-job")

state = workflow.load_state()
checkpoint = workflow.checkpoint(state)

with workflow.transaction(base_revision=state.revision) as tx:
    tx.set("status", "running")
    tx.append_event("worker.started", {"worker": "planner"})
    tx.commit()

workflow.send_message(
    sender="planner",
    recipient="executor",
    type="task.created",
    payload={"task_id": "t-123"},
)

workflow.resume()
```

The exact API may change. The semantic contract is the important part.

## MVP acceptance criteria

### Correctness

- No successful mutation may silently overwrite a newer committed revision.
- A workflow can resume from the latest valid checkpoint after process termination.
- Replaying the supported event sequence reconstructs the expected state.
- Duplicate delivery of an idempotent event does not create duplicate side effects.

### Performance

Targets must be established through measurement rather than assumed in advance. Record:

- p50/p95 state-read latency;
- p50/p95 state-write latency;
- checkpoint duration;
- recovery time;
- event-ingestion throughput;
- conflict/retry rate under concurrency.

### Developer experience

- one-command local setup;
- Python SDK first;
- clear TypeScript-compatible protocol documentation;
- example integration for one existing agent workflow;
- local test mode without cloud dependencies.

## Demo workload

The canonical demo should involve three workers:

1. planner writes a task graph;
2. executor performs tasks and reports results;
3. verifier validates outputs.

The demo deliberately injects process crashes and concurrent stale writes. Aegis must recover the workflow and surface conflicts rather than silently losing state.

## Exit criteria

The MVP is ready for external alpha when all correctness tests pass, failure recovery is reproducible, and at least three independent developers can integrate it without direct intervention from the author.
