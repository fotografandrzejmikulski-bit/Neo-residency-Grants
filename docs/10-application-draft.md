# Neo Residency Application — Draft

## Project

**Aegis — durable state and concurrency infrastructure for long-running AI agents**

## What are you building?

I am building a small infrastructure layer that makes long-running multi-agent workflows durable and recoverable.

Today, an agent workflow can fail in a surprisingly non-AI way: a worker crashes, the network drops, two agents mutate the same resource from stale state, or a partially completed workflow becomes impossible to resume reliably. Developers then rebuild persistence, retries, locking, event history, and recovery inside application code.

Aegis turns those concerns into explicit infrastructure primitives: versioned state, durable checkpoints, an append-only event history, conflict detection, idempotency, recovery, and typed messages between workers.

The goal is not to build another agent framework. It is to provide the systems layer underneath agent frameworks.

## Why this problem?

As workflows become longer and more asynchronous, reliability becomes a first-order product constraint. A one-shot response can be retried. A multi-hour or multi-day workflow with side effects cannot be safely treated as a single prompt loop.

I want to test a narrow hypothesis: developers will adopt a dedicated state layer when it gives them a simpler integration model and materially better recovery/concurrency behavior than application-managed state.

I will measure that directly instead of assuming it.

## What will I build during the Residency?

First, a minimal local implementation with a Python SDK. Then I will integrate it into a real three-worker workflow: planner, executor, and verifier.

I will inject process failures and stale concurrent writes deliberately. The first success criterion is not a benchmark score; it is correctness. Aegis must recover the workflow and refuse unsafe stale mutations instead of silently losing state.

After that, I will put the system in the hands of other technical builders, collect failure cases, simplify the API, and benchmark the system against a clearly defined baseline.

## What would convince me this should become a company?

Three things:

1. developers independently integrate the system into real workflows;
2. failure and concurrency behavior is measurably better than the baseline;
3. users continue using it after the initial experiment because removing it makes their workflows materially harder to operate.

If those conditions are not met, I will treat that as useful research rather than force the project into a company prematurely.

## Why Neo?

Neo's Residency is unusually well matched to this experiment. Its 2026 program provides students with a $40K equity-free grant, a dedicated SF workspace, a two-week Oregon bootcamp, weekly mentorship, Demo Day/VC introductions, and $100K+ of Azure, AWS, OpenAI and related infrastructure benefits. citeturn657288search0turn657288search1

More importantly, the program puts technically strong builders in the same environment. For infrastructure software, that is a direct way to turn a hypothesis into adversarial testing, integration feedback, and real technical users.

## What is ambitious here?

I am deliberately choosing a problem below the application layer. If I am right, Aegis could become a reusable primitive for persistent agentic software rather than a single application.

But I do not need to prove that entire future during the Residency. I need to prove one difficult thing clearly: that durable state and concurrency semantics are painful enough, and valuable enough, that developers will choose a dedicated layer for them.
