# Benchmark Protocol

## Principle

Aegis should be evaluated as systems infrastructure. Every claimed advantage must have a baseline, workload definition, metric, test configuration, and reproducible result.

## Baselines

At minimum compare against:

1. a direct application-managed state implementation;
2. one mainstream agent orchestration framework used with its normal persistence approach;
3. Aegis with identical model, workload, and infrastructure conditions.

Do not select a baseline after observing results.

## Workloads

### W1 — long-running workflow

A 1,000-step workflow with periodic checkpoints and controlled failure injection.

Metrics: completion rate, recovery time, duplicate-work rate, storage overhead.

### W2 — concurrent mutation

10–100 workers operate on overlapping logical resources with intentionally stale revisions.

Metrics: lost updates, conflict detection rate, successful operations/sec, p95 commit latency, retry count.

### W3 — intermittent infrastructure failures

Terminate workers, inject network failures, delay storage operations, and resume from checkpoints.

Metrics: successful recovery %, time-to-recovery, corrupt-state incidents.

### W4 — agent messaging

Multiple agents exchange typed messages while updating a shared workflow.

Metrics: message durability, duplicate delivery handling, ordering guarantees where promised, end-to-end latency.

## Optional AI-context experiment

A separate experiment may measure whether hierarchical retrieval/checkpoint strategies reduce the amount of model context supplied per successful workflow step.

This experiment must **not** be described as a direct reduction of GPU KV-cache/HBM consumption unless the serving stack and cache behavior are instrumented and the result is demonstrated empirically.

## Reproducibility

Each result should include:

- commit SHA;
- machine/provider;
- CPU/GPU/RAM;
- database version;
- model and serving configuration, if applicable;
- concurrency;
- workload seed;
- number of repetitions;
- confidence interval or distribution summary for latency metrics.

## Results format

Use Markdown tables plus machine-readable JSON under `benchmarks/results/`.

Do not publish synthetic numbers as completed results.
