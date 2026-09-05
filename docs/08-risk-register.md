# Risk Register

| Risk | Severity | Mitigation | Evidence required |
|---|---:|---|---|
| Problem is not painful enough | High | Technical-user interviews and design partners | Repeated user demand |
| Architecture adds more complexity than value | High | Narrow MVP and comparative integration test | Setup time + workload results |
| Conflict semantics are incorrect | Critical | Deterministic revision checks and fault injection | Zero silent lost updates in test suite |
| Recovery is incomplete | Critical | Kill/restart tests and event replay | Recovery success rate |
| Claims about KV cache/HBM are overstated | High | Separate storage-state thesis from model-serving benchmark | Instrumented serving experiment |
| Retrieval quality is insufficient | Medium | Keep retrieval optional in correctness layer | Recall/NDCG-type benchmark where relevant |
| Security/privacy failure | Critical | Threat model, secret filtering, tenant isolation | External review before enterprise use |
| Cloud dependency becomes excessive | Medium | Local-first MVP and portable storage interface | Offline/local test mode |
| Developer adoption is weak | High | Open-source SDK, concrete examples, direct onboarding | Activated weekly users |
| Competition closes the gap | Medium | Focus on durable correctness and measurable reliability | Comparative benchmark updates |
| Company formation happens too early | Medium | Evidence-based incorporation gate | Product usage + investor readiness |
| Program facts become outdated | Medium | Keep Neo facts in dedicated evidence file and re-verify before submission | Current official Neo source |
