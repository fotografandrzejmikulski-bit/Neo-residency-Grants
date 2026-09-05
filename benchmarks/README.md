# Aegis Benchmark Harness

This directory defines reproducible benchmark workloads. It contains no fabricated performance results.

## Required result metadata

Each completed run must record:

- repository commit SHA;
- workload identifier and seed;
- machine/runtime configuration;
- database version;
- concurrency level;
- number of repetitions;
- latency distribution summary;
- correctness failures, if any.

Results belong under `benchmarks/results/` as machine-readable JSON plus a human-readable Markdown report.

## Workloads

- `W1`: long-running execution with checkpointing and controlled worker failure.
- `W2`: concurrent mutation with stale revisions.
- `W3`: intermittent process/storage/network failures and recovery.
- `W4`: typed inter-agent messaging with duplicate-delivery tests.

A separate context-efficiency experiment may be added later. It must not be used to claim GPU KV-cache/HBM improvements without instrumentation of the serving stack.
