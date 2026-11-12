# ISO 20022 Payment Intelligence — Executive Overview

This folder contains a **two-slide, editable PowerPoint deck** designed for an executive or banking architecture review. It explains **what we are building, why it matters, which MCP tools are involved, and the end-to-end request sequence**.

## Executive message

**We are not building another XML parser.** We are building an **evidence-backed, read-only payment investigation capability** that correlates an original ISO 20022 `pacs.008` with a bank-reported `pacs.002` status message and explains confirmed facts, uncertainties and human-reviewed next actions.

The opportunity is reduced manual investigation, traceable outcomes, and an AI-facing tool contract reusable across compatible clients. This is a product objective, **not a proven production KPI**.

## Slides

| Slide | Core message | Diagram |
| --- | --- | --- |
| 1 — Strategy | Commodity validation versus evidence-backed payment investigation; objective and value | Ask → Retrieve* → Prove → Explain → Review |
| 2 — Architecture and interaction | AI orchestrates MCP tools; deterministic code correlates source evidence; bank adapters are proposed | Analyst → Agent → MCP → Evidence engine → evidence-backed answer, with future bank-adapter boundary |

### MCP tools shown

- `parse_message` — Extract payment/status fields from supported XML.
- `validate_message` — Business rules plus optional XSD and security assessments.
- `investigate_payment` — Exact `pacs.008`/`pacs.002` correlation with field-level evidence.
- `lookup_code` — Meaning of known status/rejection codes; never invent unknown meanings.
- `explain_message` — Deterministic plain-language rendering.
- `generate_test_message` — Synthetic test fixtures.

`get_payment_evidence` is **illustrative / proposed**, not an implemented MCP tool. Its future implementation requires a bank-operated adapter and authorization policies for payment hub, z/OS Connect/REST, SOAP, MQ, or batch sources.

## Actual implemented happy path

1. The analyst provides *synthetic* `pacs.008` and matching `pacs.002` XML.
2. The AI client's MCP session initializes, discovers tools (`tools/list`) and calls validation and investigation tools.
3. The deterministic investigation engine correlates the original message ID and exact transaction IDs, then interprets bank-reported status and known reason codes.
4. The MCP tool returns the status and evidence paths with uncertainty, restrictions and safe human-review recommendations.
5. The analyst receives an evidence-backed explanation. No payment modification occurs.

For a detailed, reproducible example, see [`../ISO20022_MCP_Happy_Path_Complete_Flow.md`](../ISO20022_MCP_Happy_Path_Complete_Flow.md).

## Planned connected banking path

`Analyst → AI agent → governed MCP gateway → authenticated read-only bank adapter → payment hub/legacy archive → pacs.008 + pacs.002 → investigate_payment → evidence + human review`

No production bank connection, external scheme-rule validation, payment resubmission or repair execution is included in the current repository.

## Regenerate the PPTX

Requires Node.js 20+ and PptxGenJS 4.0.0:

```bash
npm install --no-save pptxgenjs@4.0.0
OUTPUT_PPTX=docs/executive/ISO20022_Payment_Intelligence_Executive_Overview.pptx \
  node docs/executive/build_executive_slides.js
```

The PowerPoint uses native editable shapes, text and connectors rather than flattened slide images.

## Supporting architecture and diagrams

See [`../ISO20022_MCP_Solution_Architecture.md`](../ISO20022_MCP_Solution_Architecture.md) and [`../diagrams/`](../diagrams/) for detailed REST, z/OS Connect, SOAP, IBM MQ and human-controlled investigation sequences.