# Payment Evidence Intelligence (PEI) — Executive Architecture

**Working platform name:** Payment Evidence Intelligence (PEI). Subject to legal/trademark review before external branding.

This directory contains an **editable seven-slide PowerPoint** for executive sponsors, payment operations, risk officers and enterprise architects.

## What we are building
An **evidence-first, AI-assisted payment exception investigation platform**. A governed AI agent interprets analyst questions, chooses supported tools, and explains deterministic evidence. ISO 20022 business logic and bank-owned systems remain the authoritative source of truth. A proposed bank adapter would retrieve approved records using approved identities and access controls. **The current implementation does not access live banking systems or execute payments.**

## Why AI? Why MCP? Why not just REST?
- **REST / deterministic rules:** the right architecture for fixed validation and processing workflows; a single API is enough if the job is only XML checking.
- **AI:** valuable for variable investigation requests, selecting the next information need, joining evidence and uncertainty into an intelligible analyst response. The model is not itself a payment validation authority.
- **MCP:** a standard tool discovery/invocation interface for multiple compatible AI clients; it does not make XML processing smarter or safer by itself.
- **Differentiation:** exact cross-message correlation, citations to source fields, refusal to infer missing facts, explicit human-in-the-loop handling and measurable investigation quality.

## Slide index
| # | Executive question | Slide content |
|---|---|---|
| 1 | What is PEI and why build it? | Business problem, unique capability and desired outcome |
| 2 | Why AI and MCP over a single API? | Traditional API vs AI + direct APIs vs AI + MCP |
| 3 | What architecture are we proposing? | AI, MCP, deterministic core and future bank-owned trust boundary |
| 4 | Which actual and planned tools exist? | Six implemented tools vs proposed bank-connection tools |
| 5 | What is the actual happy path? | Six-step sequence and synthetic pacs.008 / pacs.002 example |
| 6 | How is it secured; what can go wrong? | Controls implemented today, future controls and residual risks |
| 7 | How will we prove value? | Pilot scorecard, delivery gates and investment ask |

## Implemented MCP tools (callable now)
| Tool | Purpose |
|---|---|
| `parse_message` | Parse supplied pacs.008 / pacs.002 XML |
| `validate_message` | Business-rule checks, security findings and optionally local XSD |
| `investigate_payment` | Exact correlation and field-level evidence for supplied messages |
| `lookup_code` | Explain known code values; unknown values remain unknown |
| `explain_message` | Deterministic natural-language explanation |
| `generate_test_message` | Create synthetic test messages |

**Not implemented:** `get_payment_evidence`, `get_payment_status`, `get_scheme_rules`, `check_duplicate_payment`, `simulate_repair`; bank authorization/gateway, production data redaction and live core-banking connection.

## Safety and risk
The prototype is read-only, uses exact identifier correlation, marks untrusted free text and provides no automated payment mutations. This limits **execution risk only**; it does **not eliminate** wrong conclusions, model hallucination, data leakage, authorization failures, evolving scheme rules or operational failures. The executive slide distinguishes `TODAY`, `TARGET` and `GAP` controls. Real banking deployment needs security review and bank approval.

## What success would mean
Evaluate mean/median investigation time, evidence coverage, expert-reviewed accuracy, unsupported statements, safety violations, case escalation quality and analyst acceptance against a documented baseline. **No production improvement has been demonstrated by the synthetic fixture benchmark.**

## Files
- [Seven-slide editable executive deck](ISO20022_Payment_Intelligence_Executive_Overview.pptx)
- [PowerPoint generator source](build_executive_slides.js)
- [Full happy path](../ISO20022_MCP_Happy_Path_Complete_Flow.md)
- [Solution architecture and legacy banking integration](../ISO20022_MCP_Solution_Architecture.md)
- [Editable Mermaid sequences](../diagrams/)

## Build
Requires Node.js 22+ and `pptxgenjs@4.0.0`:

```bash
npm install --no-save pptxgenjs@4.0.0
OUTPUT_PPTX=docs/executive/ISO20022_Payment_Intelligence_Executive_Overview.pptx node docs/executive/build_executive_slides.js
```

The repository workflow builds, validates that the deck contains exactly seven slides and commits the generated PowerPoint. Slides are native editable PowerPoint shapes, not screenshots.

## Review status
PR #2 is stacked on PR #1 (validation hardening). It should be reviewed and the base merged in dependency order. This deck describes both the current prototype and the proposed enterprise target state; do not represent future controls as deployed.
