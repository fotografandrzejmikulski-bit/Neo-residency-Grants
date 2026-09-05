# Submission Checklist

## Applicant

- [x] Author identified as Andrzej Mikulski.
- [x] Contact phone and email recorded in `AUTHOR.md`.
- [ ] Final application form reviewed for exact Neo field limits.
- [ ] Eligibility requirements checked against the applicant's current circumstances.

## Project

- [x] One-sentence project description.
- [x] Precise problem statement.
- [x] Explicit non-goals.
- [x] Executable MVP semantics.
- [x] Correctness criteria.
- [x] Benchmark protocol.
- [x] Risk register.
- [x] Developer adoption wedge.
- [x] Residency-specific execution plan.

## Evidence discipline

- [x] Neo program facts separated from project hypotheses.
- [x] Unsupported market claims flagged.
- [x] Unsupported valuation/acquisition claims excluded from the application narrative.
- [x] KV-cache/HBM claims treated as experimental hypotheses.
- [x] No fabricated performance results.

## Technical evidence

- [x] Minimal Python package metadata.
- [x] Revision-based optimistic concurrency reference implementation.
- [x] Checkpoint and resume primitives.
- [x] Ordered event log.
- [x] Correctness tests.
- [x] GitHub Actions CI.
- [ ] Durable external database adapter.
- [ ] Fault-injection harness with repeated runs.
- [ ] Real benchmark result set with commit SHA and environment metadata.
- [ ] External developer integration evidence.

## Demo readiness

The final demo should show one failure that would be unsafe in an application-managed workflow and the corresponding Aegis behavior. Prefer a live deterministic reproduction over a slide-based claim.

Required demo sequence:

1. Start a workflow.
2. Create a checkpoint.
3. Run two workers from the same revision.
4. Commit one mutation.
5. Attempt the stale mutation.
6. Show the conflict rather than silent overwrite.
7. Terminate/restart a worker.
8. Resume from the last valid checkpoint.
9. Show the durable event lineage.

## Final gate

Do not describe the project as production-ready until the external persistence, security, failure-injection, and independent integration criteria are actually satisfied.
