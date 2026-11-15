# FinServ Evidence Intelligence (FEI) — foundation

**Status:** product concept / controlled prototype, not a production banking platform.

**Vision:** Evidence-first financial-services investigations: turn fragmented payment and status records into traceable, human-reviewed explanations. **Initial wedge:** ISO 20022 payment exception investigation. Expand only after proving value on bank-approved cases.

> **Executive promise:** Investigate the *why*, show the *evidence*, make uncertainty explicit, and never bypass payment controls.

## What problem is solved?

Payment-operations analysts investigate failures by moving among payment hubs, core banking, SWIFT/message archives, and reconciliation tools. Fixed APIs excel at retrieving and validating data but do not provide flexible, case-specific explanations across sources. FEI proposes an optional AI copilot that orchestrates **governed, read-only investigation tools** while deterministic services establish the payment facts.

## Why AI and why MCP?

| Question | Defensible answer |
| --- | --- |
| Why AI? | Interpret variable questions, plan bounded tool use, summarize correlated evidence and uncertainties. The model must **not** decide payment correctness or authorization. |
| Why MCP? | Provide reusable AI-facing tool schemas and standardized tool discovery for multiple AI clients. Existing APIs remain the authoritative business interfaces. |
| Why not use only REST? | For predefined validation workflows, **do use REST**; MCP + AI is only valuable if it improves flexible, cross-system investigations in measured trials. |
| Why streaming? | Later, reconstruct lifecycle timelines and detect exceptions. Apache Pulsar / Amazon MSK / Kinesis / existing IBM MQ are **options**, not mandated MVP components. |
| Differentiation? | Exact cross-message correlation, source-level citations, no invented codes, explicit unknowns, controlled human review, measurable benchmark versus manual and REST-only approaches. |

## Current capability versus target

| Component | Implemented in feature branches | Proposed, not implemented |
| --- | --- | --- |
| ISO 20022 MCP stdio tools | parse, validate, explain, lookup_code, generate_test_message; investigate_payment is on the previous feature PR | Authenticated remote MCP access |
| Evidence | Deterministic pacs.008/pacs.002 exact identifier correlation with evidence fields | Cross-system lifecycle evidence store, authoritative account status |
| Bank connectors | Interfaces for authorized read-only access, no live connectivity | Bank-specific REST/z/OS, IBM MQ, SOAP/ESB, batch connectors |
| Security | Local XML bounds, DTD rejection, untrusted-text flags, no payment-write tools | Enterprise SSO/OIDC, RBAC/ABAC, PII controls, gateway policy, immutable audit |
| Validation | Local curated rules; optional locally supplied XSD | Official scheme-rules governance, effective-date reference data |
| Operations | Synthetic tests and CI | Production SLOs, DR, monitoring, human workflow and approval gates |

The earlier work is in stacked PRs [#1](https://github.com/Muthukumar123/iso20022-mcp/pull/1) and [#2](https://github.com/Muthukumar123/iso20022-mcp/pull/2), **not automatically merged into main**.

## Architecture and guardrails

See [target architecture](./ARCHITECTURE.md), [guardrails](./SECURITY_AND_GUARDRAILS.md), [MVP backlog](./MVP_ROADMAP.md), and editable [architecture](./diagrams/fei_high_level_architecture.mmd) / [investigation sequence](./diagrams/fei_payment_investigation.mmd).

The LLM is an **untrusted planner and communicator**, never a system of record. Read-only, allowlisted bank adapters feed a deterministic evidence service. The MCP gateway validates identity, permissions, payload size, and tool budgets. Human authorization remains mandatory for any consequential action; MVP contains **no payment-write tools**.

## Gamma AI executive deck

[Gamma-ready 10-card narrative](./GAMMA_EXECUTIVE_DECK.md) is *synthetic and non-confidential*. Gamma (gamma.app) is a **presentation publishing service**, not the runtime hosting platform for the FEI MCP service.

Create preview JSON without credentials:

\`\`\`bash
python scripts/publish_gamma.py --dry-run
\`\`\`

To generate a Gamma-hosted deck, configure \`GAMMA_API_KEY\` as a secret and run the **Publish FEI executive narrative to Gamma** manual GitHub Actions workflow, or run the script locally with \`--publish\`. API generation consumes Gamma credits. The workflow is manual by design and will not send real payment data. Deployment is **not complete** until Gamma returns an actual \`gammaUrl\`.

## MVP acceptance criteria

1. **Safety:** zero payment mutations; deny unauthorized records before data access; zero raw sensitive samples in Gamma or public logs.
2. **Correctness:** exact group and transaction correlation; unknown codes/ambiguous status flagged, never invented.
3. **Value:** benchmark verified analyst cases versus manual and API-only baselines, measuring time, evidence precision, error rate and unsafe recommendations.
4. **Operations:** audited tool calls, role tests, deterministic regression suite and monitored failures before any bank integration.

**Scope gate:** start with synthetic data and read-only controlled investigation. Expand to live bank data only after architecture, model-risk and privacy review.
