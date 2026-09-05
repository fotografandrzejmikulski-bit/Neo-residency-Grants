# Demo Day Technical Demo

## Opening — 20 seconds

"Most agent failures are not model failures. They are state failures: a worker dies, two agents write from stale state, or a long workflow cannot resume safely. Aegis makes execution state durable and concurrency explicit."

## Demo 1 — Normal execution

Run planner → executor → verifier against one workflow.

Show:

- current workflow revision;
- checkpoint count;
- event history;
- active workers.

## Demo 2 — Crash and recovery

Terminate the executor after a completed checkpoint and before the next stage.

Resume the workflow.

Show that:

- the latest durable checkpoint is recovered;
- previously committed work is not silently duplicated;
- the workflow continues from a known revision.

## Demo 3 — Concurrent stale write

Start two workers from the same revision.

Worker A commits first. Worker B attempts to commit the stale revision.

Show a deterministic conflict response containing the expected/current revision information.

## Demo 4 — Evidence

Display the benchmark dashboard with:

- recovery success rate;
- silent-lost-update rate;
- conflict detection rate;
- p50/p95 commit latency;
- recovery time;
- integration time for a clean project.

Do not display fabricated values. Show actual run IDs and commit SHAs.

## Closing — 20 seconds

"The product question is now simple: do developers building persistent agent systems prefer a dedicated state primitive over rebuilding persistence and recovery inside every application? During the Residency, I want to answer that with code, benchmarks, and real users."
