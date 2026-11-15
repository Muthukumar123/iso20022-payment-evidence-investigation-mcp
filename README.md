# iso20022-mcp

An MCP server that lets AI agents **parse, validate, explain and test ISO 20022 payment messages** — safely.

Agents handling payments fail in predictable ways: they invent reject codes, miss IBAN checksum errors, and
follow instructions hidden in free-text fields like remittance information. This server gives them
deterministic tools for the parts that must be exact, and treats message free text as untrusted data.

## FinServ Evidence Intelligence (FEI) — product direction

The repository also contains a proposed **FinServ Evidence Intelligence (FEI)**
solution blueprint. Its first product is an evidence-backed, **read-only payment
exception investigation copilot**, reusing the deterministic ISO 20022 MCP tools.
This is an evolution of the existing project, **not** a live banking product or
an AI payment executor.

- [FEI product vision and implementation boundaries](docs/finserv/README.md)
- [High-level architecture, bank integration and trust boundaries](docs/finserv/ARCHITECTURE.md)
- [Security guardrails and residual risks](docs/finserv/SECURITY_AND_GUARDRAILS.md)
- [Controlled MVP roadmap and pilot KPIs](docs/finserv/MVP_ROADMAP.md)
- [Gamma AI executive narrative](docs/finserv/GAMMA_EXECUTIVE_DECK.md)

Gamma AI creates executive presentations; **Glama** is a separate MCP discovery
and hosting provider. Neither is part of the bank's payment execution path.

## Tools

| Tool | What it does |
|---|---|
| `parse_message` | pacs.008 / pacs.002 XML → structured results (version-aware, bounded, XXE-safe) |
| `validate_message` | IBAN mod-97, BIC format, amounts and currency decimals, required parties, counts, free-text limits, prompt-injection patterns — each issue mapped to its likely reject code |
| `explain_message` | Deterministic plain-language summary: who pays whom, how much, status and reasons |
| `lookup_code` | Status reason / transaction status / charge bearer codes — returns `found: false` instead of guessing |
| `generate_test_message` | Synthetic valid and defective messages for testing (no real customer data) |
| `investigate_payment` | Exactly correlate a supplied pacs.008 and pacs.002; return bank-reported rejection evidence, limits and human-reviewed next steps |

## Architecture and complete happy-path walkthrough

- [Documentation index](docs/README.md)
- [Complete local and proposed bank-connected happy path](docs/ISO20022_MCP_Happy_Path_Complete_Flow.md)
- [Core banking, legacy integration and security design](docs/ISO20022_MCP_Solution_Architecture.md)
- [Word design document](docs/generated/ISO20022_MCP_Architecture_And_Happy_Path.docx)
- [PowerPoint architecture presentation](docs/generated/ISO20022_Payment_Intelligence_Architecture.pptx)
- [Editable Mermaid diagrams](docs/diagrams/)

The Word/PPTX and rendered diagrams are generated reproducibly with
`python docs/build_documents.py`. The GitHub documentation workflow publishes
them to the feature branch. Production bank connections and a remote authenticated
MCP gateway are **not** implemented.

## Quick start

```bash
pip install -e ".[dev]"
pytest -q
iso20022-mcp            # runs the server over stdio
```

Claude Desktop / any MCP client config:

```json
{ "mcpServers": { "iso20022": { "command": "iso20022-mcp" } } }
```

## Security design

- Free-text fields are returned with an `_UNTRUSTED` suffix and the server instructions tell agents to treat them as data.
- `validate_message` flags instruction-like content in free text (severity `security`).
- XML parsing disables entity resolution and network access.
- Only synthetic data and public example IBANs/BICs are used anywhere in this repo.

## Benchmark

`evals/` contains a generator for a banking-agent task set (`python evals/make_tasks.py`) covering validation, rejection investigation and prompt injection, plus a
deterministic scorer. Results across model families: _coming soon_.

## Hardened validation and enterprise integration (experimental)

The server remains a **local stdio MCP process**. Its ISO 20022 business tools
do not execute, modify or transmit payments.

### Supported XML versions and safety limits

- `pacs.008.001.08` and `pacs.002.001.10` are explicitly supported. A
  mismatched message root or unrecognized namespace/version is rejected.
- XML input is limited to **1,000,000 UTF-8 bytes** and **10,000 elements**.
  DTDs are rejected; external entities and XML network access are disabled.
- IBAN mod-97 and maintained country lengths, supported currency codes/minor
  units, UETR, BIC and transaction counts are checked.
- Currency codes and status reason tables are curated subsets. Maintain them
  from authoritative sources before accepting production traffic.

### Optional offline XSD validation

Official ISO 20022 XSDs are **not bundled**. Obtain the corresponding
authoritative schemas and review them through your bank's change-control
process. Install version-named local files into a trusted directory:

```bash
export ISO20022_XSD_DIR=/path/to/approved/iso20022/xsd
# Expected filenames include:
# pacs.008.001.08.xsd
# pacs.002.001.10.xsd
iso20022-mcp
```

The XSD validator reads only locally configured schema files and does not
download schemas. Imported/included files should be reviewed and kept within
the trusted schema bundle. A missing file is reported as `unavailable`, not
as a successful validation.

`validate_message` includes independent outcomes:

| Field | Meaning |
|---|---|
| `business_valid` | Business checks produced no `error` findings |
| `valid` | Backwards-compatible alias for `business_valid`, **not** XSD conformance |
| `schema_status` | `valid`, `invalid`, `not_configured`, `unavailable`, `error`, or `not_evaluated` |
| `schema_valid` | `true`, `false`, or `null` if schemas are not configured |
| `schema_issues` | XSD diagnostic messages, separate from business-rule findings |
| `security_status` | `clear`, `review_required`, or `not_evaluated` |
| `conformant` | `true` only if business rules pass, a configured XSD passes and no security finding exists |

A `conformant` result is **not** an authorization to settle or release a
payment; scheme rules and payment-hub controls are still required.

### Typed MCP responses

`parse_message`, `validate_message`, and `lookup_code` now return
Python dictionaries, allowing MCP SDKs to expose structured responses.
Previously these functions returned JSON-serialized strings. Clients that
assume a text-only response should be adapted to accept structured content.
`explain_message` and `generate_test_message` remain text tools.

### Governed read-only integration boundary

`iso20022_mcp.adapters.PaymentInspectionService` is a framework-neutral,
read-only integration contract. A bank must supply both:

1. `PaymentMessageSource.read_xml(reference)`, backed by an approved
   payment hub or message archive.
2. `PaymentReadAuthorizer.may_read(principal, reference)`, backed by
   authenticated identity and bank policy.

An unauthorized request is rejected **before** the payment-hub adapter reads
any message. This service is not automatically exposed as an MCP tool, and
there are no default credentials, unauthenticated endpoints, payment execution
methods or live bank connections.

For centralized deployment, put a separately reviewed MCP HTTP gateway in
front of the service with OAuth/OIDC, tool scopes, transport security, rate
limits, PII masking, durable audit trails and observability. A fully secured
remote gateway and concrete payment-hub adapters are **not implemented**.

### Test

```bash
pip install -e ".[dev]"
pytest -q
```

The suite includes actual stdio MCP initialization/tool-discovery checks,
validation security regression tests, and authorization tests for the
read-only adapter interface.


## Evidence-backed payment investigations (experimental)

The `investigate_payment(pacs008_xml, pacs002_xml)` MCP tool
correlates supplied pacs.008 and pacs.002 messages by original message ID
**and** exact transaction identifiers. It returns a read-only evidence ledger,
reported status codes, interpretation limits, and safe human-reviewed
recommendations. It refuses to attribute unrelated statuses to a payment.

Example (Python API, synthetic messages):

```python
from iso20022_mcp import generate, parser
from iso20022_mcp.investigate import investigate_payment

original = generate.generate_pacs008()
p = parser.parse_message(original)
status = generate.generate_pacs002(
    "AC04", p["msg_id"], p["transactions"][0]["end_to_end_id"]
)
report = investigate_payment(original, status)
assert report["cases"][0]["correlation"] == "matched"
assert report["cases"][0]["reported_reasons"][0]["code"] == "AC04"
```

The engine does not query live banking systems, verify real account status,
apply CBPR+/SEPA business rules or initiate any repair. A reason reported in
pacs.002 remains a bank-reported reason, not an independently verified cause.

Synthetic, transparent capability comparison:

```bash
python evals/compare_investigation.py
```

This comparison demonstrates exact correlation, unknown-code safety, and
provenance in fixture cases; it is **not** a real-world accuracy study.

## Roadmap

- Official XSD validation · pain.001 and camt.053 · MT103 → pacs.008 (subset) · remote HTTP deployment with auth and OpenTelemetry

## Disclaimer

Not affiliated with ISO, SWIFT or any bank. Code sets here are a curated subset; consult the official ISO 20022 external code sets for production use.
