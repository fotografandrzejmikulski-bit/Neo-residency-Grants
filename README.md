# Aegis State Management

**Neo Residency — Grant Project**  
**Author:** Andrzej Mikulski

> Durable execution state and concurrency control for long-running agentic workflows.

## Submission status

**Application package prepared for Neo outreach and the next applicable Residency window.**

As of September 5, 2026, Neo's official Residency portal says the 2026 application deadline has passed. For pre-seed or seed funding, Neo directs founders to contact the team and notes a preference for warm introductions. citeturn553091search0turn553091search7

This repository is therefore not presented as a falsely submitable 2026 portal application. It is the complete technical and narrative package to support direct Neo outreach and the next applicable application window.

## Project

Aegis is a narrowly scoped infrastructure layer for AI workflows that need to survive worker failures, coordinate concurrent mutations, preserve execution history, and resume from durable checkpoints.

The repository contains an executable in-memory reference implementation. It is intentionally not presented as a production database or as proof of market fit.

## Core thesis

Long-running agentic workflows create systems problems that are distinct from model quality:

- execution progress can disappear after worker restart;
- retries can duplicate side effects;
- concurrent workers can write from stale state;
- partial failures can make resumption ambiguous;
- debugging can require reconstructing implicit execution history.

Aegis makes these semantics explicit through versioned state, optimistic conflict detection, checkpoints, append-only events, and recovery.

## MVP semantic contract

1. **Versioned state** — every committed workflow state has a revision.
2. **Optimistic concurrency** — stale writes are rejected rather than silently overwriting newer state.
3. **Checkpoints** — recoverable state boundaries are explicit.
4. **Event history** — important transitions can be represented as typed events.
5. **Recovery** — the reference model can restore checkpoints and replay supported state events.
6. **Observable failure** — conflicts and invalid transaction lifecycle are explicit errors.

## Quick start

```bash
python -m pip install -e '.[test]'
pytest -q
PYTHONPATH=src python examples/canonical_workflow.py
```

The canonical demo intentionally creates a stale concurrent write. Expected behavior: a visible conflict instead of silent data loss.

## Evidence boundary

### Demonstrated in the repository

- stale revision detection;
- checkpoint creation and restoration;
- replay of supported `state.set` events;
- ordered event records;
- snapshot isolation;
- transaction lifecycle enforcement;
- a reproducible local demo and benchmark harness;
- automated test execution in GitHub Actions.

### Not yet demonstrated

- production-grade persistence;
- distributed consensus or cross-process locking;
- enterprise security controls;
- performance superiority over selected production baselines;
- product-market fit;
- automatic reduction in GPU KV-cache/HBM usage.

These are explicit future evidence gates, not implied capabilities.

## Neo fit

Neo's official 2026 materials state that students receive a $40K equity-free grant per person and a $10K profit share; student projects that become companies may receive Neo's standard startup investment, currently stated as $750K uncapped with participation rights in the next equity round up to 5% total ownership. Neo also describes SF workspace, an Oregon bootcamp, Demo Day/VC introductions, mentorship, and $100K+ in Azure/AWS/OpenAI and related benefits for students. citeturn553091search0turn553091search1

The application narrative uses these as current program facts and treats all Aegis performance, market, customer, and financing outcomes as hypotheses until independently demonstrated.

## Repository package

- `AUTHOR.md` — applicant/contact profile
- `docs/10-application-draft.md` — application narrative
- `docs/13-demo-script.md` — technical demo narrative
- `docs/14-verification-sources.md` — Neo source verification and current status
- `docs/12-claims-audit.md` — claim integrity controls
- `docs/03-architecture.md` — technical design
- `docs/04-mvp.md` — MVP contract
- `docs/05-benchmarks.md` + `benchmarks/` — evaluation protocol
- `src/aegis_state/` — executable reference implementation
- `tests/` — correctness tests
- `.github/workflows/ci.yml` — automated verification

## Author

**Andrzej Mikulski**  
Email: mojealterego21@gmail.com  
Phone: +48 455 575 337

## Intellectual honesty rule

No fabricated benchmark results. No fabricated customers. No invented mentors. No unsupported investment outcome. Every external claim must be backed by a current primary source or clearly marked as a hypothesis or assumption.
