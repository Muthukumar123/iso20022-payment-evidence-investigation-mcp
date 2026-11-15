# ISO 20022 Payment Intelligence — Architecture Package

This folder contains architecture documentation for the evidence-backed ISO 20022 MCP investigation prototype.

## Start here

1. [Complete happy-path walkthrough](ISO20022_MCP_Happy_Path_Complete_Flow.md) — exact tool sequence, sample pacs.008/pacs.002 messages, MCP requests, evidence response and analyst-facing answer.
2. [Solution architecture and legacy integration](ISO20022_MCP_Solution_Architecture.md) — logical architecture, trust boundaries, read-only core banking adapters, REST, z/OS Connect, IBM MQ, SOAP and batch patterns.
3. [Architecture Word document](generated/ISO20022_MCP_Architecture_And_Happy_Path.docx) — both guides with diagrams.
4. [Architecture PowerPoint presentation](generated/ISO20022_Payment_Intelligence_Architecture.pptx) — editable 18-slide review deck.
5. [Editable Mermaid source diagrams](diagrams/) and [rendered PNG diagrams](generated/diagrams/).

## Demonstrate current implemented capabilities

```bash
pip install -e ".[dev]"
pytest -q
python evals/compare_investigation.py
iso20022-mcp
```

The `investigate_payment(pacs008_xml, pacs002_xml)` MCP tool requires **both supplied XML messages**. It does not fetch payments from bank systems or execute modifications.

## Regenerate deliverables

```bash
python -m pip install "python-docx>=1.1,<2" "python-pptx>=1,<2" "Pillow>=10,<13"
python docs/build_documents.py
```

The generator creates DOCX, PPTX and PNG files under `docs/generated/`.
GitHub Actions also builds and publishes these assets on this feature branch.

## Implementation status and safety

| Capability | Status |
| --- | --- |
| Local MCP tool operations | Implemented in the feature branches |
| Exact evidence correlation | Implemented and regression-tested |
| Synthetic sample messages and comparison | Implemented; **not** a real-bank accuracy benchmark |
| Version-aware parsing and optional XSD | Implemented; approved official XSDs not bundled |
| Bank adapter interface | Implemented as read-only contract |
| Actual REST, mainframe, IBM MQ or bank credentials | **Proposed — not connected** |
| Remote authenticated MCP gateway | **Proposed — not deployed** |
| Payment modification, release or retry | **Not permitted** |

## Source review

- [PR #1 — Validation hardening](https://github.com/Muthukumar123/iso20022-payment-evidence-investigation-mcp/pull/1)
- [PR #2 — Evidence-backed investigations](https://github.com/Muthukumar123/iso20022-payment-evidence-investigation-mcp/pull/2) (originally stacked on PR #1; both are merged)

All examples are synthetic. The explanations distinguish facts reported in a bank status message from interpretations and hypotheses. Bank-governed authorization and human review remain necessary for any consequential payment action.
