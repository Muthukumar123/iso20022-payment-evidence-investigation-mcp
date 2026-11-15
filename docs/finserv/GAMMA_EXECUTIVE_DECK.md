# FinServ Evidence Intelligence (FEI)
Evidence-first, AI-assisted payment investigations — executive concept and controlled MVP

**Audience:** CIO/CTO, Head of Payments, Banking Architecture, CISO, Risk. **Status:** proposal and prototype, not production.

---
# The problem — payment investigations are fragmented
- Analysts chase pacs.008, pacs.002, payment hub, core banking, SWIFT archives and reconciliation logs.
- APIs answer predefined questions; they do not automatically compose a case-specific investigation narrative.
- The resulting overhead and investigation risk are **hypotheses to measure**, not published FEI results.
**Product purpose:** Turn scattered payment evidence into explainable, auditable and human-reviewed findings.

---
# Why AI; why MCP; why not just an API?
- **API + rule engine:** authoritative retrieval, validation, correlation and business decisions; remain deterministic.
- **AI:** interpret varied questions, select approved investigation steps and communicate evidence/unknowns.
- **MCP:** standardized tools and schemas for AI clients; not a replacement for APIs or banking infrastructure.
- Use AI + MCP **only if measured investigations beat manual and API-only baselines.**

---
# The FEI product — start narrow, scale with evidence
- Start: **Payment Exception Intelligence** using correlated pacs.008 and pacs.002.
- Demonstrate: exact identifiers, bank-reported rejection reason, XML-path provenance, unknown-state handling.
- Next: authorized read-only payment-hub and archive adapters.
- Later: lifecycle timeline, reconciliation, optional bank-approved streaming.
- **No autonomous retry, release, account amendment or payment execution.**

---
# High-level architecture — strict trust boundaries
1. **Analyst & enterprise portal:** verified identity and permission.
2. **AI agent:** untrusted planning / explanation, bounded tool calls.
3. **Governed MCP gateway (target):** OIDC, RBAC/ABAC, quotas, masked audit.
4. **FEI deterministic evidence core:** XML validation, message correlation, provenance.
5. **Bank-owned read-only adapters (target):** REST / z/OS / IBM MQ / SOAP / batch.
6. **Systems of record:** payment hub, core banking, message archives.
**No direct AI-to-core banking connectivity.** Glama is optional discovery/hosting subject to bank risk review; Gamma is presentation publishing only.

---
# Six actual MCP tools — clear evidence boundaries
- \`parse_message(xml)\`: structured pacs.008 / pacs.002.
- \`validate_message(xml)\`: local rules, optional local XSD, security flags.
- \`investigate_payment(pacs008_xml,pacs002_xml)\`: exact correlation and cited bank-reported status.
- \`lookup_code(code)\`: explain known codes, unknown remains unknown.
- \`explain_message(xml)\`: deterministic explanation.
- \`generate_test_message(kind, defect)\`: synthetic fixtures.
**Future tools, not implemented:** \`get_payment_evidence\`, \`get_payment_timeline\`, \`get_scheme_rule\`.

---
# End-to-end happy path — a defensible answer
Analyst: "Why did PAY123 fail?"
1. Proposed bank adapter retrieves authorized pacs.008 and pacs.002 with source IDs.
2. MCP validates XML; investigation engine checks original message ID + exact transaction IDs.
3. Bank status \`RJCT\` and reported reason \`AC04\` are extracted with source paths.
4. AI explains: "Bank reports closed account; this is not independent account verification."
5. Analyst reviews action; **no automatic retry or settlement**.
Today the same deterministic step works locally on **supplied synthetic XML** only.

---
# Guardrails — layered, not magic
**Implemented/partial:** no payment-write tools; bounded XML parsing; DTD rejected; prompt-injection-like text flagged; unknown codes not invented; exact correlation.
**Target:** enterprise SSO, per-user ABAC, PII tokenization, least-privilege gateway, immutable masked audit, scheme-rule governance, incident response, human decision workflow.
**Residual risk remains:** privacy leaks, fabricated interpretations, wrong correlation, stale events or misuse by a human. Read-only does NOT mean risk-free.

---
# Core banking and event streaming — conditional
- Read-only REST / z/OS Connect via bank API gateway.
- IBM MQ request/reply or event feeds through bank-owned service; SOAP/ESB or archive adapters where needed.
- **Broker choice is not a differentiator:** existing MQ/Kafka first; compare Pulsar on AWS, MSK and Kinesis only against bank requirements.
- Normalize, deduplicate and retain source/time metadata; never stream raw PII directly to an LLM.

---
# Prove value in a controlled pilot
**Comparison:** manual analyst vs REST/API-only scripted workflow vs AI + MCP, identical approved cases.
**Measures:** evidence precision, false-cause attribution, median investigation time, analyst usefulness, privacy events, unsafe recommendations, infrastructure cost.
**Investment gate:** expand only after evidence-backed improvement and security review.
**No unverified claims** of % time savings, zero hallucinations, or production readiness.

---
# Decision request — fund the evidence, not the buzzwords
- Approve an **initial read-only, synthetic-data pilot** and acceptance criteria.
- Assign payments SME, security/privacy, solution architecture and platform engineering reviewers.
- Select a safe historical/synthetic case set and baseline measurements.
- Progress to bank-connected proof only after access and governance sign-off.
**FEI: From transaction records to defensible investigation decisions.**
