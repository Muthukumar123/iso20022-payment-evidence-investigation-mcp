# FEI guardrails — zero-risk is not a valid claim

Risk categories: unauthorized payment-data exposure, prompt injection from untrusted payment text, fabricated rejection causes, wrong-message correlation, stale lifecycle events, privacy/regulatory failure, and unsafe operational advice.

| Guardrail | Enforce in | Required behavior | Current state |
| --- | --- | --- | --- |
| Identity and least privilege | Bank identity provider and MCP gateway | Verified end-user + RBAC/ABAC per payment and tool; deny-by-default | Target |
| Tool isolation | MCP gateway, service allowlist | No write, approval, retry or settlement tools in MVP; limit invocation count and output size | Partial: tools are read-only |
| Data minimization | Bank-owned adapter, evidence service | Tokenize names/account data; field-level allowlist; residency and retention policies | Target |
| Untrusted text | Parser, tool output, AI prompt handling | Remittance/additional-info treated as data; no instructions executed from payment XML | Partial: parser flags text |
| Deterministic proof | Correlation engine | IDs must match; unrecognized codes and ambiguous statuses remain unknown | Implemented in feature PR |
| Freshness and provenance | Evidence store and UI | Source IDs, time-of-observation, scheme/version, trace IDs and confidence limits | Partial: message-field evidence |
| Human authority | Workflow / bank system | No automatic account amendment, retry, release or settlement | Implemented as absence of write tools; workflow target |
| Observability | Gateway and bank audit | Masked logs, immutable audit, anomaly alarms, incident response | Target |
| Third-party data | AI/Gamma hosting review | Gamma receives synthetic executive content **only**, never payment messages | Repo policy; operational enforcement target |

**Residual risks remain:** a read-only platform can leak data or mislead an analyst. The actual bank-grade deployment requires threat modeling, privacy impact assessment, penetration testing, red-team tests, model-risk review, business continuity and production monitoring.

## Security acceptance gates

1. **No execution path:** black-box verify tools cannot initiate, modify, retry, release or settle payments.
2. **Access tests:** unauthorized users receive no payment evidence; source adapter is never queried on denial.
3. **Prompt-injection suite:** hidden instructions in remittance/additional-info never alter tool selection or decision.
4. **Evidence tests:** unrelated pacs.002 is not attributed to pacs.008; unknown reasons explicitly unmapped.
5. **Data test:** no raw PII in LLM tool trace, public demo decks or Gamma requests.
6. **Operational test:** service fails closed on identity failure, timeouts, stale data, replay ambiguity.

MCP alone does not implement these controls. The gateway and bank connectors must independently enforce them.
