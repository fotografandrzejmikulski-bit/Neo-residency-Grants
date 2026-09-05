# Aegis — Durable State for Long-Running Agentic Workflows

**Neo Residency application project · Andrzej Mikulski**

[![CI](https://github.com/fotografandrzejmikulski-bit/Neo-residency-Grants/actions/workflows/ci.yml/badge.svg)](https://github.com/fotografandrzejmikulski-bit/Neo-residency-Grants/actions/workflows/ci.yml)

## Status

**Pre-application / executable reference core.**

Aegis is a proposed infrastructure layer for long-running, asynchronous multi-agent AI workflows. The current repository contains an executable reference implementation of the core correctness semantics, tests, CI, and the evidence-grounded application/design documentation.

The project is intentionally not presented as production-ready and contains no fabricated benchmark results.

## The wedge

> **Durable execution state and concurrency control for agentic workflows.**

Aegis treats persistent agent state as a distributed-systems problem rather than as an implicit prompt history.

The first primitives are:

- versioned state;
- optimistic concurrency control;
- immutable checkpoints;
- ordered event history;
- recovery/resume semantics;
- typed workflow messages as a future protocol layer;
- observability suitable for reconstructing execution lineage.

## Why this problem

Long-running workflows can fail even when the underlying model behaves correctly: a worker can crash, a network operation can be interrupted, two workers can act on stale state, or a partially completed workflow can become difficult to resume safely.

The core research question is narrow:

> Will technically sophisticated developers adopt a dedicated state layer when it materially improves correctness/recovery while simplifying application code?

That is an empirical hypothesis. The repository defines how to test it rather than assuming the answer.

## Current executable core

The package under `src/aegis_state/` provides an in-memory reference implementation for:

```python
from aegis_state import ConflictError, InMemoryStore

store = InMemoryStore()
state = store.create("research-job")

worker_a = store.begin("research-job", state.revision)
worker_b = store.begin("research-job", state.revision)

worker_a.set("status", "running")
worker_a.append_event("worker.started", {"worker": "planner"}, "planner")
worker_a.commit()

worker_b.set("status", "stale-write")
try:
    worker_b.commit()
except ConflictError:
    pass  # stale mutation is rejected instead of silently overwriting state
```

This implementation is deliberately small. It exists to make the semantic contract executable before introducing a durable database, distributed leases, cloud infrastructure, or model-serving instrumentation.

## Repository structure

```text
.
├── AUTHOR.md
├── LICENSE
├── README.md
├── pyproject.toml
├── src/
│   └── aegis_state/
│       ├── __init__.py
│       └── core.py
├── tests/
│   └── test_core.py
├── .github/workflows/ci.yml
└── docs/
    ├── 01-thesis.md
    ├── 02-problem.md
    ├── 03-architecture.md
    ├── 04-mvp.md
    ├── 05-benchmarks.md
    ├── 06-roadmap.md
    ├── 07-go-to-market.md
    ├── 08-risk-register.md
    ├── 09-neo-fit.md
    ├── 10-application-draft.md
    ├── 11-budget.md
    ├── 12-claims-audit.md
    ├── 13-demo-script.md
    ├── 14-verification-sources.md
    └── 15-submission-checklist.md
```

## Validation model

Every material claim should be one of four things:

1. a current primary-source fact;
2. a measured project result;
3. an explicitly labeled hypothesis;
4. an explicitly labeled planning assumption.

The claims audit records where the original research draft was too categorical and prevents those statements from silently becoming application facts. See `docs/12-claims-audit.md`.

## Benchmark plan

Aegis will be compared against a clearly defined application-managed baseline and at least one mainstream persistence/orchestration approach under identical workloads.

The first benchmark family covers:

- long-running execution with controlled failure;
- concurrent stale writes;
- process/network failure and recovery;
- durable inter-worker messaging.

The repository does **not** publish synthetic performance numbers as completed results. Reproducible results must include the commit SHA, environment, workload seed, repetitions, and latency/distribution summary.

## Neo Residency fit

Neo's public 2026 Residency materials are recorded in the repository's verification documents. The application narrative uses those sources rather than unsupported assumptions about the program, mentors, acceptance rates, or investment outcomes.

The project is designed around the value of a concentrated technical environment: build a narrow systems primitive, expose it to strong technical peers, run adversarial tests, measure the result, and make an evidence-based company decision.

## Author

**Andrzej Mikulski**  
Tel. +48 455 575 337  
Email: mojealterego21@gmail.com

See `AUTHOR.md` for application/contact metadata.

## License

MIT. See `LICENSE`.
