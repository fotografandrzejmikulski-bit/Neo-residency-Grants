# Go-to-Market Wedge

## Initial customer profile

Target technically sophisticated teams building long-running AI workflows where state loss, concurrency conflicts, or difficult recovery have a material operational cost.

Prioritize:

- AI developer-tool startups;
- internal automation teams;
- research/engineering workflows with long-running jobs;
- multi-worker agent systems that mutate shared artifacts.

## Adoption strategy

Start with an open-source local SDK and a hosted control plane only after the correctness primitive proves useful.

The first growth loop is developer-to-developer:

1. integrate Aegis into a real workflow;
2. capture benchmark and failure evidence;
3. publish a reproducible example;
4. convert technical users into design partners;
5. expand from one workflow to adjacent workloads.

## Positioning

Avoid the vague category "AI memory". The sharper position is:

> Durable execution state and concurrency control for agentic workflows.

## Why open source initially

The product is an infrastructure primitive. Developers need to inspect semantics, run it locally, and trust failure behavior before placing production workflows behind it.

Open-source distribution also creates a direct technical feedback loop without requiring a large sales organization during the residency.

## Commercialization hypothesis

Potential business models:

- hosted Aegis control plane;
- enterprise deployment/support;
- usage-based durable execution;
- managed observability and compliance features.

Do not finalize pricing before real usage data exists.
