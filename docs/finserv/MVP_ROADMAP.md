# FEI execution plan — build only what proves value

## Phase 0 — foundation (this branch)

- Name and scope: **FinServ Evidence Intelligence (FEI)**, initial capability **Payment Exception Intelligence**.
- Define bank-safe architecture, integration boundary, measurable benchmark and real security gaps.
- Prepare an executive Gamma narrative and a **manual, secret-gated** Gamma publishing workflow.
- Reuse existing deterministic ISO 20022 and investigation work (stacked PRs).
- No financial institution data or external service deployment in Phase 0.

## Phase 1 — demonstrable read-only MVP

| Deliverable | Acceptance test |
| --- | --- |
| Two-message synthetic demo | Exact pacs.008 ↔ pacs.002 correlation; evidence shows original message, transaction IDs, status and reason |
| Deterministic validation | Fails safely on malformed XML, unsupported version, invalid IDs, and missing local schema |
| Agent + MCP orchestration demo | MCP `tools/list`, validation, investigation, code lookup produce a complete attributed analyst answer |
| Test-driven guardrails | No invented codes; unknown and mismatch cases clearly marked; malicious remittance never controls tool use |
| Baseline measurement | Same 20–50 curated scenarios run manual/API-only/agent-assisted; report evidence precision and unsafe claims |

## Phase 2 — connected pilot (requires bank approval)

- Select one bank-owned **read-only** payment hub or archive interface.
- Implement identity propagation, ABAC, field minimization, masked immutable audit.
- Add `get_payment_evidence` and `get_payment_timeline` only after authorized adapter exists.
- Explicitly label freshness and contradictory status sources.

## Phase 3 — event intelligence, conditional

- Assess existing IBM MQ, managed Kafka/MSK, Pulsar on AWS, Kinesis against bank standards.
- Implement an **idempotent**, order-aware ingestion adapter and event replay test harness if justified.
- Measure consumer lag, duplicate-event accuracy and correlation precision.

## Pilot decision scorecard

| Metric | Primary success criterion |
| --- | --- |
| Evidence precision | All cited facts trace to authorized source records |
| False cause attribution | Zero in controlled safety cases; report nonzero in broader evaluation |
| Unsafe operational action | Zero write calls; no unauthorized retry recommendation |
| Median time per case | Improve over a measured API-only and manual baseline; do not assert percentage in advance |
| PII exposure | Zero raw sensitive values in model logs or Gamma publishing |
| Operator value | Analysts judge explanations useful and actionable in controlled review |

The pilot **fails** if AI produces attractive prose without verifiable evidence or if MCP adds operational cost without measurable benefit.
