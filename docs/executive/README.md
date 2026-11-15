# PEI — Payment Evidence Intelligence | Executive Architecture

This folder contains the final **eleven-slide, editable PowerPoint and matching PDF** for business sponsors, CIO/CTO, banking architects, risk and control stakeholders.

**Final presentation files:**

- [Executive PowerPoint (.pptx)](./ISO20022_Payment_Intelligence_Executive_Overview.pptx) — editable slide shapes and text.
- [Executive PDF (.pdf)](./ISO20022_Payment_Intelligence_Executive_Overview.pdf) — distribution-ready fixed-layout version (11 pages).

The PowerPoint and PDF are generated from the same source so their content and slide order remain aligned.

**Product statement:** *From rejection codes to defensible decisions.* Build a read-only, evidence-first, AI-assisted investigation capability for ISO 20022 payment exceptions—not another XML validation API and not an autonomous payment executor.

## Executive narrative

| Slide | Key question answered |
| --- | --- |
| 1. Vision | What is PEI, why build it, and what must it never do? |
| 2. Traditional vs AI + MCP | Why AI? Why MCP instead of just a REST API? |
| 3. Intelligent differentiation | What is implemented beyond basic XML validation? |
| 4. **High-level target architecture** | Where are the AI client, governed access, deterministic core, bank-owned adapter and systems of record? |
| 5. **Seven-layer guardrails** | How do identity, PII, prompt/data controls, authorization, provenance, human review and audit form a defense-in-depth design? |
| 6. MCP tools | What six tools are actually implemented versus what requires bank integration? |
| 7. Happy-path sequence | How does supplied pacs.008 + pacs.002 become evidence-backed explanation? |
| 8. Core/legacy integration | How can bank adapters use REST/z/OS Connect, MQ, SOAP/ESB, batch or archives? |
| 9. Risk & residual risk | Why is read-only safer but emphatically **not risk-free**? |
| 10. Measurable value | How should PEI be compared with traditional/API-only investigation? |
| 11. Investment decision | Which gates should precede a controlled bank pilot and operational scale? |

## Current capabilities vs target

**Implemented in the Python repository:** local MCP stdio server; \`parse_message\`, \`validate_message\`, \`explain_message\`, \`lookup_code\`, \`generate_test_message\`, \`investigate_payment\`; deterministic parsing and exact pacs.008/pacs.002 correlation; curated code lookup, basic security flags and optional offline XSD validation. The payment-hub adapter interfaces exist but are **not** connected to live bank systems.

**Target only:** OIDC/mTLS-secured enterprise MCP gateway, bank-owned read-only payment-hub/core adapters, PII tokenization and data governance, immutable operational audit, official XSD/scheme-rule governance, and human investigation workflows. **No payment-write tools are provided.**

Glama is optional MCP discovery and publishing, not part of payment processing or an essential runtime dependency.

## Naming and audience

- **Platform / concept:** Payment Evidence Intelligence (**PEI**).
- **Runtime component:** PEI ISO 20022 MCP Evidence Service.
- **Business user experience:** Payment Operations Investigation Copilot.
- **Bank integration:** PEI Read-Only Evidence Adapters (planned concrete implementations).

This is a positioning proposal, not a registered mark.

## Build the slide deck

Requires Node.js and \`pptxgenjs\`:

\`\`\`bash
npm install --no-save pptxgenjs@4.0.0
OUTPUT_PPTX=docs/executive/ISO20022_Payment_Intelligence_Executive_Overview.pptx \
  node docs/executive/build_executive_slides.js
\`\`\`

The deck contains **11 editable slides**, not flattened images. The GitHub workflow in \`.github/workflows/build-executive-deck.yml\` builds and commits both the PowerPoint and a matching PDF via LibreOffice. Do not edit either generated binary manually; update the JavaScript source and rerun the workflow.

## Supporting sources

- [Executive architecture + guardrails](./ARCHITECTURE_AND_GUARDRAILS.md)
- [High-level architecture Mermaid](../diagrams/pei_high_level_architecture.mmd)
- [Guardrails & investigation sequence Mermaid](../diagrams/pei_guardrails_sequence.mmd)
- [Complete synthetic happy path](../ISO20022_MCP_Happy_Path_Complete_Flow.md)
- [Core/legacy integration architecture](../ISO20022_MCP_Solution_Architecture.md)

**Investment hypothesis, not a claimed result:** PEI may reduce evidence gathering and improve consistency. Benchmark analyst time, evidence accuracy, incorrect assertions, privacy events and unsafe action rates using bank-approved cases before making ROI or safety claims.
