# Neo Residency / Direct Outreach Application — Final Draft

## Applicant

**Andrzej Mikulski**  
Phone: +48 455 575 337  
Email: mojealterego21@gmail.com

## Project

**Aegis — durable state and concurrency infrastructure for long-running agentic workflows**

## One-sentence description

Aegis is a systems layer that makes long-running multi-agent workflows durable, recoverable, concurrency-safe, and inspectable.

## What are you building?

I am building the state layer underneath long-running AI workflows.

A multi-agent system can fail without the underlying model being wrong: a worker can crash, a network call can be repeated, two agents can mutate the same resource from stale state, or a partially completed workflow can become difficult to resume safely. Today, developers often assemble persistence, retries, versioning, event history, conflict handling, and recovery themselves inside application code.

Aegis turns those concerns into explicit infrastructure primitives:

- versioned workflow state;
- optimistic concurrency control;
- immutable checkpoints;
- append-only event history;
- idempotency and recovery semantics;
- typed inter-agent messages;
- operational observability.

The goal is **not** another agent framework, agent marketplace, or chatbot wrapper. The goal is a reusable systems primitive that existing agent applications can call into.

## The problem I want to prove

My hypothesis is narrow:

> Developers building persistent, asynchronous agentic workflows will adopt a dedicated state layer when it materially improves correctness and recovery while remaining simpler to integrate than rebuilding those semantics in application code.

I am deliberately treating that as a hypothesis, not as an established market fact.

## What exists today

This repository contains an executable in-memory reference implementation of the core semantics:

- revisioned state;
- rejection of stale writes;
- checkpoint creation;
- checkpoint restoration;
- replay of supported state events;
- ordered event records;
- transaction lifecycle enforcement.

The canonical example demonstrates a stale concurrent write being rejected rather than silently overwriting newer state.

The repository does **not** claim production-grade persistence, market validation, enterprise security, or performance superiority before those things are measured.

## What I will build next

The next implementation phase moves the reference semantics into a durable backend while preserving the same correctness contract.

The development sequence is:

1. durable transactional storage;
2. process and network fault injection;
3. concurrent worker tests;
4. idempotent side-effect boundaries;
5. recovery and replay verification;
6. a minimal Python SDK;
7. a canonical planner → executor → verifier workload;
8. reproducible baseline comparisons;
9. documentation and developer onboarding;
10. design-partner testing.

## How I will measure success

I will not define success using adjectives such as "revolutionary" or "unbeatable". I will use measurable criteria.

### Correctness

- zero silent lost updates in the supported concurrency tests;
- reproducible recovery after controlled worker termination;
- deterministic reconstruction of supported state from checkpoints and events;
- correct handling of duplicate idempotent deliveries.

### Systems performance

For each workload I will record:

- p50/p95 state-read latency;
- p50/p95 state-write/commit latency;
- checkpoint duration;
- event-ingestion throughput;
- recovery time;
- conflict rate and retry rate;
- end-to-end cost per completed workflow.

### Developer adoption

The strongest validation would be independent developers integrating Aegis into real workflows without direct implementation help, then continuing to use it because removing it makes those workflows materially harder to operate.

## Canonical demo

The demo uses three workers:

**Planner → Executor → Verifier**

The demonstration intentionally injects:

- a worker/process failure;
- a stale concurrent write;
- a recovery operation from a durable checkpoint.

The expected result is deterministic: committed work remains visible, stale mutation is rejected, and the workflow resumes from a known state boundary.

## Why Neo

Neo's public Residency materials describe a small technical cohort, three months working from the Neo San Francisco workspace, an all-expenses-paid Oregon bootcamp, mentorship, Demo Day/VC introductions, and infrastructure benefits. For students, Neo states a $40K equity-free grant per person, a $10K profit share of Neo fund carry, and $100K+ of Azure, AWS, OpenAI and related benefits. Neo also states that if a student project becomes a company, it would want to invest on its standard startup terms. citeturn646406search0turn646406search1

The fit is practical rather than promotional. A systems-infrastructure project benefits from a dense technical community where sophisticated builders can attack the design, test the prototype, and expose failure modes quickly.

## Why me

I am deliberately choosing a technically difficult problem that can be reduced to a small, falsifiable systems primitive.

I would rather spend the program proving one important systems claim with code and adversarial tests than presenting a broad product vision without evidence.

The project is designed so that the residency itself becomes part of the experiment: build quickly, let strong technical users break it, instrument everything, simplify the interface, and decide from evidence whether the primitive deserves to become a company.

## What would convince me to form a company?

Three conditions:

1. independent technical users integrate Aegis into real workflows;
2. the system demonstrates a measurable correctness/recovery advantage over reasonable application-managed baselines;
3. the value survives beyond a one-time demo because users continue to depend on the primitive.

If those conditions are not met, I will treat the result as useful technical research rather than force a startup around it.

## Long-term ambition

If the hypothesis is correct, Aegis can evolve from a local correctness primitive into infrastructure for persistent agentic software: a durable execution substrate where state, concurrency, recovery, and operational history are explicit rather than hidden inside prompts and application-specific glue code.

The long-term opportunity is intentionally not part of the proof burden for the first milestone. The first milestone is simpler: **make long-running agent execution reliably recoverable and concurrency-safe, then prove that developers care.**

## Contact

**Andrzej Mikulski**  
+48 455 575 337  
mojealterego21@gmail.com
