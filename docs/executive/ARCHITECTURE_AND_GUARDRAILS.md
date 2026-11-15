# Payment Evidence Intelligence (PEI): Executive Architecture and Guardrails

> Status: Executive target architecture and **read-only local proof of concept**. Do not interpret target security controls or bank connectivity as implemented.

## Executive premise

PEI is an **evidence-first, AI-assisted ISO 20022 payment exception investigation capability**. It uses a compatible AI agent to understand variable questions, the Model Context Protocol (MCP) to discover and invoke approved tools, and deterministic financial services for message parsing, validation and exact pacs.008/pacs.002 correlation. It does **not** authorize, change, resend or settle payments.

**Why AI?** Analysts ask varied questions crossing messages, statuses, business rules and history. An AI assistant can adapt investigation flow and explain evidence; it must never manufacture payment facts.

**Why MCP rather than simply REST?** A single REST endpoint remains appropriate for known fixed workflows. MCP standardizes tool discovery and invocation across compatible AI clients. Business rules belong in one reusable service underneath both REST and MCP.

**What differentiates PEI?** Cross-message exact correlation, provenance fields, explicit unknowns, guarded recommendations, and eventually authorized evidence from multiple banking systems—not XML parsing or Glama listing alone.

## High-level architecture

\`\`\`mermaid
flowchart TB
    subgraph CH["User & application channels"]
      APP["Banking application / REST client (target)"]
      AI["Payment Ops AI Copilot / MCP client"]
    end
    subgraph GOV["Governed access (target)"]
      IAM["Bank identity / OAuth-OIDC / mTLS"]
      GW["MCP/API gateway · RBAC · tool policy · masking · audit"]
    end
    subgraph CORE["Deterministic PEI core (implemented as local Python library + MCP)"]
      MCP["MCP: six read-only tool handlers"]
      SVC["Parser · validator · investigation engine · code lookup · evidence"]
    end
    subgraph DATA["Bank-controlled integration boundary (target)"]
      ADP["Bank-owned, read-only adapters and contract mapping"]
      HUB["Payment Hub / pacs.008 / pacs.002"]
      LEDGER["Core banking / ledger"]
      LEG["z/OS Connect · MQ · SOAP / ESB · batch archive"]
    end
    APP --> GW
    AI --> GW
    IAM --> GW
    GW --> MCP
    GW --> SVC
    MCP --> SVC
    SVC -. "authorized evidence request" .-> ADP
    ADP --> HUB
    ADP --> LEDGER
    ADP --> LEG
\`\`\`

Glama can list and distribute MCP server information, but is not required in a bank transaction path. There is no direct LLM-to-core connection or payment-write capability.

## Trust boundaries and controls

| Boundary | Threat | Required control | Implementation status |
|---|---|---|---|
| User → Agent | User lacks permission for payment evidence | Bank SSO/OIDC, approved user purpose and session identity | **Target** |
| Agent → MCP | Tool misuse, tool injection, excessive data scope | Tool allowlist, scoped RBAC, per-invocation policy, quotas/timeouts | **Partial**: existing tools are read-only; enterprise gateway absent |
| Untrusted financial XML → Parser | XXE, large XML, embedded instructions | No external entities/DTD, version checks, byte/element limits, free-text markers and injection flags | **Implemented basic checks**, not comprehensive security proof |
| MCP → Financial engine | Hallucination or false correlation | Exact original message and EndToEndId/UETR matching, evidence path, unknown-code handling | **Implemented for supplied pacs.008/pacs.002** |
| Engine → Bank adapters | Unauthorized read, credential exposure | Bank-owned adapters, read-only service identity, allowlisted reference IDs, minimal response, mTLS | **Adapter interfaces exist**; live connections and bank identity **target** |
| Evidence → LLM | PII exfiltration, stale or partial evidence | Tokenization/minimization, retention policy, disclosure bounds, freshness and source timestamps | **Target** |
| Recommendation → Payment action | Wrong retry or beneficiary change | No payment-write tools exposed; human case review and separate bank authorization path | **No-write constraint implemented**; enterprise approval workflow **target** |
| Operations | Untraceable decisions or model drift | Immutable audit, independent review, red-team, model monitoring, kill switch | **Target** |

### Fail-closed decisions

- **No match** on authoritative message/transaction identifiers: report *unmatched*, do not attribute rejection or recommend retry.
- **Unknown reason code**: preserve the code and source, mark meaning *unknown*; never synthesize code semantics.
- **Schema is missing**: report conformance as undetermined/false; do not claim official scheme compliance.
- **Security warning**: flag for human review; never follow instructions in remittance or free-text fields.
- **Bank identity or access denied**: do not retrieve the record, provide a sanitized denial.
- **Untrusted or stale source**: disclose uncertainty and escalate; do not execute a payment mutation.

## Current tool inventory

| MCP tool | Present implementation | Allowed role |
|---|---|---|
| \`parse_message(xml)\` | Extract supported ISO 20022 fields | Read-only |
| \`validate_message(xml)\` | Business checks, optional local XSD, separate security status | Read-only |
| \`investigate_payment(pacs008_xml,pacs002_xml)\` | Exact correlation, evidence ledger and safe findings | Read-only |
| \`lookup_code(code)\` | Curated status/charge/reason lookup | Read-only |
| \`explain_message(xml)\` | Deterministic explanation | Read-only |
| \`generate_test_message(...)\` | Synthetic test XML | Test-only |

Future \`get_payment_evidence\`, \`get_payment_status\`, \`get_scheme_rules\`, \`check_duplicate_payment\` and \`simulate_repair\` are **not implemented**. The proposed simulation must remain separate from execution.

## Happy path: synthetic demonstration

1. Analyst supplies a pacs.008 and matching pacs.002 with the same original message ID and transaction identifiers.
2. AI MCP client initializes and uses \`tools/list\`; it chooses \`validate_message\` for business, security and XSD state.
3. Client invokes \`investigate_payment\` with both XML strings.
4. Deterministic engine checks \`OrgnlMsgId\` and exact \`OrgnlEndToEndId\` and/or \`OrgnlUETR\`; no fuzzy party matching.
5. pacs.002 reports \`RJCT\` and reason \`AC04\`. Code lookup can explain the **bank-reported** reason but cannot verify beneficiary account state.
6. Result includes correlation outcome, field-level source evidence, schema/business/security status, limitations and no automatic retry.
7. AI explains the facts and uncertainty. A bank operator must independently verify any actual remediation.

The live banking extension adds an **authorized, audited evidence-retrieval tool** through REST/z/OS Connect, MQ, SOAP or an archive, before step 2. It is not currently deployed.

## Risk statement for executives

Read-only removes **direct agent-driven payment execution** from this project. It does **not** remove: unauthorized bank evidence access, privacy leakage to LLMs/logs, false confidence, inaccurate or stale rules, configuration drift, compromised dependencies, and analyst misuse. Residual risks must be owned and assessed in a bank-controlled pilot before any production approval.

## Proof of value (pilot design, not measured results)

Compare conventional analyst/API-only workflow with PEI on the same bank-approved, deidentified payment exception cases. Report median time, source-evidence traceability, correctness by blind expert review, unsupported assertions, unsafe suggested actions, PII exposure, and tool usage. Treat initial synthetic fixture results as a unit-testing proof, not as production ROI.

**Executive gate:** proceed with a scoped read-only pilot only after identity, source-data authorization, privacy controls, audit and review ownership are approved. Do not seek autonomous payment execution rights.

See [executive slides](./README.md), [full happy path](../ISO20022_MCP_Happy_Path_Complete_Flow.md), and [bank/legacy integration details](../ISO20022_MCP_Solution_Architecture.md).
