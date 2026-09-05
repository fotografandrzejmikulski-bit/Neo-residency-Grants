# Aegis State Management

**Neo Residency 2026 — Grant Project**  
**Author:** Andrzej Mikulski

> Durable execution state and concurrency control for long-running agentic workflows.

## Status

**Pre-application prototype / executable systems reference model.**

Aegis is a narrowly scoped infrastructure layer for AI workflows that need to survive worker failures, coordinate concurrent mutations, preserve execution history, and resume from durable checkpoints.

The current repository contains an executable in-memory reference implementation. It is intentionally not presented as a production database or as proof of market fit.

## Why this exists

Long-running agent workflows introduce systems problems that are distinct from model quality:

- progress can disappear after a worker restart;
- retries can duplicate side effects;
- concurrent workers can write from stale state;
- partial failures can make resumption ambiguous;
- debugging can require reconstructing implicit execution history.

Aegis makes these semantics explicit through versioned state, conflict detection, checkpoints, an append-only event history, and a recovery model.

## MVP semantic contract

1. **Versioned state** — every committed workflow state has a revision.
2. **Optimistic concurrency** — writes based on stale revisions are rejected rather than silently overwriting newer state.
3. **Durable-model checkpoints** — checkpoints capture a recoverable state boundary.
4. **Event history** — important transitions can be represented as typed events.
5. **Recovery** — the reference model can restore a checkpoint and replay supported state events.
6. **Observable failure** — conflicts and invalid transaction lifecycle are explicit errors.

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
├── examples/
│   └── canonical_workflow.py
├── benchmarks/
│   └── README.md
├── docs/
│   ├── 01-thesis.md
│   ├── 02-problem.md
│   ├── 03-architecture.md
│   ├── 04-mvp.md
│   ├── 05-benchmarks.md
│   ├── 06-roadmap.md
│   ├── 07-go-to-market.md
│   ├── 08-risk-register.md
│   ├── 09-neo-fit.md
│   ├── 10-application-draft.md
│   ├── 11-budget.md
│   ├── 12-claims-audit.md
│   ├── 13-demo-script.md
│   └── 14-verification-sources.md
└── .github/workflows/ci.yml
```

## Quick start

```bash
python -m pip install -e '.[test]'
pytest -q
PYTHONPATH=src python examples/canonical_workflow.py
```

The canonical demo intentionally creates a stale concurrent write. The expected behavior is a visible conflict rather than silent data loss.

## What is proven vs. what is not

### Demonstrated in the repository

- stale revision detection;
- checkpoint creation and restoration;
- replay of supported `state.set` events;
- ordered event records;
- snapshot isolation;
- transaction lifecycle enforcement.

### Not yet demonstrated

- production-grade persistence;
- distributed consensus or cross-process locking;
- enterprise security controls;
- performance superiority over selected production baselines;
- product-market fit;
- any automatic reduction in GPU KV-cache/HBM usage.

Those claims require controlled experiments and external evidence. The benchmark protocol defines how to collect it.

## Neo Residency fit

Neo's public 2026 Residency materials state that students receive an equity-free grant, profit share, workspace, the Oregon bootcamp, mentorship, Demo Day/VC introductions, and infrastructure benefits. The repository keeps program facts separate from project hypotheses and requires re-verification before final submission.

See `docs/09-neo-fit.md`, `docs/12-claims-audit.md`, and `docs/14-verification-sources.md`.

## Author

**Andrzej Mikulski**  
Phone: +48 455 575 337  
Email: mojealterego21@gmail.com

## Intellectual honesty rule

No fabricated benchmark results. No fabricated customers. No invented mentors. No unsupported investment outcome. Every external claim must be backed by a current primary source or clearly marked as a hypothesis/assumption.
