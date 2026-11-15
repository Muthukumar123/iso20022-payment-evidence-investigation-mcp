# ISO 20022 Payment Intelligence — Complete Happy-Path Walkthrough

**Version:** 1.0 · **Date:** 12 November 2026 · **Repository:** https://github.com/Muthukumar123/iso20022-mcp

**Status:** Runnable read-only local demonstration on PR #2 (built on PR #1); proposed bank integration is separately identified. All identifiers and data below are synthetic. Nothing in the example initiates, repairs, or resubmits a payment.

## 1. Business goal and what the system proves

> Analyst: “Why was payment REF123 rejected? Show the authoritative evidence, explain the reason, and tell me what the operations team can safely do next.”

A simple validator can say whether the supplied pacs.008 XML passes selected rules. An investigation engine must instead establish **which payment** a status report belongs to, **what the bank actually reported**, **which record fields support that conclusion**, **which facts are unknown**, and **what actions require human approval**.

The current implementation supports **two supplied XML messages**. It does not implement `get_payment_evidence` or any bank network integration. The live `REF123` retrieval flow below is the **target architecture**, not a current MCP tool.

## 2. Participants and actual tool inventory

| Actor / tool | Responsibility | Status |
|---|---|---|
| Analyst | Requests an explanation and reviews findings | Business role |
| AI agent / MCP client | Selects tools and formats facts; cannot authorize payment changes | Client-dependent |
| `tools/list` | Discovers the MCP tools and schemas | MCP protocol capability |
| `parse_message(xml)` | Extracts typed payment/status structures from supported XML | Implemented |
| `validate_message(xml)` | Returns `business_valid`, `schema_status`, `security_status`, warnings | Implemented on PR #1 |
| `lookup_code(code)` | Looks up reason code in curated table; unknown stays unknown | Implemented |
| `investigate_payment(pacs008_xml,pacs002_xml)` | Strictly correlates two messages and produces evidence | Implemented on PR #2 |
| `get_payment_evidence(reference)` | Retrieves bank-owned original/status records under IAM | **Proposed — not implemented** |
| Enterprise MCP gateway | Authenticates, authorizes, logs, and limits remote tool calls | **Proposed — not implemented** |
| Payment hub / legacy adapter | Provides records from authoritative systems | Interface only; no live connector |

## 3. Happy path A — executable locally using supplied ISO 20022 XML

This is the end-to-end flow the current feature branch is designed to support. It intentionally avoids live banking dependencies.

### Step A1 — Start server and initialize the MCP session

Install in a Python environment from `feat/payment-evidence-investigation-20261112` (after PR #1 is included):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
iso20022-mcp
```

MCP client config (replace the path with your installed executable):

```json
{
  "mcpServers": {
    "iso20022": {
      "command": "/absolute/path/to/iso20022-mcp/.venv/bin/iso20022-mcp"
    }
  }
}
```

The client completes `initialize`, then sends `notifications/initialized`, and calls `tools/list`. The returned tool names include `parse_message`, `validate_message`, `explain_message`, `lookup_code`, `generate_test_message`, and `investigate_payment`. The server communicates over local **stdio**; there is no HTTP banking endpoint in this flow.

### Step A2 — Obtain synthetic pacs.008 and pacs.002 messages

These two complete, synthetic fixtures use a matching group message ID and EndToEndId. In the current system, the user or trusted test harness supplies the XML.

**Original payment — pacs.008.001.08**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
  <FIToFICstmrCdtTrf>
    <GrpHdr>
      <MsgId>MSG-DEMO-001</MsgId>
      <CreDtTm>2026-11-12T09:00:00Z</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <SttlmInf><SttlmMtd>INDA</SttlmMtd></SttlmInf>
    </GrpHdr>
    <CdtTrfTxInf>
      <PmtId>
        <EndToEndId>E2E-DEMO-001</EndToEndId>
        <UETR>123e4567-e89b-42d3-a456-426614174000</UETR>
      </PmtId>
      <IntrBkSttlmAmt Ccy="EUR">1250.00</IntrBkSttlmAmt>
      <IntrBkSttlmDt>2026-11-12</IntrBkSttlmDt>
      <ChrgBr>SHAR</ChrgBr>
      <Dbtr><Nm>Demo Trading BV</Nm><PstlAdr><Ctry>NL</Ctry></PstlAdr></Dbtr>
      <DbtrAcct><Id><IBAN>NL91ABNA0417164300</IBAN></Id></DbtrAcct>
      <DbtrAgt><FinInstnId><BICFI>ABNANL2A</BICFI></FinInstnId></DbtrAgt>
      <Cdtr><Nm>Demo Supplier GmbH</Nm><PstlAdr><Ctry>DE</Ctry></PstlAdr></Cdtr>
      <CdtrAcct><Id><IBAN>DE89370400440532013000</IBAN></Id></CdtrAcct>
      <CdtrAgt><FinInstnId><BICFI>COBADEFFXXX</BICFI></FinInstnId></CdtrAgt>
      <RmtInf><Ustrd>Invoice DEMO-4471</Ustrd></RmtInf>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>
```

**Bank-reported status — pacs.002.001.10**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.002.001.10">
  <FIToFIPmtStsRpt>
    <GrpHdr><MsgId>STS-DEMO-001</MsgId><CreDtTm>2026-11-12T09:03:00Z</CreDtTm></GrpHdr>
    <OrgnlGrpInfAndSts>
      <OrgnlMsgId>MSG-DEMO-001</OrgnlMsgId>
      <OrgnlMsgNmId>pacs.008.001.08</OrgnlMsgNmId>
    </OrgnlGrpInfAndSts>
    <TxInfAndSts>
      <OrgnlEndToEndId>E2E-DEMO-001</OrgnlEndToEndId>
      <OrgnlUETR>123e4567-e89b-42d3-a456-426614174000</OrgnlUETR>
      <TxSts>RJCT</TxSts>
      <StsRsnInf><Rsn><Cd>AC04</Cd></Rsn></StsRsnInf>
    </TxInfAndSts>
  </FIToFIPmtStsRpt>
</Document>
```

### Step A3 — MCP tool calls

Tool discovery (standard MCP protocol message):

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

For locally supplied XML, the agent can call `validate_message` independently on each message, then `investigate_payment` with both complete XML strings. Example JSON-RPC envelope:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "investigate_payment",
    "arguments": {
      "pacs008_xml": "<the complete pacs.008 XML above>",
      "pacs002_xml": "<the complete pacs.002 XML above>"
    }
  }
}
```

The angle-bracketed values above are **documentation placeholders**, not literal payloads to send; replace each with its complete XML string. The actual MCP transport response wraps the tool result; the JSON below is the tool's **illustrative application-level result projection**.

### Step A4 — Internal deterministic reasoning (not LLM guessing)

1. XML parser checks the configured supported namespace and version, DTD policy, size and element limits.
2. Validation checks message IDs, created timestamp, payment fields, IBAN, BIC, currency, amount and free-text safety. Official XSD validation is reported separately (`schema_status = not_configured` unless a trusted local XSD bundle is supplied).
3. Correlation engine checks `pacs.002/OrgnlMsgId == pacs.008/GrpHdr/MsgId`.
4. It then checks the `OrgnlEndToEndId` (and supplied `OrgnlUETR`) against the pacs.008 transaction identifiers. **If identifiers disagree, it refuses attribution.**
5. It reads `TxSts = RJCT` from pacs.002, then looks up `AC04` in the curated local reference table.
6. It creates a field-level evidence ledger and a safe recommendation; it **does not** verify the beneficiary account or execute a retry.

### Step A5 — Representative structured result (selected fields)

```json
{
  "analysis_type": "deterministic_evidence_based_investigation",
  "read_only": true,
  "payment_msg_id": "MSG-DEMO-001",
  "status_msg_id": "STS-DEMO-001",
  "group_correlation": true,
  "original_validation": {
    "business_valid": true,
    "security_status": "clear",
    "schema_status": "not_configured"
  },
  "cases": [
    {
      "end_to_end_id": "E2E-DEMO-001",
      "correlation": "matched",
      "reported_status": "RJCT",
      "reported_reasons": [
        {
          "code": "AC04",
          "found_in_local_table": true,
          "reported_meaning": "Closed account number - account has been closed.",
          "interpretation_limit": "Bank-reported reason; not independent verification of the underlying account or rail condition."
        }
      ],
      "decision": "no_automatic_retry_or_mutation",
      "workflow": "human_review_required",
      "evidence": [
        {
          "source": "pacs.002",
          "field": "OrgnlGrpInfAndSts/OrgnlMsgId",
          "value": "MSG-DEMO-001",
          "statement": "Original-message identifier matches pacs.008"
        },
        {
          "source": "pacs.002",
          "field": "TxInfAndSts[0]/TxSts",
          "value": "RJCT",
          "statement": "Bank-reported transaction status"
        },
        {
          "source": "pacs.002",
          "field": "TxInfAndSts[0]/StsRsnInf[0]/Rsn/Cd",
          "value": "AC04",
          "statement": "Bank-provided status reason code"
        }
      ]
    }
  ]
}
```

This is a **projection**: the actual result also contains pacs.008 identifiers, status validation, assessment, recommended action, unmatched status indices, and limitations. It must never be mistaken for an independently verified account-status check.

### Step A6 — Expected AI-assisted analyst answer

> **Payment E2E-DEMO-001: bank-reported rejection.** A pacs.002 record matches original message `MSG-DEMO-001` and EndToEndId `E2E-DEMO-001`. It reports `RJCT` with reason `AC04` (closed account). The status and reason are supported by fields `TxInfAndSts[0]/TxSts` and `TxInfAndSts[0]/StsRsnInf[0]/Rsn/Cd`. This is a *bank-reported explanation*, not independent confirmation that the account is currently closed. Contact the customer through the approved channel to verify replacement beneficiary details. **Do not retry automatically.** An authorized operations specialist must review any resubmission. Official XSD conformance was not established because no approved XSD was configured.

**Happy-path success criteria:** correct cross-message correlation; provenance to actual XML fields; known code interpreted from reference data; unverified claims explicitly bounded; no payment mutation.

## 4. Happy path B — proposed connected bank deployment

This adds the currently missing authoritative record retrieval, using a bank-owned adapter and private MCP gateway. **Do not label the following tools as already implemented.**

### Proposed banking tool contract

| Proposed tool | Input | Output | Back end |
|---|---|---|---|
| `get_payment_evidence` | `payment_reference`, delegated principal/context | payment record identifiers, bank-controlled payload references, timestamps, source hashes | payment hub REST, z/OS Connect, MQ adapter, approved archive |
| `get_payment_message` | payload ref + approved purpose | authorized XML or redacted normalized fields | secure message archive |
| `get_transaction_timeline` | UETR / EndToEndId | ordered source status events with provenance | event read model |
| `get_rule_profile` | scheme, message version, effective date | immutable rule snapshot and reference version | bank-governed rules store |
| `create_investigation_case` | evidence summary and analyst approval | ticket ID; **not** payment execution | ticketing workflow (later, separately authorized) |

### Detailed connected sequence

```mermaid
sequenceDiagram
    autonumber
    actor Analyst
    participant Agent as AI Agent / MCP client
    participant Gateway as Private MCP Gateway (proposed)
    participant Adapter as Authorized Bank Read Adapter (proposed)
    participant Hub as Payment Hub / Archive
    participant Engine as investigate_payment (implemented)
    Analyst->>Agent: Why was payment REF123 rejected?
    Agent->>Gateway: tools/call get_payment_evidence({reference: REF123})
    Gateway->>Gateway: Authenticate user, authorize payment scope, audit intent
    Gateway->>Adapter: Read-only retrieve by REF123; propagate correlation ID
    Adapter->>Hub: Approved API/MQ query
    Hub-->>Adapter: Original + status record refs, source IDs, timestamps
    Adapter-->>Gateway: Canonical record refs / minimum authorized fields
    Gateway-->>Agent: Authorized evidence references
    Agent->>Gateway: tools/call get_payment_message(refs)
    Gateway->>Adapter: Authorize controlled payload access
    Adapter-->>Agent: Authorized pacs.008 and pacs.002
    Agent->>Engine: tools/call investigate_payment(pacs008_xml,pacs002_xml)
    Engine->>Engine: Verify group and transaction identifiers; inspect status
    Engine-->>Agent: Evidence ledger, mapped code, uncertainty, no-auto-retry
    Agent-->>Analyst: Cited findings + human-controlled remediation proposal
```

**Separation of concerns:** the bank system provides facts and access decisions; the MCP adapter exposes governed reads; deterministic code performs correlation; the LLM explains; a separate approved banking workflow handles any payment change.

## 5. Core banking / legacy connectivity: how to connect in practice

| Technology | Integration approach | Bank-specific implementation actions | Key constraint |
|---|---|---|---|
| Payment hub REST | Private gateway → approved HTTPS GET endpoints | Acquire sandbox OpenAPI spec, IAM scopes, mTLS, status mapping, source IDs | Never expose write/submit endpoints to MCP |
| Mainframe CICS / IMS / Db2 | z/OS Connect REST facade around approved read-only programs | Identify COBOL copybooks, map COMMAREA/IMS to JSON, enforce RACF/SAF or bank entitlement | Preserve transaction boundaries and source-of-truth semantics |
| IBM MQ | Controlled query request/reply or event-to-read-model | Read-only queues, `CorrelationId`, `ReplyToQ`, expiry, timeout, DLQ and duplicate handling | No shared payment-posting channel or credentials |
| SOAP / ESB | SOAP-to-canonical-JSON adapter | Service WSDL, WS-Security, XML schema, normalized source metadata | Keep XML entity protection and version controls |
| SFTP / MFT batch | Scheduled ingest into immutable bank-controlled archive | Signed manifests, completeness reconciliation, sequence IDs, ingestion timestamp, PII retention | Report freshness/lag; not real-time |
| Kafka / event store | Maintain authoritative-provenance status timeline | Partitioning key, dedupe, replay, event version, timestamps and source hashes | Projection is not necessarily current bank ledger state |

### Example proposed payment-hub REST contract

```http
GET /internal/payments/REF123/evidence
Authorization: Bearer <delegated-bank-access-token>
X-Correlation-ID: inv-20261112-001
Accept: application/json
```

```json
{
  "payment_reference": "REF123",
  "source_system": "PAYMENT_HUB_EU",
  "source_event_id": "bank-event-10031",
  "observed_at": "2026-11-12T09:03:00Z",
  "payment_message_ref": "archive://bank/pacs008/demo-001",
  "status_message_refs": ["archive://bank/pacs002/demo-001"],
  "permission": "read_only",
  "freshness": "snapshot",
  "content_hashes": "computed by bank adapter; not shown here"
}
```

The example endpoint and response are a **proposed interface**; no such endpoint has been configured in the repository or verified against a bank. Tokens, event IDs and archive refs are demonstrative only.

### Example legacy MQ request/reply

```json
{
  "command": "READ_PAYMENT_STATUS",
  "payment_reference": "REF123",
  "request_id": "inv-20261112-001",
  "reply_to": "BANK.INVESTIGATION.REPLY",
  "timeout_ms": 5000
}
```

The bank adapter translates this **illustrative** canonical request into the bank's agreed MQ message format, sends to an allowlisted query queue, checks replies for correlation and age, and maps a timeout to `unavailable`. MQ metadata such as queue name, reply behavior and TTL must come from the owning mainframe/payment team, not AI inference.

## 6. Alternate paths that demonstrate safety

| Situation | Expected behavior | Rationale |
|---|---|---|
| pacs.002 original message ID differs | `group_correlation=false`; no bank status assigned | Prevent false attribution |
| EndToEndId or supplied UETR differs | `correlation=unmatched`; no reason applied | Exact identifiers beat fuzzy guesses |
| Reason code `ZZ99` is unknown | `found_in_local_table=false`; explanation remains unknown | No invented financial code meaning |
| Payment status is `ACSP`, not `RJCT` | Do not report payment as rejected | Respect authoritative status semantics |
| Suspicious remittance text | `security_status=review_required`; ignore as instructions | Keep financial data separate from agent commands |
| No official XSD configured | `schema_status=not_configured`; never claim schema conformance | Explain evidence limitations |
| Core banking access denied | Permission error / no retrieval | Enforce delegated entitlements |
| MQ timeout / data unavailable | Explicit `unavailable` and source freshness details | Never infer approval or rejection from absence of data |
| Duplicate, conflicting pacs.002 matches | `ambiguous`; escalate to analyst | Avoid selecting arbitrary evidence |

## 7. Reproducible proof and measurable success

To execute directly through Python against **synthetic** messages:

```python
from iso20022_mcp import generate, parser
from iso20022_mcp.investigate import investigate_payment

payment_xml = generate.generate_pacs008()
payment = parser.parse_message(payment_xml)
status_xml = generate.generate_pacs002(
    reason_code="AC04",
    original_msg_id=payment["msg_id"],
    end_to_end_id=payment["transactions"][0]["end_to_end_id"],
)
report = investigate_payment(payment_xml, status_xml)
case = report["cases"][0]
assert report["group_correlation"] is True
assert case["correlation"] == "matched"
assert case["reported_status"] == "RJCT"
assert case["reported_reasons"][0]["code"] == "AC04"
assert case["decision"] == "no_automatic_retry_or_mutation"
```

```bash
pytest -q
python evals/compare_investigation.py
```

The four-scenario synthetic comparison demonstrates **capability** (known AC04, known AM05, unknown ZZ99 and mismatched group ID). It is deliberately not a measured model-accuracy, financial-risk-reduction, or operations-productivity result. Production evaluation requires expert-labeled incidents, authorization tests, false-correlation measures, adverse-case coverage and operational acceptance criteria.

## 8. Evidence and safety acceptance checklist

- Matching `OrgnlMsgId` + exact transaction identifier established before interpreting status.
- Actual bank-source record identifier, timestamp and hash attached for connected deployments.
- Reported vs inferred outcomes visibly separated.
- Official XSD and scheme-rules coverage disclosed; no blanket ISO 20022 certification claim.
- Unauthorized read attempts fail before accessing a bank source.
- No MCP tool can release, amend, or resend a payment.
- Tool logs and AI prompts observe payment-data minimization and retention policy.
- Bank IAM and audit designs approved before any live integration.

## 9. Repository and reference links

- Repository: https://github.com/Muthukumar123/iso20022-mcp
- Hardening PR #1: https://github.com/Muthukumar123/iso20022-mcp/pull/1
- Evidence-investigation PR #2: https://github.com/Muthukumar123/iso20022-mcp/pull/2
- Architecture source: `docs/ISO20022_MCP_Solution_Architecture.md`
- Sequence diagrams: `docs/diagrams/`

**Boundary of proof:** the actual running implementation consumes two supplied XML strings. The bank reference lookup, private gateway, transport adapters, approval/ticketing workflow, and production security stack are architectural extensions still to be built.