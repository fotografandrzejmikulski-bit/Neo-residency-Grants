# Neo Residency — Grant Project

## Aegis State Management

**Status:** concept / pre-application architecture

Aegis State Management is proposed as a developer infrastructure layer for long-running, asynchronous multi-agent AI workflows. The project focuses on durable execution state, checkpointing, conflict-aware shared state, and explicit agent-to-agent messaging.

### Core hypothesis

As multi-agent systems become more persistent and concurrent, developers need infrastructure that treats agent state as a durable systems problem rather than as unbounded prompt context.

### MVP scope

1. Durable execution state and checkpoints.
2. Explicit event/message log for agent actions.
3. Optimistic concurrency control for shared resources.
4. Recovery after process/network failure.
5. Developer SDK and observability surface.
6. Reproducible benchmarks comparing baseline orchestration with Aegis.

### What must be demonstrated

The project should not rely on broad claims. The MVP should produce reproducible measurements for:

- recovery success rate;
- state consistency under concurrent writes;
- time-to-recovery;
- token/context reduction where applicable;
- latency and throughput under defined workloads;
- infrastructure cost per completed workflow.

### Architecture direction

Aegis should initially be implemented as a narrow infrastructure primitive, not as another general-purpose agent framework. The first version should minimize dependencies and make the persistence and concurrency semantics explicit.

### Neo Residency fit

Neo's public 2026 Residency materials state that student participants receive a $40K equity-free grant per student, a $10K profit share of Neo fund carry, three months of SF workspace, an all-expenses-paid two-week Oregon bootcamp, mentorship, Demo Day/VC introductions, and $100K+ of Azure/AWS/OpenAI and related infrastructure benefits. citeturn657288search0turn657288search1

Neo also states that student projects that become companies may receive investment on its standard startup terms. citeturn657288search0

### Important source discipline

This repository deliberately distinguishes verified Neo program facts from project hypotheses. Claims about market size, competitors, performance advantages, fundraising outcomes, or technical superiority require independent evidence and benchmark results before being presented as facts.

## Repository roadmap

- `docs/01-thesis.md` — investment/application thesis
- `docs/02-problem.md` — problem definition and evidence
- `docs/03-architecture.md` — technical architecture
- `docs/04-mvp.md` — MVP specification
- `docs/05-benchmarks.md` — benchmark protocol
- `docs/06-roadmap.md` — residency execution plan
- `docs/07-go-to-market.md` — initial developer adoption strategy
- `docs/08-risk-register.md` — technical, product, legal and program risks
- `docs/09-neo-fit.md` — evidence-based Neo alignment
- `docs/10-application-draft.md` — application-ready narrative
- `benchmarks/` — reproducible workload definitions and results
- `src/` — implementation
- `tests/` — correctness and concurrency tests
