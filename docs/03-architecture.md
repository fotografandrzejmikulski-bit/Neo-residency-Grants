# Aegis Architecture

## Design principle

Aegis is a state layer around agent execution. It does not own the model and does not require a particular agent framework.

```text
Agent / Worker
      |
      v
 Aegis SDK
      |
 +----+-----------------------+
 | Execution API              |
 | Checkpoint / Resume API    |
 | Versioned State API        |
 | Event / Message API        |
 | Idempotency / Lease API    |
 +----+-----------------------+
      |
 +----+----------------------------+
 | Durable event log              |
 | State store                    |
 | Optional retrieval index       |
 +--------------------------------+
```

## MVP primitives

### 1. Versioned state

Every mutable workflow state has a monotonically increasing revision. A mutation may specify the revision it was based on. Aegis rejects writes against stale revisions instead of silently overwriting newer state.

### 2. Checkpoints

A checkpoint stores enough state to resume a workflow from a well-defined point. Checkpoints are immutable records referenced by workflow revision.

### 3. Durable event log

Important transitions become append-only events with timestamps, actor/worker identifiers, workflow identifiers, and schema versions.

### 4. Recovery

A worker can query the last durable checkpoint and replay subsequent events. Recovery must be deterministic for the supported MVP workload.

### 5. Leases

Aegis may issue a short-lived lease for resources that cannot safely tolerate concurrent mutation. Lease ownership is explicit and observable.

### 6. Message passing

Inter-agent messages should be first-class typed records rather than hidden state changes inside prompts.

## Concurrency semantics

The first implementation should prefer simple, defensible semantics over a novel distributed-consensus protocol. Optimistic concurrency control with explicit conflict detection is sufficient for the MVP. Distributed locks should be introduced only where the benchmark demonstrates that optimistic retries are inadequate.

## Storage strategy

The MVP should use one primary durable relational store plus an append-only event table. A vector index can be added for retrieval experiments, but semantic search should not become a dependency of the correctness layer.

## Observability

Every operation must emit enough metadata to answer:

- what changed;
- who/which worker changed it;
- from which revision;
- whether the mutation succeeded or conflicted;
- how long it took;
- which checkpoint/event lineage produced the current state.

## Security baseline

No secrets should enter the event log. Tenant/workflow isolation, authentication, authorization, encryption at rest, and data-retention policy become production requirements before external enterprise deployment.
