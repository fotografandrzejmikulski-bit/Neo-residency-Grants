# Current Status and Verification Boundary

## What exists now

Aegis has an executable local reference model implementing:

- workflow creation;
- immutable snapshots at the API boundary;
- monotonic workflow revisions;
- optimistic stale-write rejection;
- ordered event records;
- checkpoint creation;
- checkpoint restore with replay for the explicitly supported `state.set` event;
- explicit transaction lifecycle errors;
- a canonical demo and automated tests.

## What this does not prove

The implementation is not yet a durable distributed service. In particular, it does not yet provide:

- crash-safe persistence across machine restart;
- multi-process transactional guarantees;
- distributed leases;
- production authentication/authorization;
- tenant isolation;
- encrypted storage/key management;
- exactly-once external side-effect execution;
- benchmark evidence of superiority over production baselines.

## Why this boundary is intentional

The project is being developed from the correctness contract upward. The reference implementation makes the core semantics executable before introducing a database, network protocol, or cloud control plane that could hide correctness bugs behind infrastructure complexity.

## Next engineering gates

1. Replace the in-memory store with a transactional durable backend.
2. Add deterministic fault injection across process boundaries.
3. Add idempotency records for external side effects.
4. Define and test lease expiry semantics.
5. Add a machine-readable benchmark runner and result schema.
6. Compare against fixed baselines under identical workloads.
7. Perform security review before any claim of enterprise readiness.

No item above should be described as completed until the repository contains executable evidence for it.
