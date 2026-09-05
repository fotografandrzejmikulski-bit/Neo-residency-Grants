# Investment / Application Thesis

## One sentence

Aegis is a durable-state and concurrency layer for long-running multi-agent AI workflows, designed to make execution recoverable, observable, and safe under concurrent mutation.

## Why this problem

The project targets a systems-infrastructure problem: an agent workflow can fail not only because a model produces a bad output, but because execution state is lost, duplicated, overwritten, or becomes inconsistent across workers.

The thesis is therefore narrower than "AI memory": **durable execution and state consistency for agentic workloads**.

## Why now

Agentic software is increasingly asynchronous and persistent. That creates a need for infrastructure primitives that are closer to distributed-systems infrastructure than to a prompt template or chatbot wrapper.

This is a hypothesis to validate through benchmarks and developer interviews, not a statement that the market has already selected Aegis as the winning architecture.

## Why a residency

The immediate objective is not to maximize capital raised. It is to use a concentrated technical environment to:

1. build the smallest credible systems primitive;
2. benchmark it against realistic baselines;
3. put it in the hands of technically sophisticated early users;
4. determine whether the performance/reliability advantage is strong enough to support a company.

Neo publicly positions Residency around technical talent, a small cohort, close mentorship, SF workspace, a two-week Oregon bootcamp, and a Demo Day/VC-introduction phase. citeturn657288search0turn657288search1

## Success condition

The project succeeds during the residency only if the evidence demonstrates a material advantage on a clearly defined workload. The target should be expressed as measured deltas, not adjectives such as "revolutionary" or "unbeatable".

## Non-goals

Aegis v1 should not attempt to become:

- a general-purpose LLM framework;
- a model provider;
- a generic vector database;
- a full enterprise workflow suite;
- a replacement for every existing agent framework.

The wedge is durable state, concurrency semantics, recovery, and observability.
