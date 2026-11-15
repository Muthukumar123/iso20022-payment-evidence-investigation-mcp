# PEI — One-minute executive narrative

**What:** Payment Evidence Intelligence (PEI) is an AI-assisted, evidence-first investigation surface for ISO 20022 payment exceptions.

**Why:** Payment analysts cross-check initiation, bank status, payment-hub records and scheme rules. A single API can validate XML; it does not by itself address open-ended investigations across multiple sources.

**Why AI:** The analyst can ask variable questions; an AI agent chooses the relevant read-only tools and makes the evidence accessible. Deterministic code validates and correlates transaction identifiers; human reviewers approve consequential actions.

**Why MCP:** Standardized tool discovery/invocation across compatible AI clients and governance boundaries. MCP is an interface choice, not a bank system, a payment rail, or a source of truth. Existing REST/SOAP/MQ integrations remain behind controlled adapters.

**What exists now:** Six MCP tools, pacs.008/pacs.002 parsing, business validation, reference code lookup, synthetic tests and exact message correlation with evidence and limitations. Local stdio with user-supplied XML; no live payment hub.

**What comes next:** Bank-approved read-only retrieval adapters, scheme/version rule services, authentication, RBAC, PII redaction, audit logging, adversarial evaluations, controlled user pilot. No automatic resubmission.

**Why invest:** The proof point is reduced analysis effort *with* verified accuracy, traceability and safer escalation. Establish baseline investigation times and expert-labeled cases; evaluate time saved, correct evidence attribution, unsupported claims and analyst acceptance before projecting ROI.

**Risk position:** Read-only does not imply risk-free. Hallucinated conclusions, data leakage, authorization mistakes, stale rules and reliance on incomplete evidence remain material. Humans remain responsible for payment repair and release.

**Decision ask:** Sponsor a controlled prototype-to-pilot path with payment-ops SMEs, an approved anonymized fixture set, a security and governance owner, and a measurable go/no-go scorecard.

*PEI is a working concept name, not a registered or legally vetted brand.*
