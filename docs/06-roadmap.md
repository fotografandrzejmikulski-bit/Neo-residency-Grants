# 12-Week Execution Roadmap

Neo's published 2026 schedule states: June 2 program kickoff, July 12–26 Oregon bootcamp, and September 30–October 4 Demo Day and Reunion. citeturn657288search0turn657288search1

The roadmap below is intentionally milestone-driven.

## Weeks 1–2 — Systems prototype

Deliver:

- workflow state model;
- revisioned writes;
- checkpoint API;
- event log;
- local CLI;
- first fault-injection tests.

Decision gate: prove that state survives controlled worker termination.

## Weeks 3–4 — Concurrency

Deliver:

- conflict detection;
- idempotency keys;
- leases where justified;
- concurrent-worker benchmark;
- observability schema.

Decision gate: demonstrate that stale concurrent writes are detected rather than silently lost.

## Weeks 5–6 — First external users

Recruit technically sophisticated early users. Instrument onboarding and identify the smallest workflow where Aegis provides an obvious advantage.

Decision gate: at least three independent users can complete the canonical demo.

## Weeks 7–8 — Oregon alpha

Use the concentrated residency environment to run the benchmark suite, collect failure cases, simplify the API, and test whether the product solves a repeated problem for other builders.

Neo states that the Oregon bootcamp runs July 12–26 and that travel, housing, and meals are covered. citeturn657288search0

Decision gate: evidence of repeat usage and a measurable systems advantage on a defined workload.

## Weeks 9–10 — Hardening

Focus on:

- recovery correctness;
- storage and compute cost;
- security review;
- SDK ergonomics;
- documentation;
- operational dashboards.

Decision gate: no known correctness-critical failure in the tested workload.

## Weeks 11–12 — Demo and company decision

Prepare:

- benchmark report;
- five-minute technical demo;
- architecture diagram;
- product narrative;
- adoption evidence;
- company economics;
- explicit list of unresolved technical risks.

Neo's published schedule places Demo Day and Reunion on September 30–October 4. citeturn657288search0

## Post-residency trigger

Only incorporate and pursue venture financing if evidence indicates a durable product wedge. The research document's proposed Delaware C-Corp timeline should be treated as a planning assumption, not a Neo requirement.
