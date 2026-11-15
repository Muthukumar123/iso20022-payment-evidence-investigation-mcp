# FEI — target solution architecture (not yet deployed)

## Context

**Business user** → **AI Investigation Copilot (untrusted reasoning layer)** → **Governed MCP access layer** → **FEI deterministic evidence and rules services** → **bank-owned read-only adapters** → **payment hub / core banking / archives**.

Data can come from an authorized live read or a maintained evidence store fed by bank-sanctioned events. AI clients **never connect directly to a bank system of record**.

## Architecture decisions

| Layer | Proposed responsibilities | Non-goals |
| --- | --- | --- |
| Portal / Copilot | User authentication, natural-language question, display evidence and uncertainty | Payment authorization |
| AI planner | Tool selection, bounded investigation, evidence summarization | Generate transaction state, override deterministic findings |
| MCP gateway | AuthN/AuthZ, tool allowlists, rate/size limits, trace IDs, audit | Business rules, bank credentials in model context |
| MCP tool surface | \`investigate_payment\`, \`validate_message\`, \`lookup_code\`, etc. | New source of record |
| Deterministic core | ISO 20022 parsing, correlation, scheme/version rules, provenance | Autonomous account-status assertion |
| Read-only bank adapters | Bank-policy enforcement, minimum-data retrieval and normalized envelope | Direct unrestricted LLM access |
| Evidence store (future) | Event timeline, retention, lineage, freshness labels, idempotent replay | Replace authoritative core banking state |
| Event ingestion (future) | Approved integration to IBM MQ / Kafka / Pulsar / MSK / Kinesis | Mandatory MVP dependency |

## Integration patterns

| Banking integration | How | Key controls |
| --- | --- | --- |
| API-enabled core/payment hub | API gateway + bank-owned REST / z/OS Connect adapter | OIDC/mTLS, delegated identity, method and field allowlists, request correlation, timeouts |
| Legacy mainframe / MQ | Bank integration service → MQ request/reply or CDC → normalized evidence | Reply-to/correlation IDs, idempotency, dead-letter handling, RACF/RBAC, no direct agent MQ credentials |
| SOAP / ESB | Private bank-owned adapter translates approved SOAP contract into read-only evidence | XML hardening, schema pinning, least privilege |
| Batch or archive | Controlled ingestion of redacted snapshots with provenance | Checksums, immutable source IDs, retention, staleness checks |
| Streaming | Only if bank events support useful lifecycle reconstruction; broker chosen via ADR | Out-of-order and duplicate handling, per-payment keys, lag alerts, PII policies |

## Suggested read-only future tools

- \`get_payment_evidence(payment_ref)\`: authorized minimum fields and source identifiers.
- \`get_payment_timeline(payment_ref)\`: lifecycle events and last-updated stamps.
- \`get_payment_status(payment_ref)\`: authoritative current status, not inferred state.
- \`get_scheme_rule(message_type, effective_date)\`: versioned, bank-approved rule references.

These are **not** current tools. A real system must authenticate users and enforce policy in adapters independently of model prompts.

## Reliability

- Block by default when permissions fail, source response is absent, or correlation is ambiguous.
- Annotate evidence with system, immutable record ID, timestamp, message/version and freshness.
- Redact and tokenize PII before model exposure; never send payment XML to a presentation API.
- Use bounded retries for safe reads only; no agent-triggered submit/retry/repair operations.
- Preserve separate audit and telemetry streams with masking.

## Further detail

- [Security, risks and guardrails](./SECURITY_AND_GUARDRAILS.md)
- [Happy path and sequence](./diagrams/fei_payment_investigation.mmd)
- [Layered architecture diagram](./diagrams/fei_high_level_architecture.mmd)
- [Pilot backlog](./MVP_ROADMAP.md)
